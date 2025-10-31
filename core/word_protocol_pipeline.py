"""
Word Protocol Pipeline - kompletní pipeline pro generování Word protokolů
"""
import json
from pathlib import Path
from typing import Optional
from read_lsz_results import read_lsz_results  # export_charts odstraněn
from generate_word_from_two_sources import generate_word_protocol_v2, generate_word_protocol_v1


class WordProtocolPipeline:
    """Pipeline pro generování Word protokolů z Excelů a JSONů"""

    def __init__(self, project_folder: Path):
        """
        Args:
            project_folder: Cesta k složce projektu s measurement_data.json
        """
        self.project_folder = Path(project_folder)
        self.measurement_json_path = self.project_folder / "measurement_data.json"
        self.results_json_path = self.project_folder / "lsz_results.json"

    def generate_protocol(
        self,
        excel_path: Path,
        template_path: Path,
        output_path: Path
    ) -> tuple[bool, str]:
        """
        Kompletní pipeline:
        1. Načte measurement_data.json z project_folder
        2. Spustí read_lsz_results.py (Excel → lsz_results.json)
        3. Spustí generate_word_from_two_sources.py (2 JSONy + template → Word)

        Args:
            excel_path: Cesta k LSZ Excel souboru
            template_path: Cesta k Word šabloně
            output_path: Kam uložit výsledný Word protokol

        Returns:
            (success: bool, message: str)
        """
        try:
            # KROK 1: Validace measurement_data.json
            if not self.measurement_json_path.exists():
                return False, f"measurement_data.json nenalezen v:\n{self.project_folder}"

            # Načti measurement_data.json pro zjištění what_is_evaluated a worker_count
            with open(self.measurement_json_path, encoding='utf-8') as f:
                measurement_data = json.load(f)

            what_is_evaluated = measurement_data.get("section3_additional_data", {}).get("what_is_evaluated", "kusy")
            worker_count = measurement_data.get("section0_file_selection", {}).get("worker_count", 2)

            # KROK 2: Validace Excel souboru
            excel_path = Path(excel_path)
            if not excel_path.exists():
                return False, f"LSZ Excel soubor nenalezen:\n{excel_path}"

            if excel_path.suffix not in ['.xlsm', '.xlsx']:
                return False, f"Neplatný Excel soubor (očekává se .xlsm nebo .xlsx):\n{excel_path}"

            # KROK 3: Validace Word template
            template_path = Path(template_path)
            if not template_path.exists():
                return False, f"Word šablona nenalezena:\n{template_path}"

            if template_path.suffix.lower() != '.docx':
                return False, f"Neplatná Word šablona (očekává se .docx):\n{template_path}"

            # KROK 4: Spustit read_lsz_results → vytvoří lsz_results.json
            print(f"→ Načítám data z Excel: {excel_path.name}")
            print(f"→ Co se hodnotí: {what_is_evaluated}")
            print(f"→ Počet pracovníků: {worker_count}")

            results = read_lsz_results(str(excel_path), what_is_evaluated, worker_count)

            # ZAKOMENTOVÁNO: Export grafů zakázán
            # print("→ Exportuji grafy...")
            # charts = export_charts(str(excel_path))
            # results["charts"] = charts

            # Uložit lsz_results.json do project_folder
            with open(self.results_json_path, 'w', encoding='utf-8') as f:
                json.dump(results, f, ensure_ascii=False, indent=4)

            print(f"✓ lsz_results.json vytvořen: {self.results_json_path}")

            # KROK 5: Validace output path
            output_path = Path(output_path)
            if output_path.suffix.lower() != '.docx':
                return False, f"Neplatný výstupní soubor (očekává se .docx):\n{output_path}"

            # Vytvoř parent directory, pokud neexistuje
            output_path.parent.mkdir(parents=True, exist_ok=True)

            # KROK 6: Spustit generate_word_protocol_v2
            print(f"→ Generuji Word protokol...")
            generate_word_protocol_v2(
                str(self.measurement_json_path),
                str(self.results_json_path),
                str(template_path),
                str(output_path)
            )

            print(f"✓ Word protokol vygenerován: {output_path}")

            return True, f"Word protokol úspěšně vygenerován:\n{output_path}"

        except Exception as e:
            import traceback
            error_details = traceback.format_exc()
            print(f"ERROR TRACEBACK:\n{error_details}")
            return False, f"Chyba při generování Word protokolu:\n{str(e)}"
