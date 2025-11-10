"""
Word Protocol Generator Dialog V2 - Multi-protocol support
Podporuje generování LSZ, PP a CFZ protokolů z jedné složky projektu
"""
from pathlib import Path
from typing import Dict, List, Tuple, Optional
from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QLineEdit, QFileDialog, QMessageBox, QProgressDialog,
    QWidget, QCheckBox, QComboBox, QFrame, QScrollArea
)
from PyQt6.QtCore import Qt
from core.word_protocol_pipeline import WordProtocolPipeline
import json


class ProtocolSection(QWidget):
    """Widget pro jeden typ protokolu (LSZ/PP/CFZ)"""

    def __init__(
        self,
        protocol_type: str,
        protocol_name: str,
        excel_path: Path,
        templates: List[Tuple[str, Path]],
        parent=None
    ):
        """
        Args:
            protocol_type: Typ protokolu ("LSZ", "PP_CAS", "PP_KUSY", "CFZ")
            protocol_name: Displayové jméno (např. "LSZ - Lokální svalová zátěž")
            excel_path: Cesta k Excel souboru pro tento protokol
            templates: Seznam [(template_name, template_path), ...]
        """
        super().__init__(parent)
        self.protocol_type = protocol_type
        self.excel_path = excel_path
        self.templates = templates

        self._setup_ui(protocol_name)

    def _setup_ui(self, protocol_name: str):
        """Vytvoří UI pro sekci protokolu"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)

        # Checkbox pro enable/disable tohoto protokolu
        self.checkbox = QCheckBox(protocol_name)
        self.checkbox.setChecked(True)  # Default: zaškrtnuto
        self.checkbox.setStyleSheet("font-weight: bold; font-size: 12px;")
        self.checkbox.toggled.connect(self._on_checkbox_toggled)
        layout.addWidget(self.checkbox)

        # Container pro detaily (Excel, Template, Output)
        self.details_widget = QWidget()
        details_layout = QVBoxLayout(self.details_widget)
        details_layout.setContentsMargins(20, 5, 0, 5)

        # Excel file (readonly)
        excel_row = QHBoxLayout()
        excel_row.addWidget(QLabel("Excel:"))
        self.excel_label = QLabel(self.excel_path.name)
        self.excel_label.setStyleSheet("color: gray;")
        excel_row.addWidget(self.excel_label)
        excel_row.addStretch()
        details_layout.addLayout(excel_row)

        # Template selector
        template_row = QHBoxLayout()
        template_row.addWidget(QLabel("Šablona:"))

        self.template_combo = QComboBox()
        for template_name, template_path in self.templates:
            self.template_combo.addItem(template_name, template_path)

        template_row.addWidget(self.template_combo, 1)
        details_layout.addLayout(template_row)

        # Output filename
        output_row = QHBoxLayout()
        output_row.addWidget(QLabel("Výstup:"))
        self.output_label = QLabel(self._suggest_output_name())
        self.output_label.setStyleSheet("color: gray;")
        output_row.addWidget(self.output_label)
        output_row.addStretch()
        details_layout.addLayout(output_row)

        layout.addWidget(self.details_widget)

        # Separator
        line = QFrame()
        line.setFrameShape(QFrame.Shape.HLine)
        line.setFrameShadow(QFrame.Shadow.Sunken)
        layout.addWidget(line)

    def _suggest_output_name(self) -> str:
        """Navrhne jméno výstupního souboru"""
        base_name = self.excel_path.stem  # Bez přípony
        return f"{base_name}_protokol.docx"

    def _on_checkbox_toggled(self, checked: bool):
        """Handler pro změnu checkboxu"""
        self.details_widget.setEnabled(checked)

    def is_enabled(self) -> bool:
        """Vrátí True pokud je protokol zaškrtnutý"""
        return self.checkbox.isChecked()

    def get_selected_template(self) -> Optional[Path]:
        """Vrátí cestu k vybranému template"""
        if not self.is_enabled():
            return None
        return self.template_combo.currentData()

    def get_output_filename(self) -> str:
        """Vrátí jméno výstupního souboru"""
        return self.output_label.text()


class WordProtocolGeneratorDialogV2(QDialog):
    """Dialog pro generování Word protokolů - Multi-protocol support"""

    # Mapování protocol_type → displayové jméno
    PROTOCOL_NAMES = {
        "LSZ": "LSZ - Lokální svalová zátěž",
        "PP_CAS": "PP - Pracovní polohy (ČAS)",
        "PP_KUSY": "PP - Pracovní polohy (KUSY)",
        "CFZ": "CFZ - Celková fyzická zátěž"
    }

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Generování Word protokolů")
        self.setMinimumWidth(800)
        self.setMinimumHeight(600)

        # Data
        self.project_folder = None
        self.worker_count = 2
        self.gender = "muži"
        self.protocol_sections: Dict[str, ProtocolSection] = {}

        self._setup_ui()

    def _get_resource_path(self, relative_path: str) -> Path:
        """Získá správnou cestu k resource souboru pro PyInstaller"""
        import sys
        if getattr(sys, 'frozen', False):
            exe_dir = Path(sys.executable).parent
            return exe_dir / relative_path
        else:
            return Path(relative_path)

    def _setup_ui(self):
        """Vytvoří UI"""
        main_layout = QVBoxLayout()
        self.setLayout(main_layout)

        # Title
        title = QLabel("GENEROVÁNÍ WORD PROTOKOLŮ")
        title.setStyleSheet("font-size: 16px; font-weight: bold;")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(title)

        main_layout.addSpacing(20)

        # 1. Project folder
        main_layout.addWidget(self._create_section_label("1️⃣ Složka projektu"))
        self.project_line, self.project_status = self._create_file_row(
            "Vybrat složku projektu...",
            self._browse_project_folder
        )
        main_layout.addLayout(self.project_line)
        main_layout.addWidget(self.project_status)

        main_layout.addSpacing(20)

        # 2. Dostupné protokoly (dynamicky generované)
        main_layout.addWidget(self._create_section_label("2️⃣ Dostupné protokoly (vyberte, které chcete generovat)"))

        # Scroll area pro protokoly
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.StyledPanel)

        self.protocols_container = QWidget()
        self.protocols_layout = QVBoxLayout(self.protocols_container)
        self.protocols_layout.addStretch()

        scroll.setWidget(self.protocols_container)
        main_layout.addWidget(scroll, 1)  # stretch factor 1

        # Placeholder text když není vybrána složka
        self.no_protocols_label = QLabel("⏳ Vyberte složku projektu pro zobrazení dostupných protokolů")
        self.no_protocols_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.no_protocols_label.setStyleSheet("color: gray; font-style: italic;")
        self.protocols_layout.insertWidget(0, self.no_protocols_label)

        main_layout.addSpacing(10)

        # Buttons
        button_layout = QHBoxLayout()
        button_layout.addStretch()

        cancel_btn = QPushButton("Zrušit")
        cancel_btn.clicked.connect(self.reject)
        button_layout.addWidget(cancel_btn)

        self.generate_btn = QPushButton("Generovat")
        self.generate_btn.clicked.connect(self._generate)
        self.generate_btn.setDefault(True)
        self.generate_btn.setEnabled(False)  # Zakázáno, dokud není vybrána složka
        button_layout.addWidget(self.generate_btn)

        main_layout.addLayout(button_layout)

    def _create_section_label(self, text: str) -> QLabel:
        """Vytvoří label pro sekci"""
        label = QLabel(text)
        label.setStyleSheet("font-weight: bold;")
        return label

    def _create_file_row(self, button_text: str, callback):
        """Vytvoří řádek s file dialogem"""
        row_layout = QHBoxLayout()

        line_edit = QLineEdit()
        line_edit.setReadOnly(True)
        line_edit.setPlaceholderText("Žádný soubor nevybrán")
        row_layout.addWidget(line_edit)

        browse_btn = QPushButton(button_text)
        browse_btn.clicked.connect(callback)
        row_layout.addWidget(browse_btn)

        status_label = QLabel("⏳ Čeká na výběr")
        status_label.setStyleSheet("color: gray;")

        return row_layout, status_label

    def _browse_project_folder(self):
        """Dialog pro výběr složky projektu"""
        folder = QFileDialog.getExistingDirectory(
            self,
            "Vyberte složku projektu",
            "projects"
        )

        if not folder:
            return

        folder_path = Path(folder)
        measurement_json = folder_path / "measurement_data.json"

        if not measurement_json.exists():
            QMessageBox.warning(
                self,
                "Chyba",
                f"Ve vybrané složce nebyl nalezen measurement_data.json!\n\n"
                f"Složka: {folder_path}"
            )
            return

        # Nastav složku
        self.project_folder = folder_path
        self.project_line.itemAt(0).widget().setText(str(folder_path))
        self.project_status.setText("✓ measurement_data.json nalezen")
        self.project_status.setStyleSheet("color: green;")

        # Načti worker_count a gender z measurement_data.json
        self._load_measurement_metadata()

        # Detekuj dostupné protokoly
        self._detect_and_display_protocols()

        # Povolit tlačítko Generovat
        self.generate_btn.setEnabled(True)

    def _load_measurement_metadata(self):
        """Načte worker_count a gender z measurement_data.json"""
        try:
            with open(self.project_folder / "measurement_data.json", 'r', encoding='utf-8') as f:
                data = json.load(f)

            section0 = data.get("section0_file_selection", {})
            self.worker_count = section0.get("worker_count", 2)
            self.gender = section0.get("workers_gender", "muži")

            print(f"→ Metadata: {self.worker_count} pracovník(ů), pohlaví: {self.gender}")

        except Exception as e:
            print(f"⚠ Chyba při načítání metadata: {e}")
            self.worker_count = 2
            self.gender = "muži"

    def _detect_and_display_protocols(self):
        """Detekuje dostupné Excel soubory a vytvoří UI pro každý protokol"""
        # Smazat předchozí protokoly
        for section in self.protocol_sections.values():
            section.deleteLater()
        self.protocol_sections.clear()

        # Skrýt placeholder
        self.no_protocols_label.hide()

        # Detekuj dostupné protokoly
        available_protocols = self._detect_available_protocols()

        if not available_protocols:
            self.no_protocols_label.setText("⚠ Nenalezeny žádné Excel soubory pro generování protokolů")
            self.no_protocols_label.show()
            return

        # Vytvoř UI sekci pro každý nalezený protokol
        for protocol_type, excel_path in available_protocols.items():
            # Získej templates pro tento protokol
            templates = self._get_templates_for_protocol(protocol_type)

            if not templates:
                print(f"⚠ Nenalezeny templates pro {protocol_type}")
                continue

            # Vytvoř sekci
            protocol_name = self.PROTOCOL_NAMES.get(protocol_type, protocol_type)
            section = ProtocolSection(
                protocol_type,
                protocol_name,
                excel_path,
                templates,
                self
            )

            # Přidej do layoutu (před stretch)
            self.protocols_layout.insertWidget(
                self.protocols_layout.count() - 1,  # Před stretch
                section
            )

            self.protocol_sections[protocol_type] = section

        print(f"✓ Nalezeno {len(self.protocol_sections)} protokolů")

    def _detect_available_protocols(self) -> Dict[str, Path]:
        """
        Detekuje, jaké Excel soubory jsou ve složce projektu

        Returns:
            Dict[protocol_type, excel_path]
        """
        protocols = {}

        # LSZ
        lsz_files = list(self.project_folder.glob("LSZ_*.xlsm"))
        if lsz_files:
            protocols["LSZ"] = lsz_files[0]

        # PP ČAS
        pp_cas_files = list(self.project_folder.glob("PP_*_CAS.xlsx"))
        if pp_cas_files:
            protocols["PP_CAS"] = pp_cas_files[0]

        # PP KUSY
        pp_kusy_files = list(self.project_folder.glob("PP_*_KUSY.xlsx"))
        if pp_kusy_files:
            protocols["PP_KUSY"] = pp_kusy_files[0]

        # CFZ
        cfz_files = list(self.project_folder.glob("CFZ_*.xlsx"))
        if cfz_files:
            protocols["CFZ"] = cfz_files[0]

        return protocols

    def _get_templates_for_protocol(self, protocol_type: str) -> List[Tuple[str, Path]]:
        """
        Vrátí dostupné templates pro daný protokol

        Args:
            protocol_type: "LSZ", "PP_CAS", "PP_KUSY", "CFZ"

        Returns:
            List[(template_display_name, template_path), ...]
        """
        # Template mapping: (protocol, worker_count, gender) → [(name, path), ...]
        # POZOR: Zatím máme jen LSZ templates, PP a CFZ jsou placeholdery!

        key = (protocol_type, self.worker_count, self.gender)

        # Definice všech možných templates
        template_defs = {
            # LSZ templates (EXISTUJÍCÍ)
            ("LSZ", 2, "muži"): [
                ("LSZ - 2 muži (standard)", "Autorizované protokoly pro MUŽE", "lsz_placeholdery_v2.docx"),
            ],
            ("LSZ", 2, "ženy"): [
                ("LSZ - 2 ženy (standard)", "Autorizované protokoly pro MUŽE", "lsz_placeholdery_v2_females.docx"),
            ],
            ("LSZ", 1, "muži"): [
                ("LSZ - 1 muž", "Jeden zaměstnanec", "LSZ_jeden_MUŽ.DOCX"),
            ],
            ("LSZ", 1, "ženy"): [
                ("LSZ - 1 žena", "Jeden zaměstnanec", "LSZ_jedna_ŽENA.DOCX"),
            ],

            # PP templates (TESTOVACÍ - skutečný template existuje)
            ("PP_CAS", 2, "muži"): [
                ("PP ČAS - 2 muži (testovací)", "Autorizované protokoly pro MUŽE", "PP_XX_Firma_Pozice.docx"),
            ],
            ("PP_CAS", 2, "ženy"): [
                ("PP ČAS - 2 ženy (testovací)", "Autorizované protokoly pro MUŽE", "PP_XX_Firma_Pozice.docx"),
            ],
            ("PP_KUSY", 2, "muži"): [
                ("PP KUSY - 2 muži (testovací)", "Autorizované protokoly pro MUŽE", "PP_XX_Firma_Pozice.docx"),
            ],
            ("PP_KUSY", 2, "ženy"): [
                ("PP KUSY - 2 ženy (testovací)", "Autorizované protokoly pro MUŽE", "PP_XX_Firma_Pozice.docx"),
            ],

            # CFZ templates (BUDOUCNOST - zatím neexistují)
            ("CFZ", 2, "muži"): [
                ("CFZ - 2 muži (TODO)", "Autorizované protokoly pro MUŽE", "CFZ_placeholdery_v2.docx"),
            ],
            ("CFZ", 2, "ženy"): [
                ("CFZ - 2 ženy (TODO)", "Autorizované protokoly pro ŽENY", "CFZ_placeholdery_v2_females.docx"),
            ],
        }

        template_list = template_defs.get(key, [])

        # Najdi skutečné cesty k templates
        result = []
        for display_name, folder, filename in template_list:
            # Hledej v různých lokacích
            possible_paths = [
                Path("sample_protocols") / folder / filename,
                self._get_resource_path("sample_protocols") / folder / filename,
            ]

            for path in possible_paths:
                if path.exists():
                    result.append((display_name, path))
                    break
            else:
                # Template nenalezen - přidej s poznámkou
                print(f"⚠ Template nenalezen: {filename}")
                result.append((f"{display_name} [NENALEZEN]", None))

        return result

    def _generate(self):
        """Spustí generování pro všechny zaškrtnuté protokoly"""
        # Zjisti, které protokoly jsou zaškrtnuté
        protocols_to_generate = []

        for protocol_type, section in self.protocol_sections.items():
            if section.is_enabled():
                template_path = section.get_selected_template()
                if not template_path:
                    QMessageBox.warning(
                        self,
                        "Chyba",
                        f"Template pro {protocol_type} nenalezen!\n"
                        f"Vyberte šablonu ručně nebo ji přidejte do složky sample_protocols."
                    )
                    return

                protocols_to_generate.append((
                    protocol_type,
                    section.excel_path,
                    template_path,
                    section.get_output_filename()
                ))

        if not protocols_to_generate:
            QMessageBox.warning(self, "Chyba", "Vyberte alespoň jeden protokol!")
            return

        # Progress dialog
        progress = QProgressDialog(
            f"Generuji {len(protocols_to_generate)} protokol(ů)...",
            "Zrušit",
            0,
            len(protocols_to_generate),
            self
        )
        progress.setWindowTitle("Probíhá generování")
        progress.setWindowModality(Qt.WindowModality.WindowModal)
        progress.show()

        # Generuj postupně
        results = []
        for i, (protocol_type, excel_path, template_path, output_filename) in enumerate(protocols_to_generate):
            if progress.wasCanceled():
                break

            progress.setValue(i)
            progress.setLabelText(f"Generuji {protocol_type}... ({i+1}/{len(protocols_to_generate)})")

            output_path = self.project_folder / output_filename

            try:
                pipeline = WordProtocolPipeline(self.project_folder)

                success, message = pipeline.generate_protocol(
                    excel_path,
                    template_path,
                    output_path
                )

                results.append((protocol_type, success, message))

                if not success:
                    progress.close()
                    QMessageBox.critical(
                        self,
                        f"Chyba při generování {protocol_type}",
                        message
                    )
                    return

            except Exception as e:
                progress.close()
                QMessageBox.critical(
                    self,
                    f"Chyba při {protocol_type}",
                    f"Neočekávaná chyba:\n{str(e)}"
                )
                return

        progress.setValue(len(protocols_to_generate))

        # Zobraz výsledek
        success_count = sum(1 for _, success, _ in results if success)

        result_text = f"Úspěšně vygenerovány {success_count}/{len(results)} protokoly:\n\n"
        for protocol_type, success, message in results:
            status = "✓" if success else "✗"
            result_text += f"{status} {protocol_type}\n"

        QMessageBox.information(self, "Generování dokončeno", result_text)
        self.accept()
