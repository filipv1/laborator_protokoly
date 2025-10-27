"""
Project Manager - správa projektů a generování souborů
"""
import json
import shutil
from pathlib import Path
from typing import Dict, Any
from .excel_filler import ExcelFiller
from .table_copier import TableCopier
from config import LSZ_MAPPING, PP_CAS_MAPPING, PP_KUSY_MAPPING, CFZ_MAPPING


class ProjectManager:
    """Správa projektů - vytváření složek a kopírování šablon"""

    def __init__(self, base_projects_dir: str = "projects"):
        """
        Args:
            base_projects_dir: Základní složka pro projekty
        """
        self.base_dir = Path(__file__).parent.parent / base_projects_dir
        self.templates_dir = Path(__file__).parent.parent / "templates" / "excel"

        self.base_dir.mkdir(parents=True, exist_ok=True)

    def create_project(self, project_data: Dict[str, Any]) -> Path:
        """
        Vytvoří nový projekt - složku a zkopíruje příslušné Excel šablony.

        Args:
            project_data: Data z formuláře (JSON struktura)

        Returns:
            Path k vytvořené složce projektu
        """
        project_folder = self._create_project_folder(project_data)
        copied_files = self._copy_excel_templates(project_folder, project_data)
        self._fill_excel_data(copied_files, project_data)
        self._copy_time_schedule(copied_files, project_data)
        self._copy_uploaded_docx(project_folder, project_data)
        self._save_measurement_json(project_folder, project_data)

        return project_folder

    def _create_project_folder(self, project_data: Dict[str, Any]) -> Path:
        """Vytvoří složku projektu podle evidenčního čísla a firmy"""
        evidence_number = project_data["section2_firma"]["evidence_number"]
        company = project_data["section2_firma"]["company"]

        folder_name = self._sanitize_folder_name(f"{evidence_number}_{company}")
        project_path = self.base_dir / folder_name

        project_path.mkdir(parents=True, exist_ok=True)

        return project_path

    def _copy_excel_templates(self, project_folder: Path, project_data: Dict[str, Any]) -> Dict[str, Path]:
        """
        Zkopíruje Excel šablony podle výběru uživatele.

        Returns:
            Dictionary: {"lsz": Path, "cfz": Path, ...} - zkopírované soubory
        """
        file_selection = project_data["section0_file_selection"]
        evidence_number = project_data["section2_firma"]["evidence_number"]
        company = project_data["section2_firma"]["company"]

        base_filename = self._sanitize_folder_name(f"{evidence_number}_{company}")

        template_mapping = {
            "generate_lsz": {
                "template": "LSZ_template.xlsm",
                "output": f"LSZ_{base_filename}.xlsm",
                "type": "lsz"
            },
            "generate_pp_time": {
                "template": "PP_template_CAS.xlsx",
                "output": f"PP_{base_filename}_CAS.xlsx",
                "type": "pp_time"
            },
            "generate_pp_pieces": {
                "template": "PP_template_KUSY.xlsx",
                "output": f"PP_{base_filename}_KUSY.xlsx",
                "type": "pp_pieces"
            },
            "generate_cfz": {
                "template": "CFZ_template.xlsx",
                "output": f"CFZ_{base_filename}.xlsx",
                "type": "cfz"
            }
        }

        copied_files = {}

        for selection_key, file_info in template_mapping.items():
            if file_selection.get(selection_key, False):
                template_path = self.templates_dir / file_info["template"]
                output_path = project_folder / file_info["output"]

                if template_path.exists():
                    shutil.copy2(template_path, output_path)
                    copied_files[file_info["type"]] = output_path
                else:
                    print(f"Varování: Šablona neexistuje: {template_path}")

        return copied_files

    def _fill_excel_data(self, copied_files: Dict[str, Path], project_data: Dict[str, Any]) -> None:
        """
        Vyplní data do zkopírovaných Excel souborů.

        Args:
            copied_files: Dictionary se zkopírovanými soubory {"lsz": Path, ...}
            project_data: Data z formuláře
        """
        # LSZ
        if "lsz" in copied_files:
            lsz_filler = ExcelFiller(LSZ_MAPPING)
            lsz_filler.fill_excel(copied_files["lsz"], project_data)
            print(f"LSZ Excel vyplněn: {copied_files['lsz'].name}")

        # PP ČAS
        if "pp_time" in copied_files:
            pp_cas_filler = ExcelFiller(PP_CAS_MAPPING)
            pp_cas_filler.fill_excel(copied_files["pp_time"], project_data)
            print(f"PP ČAS Excel vyplněn: {copied_files['pp_time'].name}")

        # PP KUSY
        if "pp_pieces" in copied_files:
            pp_kusy_filler = ExcelFiller(PP_KUSY_MAPPING)
            pp_kusy_filler.fill_excel(copied_files["pp_pieces"], project_data)
            print(f"PP KUSY Excel vyplněn: {copied_files['pp_pieces'].name}")

        # CFZ
        if "cfz" in copied_files:
            cfz_filler = ExcelFiller(CFZ_MAPPING)
            cfz_filler.fill_excel(copied_files["cfz"], project_data)
            print(f"CFZ Excel vyplněn: {copied_files['cfz'].name}")

    def _copy_time_schedule(self, copied_files: Dict[str, Path], project_data: Dict[str, Any]) -> None:
        """
        Zkopíruje časový snímek do všech vygenerovaných Excel souborů.

        Args:
            copied_files: Dictionary se zkopírovanými soubory
            project_data: Data z formuláře
        """
        # Získej data časového snímku
        time_schedule = project_data.get("section1_uploaded_docx", {}).get("time_schedule", {})

        if not time_schedule:
            print("Varování: Časový snímek nebyl nalezen v datech")
            return

        # Vytvoř TableCopier
        copier = TableCopier()

        print("\nKopírování časového snímku do Excelů:")

        # Zkopíruj do každého vygenerovaného souboru
        for excel_type, excel_path in copied_files.items():
            copier.copy_time_schedule(excel_path, excel_type, time_schedule)

    def _copy_uploaded_docx(self, project_folder: Path, project_data: Dict[str, Any]) -> None:
        """
        Zkopíruje nahraný Word z temp složky do project folderu.

        Args:
            project_folder: Cesta k project folderu
            project_data: Data projektu (bude aktualizováno s novou cestou)
        """
        # Získej cestu k temp souboru
        uploaded_file_path = project_data.get("section1_uploaded_docx", {}).get("uploaded_file_path")

        if not uploaded_file_path or not Path(uploaded_file_path).exists():
            print("Varování: Nahraný Word soubor nebyl nalezen")
            return

        # Vytvoř název podle evidence čísla a firmy
        evidence_number = project_data["section2_firma"]["evidence_number"]
        company = project_data["section2_firma"]["company"]
        # Sanitizuj pouze basename (bez přípony), pak přidej .docx
        basename = self._sanitize_folder_name(f"popis_prace_{evidence_number}_{company}")
        filename = f"{basename}.docx"

        # Cílová cesta
        dest_path = project_folder / filename

        # Zkopíruj
        shutil.copy2(uploaded_file_path, dest_path)

        # Aktualizuj JSON s ABSOLUTNÍ cestou k finálnímu souboru
        project_data["section1_uploaded_docx"]["copied_file_path"] = str(dest_path.resolve())

        print(f"Word dokument zkopírován: {dest_path.name}")

    def _save_measurement_json(self, project_folder: Path, project_data: Dict[str, Any]) -> None:
        """
        Uloží measurement_data.json do project folderu.

        Args:
            project_folder: Cesta k project folderu
            project_data: Data projektu k uložení
        """
        json_path = project_folder / "measurement_data.json"

        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(project_data, f, ensure_ascii=False, indent=2)

        print(f"JSON data uložena: {json_path.name}")

    def _sanitize_folder_name(self, name: str) -> str:
        """Očistí název složky od nežádoucích znaků"""
        replacements = {
            " ": "_",
            "/": "-",
            "\\": "-",
            ":": "-",
            "*": "",
            "?": "",
            '"': "",
            "<": "",
            ">": "",
            "|": "",
            ".": "",
            ",": ""
        }

        sanitized = name
        for old, new in replacements.items():
            sanitized = sanitized.replace(old, new)

        return sanitized
