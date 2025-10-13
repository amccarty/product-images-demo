from typing import Dict, Any
import json

FLAGS = {
    "af": "🇿🇦",  # Afrikaans - South Africa
    "am": "🇪🇹",  # Amharic - Ethiopia
    "an": "🇪🇸",  # Aragonese - Spain
    "ar": "🇸🇦",  # Arabic - Saudi Arabia
    "as": "🇮🇳",  # Assamese - India
    "az": "🇦🇿",  # Azerbaijani - Azerbaijan
    "be": "🇧🇾",  # Belarusian - Belarus
    "bg": "🇧🇬",  # Bulgarian - Bulgaria
    "bn": "🇧🇩",  # Bengali - Bangladesh
    "br": "🇫🇷",  # Breton - France
    "bs": "🇧🇦",  # Bosnian - Bosnia and Herzegovina
    "ca": "🇦🇩",  # Catalan - Andorra
    "cs": "🇨🇿",  # Czech - Czech Republic
    "cy": "🏴󠁧󠁢󠁷󠁬󠁳󠁿",  # Welsh - Wales
    "da": "🇩🇰",  # Danish - Denmark
    "de": "🇩🇪",  # German - Germany
    "dz": "🇧🇹",  # Dzongkha - Bhutan
    "el": "🇬🇷",  # Greek - Greece
    "en": "🇬🇧",  # English - United Kingdom
    "eo": "🌍",  # Esperanto - International
    "es": "🇪🇸",  # Spanish - Spain
    "et": "🇪🇪",  # Estonian - Estonia
    "eu": "🇪🇸",  # Basque - Spain
    "fa": "🇮🇷",  # Persian/Farsi - Iran
    "fi": "🇫🇮",  # Finnish - Finland
    "fo": "🇫🇴",  # Faroese - Faroe Islands
    "fr": "🇫🇷",  # French - France
    "ga": "🇮🇪",  # Irish - Ireland
    "gl": "🇪🇸",  # Galician - Spain
    "gu": "🇮🇳",  # Gujarati - India
    "he": "🇮🇱",  # Hebrew - Israel
    "hi": "🇮🇳",  # Hindi - India
    "hr": "🇭🇷",  # Croatian - Croatia
    "ht": "🇭🇹",  # Haitian Creole - Haiti
    "hu": "🇭🇺",  # Hungarian - Hungary
    "hy": "🇦🇲",  # Armenian - Armenia
    "id": "🇮🇩",  # Indonesian - Indonesia
    "is": "🇮🇸",  # Icelandic - Iceland
    "it": "🇮🇹",  # Italian - Italy
    "ja": "🇯🇵",  # Japanese - Japan
    "jv": "🇮🇩",  # Javanese - Indonesia
    "ka": "🇬🇪",  # Georgian - Georgia
    "kk": "🇰🇿",  # Kazakh - Kazakhstan
    "km": "🇰🇭",  # Khmer - Cambodia
    "kn": "🇮🇳",  # Kannada - India
    "ko": "🇰🇷",  # Korean - South Korea
    "ku": "🇮🇶",  # Kurdish - Iraq
    "ky": "🇰🇬",  # Kyrgyz - Kyrgyzstan
    "la": "🇻🇦",  # Latin - Vatican City
    "lb": "🇱🇺",  # Luxembourgish - Luxembourg
    "lo": "🇱🇦",  # Lao - Laos
    "lt": "🇱🇹",  # Lithuanian - Lithuania
    "lv": "🇱🇻",  # Latvian - Latvia
    "mg": "🇲🇬",  # Malagasy - Madagascar
    "mk": "🇲🇰",  # Macedonian - North Macedonia
    "ml": "🇮🇳",  # Malayalam - India
    "mn": "🇲🇳",  # Mongolian - Mongolia
    "mr": "🇮🇳",  # Marathi - India
    "ms": "🇲🇾",  # Malay - Malaysia
    "mt": "🇲🇹",  # Maltese - Malta
    "nb": "🇳🇴",  # Norwegian Bokmål - Norway
    "ne": "🇳🇵",  # Nepali - Nepal
    "nl": "🇳🇱",  # Dutch - Netherlands
    "nn": "🇳🇴",  # Norwegian Nynorsk - Norway
    "no": "🇳🇴",  # Norwegian - Norway
    "oc": "🇫🇷",  # Occitan - France
    "or": "🇮🇳",  # Odia - India
    "pa": "🇮🇳",  # Punjabi - India
    "pl": "🇵🇱",  # Polish - Poland
    "ps": "🇦🇫",  # Pashto - Afghanistan
    "pt": "🇵🇹",  # Portuguese - Portugal
    "qu": "🇵🇪",  # Quechua - Peru
    "ro": "🇷🇴",  # Romanian - Romania
    "ru": "🇷🇺",  # Russian - Russia
    "rw": "🇷🇼",  # Kinyarwanda - Rwanda
    "se": "🇳🇴",  # Northern Sami - Norway
    "si": "🇱🇰",  # Sinhala - Sri Lanka
    "sk": "🇸🇰",  # Slovak - Slovakia
    "sl": "🇸🇮",  # Slovenian - Slovenia
    "sq": "🇦🇱",  # Albanian - Albania
    "sr": "🇷🇸",  # Serbian - Serbia
    "sv": "🇸🇪",  # Swedish - Sweden
    "sw": "🇰🇪",  # Swahili - Kenya
    "ta": "🇮🇳",  # Tamil - India
    "te": "🇮🇳",  # Telugu - India
    "th": "🇹🇭",  # Thai - Thailand
    "tl": "🇵🇭",  # Tagalog - Philippines
    "tr": "🇹🇷",  # Turkish - Turkey
    "ug": "🇨🇳",  # Uyghur - China
    "uk": "🇺🇦",  # Ukrainian - Ukraine
    "ur": "🇵🇰",  # Urdu - Pakistan
    "vi": "🇻🇳",  # Vietnamese - Vietnam
    "vo": "🌐",  # Volapük - International
    "wa": "🇧🇪",  # Walloon - Belgium
    "xh": "🇿🇦",  # Xhosa - South Africa
    "zh": "🇨🇳",  # Chinese - China
    "zu": "🇿🇦",  # Zulu - South Africa
}
UNKNOWN = "❓"


def make_chart(languages: Any) -> Dict[str, Any]:

    # Sort by count descending
    sorted_languages = sorted(languages, key=lambda x: x[1], reverse=True)

    # Create labels combining flag emoji and language code
    chart_data = []
    for code, count in sorted_languages:
        flag = FLAGS.get(code, UNKNOWN)
        chart_data.append({"language": f"{flag} {code}", "count": count})

    # Create Vega Lite specification
    spec = {
        "$schema": "https://vega.github.io/schema/vega-lite/v6.json",
        "description": "Horizontal bar chart of language frequencies sorted by count descending",
        "width": 500,
        "height": 400,
        "data": {"values": chart_data},
        "mark": "bar",
        "encoding": {
            "y": {
                "field": "language",
                "type": "nominal",
                "sort": None,
                "axis": {"title": "Language"},
            },
            "x": {"field": "count", "type": "quantitative", "axis": {"title": "Count"}},
        },
    }

    return spec


# DO NOT EDIT ANYTHING BELOW THIS LINE
if __name__ == "__main__":
    import json
    import sys

    chart = make_chart(json.load(open(sys.argv[1])))
    print(json.dumps(chart))
