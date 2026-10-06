project = "Lugha Reference API"

author = "Mumpe Cydrone"

copyright = "2026, Mumpe Cydrone"

extensions = [
    "myst_parser",
    "sphinx_copybutton",
    "sphinx_design",
]

myst_enable_extensions = [
    "colon_fence",
    "tasklist",
    "deflist",
]

myst_heading_anchors = 3

exclude_patterns = ["_build"]

html_theme = "furo"

html_title = "Lugha Reference API"

html_theme_options = {
    "light_css_variables": {
        "color-brand-primary": "#0D7A7A",
        "color-brand-content": "#0D7A7A",
    },
    "dark_css_variables": {
        "color-brand-primary": "#4FB3B3",
        "color-brand-content": "#4FB3B3",
    },
}

# Localization
language = "en"

locale_dirs = ["locales/"]

gettext_compact = False
gettext_uuid = False

languages = [
    "en",
    "fr",
    "pt",
    "sw",
    "zu",
    "yo",
    "ar",
]

# Custom templates and styling
templates_path = ["_templates"]

html_static_path = ["_static"]

html_css_files = [
    "language-picker.css",
]

html_js_files = [
    "language-picker.js",
]