"""Static lists of models, languages and data regions."""

LANGUAGES = {
    "en": "English",
    "sw": "Swahili",
    "ha": "Hausa",
    "yo": "Yoruba",
    "lg": "Luganda",
    "am": "Amharic",
}

REGIONS = {
    "ke": "Kenya",
    "ug": "Uganda",
    "ma": "Morocco",
    "mu": "Mauritius",
}

DEFAULT_LANGUAGE = "en"
DEFAULT_REGION = "ke"

MODELS = {
    "lugha-demo-small": {
        "max_output_tokens": 128,
        "languages": ["en", "sw", "lg"],
    },
    "lugha-demo-large": {
        "max_output_tokens": 512,
        "languages": ["en", "sw", "ha", "yo", "lg", "am"],
    },
}
