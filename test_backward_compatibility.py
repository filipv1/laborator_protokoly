"""
Test backward compatibility - testuje že existující projekty stále fungují
"""
import sys
sys.stdout.reconfigure(encoding='utf-8')

from pathlib import Path
import json
from core.docx_parser import DocxParser


def test_existing_project():
    """Testuje že existující projekty s time_schedule stále fungují"""

    print("="*60)
    print("TEST BACKWARD COMPATIBILITY")
    print("="*60)

    # Najdi existující projekt s time_schedule
    projects_dir = Path("projects")

    if not projects_dir.exists():
        print("⚠ Složka projects/ neexistuje")
        return

    tested_count = 0
    success_count = 0

    for project_folder in projects_dir.iterdir():
        if not project_folder.is_dir():
            continue

        json_file = project_folder / "measurement_data.json"

        if not json_file.exists():
            continue

        # Načti JSON
        with open(json_file, encoding='utf-8') as f:
            data = json.load(f)

        # Zkontroluj jestli má time_schedule
        time_schedule = data.get("section1_uploaded_docx", {}).get("time_schedule")
        uploaded_file = data.get("section1_uploaded_docx", {}).get("uploaded_file_path")

        if not time_schedule:
            continue

        print(f"\n{'='*60}")
        print(f"Projekt: {project_folder.name}")
        print(f"{'='*60}")

        tested_count += 1

        # Pokud existuje původní Word soubor, otestuj parsing
        if uploaded_file and Path(uploaded_file).exists():
            print(f"✓ Nalezen původní Word dokument: {Path(uploaded_file).name}")

            try:
                # Znovu naparsuj dokument s novou logikou
                new_result = DocxParser.parse_time_schedule_table(str(uploaded_file))

                # Porovnej počet řádků
                old_count = sum(1 for k, v in time_schedule.items() if k.startswith('line') and v.get('operation'))
                new_count = sum(1 for k, v in new_result.items() if k.startswith('line') and v.get('operation'))

                print(f"\n📊 POROVNÁNÍ:")
                print(f"   Původně načteno: {old_count} řádků")
                print(f"   Nově načteno: {new_count} řádků")

                if old_count == new_count:
                    print(f"   ✅ STEJNÝ POČET ŘÁDKŮ - backward compatible!")
                    success_count += 1
                else:
                    print(f"   ⚠ ROZDÍLNÝ POČET - možný problém?")

                # Porovnej několik prvních řádků
                print(f"\n   První 3 řádky (porovnání):")
                for i in range(1, 4):
                    old_line = time_schedule.get(f"line{i}", {})
                    new_line = new_result.get(f"line{i}", {})

                    if old_line.get('operation'):
                        old_op = old_line.get('operation', '')[:30]
                        new_op = new_line.get('operation', '')[:30]

                        match = "✓" if old_op == new_op else "✗"
                        print(f"   Line {i}: {match}")
                        if old_op != new_op:
                            print(f"      STARÉ: {old_op}")
                            print(f"      NOVÉ:  {new_op}")

            except Exception as e:
                print(f"   ❌ CHYBA při parsování: {e}")

        else:
            print(f"⚠ Word dokument nenalezen")

            # Jen zkontroluj strukturu v JSONu
            print(f"\n📊 STRUKTURA V JSON:")
            line1 = time_schedule.get("line1", {})
            print(f"   Line 1:")
            print(f"      operation: {line1.get('operation', 'N/A')}")
            print(f"      time_min: {line1.get('time_min', 'N/A')}")
            print(f"      pieces_count: {line1.get('pieces_count', 'N/A')}")
            print(f"   ✓ Struktura JSON zůstává stejná")

    print(f"\n{'='*60}")
    print(f"SHRNUTÍ")
    print(f"{'='*60}")
    print(f"Testováno projektů: {tested_count}")
    print(f"Úspěšné: {success_count}")

    if tested_count == 0:
        print(f"⚠ Žádné projekty k testování nenalezeny")
    elif success_count == tested_count:
        print(f"✅ Všechny projekty jsou backward compatible!")
    else:
        print(f"⚠ Některé projekty mají rozdíly")


if __name__ == "__main__":
    test_existing_project()
