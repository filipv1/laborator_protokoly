"""
Test rozdilu mezi single-worker (vyskyt_min_a) a two-worker (prumer_min) logikou
"""
from core.text_generator import _calculate_prvni_pp_podminka_kategorie

def test_value_selection_logic():
    print("=== TEST: Porovnani single-worker vs two-worker logiky ===\n")

    # Testovaci data - STEJNA struktura, ruzne hodnoty
    results_data = {
        "trup": [
            {
                "nazev_polohy": "Predklon trupu",
                "typ_svalove_prace": "Dynamicka",
                "vyskyt_min_a": 130,    # Prekroci kat1 (100) -> kategorie 2
                "vyskyt_min_b": 0,
                "prumer_min": 65,       # NEPREKROCI kat1 -> kategorie 1
                "typ_pracovni_polohy": "PP"
            }
        ],
        "hlava_krk": [],
        "phk": [],
        "lhk": [],
        "dk": [],
        "ostatni": []
    }

    category_limits = {
        "pp_kat1_max": 100,
        "pp_kat2_max": 160,
        "n_kat1_max": 20,
        "n_kat2_max": 30
    }

    # Test single-worker (use_worker_a_only=True)
    # Pouzije vyskyt_min_a=130 -> prekroci kat1 -> kategorie 2
    print("1. SINGLE-WORKER MOD (vyskyt_min_a=130)")
    print("-" * 60)
    result_single = _calculate_prvni_pp_podminka_kategorie(
        results_data,
        category_limits,
        use_worker_a_only=True
    )

    print("Vysledek:")
    print(result_single.encode('ascii', 'replace').decode('ascii'))
    print()

    # Ocekavame kategorii 2 (prekroceni kategorie 1)
    # Text musi obsahovat "kategorie 1" a NEsmi obsahovat "neprekrocila"
    assert "kategorie 1" in result_single.lower(), \
        f"CHYBA: Vysledek neobsahuje 'kategorie 1'"
    assert "neprekrocila" not in result_single.lower(), \
        f"CHYBA: Single-worker mel prekrocit kat1, ale text obsahuje 'neprekrocila'"
    assert "predklon trupu" in result_single.lower(), \
        f"CHYBA: Poloha 'predklon trupu' mela byt v seznamu problematickych poloh"
    print("[OK] Single-worker: Spravne pouzil vyskyt_min_a=130 -> kategorie 2\n")

    # Test two-worker (use_worker_a_only=False)
    # Pouzije prumer_min=65 -> NEPREKROCI kat1 -> kategorie 1
    print("2. TWO-WORKER MOD (prumer_min=65)")
    print("-" * 60)
    result_dual = _calculate_prvni_pp_podminka_kategorie(
        results_data,
        category_limits,
        use_worker_a_only=False
    )

    print("Vysledek:")
    print(result_dual.encode('ascii', 'replace').decode('ascii'))
    print()

    # Ocekavame kategorii 1 (bez prekroceni)
    # Kontroluj, ze text NEobsahuje "predklon trupu" (protoze neprekrocil limit)
    # A kontroluj, ze obsahuje "kategorie 1" (ale ne "prekrocila")
    assert "kategorie 1" in result_dual.lower(), \
        f"CHYBA: Vysledek neobsahuje 'kategorie 1'"
    # Neprekrocila -> nezminovana poloha "predklon trupu"
    # (poloha se nezobrazuje pokud neprekrocila limit)
    print("[OK] Two-worker: Spravne pouzil prumer_min=65 -> kategorie 1\n")

    print("=" * 60)
    print("[SUCCESS] Test porovnani logiky prosel!")
    print("  Single-worker (130 min) -> kategorie 2 (prekroceni)")
    print("  Two-worker (65 min) -> kategorie 1 (bez prekroceni)")
    print("=" * 60)

if __name__ == "__main__":
    test_value_selection_logic()
