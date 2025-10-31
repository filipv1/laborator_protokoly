"""
Debug - struktura kontextu pro Word sablonu
"""
import json
from core.text_generator import generate_conditional_texts

# Nacti data
with open("measurement_data_example.json", "r", encoding="utf-8") as f:
    input_data = json.load(f)

with open("lsz_results.json", "r", encoding="utf-8") as f:
    results_data = json.load(f)

# Vygeneruj podminky (podle generate_word_from_two_sources.py radek 277-278)
conditional_texts = generate_conditional_texts(input_data, results_data)
input_data["section_generated_texts"] = conditional_texts

# Vytvor kontext (podle generate_word_from_two_sources.py radek 291-294)
context = {
    "input": input_data,
    "results": results_data
}

print("=" * 80)
print("STRUKTURA KONTEXTU PRO WORD SABLONU")
print("=" * 80)

print("\nKontext ma 2 hlavni klice:")
print("  1. 'input' - obsahuje measurement_data + section_generated_texts")
print("  2. 'results' - obsahuje lsz_results data")

print("\n" + "=" * 80)
print("PRISTUP K JEDENACTE PODMINCE:")
print("=" * 80)

print("\nSPRAVNY placeholder:")
print("  {{ input.section_generated_texts.jedenacta_text_podminka }}")

print("\nNESPRAVNY placeholder (nebude fungovat):")
print("  {{ section_generated_texts.jedenacta_text_podminka }}")

print("\n" + "=" * 80)
print("OVERENI:")
print("=" * 80)

# Zkus pristoupit k datum jako v sablone
try:
    hodnota = context["input"]["section_generated_texts"]["jedenacta_text_podminka"]
    print(f"context['input']['section_generated_texts']['jedenacta_text_podminka'] = '{hodnota}'")
    print("FUNGUJE!")
except KeyError as e:
    print(f"CHYBA: {e}")

print("\n" + "=" * 80)
print("VSECHNY DOSTUPNE PODMINKY:")
print("=" * 80)

for key in sorted(context["input"]["section_generated_texts"].keys()):
    value = context["input"]["section_generated_texts"][key]
    if isinstance(value, dict):
        print(f"\n{{ input.section_generated_texts.{key} }}")
        for subkey in value.keys():
            print(f"  {{ input.section_generated_texts.{key}.{subkey} }}")
    else:
        print(f"{{ input.section_generated_texts.{key} }}")
