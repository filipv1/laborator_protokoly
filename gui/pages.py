"""
QWizardPage třídy pro jednotlivé sekce formuláře
"""
from PyQt6.QtWidgets import (
    QWizardPage, QFormLayout, QVBoxLayout, QHBoxLayout, QLineEdit, QComboBox,
    QDateEdit, QTimeEdit, QSpinBox, QDoubleSpinBox, QTextEdit, QCheckBox, QLabel,
    QPushButton, QFileDialog, QTableWidget, QTableWidgetItem, QHeaderView,
    QMessageBox, QRadioButton, QButtonGroup
)
from PyQt6.QtCore import QDate, QTime, Qt
from core import DocxParser, FileManager
from core.text_generator import get_selected_holter_numbers, highlight_selected_holters
import json
from docxtpl import DocxTemplate, RichText
import requests


# ============================================================================
# ARES API Helper Functions
# ============================================================================

def fetch_ares_data(ico: str) -> dict:
    """
    Načte data z ARES API podle IČO.

    Args:
        ico: IČO firmy (string nebo int)

    Returns:
        dict: JSON odpověď z ARES API, nebo None pokud se načtení nezdařilo
    """
    # Odstraň mezery a nealfanumerické znaky z IČO
    ico_clean = ''.join(filter(str.isdigit, str(ico)))

    if not ico_clean:
        return None

    url = f"https://ares.gov.cz/ekonomicke-subjekty-v-be/rest/ekonomicke-subjekty/{ico_clean}"

    try:
        response = requests.get(url, timeout=10)

        if response.status_code == 200:
            return response.json()
        elif response.status_code == 404:
            return None
        else:
            return None

    except requests.exceptions.Timeout:
        return None
    except requests.exceptions.RequestException:
        return None
    except Exception:
        return None


def extract_company_data_from_ares(ares_response: dict) -> dict:
    """
    Extrahuje relevantní data z ARES API odpovědi a mapuje je na naše pole.

    Args:
        ares_response: JSON odpověď z ARES API

    Returns:
        dict: Slovník s klíči odpovídajícími našim polím (company, address, atd.)
    """
    if not ares_response:
        return {}

    result = {}

    # Obchodní jméno
    result['company'] = ares_response.get('obchodniJmeno', '')

    # Adresa z objektu "sidlo"
    sidlo = ares_response.get('sidlo', {})

    if sidlo:
        # Název ulice
        result['address'] = sidlo.get('nazevUlice', '')

        # Číslo popisné/orientační (formát: "1307/2")
        cislo_domovni = sidlo.get('cisloDomovni')
        cislo_orientacni = sidlo.get('cisloOrientacni')

        if cislo_domovni and cislo_orientacni:
            result['house_number'] = f"{cislo_domovni}/{cislo_orientacni}"
        elif cislo_domovni:
            result['house_number'] = str(cislo_domovni)
        else:
            result['house_number'] = ''

        # Město
        result['city'] = sidlo.get('nazevObce', '')

        # Městská část (používáme nazevMestskeCastiObvodu nebo nazevCastiObce)
        result['city_district'] = sidlo.get('nazevMestskeCastiObvodu') or sidlo.get('nazevCastiObce', '')

        # PSČ
        psc = sidlo.get('psc')
        result['postal_code'] = str(psc) if psc else ''

    return result


# ============================================================================
# Wizard Pages
# ============================================================================

class Page_InitialChoice(QWizardPage):
    """Úvodní stránka: Výběr mezi Excel workflow a Word workflow"""

    def __init__(self):
        super().__init__()
        self.setTitle("Vyberte typ operace")
        self.setSubTitle("Co chcete vygenerovat?")

        layout = QVBoxLayout()
        self.setLayout(layout)

        self.button_group = QButtonGroup(self)

        self.radio_excel = QRadioButton("Vygenerovat Excely + JSON (původní workflow)")
        self.radio_word = QRadioButton("Vygenerovat Word protokol z JSON")

        self.button_group.addButton(self.radio_excel)
        self.button_group.addButton(self.radio_word)

        self.radio_excel.setChecked(True)

        layout.addWidget(self.radio_excel)
        layout.addWidget(self.radio_word)
        layout.addStretch()

    def nextId(self):
        """Určí, na kterou stránku se má pokračovat"""
        if self.radio_excel.isChecked():
            return 1  # Page0_VyberSouboru
        else:
            return 8  # Page_WordGenerator


class Page_WordGenerator(QWizardPage):
    """Stránka pro generování Word protokolu z JSON"""

    def __init__(self):
        super().__init__()
        self.setTitle("Generování Word protokolu")
        self.setSubTitle("Vyberte JSON soubor s daty")

        layout = QVBoxLayout()
        self.setLayout(layout)

        # File picker
        file_layout = QHBoxLayout()
        file_layout.addWidget(QLabel("JSON soubor:"))

        self.file_path_edit = QLineEdit()
        self.file_path_edit.setReadOnly(True)
        file_layout.addWidget(self.file_path_edit)

        self.browse_button = QPushButton("Procházet...")
        self.browse_button.clicked.connect(self._browse_json)
        file_layout.addWidget(self.browse_button)

        layout.addLayout(file_layout)
        layout.addStretch()

        self.selected_json_path = None

    def _browse_json(self):
        """Otevře dialog pro výběr JSON souboru"""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Vyberte JSON soubor",
            "",
            "JSON soubory (*.json);;Všechny soubory (*.*)"
        )

        if file_path:
            self.selected_json_path = file_path
            self.file_path_edit.setText(file_path)

    def _add_purple_highlight(self, data):
        """Rekurzivně obalí všechny hodnoty do RichText s fialovým pozadím"""
        if isinstance(data, dict):
            return {k: self._add_purple_highlight(v) for k, v in data.items()}
        elif isinstance(data, list):
            return [self._add_purple_highlight(item) for item in data]
        elif isinstance(data, str):
            return RichText(data, highlight='violet')
        elif isinstance(data, (int, float)):
            return RichText(str(data), highlight='violet')
        else:
            return data

    def validatePage(self):
        """Validace a generování Word protokolu při kliknutí na Finish"""
        if not self.selected_json_path:
            QMessageBox.warning(self, "Chyba", "Vyberte JSON soubor!")
            return False

        try:
            # Load JSON
            with open(self.selected_json_path, encoding='utf-8') as f:
                data = json.load(f)

            # Add purple highlight
            data_with_highlight = self._add_purple_highlight(data)

            # Load Word template
            template_path = r"Vzorové protokoly\Autorizované protokoly pro MUŽE\lsz_placeholdery_v2.docx"
            doc = DocxTemplate(template_path)

            # Render
            doc.render(data_with_highlight)

            # Save
            output_path = "LSZ_vyplneny.docx"
            doc.save(output_path)

            # POST-PROCESSING: Zvýrazni vybrané holteru tučně
            selected_holters = get_selected_holter_numbers(data)
            if selected_holters:
                highlight_selected_holters(output_path, selected_holters)

            QMessageBox.information(
                self,
                "Úspěch",
                f"Word protokol byl vygenerován:\n{output_path}"
            )

            return True

        except Exception as e:
            QMessageBox.critical(
                self,
                "Chyba",
                f"Nepodařilo se vygenerovat Word protokol:\n{str(e)}"
            )
            return False

    def nextId(self):
        """Konec wizardu"""
        return -1


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
        layout.addSpacing(20)

        # === Počet pracovníků ===
        worker_count_label = QLabel("<b>Počet měřených pracovníků:</b>")
        layout.addWidget(worker_count_label)

        self.worker_count_group = QButtonGroup(self)
        self.radio_one_worker = QRadioButton("1 pracovník")
        self.radio_two_workers = QRadioButton("2 pracovníci")

        self.worker_count_group.addButton(self.radio_one_worker, 1)
        self.worker_count_group.addButton(self.radio_two_workers, 2)

        self.radio_two_workers.setChecked(True)  # Default: 2 pracovníci

        layout.addWidget(self.radio_one_worker)
        layout.addWidget(self.radio_two_workers)
        layout.addSpacing(20)

        # === Výběr pohlaví pracovníků ===
        gender_label = QLabel("<b>Pohlaví měřených pracovníků:</b>")
        layout.addWidget(gender_label)

        self.gender_combo = QComboBox()
        self.gender_combo.addItems(["Muži", "Ženy"])
        self.gender_combo.setCurrentIndex(0)  # Default: Muži
        layout.addWidget(self.gender_combo)

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
            # 1. Zkopíruj Word do temp složky
            file_manager = FileManager()
            temp_path = file_manager.save_uploaded_docx(file_path)

            # 2. Ulož absolutní cestu k temp souboru
            self.selected_file_path = str(temp_path)

            # 3. Update GUI
            self.file_path_label.setText(f"📄 {temp_path.name}")
            self.file_path_label.setStyleSheet("color: green;")

            # 4. Extrahuj tabulku (ZACHOVAT - parser může číst z originálního souboru)
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
        self.adresa = QLineEdit()
        self.cislo_popisne = QLineEdit()
        self.mesto = QLineEdit()
        self.mestska_cast = QLineEdit()
        self.psc = QLineEdit()
        self.nazev_profese = QLineEdit()
        self.pracoviste = QLineEdit()
        self.ico = QLineEdit()

        # Tlačítko "Dohledat" pro ARES API
        self.ares_button = QPushButton("🔍 Dohledat")
        self.ares_button.clicked.connect(self._on_ares_lookup)
        self.ares_button.setMaximumWidth(120)

        self.smennost = QComboBox()
        self.smennost.addItems(["jednosměnný", "dvousměnný", "třísměnný", "nepřetržitý"])

        self.datum_mereni = QDateEdit()
        self.datum_mereni.setDate(QDate.currentDate())
        self.datum_mereni.setCalendarPopup(True)

        self.doba_mereni = QTimeEdit()
        self.doba_mereni.setTime(QTime(8, 0))  # Default 08:00:00
        self.doba_mereni.setDisplayFormat("HH:mm:ss")

        self.evidencni_cislo = QLineEdit()

        self.pocet_dni_mereni = QComboBox()
        self.pocet_dni_mereni.addItems(["1", "2"])

        layout.addRow("Firma:", self.firma)
        layout.addRow("Adresa:", self.adresa)
        layout.addRow("Číslo popisné:", self.cislo_popisne)
        layout.addRow("Město:", self.mesto)
        layout.addRow("Městská část:", self.mestska_cast)
        layout.addRow("PSČ:", self.psc)
        layout.addRow("Název Profese:", self.nazev_profese)
        layout.addRow("Pracoviště:", self.pracoviste)

        # IČO + tlačítko Dohledat na stejném řádku
        ico_layout = QHBoxLayout()
        ico_layout.addWidget(self.ico)
        ico_layout.addWidget(self.ares_button)
        layout.addRow("IČO:", ico_layout)

        layout.addRow("Směnnost:", self.smennost)
        layout.addRow("Datum měření:", self.datum_mereni)
        layout.addRow("Délka měření:", self.doba_mereni)
        layout.addRow("Evidenční číslo:", self.evidencni_cislo)
        layout.addRow("Počet dní měření:", self.pocet_dni_mereni)

    def _on_ares_lookup(self):
        """Zavolá ARES API a vyplní firemní údaje"""
        ico = self.ico.text().strip()

        if not ico:
            QMessageBox.warning(
                self,
                "Chyba",
                "Zadejte IČO před použitím tlačítka Dohledat."
            )
            return

        # Zobraz loading message
        self.ares_button.setEnabled(False)
        self.ares_button.setText("Načítám...")

        try:
            # Zavolej ARES API
            ares_response = fetch_ares_data(ico)

            if not ares_response:
                QMessageBox.warning(
                    self,
                    "IČO nenalezeno",
                    f"IČO {ico} nebylo nalezeno v databázi ARES.\n\n"
                    f"Zkontrolujte prosím správnost zadaného IČO."
                )
                return

            # Extrahuj data
            company_data = extract_company_data_from_ares(ares_response)

            # Vyplň pole (pouze pokud nejsou prázdné v odpovědi)
            if company_data.get('company'):
                self.firma.setText(company_data['company'])

            if company_data.get('address'):
                self.adresa.setText(company_data['address'])

            if company_data.get('house_number'):
                self.cislo_popisne.setText(company_data['house_number'])

            if company_data.get('city'):
                self.mesto.setText(company_data['city'])

            if company_data.get('city_district'):
                self.mestska_cast.setText(company_data['city_district'])

            if company_data.get('postal_code'):
                self.psc.setText(company_data['postal_code'])

            # Zobraz success message
            QMessageBox.information(
                self,
                "Úspěch",
                f"✓ Data firmy '{company_data.get('company', 'N/A')}' byla načtena z ARES.\n\n"
                f"Zkontrolujte prosím správnost údajů."
            )

        except Exception as e:
            QMessageBox.critical(
                self,
                "Chyba",
                f"Nepodařilo se načíst data z ARES:\n{str(e)}"
            )

        finally:
            # Obnov tlačítko
            self.ares_button.setEnabled(True)
            self.ares_button.setText("🔍 Dohledat")


class Page3_DalsiUdaje(QWizardPage):
    """Stránka 3: Další údaje o měření"""

    def __init__(self):
        super().__init__()
        self.setTitle("Další údaje")
        layout = QFormLayout()
        self.setLayout(layout)

        self.prace_vykonavana = QComboBox()
        self.prace_vykonavana.addItems(["stoj", "sed", "chůze"])

        self.co_se_hodnoti = QComboBox()
        self.co_se_hodnoti.addItems(["kusy", "čas"])

        layout.addRow("Práce je vykonávaná:", self.prace_vykonavana)
        layout.addRow("Co se hodnotí:", self.co_se_hodnoti)


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

        # Nová číselná pole pro minuty
        self.doba_vykonu_min_a = QSpinBox()
        self.doba_vykonu_min_a.setMaximum(9999)
        self.doba_vykonu_min_a.setSuffix(" min")

        self.bezpecnostni_prestavka_min_a = QSpinBox()
        self.bezpecnostni_prestavka_min_a.setMaximum(9999)
        self.bezpecnostni_prestavka_min_a.setSuffix(" min")

        self.cislo_hrudniho_pasu_a = QLineEdit()

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
        layout.addRow("Směna (min):", self.doba_vykonu_a)
        layout.addRow("Přestávka na jídlo a oddech (min):", self.prestavky_a)
        layout.addRow("Doba výkonu práce (min):", self.doba_vykonu_min_a)
        layout.addRow("Bezpečnostní přestávka (min):", self.bezpecnostni_prestavka_min_a)
        layout.addRow("Číslo hrudního pásu:", self.cislo_hrudniho_pasu_a)

    def nextId(self):
        """
        Přeskočí Page5 (Pracovník B) pokud je vybrán pouze 1 pracovník.
        """
        # Získej wizard a Page0
        wizard = self.wizard()
        if wizard:
            page0 = wizard.page0
            # Pokud je vybrán 1 pracovník, přeskoč na Page6
            if page0.worker_count_group.checkedId() == 1:
                return 6  # Page6_Zaverecne
        # Jinak pokračuj normálně na Page5
        return 5  # Page5_PracovnikB


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

        self.cislo_hrudniho_pasu_b = QLineEdit()

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
        layout.addRow("Číslo hrudního pásu:", self.cislo_hrudniho_pasu_b)


class Page6_Zaverecne(QWizardPage):
    """Stránka 6: Závěrečné údaje"""

    def __init__(self):
        super().__init__()
        self.setTitle("Závěrečné údaje")
        layout = QFormLayout()
        self.setLayout(layout)

        self.mereni_provedl = QLineEdit()

        layout.addRow("Měření provedl:", self.mereni_provedl)

    def nextId(self):
        """Konec wizardu pro Excel workflow"""
        return -1
