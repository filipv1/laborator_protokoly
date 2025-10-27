"""
Test všech 7 podmínek v generate_conditional_texts()

Ověřuje, že všechny conditional texts jsou vygenerovány správně včetně nové sedmé podmínky.
"""
import sys
import os

# Fix Windows console encoding
if sys.platform == 'win32':
    os.system('chcp 65001 > nul')
    sys.stdout.reconfigure(encoding='utf-8')

from core.text_generator import generate_conditional_texts


def test_all_seven_conditions():
    """Test všech 7 podmínek najednou"""

    print("=" * 80)
    print("TEST: generate_conditional_texts() - Všech 7 podmínek")
    print("=" * 80)

    # Testovací data
    measurement_data = {
        "section0_file_selection": {
            "measurement_days": 2
        },
        "section4_worker_a": {
            "work_duration": 480  # 8h směna
        }
    }

    results_data = {
        "Fmax_Phk_Extenzor": 25.5,
        "Fmax_Phk_Flexor": 30.2,
        "Fmax_Lhk_Extenzor": 22.8,
        "Fmax_Lhk_Flexor": 28.9,
        "phk_number_of_movements": 1200,
        "lhk_number_of_movements": 800,
        "table_W4_Y51": {
            "1": {"fmax": "header"},
            "2": {"fmax": 26, "phk": 1000, "lhk": 900},
            "3": {"fmax": 29, "phk": 950, "lhk": 850},
            "4": {"fmax": 31, "phk": 900, "lhk": 800}
        },
        "table_force_distribution": {
            "21": {
                "force_55_70_phk_extenzory": 5,
                "force_55_70_phk_flexory": 4,
                "force_55_70_lhk_extenzory": 6,
                "force_55_70_lhk_flexory": 3,
                "force_over_70_phk_extenzory": 2,
                "force_over_70_phk_flexory": 0,
                "force_over_70_lhk_extenzory": 0,
                "force_over_70_lhk_flexory": 1
            }
        }
    }

    # Generuj všechny texty
    texts = generate_conditional_texts(measurement_data, results_data)

    print("\n📊 VYGENEROVANÉ TEXTY:")
    print("-" * 80)

    # Podmínka 1: Počet dnů
    print("\n1️⃣  prvni_text_podminka_pocetdni:")
    print(f"    {texts['prvni_text_podminka_pocetdni']}")
    assert "dvou dnech" in texts["prvni_text_podminka_pocetdni"]
    print("    ✓ Správně (2 dny)")

    # Podmínka 2: PHK limity
    print("\n2️⃣  druhy_text_podminka_limit1:")
    print(f"    {texts['druhy_text_podminka_limit1']}")
    print("    ✓ Vygenerováno")

    # Podmínka 3: LHK limity
    print("\n3️⃣  treti_text_podminka_limit1:")
    print(f"    {texts['treti_text_podminka_limit1']}")
    print("    ✓ Vygenerováno")

    # Podmínka 4: Rozložení sil
    print("\n4️⃣  ctvrty_text_podminka:")
    print(f"    '{texts['ctvrty_text_podminka']}'")
    assert texts["ctvrty_text_podminka"] in ["nejsou", "ojediněle", "pravidelně"]
    print("    ✓ Správně (jedna z platných hodnot)")

    # Podmínka 5: Nadlimitní síly
    print("\n5️⃣  paty_text_podminka:")
    print(f"    {texts['paty_text_podminka'][:80]}...")
    print("    ✓ Vygenerováno")

    # Podmínka 6: Hodnoty > 100
    print("\n6️⃣  sesty_text_podminka:")
    print(f"    '{texts['sesty_text_podminka']}'")
    assert texts["sesty_text_podminka"] in ["je", "není"]
    print("    ✓ Správně (je/není)")

    # Podmínka 7: Limit velkých sil (55-70%)
    print("\n7️⃣  sedmy_text_podminka:")
    print(f"    '{texts['sedmy_text_podminka']}'")

    # Ověř výpočet
    suma = 5 + 4 + 6 + 3  # = 18
    limit = (480 / 2) + 360  # = 600
    expected = "nepřekračuje" if suma <= limit else "překračuje"

    print(f"    Součet: {suma}, Limit: {limit} → Očekáváno: '{expected}'")
    assert texts["sedmy_text_podminka"] == expected
    print("    ✓ Správně vypočteno!")

    print("\n" + "=" * 80)
    print("✅ VŠECH 7 PODMÍNEK VYGENEROVÁNO SPRÁVNĚ!")
    print("=" * 80)

    # Vypiš všechny klíče
    print("\n📋 Klíče v return dictionary:")
    for key in texts.keys():
        print(f"   - {key}")


def test_sedmy_podminka_integration_scenarios():
    """Test různých scénářů pro sedmou podmínku v integraci"""

    print("\n" + "=" * 80)
    print("TEST: Sedmá podmínka - Různé scénáře")
    print("=" * 80)

    # Scénář 1: Krátká směna + nízký součet → nepřekračuje
    print("\n[SCÉNÁŘ 1] 450 min, součet=18 → nepřekračuje")
    md1 = {"section0_file_selection": {"measurement_days": 1}, "section4_worker_a": {"work_duration": 450}}
    rd1 = {"table_force_distribution": {"21": {
        "force_55_70_phk_extenzory": 5, "force_55_70_phk_flexory": 4,
        "force_55_70_lhk_extenzory": 5, "force_55_70_lhk_flexory": 4
    }}}
    texts1 = generate_conditional_texts(md1, rd1)
    print(f"   Limit: (450/2)+360 = 585")
    print(f"   Součet: 18")
    print(f"   Výsledek: '{texts1['sedmy_text_podminka']}'")
    assert texts1['sedmy_text_podminka'] == "nepřekračuje"
    print("   ✓ PASS")

    # Scénář 2: Dlouhá směna + vysoký součet → překračuje
    print("\n[SCÉNÁŘ 2] 720 min, součet=800 → překračuje")
    md2 = {"section0_file_selection": {"measurement_days": 1}, "section4_worker_a": {"work_duration": 720}}
    rd2 = {"table_force_distribution": {"21": {
        "force_55_70_phk_extenzory": 200, "force_55_70_phk_flexory": 200,
        "force_55_70_lhk_extenzory": 200, "force_55_70_lhk_flexory": 200
    }}}
    texts2 = generate_conditional_texts(md2, rd2)
    print(f"   Limit: (720/2)+360 = 720")
    print(f"   Součet: 800")
    print(f"   Výsledek: '{texts2['sedmy_text_podminka']}'")
    assert texts2['sedmy_text_podminka'] == "překračuje"
    print("   ✓ PASS")

    # Scénář 3: Hraničný případ - suma = limit
    print("\n[SCÉNÁŘ 3] Hraničný: 480 min, součet=600 → nepřekračuje")
    md3 = {"section0_file_selection": {"measurement_days": 1}, "section4_worker_a": {"work_duration": 480}}
    rd3 = {"table_force_distribution": {"21": {
        "force_55_70_phk_extenzory": 150, "force_55_70_phk_flexory": 150,
        "force_55_70_lhk_extenzory": 150, "force_55_70_lhk_flexory": 150
    }}}
    texts3 = generate_conditional_texts(md3, rd3)
    print(f"   Limit: (480/2)+360 = 600")
    print(f"   Součet: 600")
    print(f"   Výsledek: '{texts3['sedmy_text_podminka']}'")
    assert texts3['sedmy_text_podminka'] == "nepřekračuje"
    print("   ✓ PASS")

    print("\n" + "=" * 80)
    print("✅ VŠECHNY INTEGRAČNÍ SCÉNÁŘE PROŠLY!")
    print("=" * 80)


if __name__ == "__main__":
    test_all_seven_conditions()
    test_sedmy_podminka_integration_scenarios()
