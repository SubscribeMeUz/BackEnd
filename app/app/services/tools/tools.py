TOOLS = [
    {"id": 1,  "name": "Sochiq",                 "icon": "tools/sochiq.png"},
    {"id": 2,  "name": "Krasovka",               "icon": "tools/krasovka.png"},
    {"id": 3,  "name": "Sumka",                  "icon": "tools/sumka.png"},
    {"id": 4,  "name": "Gul",                    "icon": "tools/gul.png"},
    {"id": 5,  "name": "Qarshilik lentalari",    "icon": "tools/qarshilik_lentalari.png"},
    {"id": 6,  "name": "Girya",                  "icon": "tools/girya.png"},
    {"id": 7,  "name": "Sakrash arqoni",         "icon": "tools/sakrash_arqoni.png"},
    {"id": 8,  "name": "Yotib shtanga ko'tarish","icon": "tools/shtanga.png"},
    {"id": 9,  "name": "Eshkak trenajyori",      "icon": "tools/eshkak_trenajyori.png"},
    {"id": 10, "name": "Yoga gilamchasi",        "icon": "tools/yoga_gilamchasi.png"},
]


def get_all_tools():
    return TOOLS


def get_tool_by_id(tool_id: int):
    return next((t for t in TOOLS if t["id"] == tool_id), None)
