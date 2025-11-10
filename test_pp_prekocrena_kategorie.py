"""
Test nového placeholderu: pp_prekocrena_kategorie
Vrací číslo PŘEKROČENÉ kategorie (ne výsledné)
"""
import sys
from core.text_generator import generate_conditional_texts

# Fix Windows console encoding
sys.stdout.reconfigure(encoding='utf-8')

# SIMULOVANÁ DATA - measurement_data
measurement_data = {
    "section0_file_selection": {
        "workers_gender": "muži",
        "worker_count": 2
    },
    "section2_firma": {
        "measurement_days": 2
    },
    "section4_worker_a": {
        "work_duration": "480"  # Standardní směna
    }
}

# TESTOVACÍ SCÉNÁŘE

# Scénář 1: KATEGORIE 1 (vše OK) → NEPŘEKROČENO NIC
pp_results_kat1 = {
    "trup": [
        {"nazev_polohy": "Předklon trupu", "typ_svalove_prace": "Dynamická", "prumer_min": 50, "typ_pracovni_polohy": "PP"},
    ],
    "hlava_krk": [],
    "phk": [],
    "lhk": [],
    "dk": [],
    "ostatni": []
}

# Scénář 2: KATEGORIE 2 → PŘEKROČENA KATEGORIE 1
pp_results_kat2 = {
    "trup": [
        {"nazev_polohy": "Předklon trupu", "typ_svalove_prace": "Dynamická", "prumer_min": 120, "typ_pracovni_polohy": "PP"},
    ],
    "hlava_krk": [],
    "phk": [],
    "lhk": [],
    "dk": [],
    "ostatni": []
}

# Scénář 3: KATEGORIE 3 → PŘEKROČENA KATEGORIE 2
pp_results_kat3 = {
    "trup": [
        {"nazev_polohy": "Předklon trupu", "typ_svalove_prace": "Dynamická", "prumer_min": 170, "typ_pracovni_polohy": "PP"},
    ],
    "hlava_krk": [],
    "phk": [],
    "lhk": [],
    "dk": [],
    "ostatni": []
}

print("="*80)
print("TEST: PP překročená kategorie (nový placeholder)")
print("="*80)
print()
print("ROZDÍL MEZI PLACEHOLDERY:")
print("  pp_kategorie_cislo      = Výsledná kategorie (1, 2, 3)")
print("  pp_prekocrena_kategorie = Překročená kategorie ('', 1, 2)")
print()
print("="*80)
print()

scenarios = [
    ("KATEGORIE 1 (vše OK)", pp_results_kat1),
    ("KATEGORIE 2 (překročena kat1)", pp_results_kat2),
    ("KATEGORIE 3 (překročena kat2)", pp_results_kat3),
]

for scenario_name, pp_results in scenarios:
    print(f"SCÉNÁŘ: {scenario_name}")
    print("-" * 80)

    texts = generate_conditional_texts(
        measurement_data=measurement_data,
        results_data=pp_results,
        protocol_type="PP_CAS"
    )

    print()
    print(f"  Výsledná kategorie:   {texts['pp_kategorie_cislo']}")
    print(f"  Překročená kategorie: '{texts['pp_prekocrena_kategorie']}'")
    print()

    # Ukázka věty
    if texts['pp_prekocrena_kategorie']:
        print(f"  → Celková doba překročila přípustný limit kategorie {texts['pp_prekocrena_kategorie']}.")
    else:
        print(f"  → Celková doba nepřekročila žádný limit.")

    print()
    print()

# ============================================================================
# PŘÍKLADY POUŽITÍ V WORD ŠABLONĚ
# ============================================================================
print("="*80)
print("POUŽITÍ V WORD ŠABLONĚ:")
print("="*80)
print()

print("1. PŘÍMÉ POUŽITÍ V VĚTĚ:")
print("   Celková doba překročila přípustný limit kategorie")
print("   {{ texts.pp_prekocrena_kategorie }}.")
print()
print("   Výstup (kat2): 'Celková doba překročila přípustný limit kategorie 1.'")
print("   Výstup (kat3): 'Celková doba překročila přípustný limit kategorie 2.'")
print("   Výstup (kat1): 'Celková doba překročila přípustný limit kategorie .'")
print("                  ⚠️  POZOR: prázdný string - lepší použít podmínku!")
print()

print("2. PODMÍNKA (DOPORUČENO):")
print("   {% if texts.pp_prekocrena_kategorie %}")
print("     Celková doba překročila přípustný limit kategorie")
print("     {{ texts.pp_prekocrena_kategorie }}.")
print("   {% else %}")
print("     Celková doba nepřekročila žádný limit.")
print("   {% endif %}")
print()

print("3. KOMBINACE S VÝSLEDNOU KATEGORIÍ:")
print("   Výsledná kategorie: {{ texts.pp_kategorie_cislo }}")
print("   {% if texts.pp_prekocrena_kategorie %}")
print("     (překročena kategorie {{ texts.pp_prekocrena_kategorie }})")
print("   {% endif %}")
print()

print("4. PODMÍNKA DLE PŘEKROČENÉ KATEGORIE:")
print("   {% if texts.pp_prekocrena_kategorie == '2' %}")
print("     🔴 KRITICKÉ: Překročena kategorie 2!")
print("   {% elif texts.pp_prekocrena_kategorie == '1' %}")
print("     🟡 VAROVÁNÍ: Překročena kategorie 1")
print("   {% else %}")
print("     🟢 V POŘÁDKU: Žádné překročení")
print("   {% endif %}")
print()

print("="*80)
print("SHRNUTÍ - VŠECHNY 4 PP PLACEHOLDERY:")
print("="*80)
print()
print("| Placeholder                      | Kat1 | Kat2 | Kat3 | Použití          |")
print("|----------------------------------|------|------|------|------------------|")
print("| pp_kategorie_cislo               | '1'  | '2'  | '3'  | Výsledná kat     |")
print("| pp_prekocrena_kategorie          | ''   | '1'  | '2'  | Překročená kat   |")
print("| pp_problematicke_polohy_seznam   | ''   | seznam | seznam | Problémové polohy |")
print("| prvni_pp_podminka_kategorie      | text | text | text | Celý text        |")
print()

print("="*80)
print("DŮLEŽITÉ:")
print("="*80)
print("- pp_prekocrena_kategorie vrací STRING ('1', '2') nebo prázdný string ('')")
print("- Pro kategorii 1 vrací PRÁZDNÝ STRING (ne '0')!")
print("- Vždy používej podmínku před výpisem, jinak dostaneš prázdné místo!")
print("="*80)
