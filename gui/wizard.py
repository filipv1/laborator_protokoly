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
                "generate_cfz": False,  # CFZ skryto z GUI (kód ponechán pro budoucnost)
                "worker_count": self.page0.worker_count_group.checkedId(),  # 1 nebo 2
                "workers_gender": self.page0.gender_combo.currentText().lower()  # "muži" nebo "ženy"
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
                "evidence_number_lsz": self.page2.evidencni_cislo_lsz.text(),
                "evidence_number_pp": self.page2.evidencni_cislo_pp.text(),
                "measurement_days": int(self.page2.pocet_dni_mereni.currentText())
            },
            "section3_additional_data": {
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
                "measurement_duration": self.page4.measurement_duration_a.time().toString("HH:mm:ss"),
                "work_duration": self.page4.doba_vykonu_a.text(),
                "breaks": self.page4.prestavky_a.text(),
                "work_duration_min": self.page4.doba_vykonu_min_a.value(),
                "safety_break_min": self.page4.bezpecnostni_prestavka_min_a.value()
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
                # If worker_b has no name (single worker mode), set emg_holter to empty string
                "emg_holter": self.page5.emg_holter_b.currentText() if self.page5.jmeno_b.text().strip() else "",
                "measurement_duration": self.page5.measurement_duration_b.time().toString("HH:mm:ss"),
                # 4 hodnoty se kopírují z worker A
                "work_duration": self.page4.doba_vykonu_a.text(),
                "breaks": self.page4.prestavky_a.text(),
                "work_duration_min": self.page4.doba_vykonu_min_a.value(),
                "safety_break_min": self.page4.bezpecnostni_prestavka_min_a.value()
            },
            "section6_final": {
                "measured_by": self.page6.mereni_provedl.text()
            }
        }
        return data

    def _calculate_averages(self, data):
        """Vypočítá průměry hodnot mezi worker_a a worker_b"""
        worker_a = data.get("section4_worker_a", {})
        worker_b = data.get("section5_worker_b", {})

        # Kontrola zda worker_b má vyplněné jméno (single vs dual worker mode)
        has_worker_b = bool(worker_b.get("full_name", "").strip())

        fields = ["age_years", "exposure_length_years", "height_cm", "weight_kg"]
        prumery = {}

        for field in fields:
            val_a = worker_a.get(field, 0) or 0
            if has_worker_b:
                val_b = worker_b.get(field, 0) or 0
                prumery[field] = round((val_a + val_b) / 2, 1)
            else:
                prumery[field] = val_a

        return prumery

    def _on_finished(self, result):
        """Handler při dokončení wizardu"""
        if result == QWizard.DialogCode.Accepted:
            data = self._collect_data()

            # Přidání průměrů do dat
            data["prumery"] = self._calculate_averages(data)

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
                f"• Excel soubory (LSZ, PP)\n\n"
                f"Nyní můžete:\n"
                f"1. Otevřít Excel soubory a spustit makra\n"
                f"2. Zkontrolovat/upravit data\n"
                f"3. Použít 'Generovat Word protokol' pro vytvoření protokolu"
            )
