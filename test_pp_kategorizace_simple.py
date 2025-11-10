"""
Test PP kategorizace - zjednodusena verze bez Unicode printu
"""
import json
from pathlib import Path
from core.text_generator import generate_conditional_texts

# Nacti data
project_path = Path("projects/_fjfjfe")
measurement_data_path = project_path / "measurement_data.json"
pp_results_path = project_path / "pp_results.json"

with open(measurement_data_path, 'r', encoding='utf-8') as f:
    measurement_data = json.load(f)

with open(pp_results_path, 'r', encoding='utf-8') as f:
    pp_results = json.load(f)

# Vygeneruj podminko ve texty (bez printu)
import sys
import io
old_stdout = sys.stdout
sys.stdout = io.StringIO()  # Suppress prints

texts = generate_conditional_texts(
    measurement_data=measurement_data,
    results_data=pp_results,
    protocol_type="PP_CAS"
)

sys.stdout = old_stdout  # Restore

# Uloz vysledek do JSON
output = {
    "prvni_pp_podminka_kategorie": texts.get("prvni_pp_podminka_kategorie", "N/A"),
    "pp_kat1_max": texts.get("pp_kat1_max"),
    "pp_kat2_max": texts.get("pp_kat2_max"),
    "n_kat1_max": texts.get("n_kat1_max"),
    "n_kat2_max": texts.get("n_kat2_max"),
}

output_path = Path("test_kategorizace_result.json")
with open(output_path, 'w', encoding='utf-8') as f:
    json.dump(output, f, ensure_ascii=False, indent=2)

print(f"[OK] Vysledek ulozen do: {output_path}")
print(f"     Kategorie: {output['prvni_pp_podminka_kategorie'][:30]}...")
