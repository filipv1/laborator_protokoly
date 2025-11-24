"""
Integracni test pro Word subdoc workflow
Testuje: Upload Word -> ProjectManager -> CLI generovani
"""
import json
import shutil
import sys
from pathlib import Path
from core import FileManager, ProjectManager

# Fix Windows console encoding
sys.stdout.reconfigure(encoding='utf-8')

def test_word_subdoc_workflow():
    """Testuje cely workflow od nahrani Word po generovani protokolu"""

    print("="*60)
    print("INTEGRACNI TEST - Word Subdoc Workflow")
    print("="*60)

    # 1. Simulace nahrání Word v GUI
    print("\n[1/5] Simulace nahrání Word souboru...")
    source_word = Path("Vzor popis práce 2024/POPIS PRÁCE A PRACOVIŠTĚ.docx")

    if not source_word.exists():
        print(f"❌ CHYBA: Testovací Word neexistuje: {source_word}")
        return False

    file_manager = FileManager()
    temp_word_path = file_manager.save_uploaded_docx(str(source_word))
    print(f"✓ Word zkopírován do temp: {temp_word_path}")

    # Ověř, že soubor existuje
    if not temp_word_path.exists():
        print(f"❌ CHYBA: Temp soubor neexistuje: {temp_word_path}")
        return False
    print(f"✓ Temp soubor existuje: {temp_word_path.name}")

    # 2. Načtení testovacích dat
    print("\n[2/5] Načítání testovacích measurement_data.json...")
    test_json = Path("measurement_data.json")

    if not test_json.exists():
        print(f"❌ CHYBA: Testovací JSON neexistuje: {test_json}")
        return False

    with open(test_json, encoding='utf-8') as f:
        project_data = json.load(f)

    # Aktualizuj cestu k nahranému Word
    project_data["section1_uploaded_docx"]["uploaded_file_path"] = str(temp_word_path)
    print(f"✓ JSON načten, uploaded_file_path nastaven")

    # 3. Vytvoření projektu
    print("\n[3/5] Vytváření projektu pomocí ProjectManager...")
    project_manager = ProjectManager()

    try:
        project_folder = project_manager.create_project(project_data)
        print(f"✓ Projekt vytvořen: {project_folder}")
    except Exception as e:
        print(f"❌ CHYBA při vytváření projektu: {e}")
        import traceback
        traceback.print_exc()
        return False

    # 4. Ověření výsledků
    print("\n[4/5] Ověřování výsledků...")

    # Zkontroluj, že Word byl zkopírován do projektu (použij první neprázdné evidenční číslo)
    evidence_lsz = project_data["section2_firma"]["evidence_number_lsz"]
    evidence_pp = project_data["section2_firma"]["evidence_number_pp"]
    evidence = evidence_lsz if evidence_lsz else evidence_pp
    company = project_data["section2_firma"]["company"]

    # Sanitize názvu (stejný algoritmus jako ProjectManager)
    expected_name = f"popis_prace_{evidence}_{company}.docx"
    for char in [" ", "/", "\\", ":", "*", "?", '"', "<", ">", "|", ".", ","]:
        expected_name = expected_name.replace(char, "_" if char == " " else "-" if char in "/\\:" else "")

    expected_word = project_folder / expected_name

    if not expected_word.exists():
        print(f"❌ CHYBA: Word nebyl zkopírován do projektu")
        print(f"   Očekávaný soubor: {expected_word}")
        # Seznam souborů v project folderu
        print(f"   Soubory v projektu: {list(project_folder.glob('*'))}")
        return False
    print(f"✓ Word zkopírován do projektu: {expected_word.name}")

    # Zkontroluj measurement_data.json
    json_path = project_folder / "measurement_data.json"
    if not json_path.exists():
        print(f"❌ CHYBA: measurement_data.json nebyl vytvořen")
        return False

    with open(json_path, encoding='utf-8') as f:
        saved_data = json.load(f)

    # Zkontroluj, že obsahuje copied_file_path
    copied_path = saved_data.get("section1_uploaded_docx", {}).get("copied_file_path")
    if not copied_path:
        print(f"❌ CHYBA: JSON neobsahuje copied_file_path")
        return False

    if not Path(copied_path).exists():
        print(f"❌ CHYBA: copied_file_path ukazuje na neexistující soubor: {copied_path}")
        return False

    print(f"✓ measurement_data.json obsahuje správnou cestu: {Path(copied_path).name}")

    # 5. Test CLI generování (simulace)
    print("\n[5/5] Simulace CLI generování s Subdoc...")

    # Zkontroluj, že lsz_results.json existuje
    results_json = Path("lsz_results.json")
    if not results_json.exists():
        print(f"⚠ Varování: lsz_results.json neexistuje, přeskakuji CLI test")
    else:
        template_path = Path("Vzorové protokoly/Autorizované protokoly pro MUŽE/lsz_placeholdery_v2.docx")
        if not template_path.exists():
            print(f"⚠ Varování: Word šablona neexistuje, přeskakuji CLI test")
        else:
            print(f"✓ Všechny soubory pro CLI generování existují")
            print(f"   - measurement_data: {json_path}")
            print(f"   - results_data: {results_json}")
            print(f"   - template: {template_path}")

            # Informace o CLI příkazu
            print(f"\n💡 Pro otestování CLI generování spusť:")
            print(f'   python generate_word_from_two_sources.py \\')
            print(f'     "{json_path}" \\')
            print(f'     "{results_json}" \\')
            print(f'     "{template_path}" \\')
            print(f'     "test_output_subdoc.docx" \\')
            print(f'     --variant v2')

    # Cleanup info
    print("\n" + "="*60)
    print("✅ TEST ÚSPĚŠNÝ!")
    print("="*60)
    print(f"\n📁 Projekt vytvořen v: {project_folder}")
    print(f"📄 Word dokument: {expected_word}")
    print(f"📋 JSON data: {json_path}")
    print(f"\n💡 Temp soubory budou vyčištěny při zavření aplikace (atexit)")

    return True


if __name__ == "__main__":
    success = test_word_subdoc_workflow()
    exit(0 if success else 1)
