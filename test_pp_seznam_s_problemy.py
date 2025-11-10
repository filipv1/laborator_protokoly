"""
Test pp_problematicke_polohy_seznam - SIMULACE s problematickými polohami
Ukázka jak vypadá výstup když JSOU překročené limity
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

# SIMULOVANÁ DATA - pp_results s PROBLEMATICKÝMI polohami
# Limity pro 480 min:
# PP: kat1 0-100, kat2 101-160, kat3 >160
# N: kat1 0-20, kat2 21-30, kat3 >30

pp_results_kategorie_2 = {
    "trup": [
        {"nazev_polohy": "Předklon trupu", "typ_svalove_prace": "Dynamická", "prumer_min": 120, "typ_pracovni_polohy": "PP"},  # KAT 2
        {"nazev_polohy": "Pokles trupu", "typ_svalove_prace": "Statická", "prumer_min": 15, "typ_pracovni_polohy": "N"},  # KAT 1
    ],
    "hlava_krk": [
        {"nazev_polohy": "Otočení hlavy", "typ_svalove_prace": "Statická", "prumer_min": 25, "typ_pracovni_polohy": "N"},  # KAT 2
        {"nazev_polohy": "Předklon hlavy", "typ_svalove_prace": "Dynamická", "prumer_min": 50, "typ_pracovni_polohy": "PP"},  # KAT 1
    ],
    "phk": [],
    "lhk": [],
    "dk": [],
    "ostatni": []
}

pp_results_kategorie_3 = {
    "trup": [
        {"nazev_polohy": "Předklon trupu", "typ_svalove_prace": "Dynamická", "prumer_min": 170, "typ_pracovni_polohy": "PP"},  # KAT 3
        {"nazev_polohy": "Pokles trupu", "typ_svalove_prace": "Statická", "prumer_min": 15, "typ_pracovni_polohy": "N"},  # KAT 1
    ],
    "hlava_krk": [
        {"nazev_polohy": "Otočení hlavy", "typ_svalove_prace": "Statická", "prumer_min": 35, "typ_pracovni_polohy": "N"},  # KAT 3
        {"nazev_polohy": "Předklon hlavy", "typ_svalove_prace": "Dynamická", "prumer_min": 80, "typ_pracovni_polohy": "PP"},  # KAT 1
    ],
    "phk": [
        {"nazev_polohy": "Zvedání paže nad horizontálu", "typ_svalove_prace": "Dynamická", "prumer_min": 165, "typ_pracovni_polohy": "PP"},  # KAT 3
    ],
    "lhk": [],
    "dk": [],
    "ostatni": []
}

print("="*80)
print("TEST: PP seznam - SIMULACE s překročenými limity")
print("="*80)
print()

# ============================================================================
# SCÉNÁŘ 1: Kategorie 2 (překročena kat1, ale ne kat2)
# ============================================================================
print("SCÉNÁŘ 1: KATEGORIE 2 (překročena kategorie 1)")
print("-" * 80)

texts_kat2 = generate_conditional_texts(
    measurement_data=measurement_data,
    results_data=pp_results_kategorie_2,
    protocol_type="PP_CAS"
)

print()
print("1a) KOMPLETNÍ TEXT:")
print(texts_kat2["prvni_pp_podminka_kategorie"])
print()

print("1b) NOVÝ PLACEHOLDER - POUZE SEZNAM:")
print(f'"{texts_kat2["pp_problematicke_polohy_seznam"]}"')
print()

print("1c) POUŽITÍ V WORD:")
print(f'Překročení limitů kategorie 1 u: {texts_kat2["pp_problematicke_polohy_seznam"]}')
print()
print()

# ============================================================================
# SCÉNÁŘ 2: Kategorie 3 (překročena kat2)
# ============================================================================
print("SCÉNÁŘ 2: KATEGORIE 3 (překročena kategorie 2)")
print("-" * 80)

texts_kat3 = generate_conditional_texts(
    measurement_data=measurement_data,
    results_data=pp_results_kategorie_3,
    protocol_type="PP_CAS"
)

print()
print("2a) KOMPLETNÍ TEXT:")
print(texts_kat3["prvni_pp_podminka_kategorie"])
print()

print("2b) NOVÝ PLACEHOLDER - POUZE SEZNAM:")
print(f'"{texts_kat3["pp_problematicke_polohy_seznam"]}"')
print()

print("2c) POUŽITÍ V WORD:")
print(f'Překročení limitů kategorie 2 u: {texts_kat3["pp_problematicke_polohy_seznam"]}')
print()
print()

# ============================================================================
# SHRNUTÍ
# ============================================================================
print("="*80)
print("SHRNUTÍ - KDE POUŽÍT:")
print("="*80)
print()
print("V Word šabloně máte 2 možnosti:")
print()
print("MOŽNOST A - Kompletní text (automatický):")
print("  {{ texts.prvni_pp_podminka_kategorie }}")
print()
print("MOŽNOST B - Vlastní formulace + seznam:")
print("  Pracovní polohy překračující limity: {{ texts.pp_problematicke_polohy_seznam }}")
print()
print("MOŽNOST C - Podmínka:")
print('  {% if texts.pp_problematicke_polohy_seznam %}')
print('    POZOR: Překročení u {{ texts.pp_problematicke_polohy_seznam }}')
print('  {% else %}')
print('    Vše OK (kategorie 1)')
print('  {% endif %}')
print()

print("="*80)
print("DŮLEŽITÉ:")
print("="*80)
print("- Kategorie 2: Vypíše VŠECHNY polohy, které překročily kat1")
print("- Kategorie 3: Vypíše POUZE ty, které překročily kat2 (nejhorší)")
print("- Formát: 'dynamické předklon trupu, statické otočení hlavy' (lowercase)")
print("- Odděleno čárkami")
print("="*80)
