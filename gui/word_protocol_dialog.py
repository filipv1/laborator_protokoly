"""
Word Protocol Generator Dialog - dialog pro generování Word protokolů
"""
from pathlib import Path
from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QLineEdit, QFileDialog, QMessageBox, QProgressDialog
)
from PyQt6.QtCore import Qt
from core.word_protocol_pipeline import WordProtocolPipeline


class WordProtocolGeneratorDialog(QDialog):
    """Dialog pro generování Word protokolů z existujících projektů"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Generování Word protokolu")
        self.setMinimumWidth(700)
        self.setMinimumHeight(400)

        # File paths
        self.project_folder = None
        self.excel_path = None
        self.template_path = None
        self.output_path = None

        # Default template path - pro PyInstaller kompatibilitu
        try:
            # Zkus najít šablonu v různých lokacích
            possible_paths = [
                Path(r"Vzorové protokoly\Autorizované protokoly pro MUŽE\lsz_placeholdery_v2.docx"),
                Path("Vzorové protokoly") / "Autorizované protokoly pro MUŽE" / "lsz_placeholdery_v2.docx",
                # Pro PyInstaller - hledej relativně k exe
                self._get_resource_path("Vzorové protokoly") / "Autorizované protokoly pro MUŽE" / "lsz_placeholdery_v2.docx"
            ]

            self.default_template_path = None
            for path in possible_paths:
                if path.exists():
                    self.default_template_path = path
                    print(f"✓ Našel jsem default šablonu: {path}")
                    break

            if not self.default_template_path:
                print("⚠ Default šablona nenalezena - bude třeba vybrat ručně")

        except Exception as e:
            print(f"⚠ Chyba při hledání default šablony: {e}")
            self.default_template_path = None

        self._setup_ui()
        self._auto_select_default_template()

    def _get_resource_path(self, relative_path):
        """Získá správnou cestu k resource souboru pro PyInstaller"""
        import sys
        import os

        # Pro PyInstaller - hledej vedle EXE souboru, ne v _MEIPASS
        # Protože složka "Vzorové protokoly" má diakritiku a PyInstaller ji neumí zabalit
        if getattr(sys, 'frozen', False):
            # Běží jako EXE
            exe_dir = Path(sys.executable).parent
            return exe_dir / relative_path
        else:
            # Běží jako Python script
            return Path(relative_path)

    def _setup_ui(self):
        """Vytvoří UI s file dialogy"""
        layout = QVBoxLayout()
        self.setLayout(layout)

        # Title
        title = QLabel("GENEROVÁNÍ WORD PROTOKOLU")
        title.setStyleSheet("font-size: 16px; font-weight: bold;")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)

        layout.addSpacing(20)

        # 1. Project folder
        layout.addWidget(self._create_section_label("1️⃣ Složka projektu"))
        self.project_line, self.project_status = self._create_file_row(
            "Vybrat složku projektu...",
            self._browse_project_folder
        )
        layout.addLayout(self.project_line)
        layout.addWidget(self.project_status)

        layout.addSpacing(15)

        # 2. LSZ Excel
        layout.addWidget(self._create_section_label("2️⃣ LSZ Excel soubor"))
        self.excel_line, self.excel_status = self._create_file_row(
            "Vybrat LSZ Excel...",
            self._browse_excel
        )
        layout.addLayout(self.excel_line)
        layout.addWidget(self.excel_status)

        layout.addSpacing(15)

        # 3. Word template
        layout.addWidget(self._create_section_label("3️⃣ Word šablona"))
        self.template_line, self.template_status = self._create_file_row(
            "Vybrat Word šablonu...",
            self._browse_template
        )
        layout.addLayout(self.template_line)
        layout.addWidget(self.template_status)

        layout.addSpacing(15)

        # 4. Output path
        layout.addWidget(self._create_section_label("4️⃣ Výstupní soubor"))
        self.output_line, self.output_status = self._create_file_row(
            "Kam uložit Word...",
            self._browse_output
        )
        layout.addLayout(self.output_line)
        layout.addWidget(self.output_status)

        layout.addStretch()

        # Buttons
        button_layout = QHBoxLayout()
        button_layout.addStretch()

        cancel_btn = QPushButton("Zrušit")
        cancel_btn.clicked.connect(self.reject)
        button_layout.addWidget(cancel_btn)

        self.generate_btn = QPushButton("Generovat")
        self.generate_btn.clicked.connect(self._generate)
        self.generate_btn.setDefault(True)
        button_layout.addWidget(self.generate_btn)

        layout.addLayout(button_layout)

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

        if folder:
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

            self.project_folder = folder_path
            self.project_line.itemAt(0).widget().setText(str(folder_path))
            self.project_status.setText("✓ JSON nalezen")
            self.project_status.setStyleSheet("color: green;")

            # Auto-select LSZ Excel pokud existuje
            self._auto_select_lsz_excel()

            # Auto-suggest output path
            self._auto_suggest_output()

            # NOVÉ: Auto-select správný Word template podle pohlaví
            self._auto_select_template_by_gender()

    def _auto_select_lsz_excel(self):
        """Automaticky najde LSZ Excel v project folder"""
        if not self.project_folder:
            return

        lsz_files = list(self.project_folder.glob("LSZ_*.xlsm"))
        if lsz_files:
            self.excel_path = lsz_files[0]
            self.excel_line.itemAt(0).widget().setText(str(self.excel_path))
            self.excel_status.setText("✓ Excel nalezen")
            self.excel_status.setStyleSheet("color: green;")

    def _auto_suggest_output(self):
        """Automaticky navrhne output path"""
        if not self.project_folder:
            return

        output_path = self.project_folder / "LSZ_protokol.docx"
        self.output_path = output_path
        self.output_line.itemAt(0).widget().setText(str(output_path))
        self.output_status.setText("✓ Cesta nastavena")
        self.output_status.setStyleSheet("color: green;")

    def _auto_select_template_by_gender(self):
        """Automaticky vybere správný Word template podle počtu pracovníků a pohlaví z measurement_data.json"""
        if not self.project_folder:
            return

        try:
            import json
            measurement_json = self.project_folder / "measurement_data.json"

            if not measurement_json.exists():
                print("⚠ measurement_data.json nenalezen pro auto-select template")
                return

            # Načti JSON
            with open(measurement_json, 'r', encoding='utf-8') as f:
                data = json.load(f)

            # Zjisti počet pracovníků a pohlaví ze section0_file_selection
            section0 = data.get("section0_file_selection", {})
            worker_count = section0.get("worker_count", 2)  # Default: 2 pracovníci
            gender = section0.get("workers_gender", "muži")  # Default: muži

            print(f"→ Zjištěno: {worker_count} pracovník(ů), pohlaví: {gender}")

            # Mapování (worker_count, gender) → (template_filename, folder)
            template_map = {
                (1, "muži"): ("LSZ_jeden_MUŽ.DOCX", "Jeden zaměstnanec"),
                (1, "ženy"): ("LSZ_jeden_ŽENA.DOCX", "Jeden zaměstnanec"),
                (2, "muži"): ("lsz_placeholdery_v2.docx", "Autorizované protokoly pro MUŽE"),
                (2, "ženy"): ("lsz_placeholdery_v2_females.docx", "Autorizované protokoly pro MUŽE")
            }

            # Zjisti template filename a složku
            template_info = template_map.get((worker_count, gender))
            if not template_info:
                print(f"⚠ Neznámá kombinace: {worker_count} pracovník(ů) + {gender}")
                self.template_status.setText("⚠ Vyberte šablonu ručně")
                self.template_status.setStyleSheet("color: orange;")
                return

            template_filename, template_folder = template_info

            # Hledej template v různých lokacích
            possible_paths = [
                Path(f"Vzorové protokoly/{template_folder}/{template_filename}"),
                self._get_resource_path("Vzorové protokoly") / template_folder / template_filename,
            ]

            # Najdi první existující cestu
            selected_template = None
            for path in possible_paths:
                if path.exists():
                    selected_template = path
                    break

            if selected_template:
                self.template_path = selected_template
                self.template_line.itemAt(0).widget().setText(str(selected_template))
                self.template_status.setText(f"✓ Template pro {worker_count} {gender} nastaven")
                self.template_status.setStyleSheet("color: green;")
                print(f"✓ Auto-selected template: {selected_template}")
            else:
                print(f"⚠ Template pro {worker_count} {gender} nenalezen: {template_filename}")
                self.template_status.setText("⚠ Vyberte šablonu ručně")
                self.template_status.setStyleSheet("color: orange;")

        except Exception as e:
            print(f"⚠ Chyba při auto-select template: {e}")
            import traceback
            traceback.print_exc()

    def _browse_excel(self):
        """Dialog pro výběr LSZ Excel"""
        start_dir = str(self.project_folder) if self.project_folder else "projects"

        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Vyberte LSZ Excel soubor",
            start_dir,
            "Excel soubory (*.xlsm *.xlsx);;Všechny soubory (*.*)"
        )

        if file_path:
            self.excel_path = Path(file_path)
            self.excel_line.itemAt(0).widget().setText(str(self.excel_path))
            self.excel_status.setText("✓ Excel vybrán")
            self.excel_status.setStyleSheet("color: green;")

    def _browse_template(self):
        """Dialog pro výběr Word šablony"""
        # Najdi výchozí složku pro šablony
        start_dir = "."
        try:
            vzorove_path = self._get_resource_path("Vzorové protokoly")
            if vzorove_path.exists():
                start_dir = str(vzorove_path)
            elif Path("Vzorové protokoly").exists():
                start_dir = "Vzorové protokoly"
        except:
            pass

        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Vyberte Word šablonu",
            start_dir,
            "Word šablony (*.docx);;Všechny soubory (*.*)"
        )

        if file_path:
            self.template_path = Path(file_path)
            self.template_line.itemAt(0).widget().setText(str(self.template_path))
            self.template_status.setText("✓ Šablona vybrána")
            self.template_status.setStyleSheet("color: green;")

    def _browse_output(self):
        """Dialog pro výstupní Word soubor"""
        start_dir = str(self.project_folder) if self.project_folder else "projects"

        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Kam uložit Word protokol",
            start_dir,
            "Word dokumenty (*.docx);;Všechny soubory (*.*)"
        )

        if file_path:
            output_path = Path(file_path)
            if output_path.suffix.lower() != '.docx':
                output_path = output_path.with_suffix('.docx')

            self.output_path = output_path
            self.output_line.itemAt(0).widget().setText(str(self.output_path))
            self.output_status.setText("✓ Cesta nastavena")
            self.output_status.setStyleSheet("color: green;")

    def _auto_select_default_template(self):
        """Automaticky nastaví default template pokud existuje"""
        if self.default_template_path and self.default_template_path.exists():
            self.template_path = self.default_template_path
            self.template_line.itemAt(0).widget().setText(str(self.template_path))
            self.template_status.setText("✓ Default šablona nastavena")
            self.template_status.setStyleSheet("color: green;")
        else:
            self.template_status.setText("⚠ Vyberte šablonu ručně")
            self.template_status.setStyleSheet("color: orange;")

    def _generate(self):
        """Spustí pipeline generování"""
        # Validace všech cest
        if not self.project_folder:
            QMessageBox.warning(self, "Chyba", "Vyberte složku projektu!")
            return

        if not self.excel_path:
            QMessageBox.warning(self, "Chyba", "Vyberte LSZ Excel soubor!")
            return

        if not self.template_path:
            QMessageBox.warning(self, "Chyba", "Vyberte Word šablonu!")
            return

        if not self.output_path:
            QMessageBox.warning(self, "Chyba", "Vyberte výstupní soubor!")
            return

        # Progress dialog
        progress = QProgressDialog("Generuji Word protokol...", None, 0, 0, self)
        progress.setWindowTitle("Probíhá generování")
        progress.setWindowModality(Qt.WindowModality.WindowModal)
        progress.show()

        try:
            # Vytvoř pipeline
            pipeline = WordProtocolPipeline(self.project_folder)

            # Spusť generování
            success, message = pipeline.generate_protocol(
                self.excel_path,
                self.template_path,
                self.output_path
            )

            progress.close()

            if success:
                QMessageBox.information(
                    self,
                    "Úspěch",
                    f"{message}\n\n"
                    f"Soubory vytvořené:\n"
                    f"• lsz_results.json\n"
                    f"• {self.output_path.name}\n"
                    f"• Grafy (lsz_charts/)"
                )
                self.accept()
            else:
                QMessageBox.critical(
                    self,
                    "Chyba",
                    message
                )

        except Exception as e:
            progress.close()
            QMessageBox.critical(
                self,
                "Chyba",
                f"Nepodařilo se vygenerovat Word protokol:\n{str(e)}"
            )
