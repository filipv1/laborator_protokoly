"""
Word Protocol Pipeline - kompletní pipeline pro generování Word protokolů
Podporuje LSZ, PP a CFZ protokoly
"""
import json
from pathlib import Path
from typing import Optional, Literal
from read_lsz_results import read_lsz_results
from read_pp_results import read_pp_results
from generate_word_from_two_sources import generate_word_protocol_v2, generate_word_protocol_v1

# Type hint pro protocol types
ProtocolType = Literal["LSZ", "PP_CAS", "PP_KUSY", "CFZ"]


class WordProtocolPipeline:
    """Pipeline pro generování Word protokolů z Excelů a JSONů"""

    def __init__(self, project_folder: Path):
        """
        Args:
            project_folder: Cesta k složce projektu s measurement_data.json
        """
        self.project_folder = Path(project_folder)
        self.measurement_json_path = self.project_folder / "measurement_data.json"
        # results_json_path bude nastaven dynamicky podle protokolu
        self.results_json_path = None

    def _detect_protocol(self, excel_path: Path) -> ProtocolType:
        """
        Detekuje typ protokolu z názvu Excel souboru

        Args:
            excel_path: Cesta k Excel souboru

        Returns:
            Protocol type ("LSZ", "PP_CAS", "PP_KUSY", "CFZ")

        Raises:
            ValueError: Pokud nelze detekovat protokol
        """
        name = excel_path.name.upper()

        if name.startswith("LSZ_"):
            return "LSZ"
        elif "_CAS" in name and name.startswith("PP_"):
            return "PP_CAS"
        elif "_KUSY" in name and name.startswith("PP_"):
            return "PP_KUSY"
        elif name.startswith("CFZ_"):
            return "CFZ"
        else:
            raise ValueError(
                f"Nelze detekovat typ protokolu z názvu souboru: {excel_path.name}\n"
                f"Očekávané formáty: LSZ_*.xlsm, PP_*_CAS.xlsx, PP_*_KUSY.xlsx, CFZ_*.xlsx"
            )

    def generate_protocol(
        self,
        excel_path: Path,
        template_path: Path,
        output_path: Path
    ) -> tuple[bool, str]:
        """
        Kompletní pipeline pro generování Word protokolů
        Podporuje LSZ, PP (ČAS/KUSY) a CFZ protokoly

        Pipeline:
        1. Detekuje typ protokolu z názvu Excel souboru
        2. Načte measurement_data.json z project_folder
        3. Spustí příslušný reader (read_lsz_results nebo read_pp_results)
        4. Vytvoří results JSON (lsz_results.json nebo pp_results.json)
        5. Spustí generate_word_protocol_v2 s protocol_type parametrem

        Args:
            excel_path: Cesta k Excel souboru (LSZ/PP/CFZ)
            template_path: Cesta k Word šabloně
            output_path: Kam uložit výsledný Word protokol

        Returns:
            (success: bool, message: str)
        """
        try:
            # KROK 0: Detekuj typ protokolu z Excel názvu
            excel_path = Path(excel_path)
            protocol_type = self._detect_protocol(excel_path)
            print(f"Detekovan protocol: {protocol_type}")

            # KROK 1: Validace measurement_data.json
            if not self.measurement_json_path.exists():
                return False, f"measurement_data.json nenalezen v:\n{self.project_folder}"

            # Načti measurement_data.json pro zjištění what_is_evaluated a worker_count
            with open(self.measurement_json_path, encoding='utf-8') as f:
                measurement_data = json.load(f)

            what_is_evaluated = measurement_data.get("section3_additional_data", {}).get("what_is_evaluated", "kusy")
            worker_count = measurement_data.get("section0_file_selection", {}).get("worker_count", 2)

            # KROK 2: Validace Excel souboru
            if not excel_path.exists():
                return False, f"Excel soubor nenalezen:\n{excel_path}"

            if excel_path.suffix not in ['.xlsm', '.xlsx']:
                return False, f"Neplatný Excel soubor (očekává se .xlsm nebo .xlsx):\n{excel_path}"

            # KROK 3: Validace Word template
            template_path = Path(template_path)
            if not template_path.exists():
                return False, f"Word šablona nenalezena:\n{template_path}"

            if template_path.suffix.lower() != '.docx':
                return False, f"Neplatná Word šablona (očekává se .docx):\n{template_path}"

            # KROK 4: Spustit příslušný reader podle protokolu
            print(f"Nacitam data z Excel: {excel_path.name}")
            print(f"Co sehodnoti: {what_is_evaluated}")
            print(f"Pocet pracovniku: {worker_count}")

            # Dispatch k příslušnému readeru
            if protocol_type == "LSZ":
                results = read_lsz_results(str(excel_path), what_is_evaluated, worker_count)
                self.results_json_path = self.project_folder / "lsz_results.json"
            elif protocol_type in ("PP_CAS", "PP_KUSY"):
                # PP používá stejný reader pro ČAS i KUSY
                what_is_evaluated_pp = "cas" if protocol_type == "PP_CAS" else "kusy"
                results = read_pp_results(str(excel_path), what_is_evaluated_pp, worker_count)
                self.results_json_path = self.project_folder / "pp_results.json"
            elif protocol_type == "CFZ":
                # CFZ zatím není implementován
                return False, f"CFZ protokol zatím není implementován!"
            else:
                return False, f"Neznámý typ protokolu: {protocol_type}"

            # Uložit results JSON do project_folder
            with open(self.results_json_path, 'w', encoding='utf-8') as f:
                json.dump(results, f, ensure_ascii=False, indent=4)

            print(f"OK {self.results_json_path.name} vytvoren: {self.results_json_path}")

            # KROK 5: Validace output path
            output_path = Path(output_path)
            if output_path.suffix.lower() != '.docx':
                return False, f"Neplatný výstupní soubor (očekává se .docx):\n{output_path}"

            # Vytvoř parent directory, pokud neexistuje
            output_path.parent.mkdir(parents=True, exist_ok=True)

            # KROK 6: Spustit generate_word_protocol_v2 s protocol_type
            print(f"Generuji Word protokol ({protocol_type})...")
            generate_word_protocol_v2(
                str(self.measurement_json_path),
                str(self.results_json_path),
                str(template_path),
                str(output_path),
                protocol_type=protocol_type  # NOVÝ PARAMETR
            )

            print(f"OK Word protokol vygenerovan: {output_path}")

            return True, f"Word protokol úspěšně vygenerován:\n{output_path}"

        except Exception as e:
            import traceback
            error_details = traceback.format_exc()
            print(f"ERROR TRACEBACK:\n{error_details}")
            return False, f"Chyba při generování Word protokolu:\n{str(e)}"
