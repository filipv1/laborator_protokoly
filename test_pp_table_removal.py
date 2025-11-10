"""
Test odstranění celých prázdných PP tabulek
"""
import shutil
from pathlib import Path
from docx import Document
from generate_word_from_two_sources import remove_empty_pp_rows


def count_pp_tables(docx_path):
    """Spočítá PP tabulky v dokumentu"""
    doc = Document(docx_path)
    pp_count = 0

    pp_keywords = [
        "TRUP", "Trup",
        "HLAVA_KRK", "HLAVA A KRK", "Hlava a krk",
        "PHK", "Pravá horní končetina",
        "LHK", "Levá horní končetina",
        "DOLNÍ KONČETINY", "Dolní končetiny", "DKK",
        "OSTATNÍ ČÁSTI TĚLA", "Ostatní části těla", "OST",
        "Statická", "Dynamická"
    ]

    for table in doc.tables:
        if len(table.columns) != 6:
            continue

        # Zkontroluj PP keywords
        is_pp_table = False
        for row in table.rows[:5]:
            row_text = " ".join(cell.text for cell in row.cells)
            for keyword in pp_keywords:
                if keyword in row_text:
                    is_pp_table = True
                    break
            if is_pp_table:
                break

        if is_pp_table:
            pp_count += 1

    return pp_count


def test_pp_table_removal():
    """Test odstranění prázdných PP tabulek"""

    # Použij existující PP dokument
    source_path = Path("projects/325_Ascari_sro/PP_325_Ascari_sro_CAS_protokol.docx")
    test_path = Path("test_pp_removal.docx")

    if not source_path.exists():
        print(f"ERROR: Zdrojový soubor neexistuje: {source_path}")
        return

    # Zkopíruj dokument pro test
    shutil.copy2(source_path, test_path)
    print(f"Zkopírován dokument: {source_path} -> {test_path}")

    # Spočítej tabulky před úpravou
    tables_before = count_pp_tables(test_path)
    print(f"Počet PP tabulek před úpravou: {tables_before}")

    # Spusť funkci odstranění
    print("\n" + "="*60)
    print("Spouštím remove_empty_pp_rows()...")
    print("="*60)
    remove_empty_pp_rows(str(test_path))
    print("="*60 + "\n")

    # Spočítej tabulky po úpravě
    tables_after = count_pp_tables(test_path)
    print(f"Počet PP tabulek po úpravě: {tables_after}")

    if tables_before > tables_after:
        print(f"✓ ÚSPĚCH: Odstraněno {tables_before - tables_after} prázdných tabulek")
    else:
        print(f"ℹ Žádné tabulky nebyly odstraněny")

    # Analýza zbývajících tabulek
    if tables_after > 0:
        print(f"\nZbývající PP tabulky obsahují datové řádky.")

    print(f"\nVýsledný dokument uložen jako: {test_path}")
    print("Otevřete dokument v MS Word pro vizuální kontrolu.")


if __name__ == "__main__":
    print("TEST ODSTRANĚNÍ PRÁZDNÝCH PP TABULEK")
    print("="*60)
    test_pp_table_removal()