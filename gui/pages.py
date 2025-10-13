"""
QWizardPage třídy pro jednotlivé sekce formuláře
"""
from PyQt6.QtWidgets import (
    QWizardPage, QFormLayout, QVBoxLayout, QHBoxLayout, QLineEdit, QComboBox,
    QDateEdit, QSpinBox, QDoubleSpinBox, QTextEdit, QCheckBox, QLabel,
    QPushButton, QFileDialog, QTableWidget, QTableWidgetItem, QHeaderView,
    QMessageBox
)
from PyQt6.QtCore import QDate, Qt
from core import DocxParser


class Page0_VyberSouboru(QWizardPage):
    """Stránka 0: Výběr souborů k vygenerování"""

    def __init__(self):
        super().__init__()
        self.setTitle("Výběr souborů k vygenerování")
        self.setSubTitle("Vyberte, které Excel soubory chcete vygenerovat")

        layout = QVBoxLayout()
        self.setLayout(layout)

        info_label = QLabel("Vyberte soubory ze složky 'Programy na vyhodnocování':")
        layout.addWidget(info_label)
        layout.addSpacing(10)

        self.checkbox_lsz = QCheckBox("LSZ - Lokální svalová zátěž (LSZ_XX_firma_pozice.xlsm)")
        self.checkbox_pp_cas = QCheckBox("PP - Pracovní polohy - ČAS (PP_XX_firma_pozice[ČAS].xlsx)")
        self.checkbox_pp_kusy = QCheckBox("PP - Pracovní polohy - KUSY (PP_XX_firma_pozice[KUSY].xlsx)")
        self.checkbox_cfz = QCheckBox("CFZ - Celková fyzická zátěž (CFZ_XX_firma_pozice.xlsx)")

        layout.addWidget(self.checkbox_lsz)
        layout.addWidget(self.checkbox_pp_cas)
        layout.addWidget(self.checkbox_pp_kusy)
        layout.addWidget(self.checkbox_cfz)
        layout.addStretch()


class Page1_UploadDocx(QWizardPage):
    """Stránka 1: Upload Word dokumentu a editace časového snímku"""

    def __init__(self):
        super().__init__()
        self.setTitle("Časový snímek pracovní směny")
        self.setSubTitle("Nahrajte Word dokument nebo vyplňte tabulku ručně")

        layout = QVBoxLayout()
        self.setLayout(layout)

        # === Horní sekce: Upload souboru ===
        upload_section = QHBoxLayout()

        info_label = QLabel("Nahrát z Word dokumentu:")
        upload_section.addWidget(info_label)

        self.upload_button = QPushButton("Vybrat soubor...")
        self.upload_button.clicked.connect(self._select_file)
        upload_section.addWidget(self.upload_button)

        self.file_path_label = QLabel("(Žádný soubor)")
        self.file_path_label.setStyleSheet("color: gray; font-style: italic;")
        upload_section.addWidget(self.file_path_label)
        upload_section.addStretch()

        layout.addLayout(upload_section)
        layout.addSpacing(10)

        # === Tlačítka pro úpravu tabulky ===
        buttons_layout = QHBoxLayout()

        self.add_row_button = QPushButton("➕ Přidat řádek")
        self.add_row_button.clicked.connect(self._add_row)
        buttons_layout.addWidget(self.add_row_button)

        self.remove_row_button = QPushButton("➖ Odebrat vybraný řádek")
        self.remove_row_button.clicked.connect(self._remove_row)
        buttons_layout.addWidget(self.remove_row_button)

        self.clear_button = QPushButton("🗑️ Vymazat vše")
        self.clear_button.clicked.connect(self._clear_table)
        buttons_layout.addWidget(self.clear_button)

        buttons_layout.addStretch()
        layout.addLayout(buttons_layout)
        layout.addSpacing(5)

        # === Tabulka časového snímku ===
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels([
            "Číslo",
            "Operace/Činnost",
            "Čas (min)",
            "Počet kusů"
        ])

        # Nastavení šířky sloupců
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)  # Číslo
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)  # Operace (roztažitelný)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)  # Čas
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)  # Kusy

        self.table.setMinimumHeight(300)
        layout.addWidget(self.table)

        # === Řádek CELKEM (read-only, automaticky vypočítaný) ===
        total_layout = QHBoxLayout()
        total_layout.addWidget(QLabel("<b>CELKEM:</b>"))

        self.total_time_label = QLabel("Čas: 0 min")
        self.total_time_label.setStyleSheet("font-weight: bold; color: #0066cc;")
        total_layout.addWidget(self.total_time_label)

        total_layout.addSpacing(20)

        self.total_pieces_label = QLabel("Kusů: 0")
        self.total_pieces_label.setStyleSheet("font-weight: bold; color: #0066cc;")
        total_layout.addWidget(self.total_pieces_label)

        total_layout.addStretch()
        layout.addLayout(total_layout)

        # Připoj signál pro aktualizaci celkových hodnot
        self.table.cellChanged.connect(self._update_totals)

        # Interní proměnná
        self.selected_file_path = None

        # Inicializuj s prázdnými řádky
        self._initialize_empty_table()

    def _initialize_empty_table(self):
        """Inicializuje tabulku s 5 prázdnými řádky"""
        for _ in range(5):
            self._add_row()

    def _select_file(self):
        """Otevře dialog pro výběr .docx souboru a načte data"""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Vyberte Word dokument",
            "",
            "Word dokumenty (*.docx);;Všechny soubory (*.*)"
        )

        if file_path:
            self.selected_file_path = file_path
            self.file_path_label.setText(f"📄 {file_path.split('/')[-1]}")
            self.file_path_label.setStyleSheet("color: green;")

            # Automaticky načti data z Word dokumentu
            self._load_from_docx(file_path)

    def _load_from_docx(self, file_path: str):
        """Načte data z Word dokumentu a naplní tabulku"""
        try:
            # Naparsuj Word dokument
            time_schedule = DocxParser.parse_time_schedule_table(file_path)

            # Vymaž aktuální obsah tabulky
            self.table.setRowCount(0)

            # Naplň tabulku daty
            for i in range(1, 21):  # line1...line20
                line_data = time_schedule.get(f"line{i}", {})

                # Přeskoč prázdné řádky na konci
                if not line_data.get("operation") and not line_data.get("time_min"):
                    continue

                row_position = self.table.rowCount()
                self.table.insertRow(row_position)

                # Vyplň buňky
                self.table.setItem(row_position, 0, QTableWidgetItem(str(line_data.get("number", ""))))
                self.table.setItem(row_position, 1, QTableWidgetItem(str(line_data.get("operation", ""))))
                self.table.setItem(row_position, 2, QTableWidgetItem(str(line_data.get("time_min") or "")))
                self.table.setItem(row_position, 3, QTableWidgetItem(str(line_data.get("pieces_count") or "")))

            self._update_totals()

            QMessageBox.information(
                self,
                "Úspěch",
                f"Načteno {self.table.rowCount()} řádků z Word dokumentu."
            )

        except Exception as e:
            QMessageBox.warning(
                self,
                "Chyba při načítání",
                f"Nepodařilo se načíst data z dokumentu:\n{str(e)}"
            )

    def _add_row(self):
        """Přidá nový prázdný řádek do tabulky"""
        row_position = self.table.rowCount()
        self.table.insertRow(row_position)

        # Automaticky vyplň číslo řádku
        self.table.setItem(row_position, 0, QTableWidgetItem(str(row_position + 1)))

    def _remove_row(self):
        """Odebere aktuálně vybraný řádek"""
        current_row = self.table.currentRow()
        if current_row >= 0:
            self.table.removeRow(current_row)
            self._update_totals()
        else:
            QMessageBox.information(self, "Info", "Nejprve vyberte řádek k odstranění.")

    def _clear_table(self):
        """Vymaže všechny řádky tabulky"""
        reply = QMessageBox.question(
            self,
            "Potvrzení",
            "Opravdu chcete vymazat všechny řádky?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )

        if reply == QMessageBox.StandardButton.Yes:
            self.table.setRowCount(0)
            self._update_totals()

    def _update_totals(self):
        """Aktualizuje celkové součty (čas a kusy)"""
        total_time = 0
        total_pieces = 0

        for row in range(self.table.rowCount()):
            # Čas
            time_item = self.table.item(row, 2)
            if time_item and time_item.text().strip():
                try:
                    total_time += int(time_item.text())
                except ValueError:
                    pass

            # Kusy
            pieces_item = self.table.item(row, 3)
            if pieces_item and pieces_item.text().strip():
                try:
                    total_pieces += int(pieces_item.text())
                except ValueError:
                    pass

        self.total_time_label.setText(f"Čas: {total_time} min")
        self.total_pieces_label.setText(f"Kusů: {total_pieces}")

    def get_table_data(self):
        """
        Vrátí data z tabulky ve formátu kompatibilním s DocxParser výstupem.

        Returns:
            Dictionary s line1...lineN a total
        """
        result = {}

        for row in range(self.table.rowCount()):
            number_item = self.table.item(row, 0)
            operation_item = self.table.item(row, 1)
            time_item = self.table.item(row, 2)
            pieces_item = self.table.item(row, 3)

            result[f"line{row + 1}"] = {
                "number": number_item.text() if number_item else "",
                "operation": operation_item.text() if operation_item else "",
                "time_min": int(time_item.text()) if time_item and time_item.text().strip() else None,
                "pieces_count": int(pieces_item.text()) if pieces_item and pieces_item.text().strip() else None
            }

        # Přidej total (spočítané hodnoty)
        total_time = 0
        total_pieces = 0
        for row_data in result.values():
            if row_data.get("time_min"):
                total_time += row_data["time_min"]
            if row_data.get("pieces_count"):
                total_pieces += row_data["pieces_count"]

        result["total"] = {
            "time_min": total_time,
            "pieces_count": total_pieces
        }

        return result


class Page2_Firma(QWizardPage):
    """Stránka 2: Základní údaje o firmě"""

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


class Page3_DalsiUdaje(QWizardPage):
    """Stránka 3: Další údaje o měření"""

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


class Page4_PracovnikA(QWizardPage):
    """Stránka 4: Údaje o pracovníkovi A"""

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


class Page5_PracovnikB(QWizardPage):
    """Stránka 5: Údaje o pracovníkovi B (optional)"""

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


class Page6_Zaverecne(QWizardPage):
    """Stránka 6: Závěrečné údaje"""

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
