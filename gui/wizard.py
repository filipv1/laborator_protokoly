"""
Hlavní QWizard třída pro zadání údajů o měření
"""
import json
from pathlib import Path
from PyQt6.QtWidgets import QWizard, QMessageBox
from .pages import (
    Page0_VyberSouboru,
    Page1_UploadDocx,
    Page2_Firma,
    Page3_DalsiUdaje,
    Page4_PracovnikA,
    Page5_PracovnikB,
    Page6_Zaverecne
)
from core import ProjectManager


def calculate_initials(full_name):
    """
    Vypočítá iniciály ze jména a příjmení ve formátu 'F. T.'

    Args:
        full_name (str): Celé jméno ve formátu "Jan Novák"

    Returns:
        str: Iniciály ve formátu "J. N."
    """
    if not full_name or not full_name.strip():
        return ""

    parts = full_name.strip().split()
    if len(parts) >= 2:
        # První písmeno jména + tečka + mezera + první písmeno příjmení + tečka
        return f"{parts[0][0].upper()}. {parts[1][0].upper()}."
    elif len(parts) == 1:
        # Pokud je jen jedno slovo, vrať iniciálu s tečkou
        return f"{parts[0][0].upper()}."
    return ""


class MeasurementGUI(QWizard):
    """Hlavní wizard pro zadání údajů o měření"""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Zadání údajů o měření")
        self.setWizardStyle(QWizard.WizardStyle.ModernStyle)

        # Excel workflow stránky
        self.page0 = Page0_VyberSouboru()
        self.page1 = Page1_UploadDocx()
        self.page2 = Page2_Firma()
        self.page3 = Page3_DalsiUdaje()
        self.page4 = Page4_PracovnikA()
        self.page5 = Page5_PracovnikB()
        self.page6 = Page6_Zaverecne()

        # Přidání stránek
        self.addPage(self.page0)  # ID 0
        self.addPage(self.page1)  # ID 1
        self.addPage(self.page2)  # ID 2
        self.addPage(self.page3)  # ID 3
        self.addPage(self.page4)  # ID 4
        self.addPage(self.page5)  # ID 5
        self.addPage(self.page6)  # ID 6

        self.finished.connect(self._on_finished)

    def _collect_data(self):
        """Sebere všechna data z formuláře"""
        # Získej data z tabulky časového snímku (editovatelná uživatelem)
        time_schedule = self.page1.get_table_data()

        data = {
            "section0_file_selection": {
                "generate_lsz": self.page0.checkbox_lsz.isChecked(),
                "generate_pp_time": self.page0.checkbox_pp_cas.isChecked(),
                "generate_pp_pieces": self.page0.checkbox_pp_kusy.isChecked(),
                "generate_cfz": self.page0.checkbox_cfz.isChecked()
            },
            "section1_uploaded_docx": {
                "uploaded_file_path": self.page1.selected_file_path if self.page1.selected_file_path else "",
                "time_schedule": time_schedule
            },
            "section2_firma": {
                "company": self.page2.firma.text(),
                "address": self.page2.adresa.text(),
                "house_number": self.page2.cislo_popisne.text(),
                "city": self.page2.mesto.text(),
                "city_district": self.page2.mestska_cast.text(),
                "postal_code": self.page2.psc.text(),
                "profession_name": self.page2.nazev_profese.text(),
                "workplace": self.page2.pracoviste.text(),
                "ico": self.page2.ico.text(),
                "shift_pattern": self.page2.smennost.currentText(),
                "measurement_date": self.page2.datum_mereni.date().toString("dd.MM.yyyy"),
                "evidence_number": self.page2.evidencni_cislo.text(),
                "measurement_days": int(self.page2.pocet_dni_mereni.currentText())
            },
            "section3_additional_data": {
                "work_performed": self.page3.prace_vykonavana.currentText(),
                "what_is_evaluated": self.page3.co_se_hodnoti.currentText()
            },
            "section4_worker_a": {
                "full_name": self.page4.jmeno_a.text(),
                "initials": calculate_initials(self.page4.jmeno_a.text()),
                "age_years": self.page4.vek_a.value(),
                "exposure_length_years": self.page4.delka_expozice_a.value(),
                "height_cm": self.page4.vyska_a.value(),
                "weight_kg": self.page4.vaha_a.value(),
                "laterality": self.page4.lateralita_a.currentText(),
                "grip_strength_phk_n": self.page4.sila_phk_a.value(),
                "grip_strength_lhk_n": self.page4.sila_lhk_a.value(),
                "emg_holter": self.page4.emg_holter_a.currentText(),
                "polar": self.page4.polar_a.currentText(),
                "work_duration": self.page4.doba_vykonu_a.text(),
                "breaks": self.page4.prestavky_a.text(),
                "work_duration_min": self.page4.doba_vykonu_min_a.value(),
                "safety_break_min": self.page4.bezpecnostni_prestavka_min_a.value(),
                "chest_strap_number": self.page4.cislo_hrudniho_pasu_a.text()
            },
            "section5_worker_b": {
                "full_name": self.page5.jmeno_b.text(),
                "initials": calculate_initials(self.page5.jmeno_b.text()),
                "age_years": self.page5.vek_b.value(),
                "exposure_length_years": self.page5.delka_expozice_b.value(),
                "height_cm": self.page5.vyska_b.value(),
                "weight_kg": self.page5.vaha_b.value(),
                "laterality": self.page5.lateralita_b.currentText(),
                "grip_strength_phk_n": self.page5.sila_phk_b.value(),
                "grip_strength_lhk_n": self.page5.sila_lhk_b.value(),
                "emg_holter": self.page5.emg_holter_b.currentText(),
                "polar": self.page5.polar_b.currentText(),
                "chest_strap_number": self.page5.cislo_hrudniho_pasu_b.text()
            },
            "section6_final": {
                "measured_by": self.page6.mereni_provedl.text()
            }
        }
        return data

    def _on_finished(self, result):
        """Handler při dokončení wizardu"""
        if result == QWizard.DialogCode.Accepted:
            data = self._collect_data()

            project_manager = ProjectManager()
            project_folder = project_manager.create_project(data)

            json_path = project_folder / "measurement_data.json"
            with open(json_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=4)

            print(f"Projekt vytvořen: {project_folder.absolute()}")
            print(f"Data uložena do: {json_path.absolute()}")

            # Zobraz success message
            QMessageBox.information(
                self,
                "Projekt vytvořen",
                f"Projekt úspěšně vytvořen:\n{project_folder.absolute()}\n\n"
                f"Vygenerované soubory:\n"
                f"• measurement_data.json\n"
                f"• Excel soubory (LSZ, PP, CFZ)\n\n"
                f"Nyní můžete:\n"
                f"1. Otevřít Excel soubory a spustit makra\n"
                f"2. Zkontrolovat/upravit data\n"
                f"3. Použít 'Generovat Word protokol' pro vytvoření protokolu"
            )
