"""
Integracni test: Vygenerovani PP protokolu pro single-worker
"""
import json
from pathlib import Path
from core.text_generator import generate_conditional_texts

def test_single_worker_integration():
    print("=== INTEGRACNI TEST: Single-worker PP protokol ===\n")

    # Nacist testovaci data
    project_path = Path("projects/test_single_worker_PP")

    with open(project_path / "measurement_data.json", "r", encoding="utf-8") as f:
        measurement_data = json.load(f)

    with open(project_path / "pp_results.json", "r", encoding="utf-8") as f:
        pp_results = json.load(f)

    # Vygenerovat conditional texts
    print("Generuji conditional texts pro single-worker PP protokol...")
    print("-" * 60)

    texts = generate_conditional_texts(
        measurement_data=measurement_data,
        results_data=pp_results,
        protocol_type="PP_CAS"
    )

    # Vypsat vysledky
    print("\n" + "=" * 60)
    print("VYSLEDKY:")
    print("=" * 60)

    print("\n1. prvni_pp_podminka_kategorie:")
    print(texts["prvni_pp_podminka_kategorie"].encode('ascii', 'replace').decode('ascii'))

    print("\n2. pp_problematicke_polohy_seznam:")
    print(texts["pp_problematicke_polohy_seznam"].encode('ascii', 'replace').decode('ascii'))

    print("\n3. pp_kategorie_cislo:")
    print(texts["pp_kategorie_cislo"])

    print("\n" + "=" * 60)

    # Kontroly - ocekavame kategorii 2 (vyskyt_min_a=130 prekroci kat1=100)
    assert "kategorie 1" in texts["prvni_pp_podminka_kategorie"].lower(), \
        f"CHYBA: Vysledek neobsahuje 'kategorie 1'"

    assert "neprekrocila" not in texts["prvni_pp_podminka_kategorie"].lower(), \
        f"CHYBA: Single-worker mel prekrocit kat1, ale text obsahuje 'neprekrocila'"

    assert texts["pp_kategorie_cislo"] == "2", \
        f"CHYBA: pp_kategorie_cislo mel byt '2', je '{texts['pp_kategorie_cislo']}'"

    assert len(texts["pp_problematicke_polohy_seznam"]) > 0, \
        f"CHYBA: pp_problematicke_polohy_seznam mel obsahovat polohy"

    print("[SUCCESS] Kategorizace probehla podle vyskyt_min_a!")
    print("  - Kategorie 2 (vyskyt_min_a=130 > kat1_max=100)")
    print("  - Problematicke polohy: " + texts["pp_problematicke_polohy_seznam"])

    # Ulozit vysledky pro inspekci
    output_path = project_path / "conditional_texts_output.json"
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(texts, f, indent=2, ensure_ascii=False)

    print(f"\n[INFO] Vysledky ulozeny do: {output_path}")

if __name__ == "__main__":
    test_single_worker_integration()
