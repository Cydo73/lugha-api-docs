"""Write the OpenAPI description to openapi/openapi.yaml.

The API code is the source of truth. CI runs this script and fails if the
committed file is out of date, so the reference can never drift from the service.
"""
import pathlib
import sys

import yaml

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from app.main import app  # noqa: E402


def main() -> None:
    target = ROOT / "openapi" / "openapi.yaml"
    target.write_text(yaml.safe_dump(app.openapi(), sort_keys=False, allow_unicode=True), encoding="utf-8")
    print(f"Wrote {target.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
