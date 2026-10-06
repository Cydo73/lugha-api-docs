"""Build docs/api-reference.md from openapi/openapi.yaml.

The reference is generated so nobody has to copy parameters by hand. CI runs
this script and fails if the committed page is out of date.
"""
import json
import pathlib

import yaml

ROOT = pathlib.Path(__file__).resolve().parent.parent
SPEC = ROOT / "openapi" / "openapi.yaml"
TARGET = ROOT / "docs" / "api-reference.md"


def ref_name(schema: dict) -> str | None:
    ref = schema.get("$ref")
    return ref.rsplit("/", 1)[-1] if ref else None


def type_of(schema: dict) -> str:
    name = ref_name(schema)
    if name:
        return f"{name} object"
    if "enum" in schema:
        return "string, one of " + ", ".join(f"`{value}`" for value in schema["enum"])
    if schema.get("type") == "array":
        return f"array of {type_of(schema.get('items', {}))}"
    return {"integer": "integer", "number": "number", "string": "string", "object": "object"}.get(schema.get("type"), "any")


def notes_for(schema: dict) -> str:
    notes = []
    if "default" in schema:
        notes.append(f"Default: `{json.dumps(schema['default'])}`.")
    if "minLength" in schema and "maxLength" in schema:
        notes.append(f"Length {schema['minLength']} to {schema['maxLength']} characters.")
    elif "maxLength" in schema:
        notes.append(f"Up to {schema['maxLength']} characters.")
    if "minimum" in schema:
        minimum = schema["minimum"]
        minimum = int(minimum) if float(minimum).is_integer() else minimum
        notes.append(f"Minimum {minimum}.")
    return " ".join(notes)


def fields_table(name: str, components: dict, with_required: bool) -> list[str]:
    schema = components[name]
    required = set(schema.get("required", []))
    header = "| Field | Type | Required | Description |" if with_required else "| Field | Type | Description |"
    divider = "| --- | --- | --- | --- |" if with_required else "| --- | --- | --- |"
    lines = [header, divider]
    for field, prop in schema.get("properties", {}).items():
        description = " ".join(part for part in [prop.get("description", ""), notes_for(prop)] if part)
        cells = [f"`{field}`", type_of(prop)]
        if with_required:
            cells.append("Yes" if field in required else "No")
        cells.append(description)
        lines.append("| " + " | ".join(cells) + " |")
    return lines


def example_request(name: str, components: dict) -> dict:
    schema = components[name]
    return {field: prop["examples"][0] for field, prop in schema.get("properties", {}).items() if prop.get("examples")}


def nested_refs(name: str, components: dict) -> list[tuple[str, str, bool]]:
    """Return (property name, schema name, is_array) for properties that point at other schemas."""
    found = []
    for field, prop in components[name].get("properties", {}).items():
        direct = ref_name(prop)
        if direct:
            found.append((field, direct, False))
            continue
        item = ref_name(prop.get("items", {}))
        if item:
            found.append((field, item, True))
    return found


def operation_section(path: str, method: str, operation: dict, components: dict) -> list[str]:
    lines = [f"## {method.upper()} {path}", "", f"**{operation['summary']}**", ""]
    if operation.get("description"):
        lines += [operation["description"], ""]
    lines += ["Requires an API key." if operation.get("security") else "No API key needed.", ""]

    body = operation.get("requestBody", {}).get("content", {}).get("application/json", {}).get("schema")
    if body:
        name = ref_name(body)
        lines += ["### Request body", "", *fields_table(name, components, with_required=True), ""]
        example = example_request(name, components)
        if example:
            lines += ["Example request body:", "", "```json", json.dumps(example, indent=2, ensure_ascii=False), "```", ""]

    lines += ["### Responses", "", "| Status | Meaning |", "| --- | --- |"]
    for status, response in operation["responses"].items():
        lines.append(f"| {status} | {response['description']} |")
    lines.append("")

    success = operation["responses"].get("200", {}).get("content", {}).get("application/json", {}).get("schema")
    if success and ref_name(success):
        name = ref_name(success)
        lines += ["A `200` response has these fields.", "", *fields_table(name, components, with_required=False), ""]
        for field, nested, is_array in nested_refs(name, components):
            intro = f"Each item in `{field}` has these fields." if is_array else f"The `{field}` object has these fields."
            lines += [intro, "", *fields_table(nested, components, with_required=False), ""]
    if any(code != "200" for code in operation["responses"]):
        lines += ["Failures use the standard error body described in [Errors](errors.md).", ""]
    return lines


def main() -> None:
    spec = yaml.safe_load(SPEC.read_text(encoding="utf-8"))
    components = spec["components"]["schemas"]
    tag_order = [tag["name"] for tag in spec.get("tags", [])]

    operations = []
    for path, methods in spec["paths"].items():
        for method, operation in methods.items():
            tag = operation["tags"][0]
            operations.append((tag_order.index(tag), path, method, operation))
    operations.sort(key=lambda item: item[0])

    lines = [
        "<!-- Generated by scripts/build_reference.py from openapi/openapi.yaml. Do not edit by hand. -->",
        "",
        "# API reference",
        "",
        "This page is generated from the OpenAPI file, which is exported from the service code. When the API changes, this page changes with it.",
        "",
        "All endpoints except `/health` need an API key. See [Authentication](authentication.md).",
        "",
    ]
    for _, path, method, operation in operations:
        lines += operation_section(path, method, operation, components)

    TARGET.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")
    print(f"Wrote {TARGET.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
