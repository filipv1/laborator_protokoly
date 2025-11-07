"""
Test PP kategorizace s mock daty pro vsechny 3 kategorie
"""
import json
from core.text_generator import generate_conditional_texts

# Mock measurement_data (500 min smena)
measurement_data = {
    "section0_file_selection": {"workers_gender": "muzi", "worker_count": 2},
    "section2_firma": {"measurement_days": 1},
    "section4_worker_a": {"work_duration": "500"}  # 500 min -> koef 1.025
}

print("="*80)
print("TEST: PP kategorizace - vsechny kategorie")
print("="*80)
print()

# Limity pro 500 min (koeficient 1.025):
# PP: kat1 0-102, kat2 103-164, kat3 >164
# N:  kat1 0-21,  kat2 22-31,   kat3 >31

# TEST 1: Kategorie 1 (vse pod limitem)
print("[TEST 1] Kategorie 1 - vsechny polohy pod limitem")
pp_results_kat1 = {
    "excel_type": "PP_CAS",
    "worker_count": 2,
    "trup": [
        {"nazev_polohy": "Predklon trupu vetsi nez 60", "typ_svalove_prace": "Staticka",
         "prumer_min": 50, "typ_pracovni_polohy": "PP"},
        {"nazev_polohy": "Zaklon bez opory", "typ_svalove_prace": "Staticka",
         "prumer_min": 10, "typ_pracovni_polohy": "N"}
    ],
    "hlava_krk": [],
    "phk": [],
    "lhk": [],
    "dk": [],
    "ostatni": []
}

texts1 = generate_conditional_texts(measurement_data, pp_results_kat1, "PP_CAS")
result1 = texts1.get("prvni_pp_podminka_kategorie", "N/A")
with open("test_result_kat1.json", "w", encoding="utf-8") as f:
    json.dump({"text": result1}, f, ensure_ascii=False, indent=2)
print(f"Vysledek ulozen do: test_result_kat1.json")
print()

# TEST 2: Kategorie 2 - jen PP prekrocilo
print("[TEST 2] Kategorie 2 - jen PP polohy prekrocily kat1")
pp_results_kat2_pp = {
    "excel_type": "PP_CAS",
    "worker_count": 2,
    "trup": [
        {"nazev_polohy": "Predklon trupu vetsi nez 60", "typ_svalove_prace": "Staticka",
         "prumer_min": 120, "typ_pracovni_polohy": "PP"},  # 120 > 102 (kat1) ale < 164 (kat2)
        {"nazev_polohy": "Uklon trupu vetsi nez 20", "typ_svalove_prace": "Dynamicka",
         "prumer_min": 150, "typ_pracovni_polohy": "PP"}
    ],
    "hlava_krk": [],
    "phk": [],
    "lhk": [],
    "dk": [],
    "ostatni": []
}

texts2 = generate_conditional_texts(measurement_data, pp_results_kat2_pp, "PP_CAS")
result2 = texts2.get("prvni_pp_podminka_kategorie", "N/A")
# Uloz do JSON (kvuli Unicode)
with open("test_result_kat2_pp.json", "w", encoding="utf-8") as f:
    json.dump({"text": result2}, f, ensure_ascii=False, indent=2)
print(f"Vysledek ulozen do: test_result_kat2_pp.json")
print()

# TEST 3: Kategorie 2 - jen N prekrocilo
print("[TEST 3] Kategorie 2 - jen N polohy prekrocily kat1")
pp_results_kat2_n = {
    "excel_type": "PP_CAS",
    "worker_count": 2,
    "trup": [
        {"nazev_polohy": "Zaklon bez opory celeho tela", "typ_svalove_prace": "Staticka",
         "prumer_min": 25, "typ_pracovni_polohy": "N"},  # 25 > 21 (kat1) ale < 31 (kat2)
    ],
    "hlava_krk": [
        {"nazev_polohy": "Predklon hlavy vetsi nez 25", "typ_svalove_prace": "Dynamicka",
         "prumer_min": 28, "typ_pracovni_polohy": "N"}
    ],
    "phk": [],
    "lhk": [],
    "dk": [],
    "ostatni": []
}

texts3 = generate_conditional_texts(measurement_data, pp_results_kat2_n, "PP_CAS")
result3 = texts3.get("prvni_pp_podminka_kategorie", "N/A")
with open("test_result_kat2_n.json", "w", encoding="utf-8") as f:
    json.dump({"text": result3}, f, ensure_ascii=False, indent=2)
print(f"Vysledek ulozen do: test_result_kat2_n.json")
print()

# TEST 4: Kategorie 2 - PP i N prekrocilo
print("[TEST 4] Kategorie 2 - PP i N polohy prekrocily kat1")
pp_results_kat2_both = {
    "excel_type": "PP_CAS",
    "worker_count": 2,
    "trup": [
        {"nazev_polohy": "Predklon trupu vetsi nez 60", "typ_svalove_prace": "Staticka",
         "prumer_min": 120, "typ_pracovni_polohy": "PP"},
        {"nazev_polohy": "Zaklon bez opory", "typ_svalove_prace": "Staticka",
         "prumer_min": 25, "typ_pracovni_polohy": "N"}
    ],
    "hlava_krk": [],
    "phk": [],
    "lhk": [],
    "dk": [],
    "ostatni": []
}

texts4 = generate_conditional_texts(measurement_data, pp_results_kat2_both, "PP_CAS")
result4 = texts4.get("prvni_pp_podminka_kategorie", "N/A")
with open("test_result_kat2_both.json", "w", encoding="utf-8") as f:
    json.dump({"text": result4}, f, ensure_ascii=False, indent=2)
print(f"Vysledek ulozen do: test_result_kat2_both.json")
print()

# TEST 5: Kategorie 3 - PP prekrocilo kat2
print("[TEST 5] Kategorie 3 - PP polohy prekrocily kat2")
pp_results_kat3 = {
    "excel_type": "PP_CAS",
    "worker_count": 2,
    "trup": [
        {"nazev_polohy": "Vzpazeni prave paze vetsi nez 60", "typ_svalove_prace": "Dynamicka",
         "prumer_min": 200, "typ_pracovni_polohy": "PP"},  # 200 > 164 (kat2)
    ],
    "hlava_krk": [],
    "phk": [],
    "lhk": [],
    "dk": [],
    "ostatni": []
}

texts5 = generate_conditional_texts(measurement_data, pp_results_kat3, "PP_CAS")
result5 = texts5.get("prvni_pp_podminka_kategorie", "N/A")
with open("test_result_kat3.json", "w", encoding="utf-8") as f:
    json.dump({"text": result5}, f, ensure_ascii=False, indent=2)
print(f"Vysledek ulozen do: test_result_kat3.json")
print()

print("="*80)
print("[OK] Vsechny testy dokonceny - vysledky ulozeny do JSON souboru")
print("="*80)
