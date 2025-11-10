"""
Test na reálném PP dokumentu
"""
import shutil
from pathlib import Path
from docx import Document
from generate_word_from_two_sources import remove_empty_pp_rows


def analyze_pp_document_before_after(docx_path):
    """Analyzuje PP dokument před a po úpravě"""
    doc = Document(docx_path)

    pp_count = 0
    empty_tables = []

    for idx, table in enumerate(doc.tables):
        if len(table.columns) != 6:
            continue

        # Je to PP tabulka?
        is_pp = False
        for row in table.rows[:5]:
            row_text = " ".join(cell.text for cell in row.cells)
            if "Statická" in row_text or "Dynamická" in row_text or "TRUP" in row_text:
                is_pp = True
                break

        if is_pp:
            pp_count += 1

            # Spočítej datové řádky
            data_rows = 0
            for row_idx in range(1, len(table.rows)):
                text = table.rows[row_idx].cells[0].text.strip().upper()
                # Skip záhlaví, sekce, OSTATNI
                if ("NEPŘIJATELNÁ" in text or "PODMÍNĚNĚ" in text or
                    text in ["TRUP", "HLAVA_KRK", "PHK", "LHK", "DK", "OSTATNI"] or
                    "OSTATNI" in text or "ULTRATHINK" in text):
                    continue

                # Zkontroluj hodnoty
                try:
                    val2 = table.rows[row_idx].cells[2].text.strip()
                    val3 = table.rows[row_idx].cells[3].text.strip()
                    if "VÝSKYT" not in val2.upper() and "MUŽ" not in val2.upper():
                        data_rows += 1
                except:
                    pass

            if data_rows == 0:
                empty_tables.append(idx)

    return pp_count, empty_tables


def test_real_document():
    """Test na reálném PP dokumentu"""
    source = Path("projects/325_Ascari_sro/PP_325_Ascari_sro_CAS_protokol.docx")
    test_copy = Path("test_real_pp_copy.docx")

    # Zkopíruj dokument
    shutil.copy2(source, test_copy)
    print(f"Zkopírován dokument: {source} → {test_copy}")

    # Analýza před
    pp_before, empty_before = analyze_pp_document_before_after(test_copy)
    print(f"\nPŘED ÚPRAVOU:")
    print(f"  PP tabulek celkem: {pp_before}")
    print(f"  Prázdných tabulek (pouze záhlaví/sekce/OSTATNI): {len(empty_before)}")
    if empty_before:
        print(f"  Indexy prázdných tabulek: {empty_before}")

    # Spusť funkci
    print("\nSpouštím remove_empty_pp_rows()...")
    print("-"*60)
    remove_empty_pp_rows(str(test_copy))
    print("-"*60)

    # Analýza po
    pp_after, empty_after = analyze_pp_document_before_after(test_copy)
    print(f"\nPO ÚPRAVĚ:")
    print(f"  PP tabulek celkem: {pp_after}")
    print(f"  Prázdných tabulek: {len(empty_after)}")

    # Výsledek
    print("\n" + "="*60)
    if len(empty_after) == 0:
        print("✓✓✓ ÚSPĚCH! Všechny prázdné tabulky byly odstraněny!")
    else:
        print(f"✗✗✗ CHYBA! Zbývá {len(empty_after)} prázdných tabulek")
    print("="*60)

    print(f"\nVýsledný dokument uložen jako: {test_copy}")
    print("Otevřete v MS Word pro vizuální kontrolu.")


if __name__ == "__main__":
    print("TEST NA REÁLNÉM PP DOKUMENTU")
    print("="*60)
    test_real_document()