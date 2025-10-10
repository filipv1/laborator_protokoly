"""
GUI pro zadání údajů o měření - LABORATO5
"""
import sys
from PyQt6.QtWidgets import (
    QApplication, QWizard, QWizardPage, QVBoxLayout, QFormLayout,
    QLineEdit, QComboBox, QDateEdit, QSpinBox, QDoubleSpinBox,
    QTextEdit
)
from PyQt6.QtCore import QDate


class Page1_Firma(QWizardPage):
    def __init__(self):
        super().__init__()
        self.setTitle("Firma")
        layout = QFormLayout()
        self.setLayout(layout)

        self.firma = QLineEdit()
        self.nazev_profese = QLineEdit()
        self.misto_mereni = QLineEdit()
        self.pracoviste = QLineEdit()
        self.ico = QLineEdit()
        self.smennost = QLineEdit()
        self.datum_mereni = QDateEdit()
        self.datum_mereni.setDate(QDate.currentDate())
        self.datum_mereni.setCalendarPopup(True)
        self.evidencni_cislo = QLineEdit()

        layout.addRow("Firma:", self.firma)
        layout.addRow("Název Profese:", self.nazev_profese)
        layout.addRow("Místo měření:", self.misto_mereni)
        layout.addRow("Pracoviště:", self.pracoviste)
        layout.addRow("IČO:", self.ico)
        layout.addRow("Směnnost:", self.smennost)
        layout.addRow("Datum měření:", self.datum_mereni)
        layout.addRow("Evidenční číslo:", self.evidencni_cislo)


class Page2_DalsiUdaje(QWizardPage):
    def __init__(self):
        super().__init__()
        self.setTitle("Další údaje")
        layout = QFormLayout()
        self.setLayout(layout)

        self.stanovena_norma = QLineEdit()
        self.typ_vyrobku = QLineEdit()

        self.prace_vykonavana = QComboBox()
        self.prace_vykonavana.addItems(["stoj", "sed", "chůze"])

        self.pohlavi_pracovniku = QComboBox()
        self.pohlavi_pracovniku.addItems(["muži", "ženy"])

        self.vyska_pracovni_roviny = QLineEdit()
        self.hmotnost_min = QDoubleSpinBox()
        self.hmotnost_min.setMaximum(999.99)
        self.hmotnost_min.setSuffix(" kg")
        self.hmotnost_max = QDoubleSpinBox()
        self.hmotnost_max.setMaximum(999.99)
        self.hmotnost_max.setSuffix(" kg")

        layout.addRow("Stanovená norma:", self.stanovena_norma)
        layout.addRow("Typ výrobku:", self.typ_vyrobku)
        layout.addRow("Práce je vykonávaná:", self.prace_vykonavana)
        layout.addRow("Pohlaví pracovníků na měřené pozici:", self.pohlavi_pracovniku)
        layout.addRow("Výška pracovní roviny:", self.vyska_pracovni_roviny)
        layout.addRow("Hmotnost ručně zvedaných břemen (min):", self.hmotnost_min)
        layout.addRow("Hmotnost ručně zvedaných břemen (max):", self.hmotnost_max)


class Page3_PracovnikA(QWizardPage):
    def __init__(self):
        super().__init__()
        self.setTitle("Pracovník A")
        layout = QFormLayout()
        self.setLayout(layout)

        self.jmeno_a = QLineEdit()
        self.vek_a = QSpinBox()
        self.vek_a.setMaximum(120)
        self.delka_expozice_a = QSpinBox()
        self.delka_expozice_a.setMaximum(100)
        self.vyska_a = QSpinBox()
        self.vyska_a.setMaximum(250)
        self.vaha_a = QDoubleSpinBox()
        self.vaha_a.setMaximum(300.0)

        self.lateralita_a = QComboBox()
        self.lateralita_a.addItems(["pravostranná", "levostranná"])

        self.sila_phk_a = QDoubleSpinBox()
        self.sila_phk_a.setMaximum(9999.99)
        self.sila_lhk_a = QDoubleSpinBox()
        self.sila_lhk_a.setMaximum(9999.99)

        self.emg_holter_a = QComboBox()
        self.emg_holter_a.addItems(["A", "B", "C", "D", "E", "F"])

        self.polar_a = QComboBox()
        self.polar_a.addItems(["1", "2", "3", "4", "5", "6", "7", "8"])

        self.doba_vykonu_a = QLineEdit()
        self.prestavky_a = QLineEdit()
        self.cislo_hrudniho_pasu_a = QLineEdit()
        self.zacatek_mereni_a = QLineEdit()
        self.kod_a = QLineEdit()

        layout.addRow("Jméno a příjmení:", self.jmeno_a)
        layout.addRow("Věk (let):", self.vek_a)
        layout.addRow("Délka expozice (let):", self.delka_expozice_a)
        layout.addRow("Výška (cm):", self.vyska_a)
        layout.addRow("Váha (kg):", self.vaha_a)
        layout.addRow("Lateralita:", self.lateralita_a)
        layout.addRow("Síla stisku ruky PHK (N):", self.sila_phk_a)
        layout.addRow("Síla stisku ruky LHK (N):", self.sila_lhk_a)
        layout.addRow("EMG Holter:", self.emg_holter_a)
        layout.addRow("Polar:", self.polar_a)
        layout.addRow("Doba výkonu práce:", self.doba_vykonu_a)
        layout.addRow("Přestávky:", self.prestavky_a)
        layout.addRow("Číslo hrudního pásu:", self.cislo_hrudniho_pasu_a)
        layout.addRow("Začátek měření:", self.zacatek_mereni_a)
        layout.addRow("Kód:", self.kod_a)


class Page4_PracovnikB(QWizardPage):
    def __init__(self):
        super().__init__()
        self.setTitle("Pracovník B (optional)")
        layout = QFormLayout()
        self.setLayout(layout)

        self.jmeno_b = QLineEdit()
        self.vek_b = QSpinBox()
        self.vek_b.setMaximum(120)
        self.delka_expozice_b = QSpinBox()
        self.delka_expozice_b.setMaximum(100)
        self.vyska_b = QSpinBox()
        self.vyska_b.setMaximum(250)
        self.vaha_b = QDoubleSpinBox()
        self.vaha_b.setMaximum(300.0)

        self.lateralita_b = QComboBox()
        self.lateralita_b.addItems(["pravostranná", "levostranná"])

        self.sila_phk_b = QDoubleSpinBox()
        self.sila_phk_b.setMaximum(9999.99)
        self.sila_lhk_b = QDoubleSpinBox()
        self.sila_lhk_b.setMaximum(9999.99)

        self.emg_holter_b = QComboBox()
        self.emg_holter_b.addItems(["A", "B", "C", "D", "E", "F"])

        self.polar_b = QComboBox()
        self.polar_b.addItems(["1", "2", "3", "4", "5", "6", "7", "8"])

        self.doba_vykonu_b = QLineEdit()
        self.prestavky_b = QLineEdit()
        self.cislo_hrudniho_pasu_b = QLineEdit()
        self.zacatek_mereni_b = QLineEdit()
        self.kod_b = QLineEdit()

        layout.addRow("Jméno a příjmení:", self.jmeno_b)
        layout.addRow("Věk (let):", self.vek_b)
        layout.addRow("Délka expozice (let):", self.delka_expozice_b)
        layout.addRow("Výška (cm):", self.vyska_b)
        layout.addRow("Váha (kg):", self.vaha_b)
        layout.addRow("Lateralita:", self.lateralita_b)
        layout.addRow("Síla stisku ruky PHK (N):", self.sila_phk_b)
        layout.addRow("Síla stisku ruky LHK (N):", self.sila_lhk_b)
        layout.addRow("EMG Holter:", self.emg_holter_b)
        layout.addRow("Polar:", self.polar_b)
        layout.addRow("Doba výkonu práce:", self.doba_vykonu_b)
        layout.addRow("Přestávky:", self.prestavky_b)
        layout.addRow("Číslo hrudního pásu:", self.cislo_hrudniho_pasu_b)
        layout.addRow("Začátek měření:", self.zacatek_mereni_b)
        layout.addRow("Kód:", self.kod_b)


class Page5_Zaverecne(QWizardPage):
    def __init__(self):
        super().__init__()
        self.setTitle("Závěrečné údaje")
        layout = QFormLayout()
        self.setLayout(layout)

        self.mereni_provedl = QLineEdit()
        self.poznamky = QTextEdit()
        self.poznamky.setMaximumHeight(100)

        layout.addRow("Měření provedl:", self.mereni_provedl)
        layout.addRow("Poznámky:", self.poznamky)


class MeasurementGUI(QWizard):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Zadání údajů o měření")
        self.setWizardStyle(QWizard.WizardStyle.ModernStyle)

        self.addPage(Page1_Firma())
        self.addPage(Page2_DalsiUdaje())
        self.addPage(Page3_PracovnikA())
        self.addPage(Page4_PracovnikB())
        self.addPage(Page5_Zaverecne())


def main():
    app = QApplication(sys.argv)
    window = MeasurementGUI()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
