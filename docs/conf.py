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
    "source_repository": "https://github.com/Cydo73/lugha-api-docs/",
    "source_branch": "main",
    "source_directory": "docs/",
    "footer_icons": [
        {
            "name": "GitHub",
            "url": "https://github.com/Cydo73/lugha-api-docs",
            "html": """
                <svg stroke="currentColor" fill="currentColor" stroke-width="0" viewBox="0 0 16 16">
                    <path fill-rule="evenodd" d="M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82.64-.18 1.32-.27 2-.27.68 0 1.36.09 2 .27 1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.013 8.013 0 0016 8c0-4.42-3.58-8-8-8z"></path>
                </svg>
            """,
            "class": "",
        },
    ],
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