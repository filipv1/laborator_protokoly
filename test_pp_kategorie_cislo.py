"""
Test nového placeholderu: pp_kategorie_cislo
Vrací POUZE číslo kategorie (1, 2, nebo 3)
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

# Scénář 1: KATEGORIE 1 (vše OK)
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

# Scénář 2: KATEGORIE 2 (překročena kat1, ale ne kat2)
# PP limity: 0-100 (kat1), 101-160 (kat2), 161+ (kat3)
pp_results_kat2 = {
    "trup": [
        {"nazev_polohy": "Předklon trupu", "typ_svalove_prace": "Dynamická", "prumer_min": 120, "typ_pracovni_polohy": "PP"},  # KAT 2
    ],
    "hlava_krk": [],
    "phk": [],
    "lhk": [],
    "dk": [],
    "ostatni": []
}

# Scénář 3: KATEGORIE 3 (překročena kat2)
pp_results_kat3 = {
    "trup": [
        {"nazev_polohy": "Předklon trupu", "typ_svalove_prace": "Dynamická", "prumer_min": 170, "typ_pracovni_polohy": "PP"},  # KAT 3
    ],
    "hlava_krk": [],
    "phk": [],
    "lhk": [],
    "dk": [],
    "ostatni": []
}

print("="*80)
print("TEST: PP kategorie číslo (nový placeholder)")
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
    print(f"  1) ČÍSLO KATEGORIE (nový placeholder): {texts['pp_kategorie_cislo']}")
    print(f"  2) SEZNAM PROBLÉMŮ: '{texts['pp_problematicke_polohy_seznam']}'")
    print(f"  3) KOMPLETNÍ TEXT: {texts['prvni_pp_podminka_kategorie'][:80]}...")
    print()
    print()

# ============================================================================
# PŘÍKLADY POUŽITÍ V WORD ŠABLONĚ
# ============================================================================
print("="*80)
print("POUŽITÍ V WORD ŠABLONĚ:")
print("="*80)
print()

print("1. PŘÍMÉ ZOBRAZENÍ ČÍSLA:")
print("   Pracovní polohy jsou zařazeny do kategorie {{ texts.pp_kategorie_cislo }}")
print()

print("2. PODMÍNKA PODLE KATEGORIE:")
print("   {% if texts.pp_kategorie_cislo == '1' %}")
print("     Všechny polohy v kategorii 1 - bez problémů")
print("   {% elif texts.pp_kategorie_cislo == '2' %}")
print("     Některé polohy překročily kategorii 1")
print("   {% else %}")
print("     POZOR: Polohy překročily kategorii 2!")
print("   {% endif %}")
print()

print("3. DYNAMICKÝ TEXT S ČÍSLEM:")
print("   Celková doba překročila přípustný limit kategorie")
print("   {% if texts.pp_kategorie_cislo == '3' %}2{% else %}1{% endif %}")
print()

print("4. V TABULCE:")
print("   | Výsledná kategorie | {{ texts.pp_kategorie_cislo }} |")
print()

print("5. KOMBINACE S DALŠÍMI PLACEHOLDERY:")
print("   Kategorie {{ texts.pp_kategorie_cislo }}")
print("   {% if texts.pp_problematicke_polohy_seznam %}")
print("     - problematické polohy: {{ texts.pp_problematicke_polohy_seznam }}")
print("   {% endif %}")
print()

print("="*80)
print("DŮLEŽITÉ:")
print("="*80)
print("- Vrací STRING '1', '2', nebo '3' (ne integer!)")
print("- Logika: Pokud jakákoliv poloha překročí kategorii X, výsledek je X+1")
print("  - Překročena kat1 → vrátí '2'")
print("  - Překročena kat2 → vrátí '3'")
print("  - Nepřekročeno nic → vrátí '1'")
print("="*80)
