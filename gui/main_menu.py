"""
Main Menu - hlavní okno s výběrem workflow
"""
from PyQt6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QPushButton, QLabel
from PyQt6.QtCore import Qt


class MainMenuWindow(QMainWindow):
    """Hlavní menu s výběrem workflow"""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("LABORATO5 - Automatizace laboratoře")
        self.setMinimumSize(600, 450)

        self._setup_ui()

    def _setup_ui(self):
        """Vytvoří UI s 2 velkými tlačítky"""
        central = QWidget()
        self.setCentralWidget(central)

        layout = QVBoxLayout(central)
        layout.setSpacing(20)
        layout.setContentsMargins(40, 40, 40, 40)

        # Title
        title = QLabel("LABORATO5")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("font-size: 24px; font-weight: bold; color: #2c3e50;")
        layout.addWidget(title)

        subtitle = QLabel("Automatizace laboratoře fyzické zátěže")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        subtitle.setStyleSheet("font-size: 14px; color: #7f8c8d;")
        layout.addWidget(subtitle)

        layout.addSpacing(20)

        # Button 1: Excel workflow
        btn_excel = QPushButton()
        btn_excel.setText("📊 NOVÝ PROJEKT\n\nVytvořit měření + Excel soubory\n(LSZ, PP, CFZ)")
        btn_excel.setMinimumHeight(120)
        btn_excel.setStyleSheet("""
            QPushButton {
                background-color: #3498db;
                color: white;
                border: none;
                border-radius: 10px;
                font-size: 14px;
                font-weight: bold;
                padding: 20px;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
            QPushButton:pressed {
                background-color: #21618c;
            }
        """)
        btn_excel.clicked.connect(self._open_excel_wizard)
        layout.addWidget(btn_excel)

        # Button 2: Word workflow
        btn_word = QPushButton()
        btn_word.setText("📝 GENEROVAT WORD PROTOKOL\n\nZ existujícího projektu a Excelu")
        btn_word.setMinimumHeight(120)
        btn_word.setStyleSheet("""
            QPushButton {
                background-color: #2ecc71;
                color: white;
                border: none;
                border-radius: 10px;
                font-size: 14px;
                font-weight: bold;
                padding: 20px;
            }
            QPushButton:hover {
                background-color: #27ae60;
            }
            QPushButton:pressed {
                background-color: #1e8449;
            }
        """)
        btn_word.clicked.connect(self._open_word_generator)
        layout.addWidget(btn_word)

        layout.addStretch()

        # Exit button
        btn_exit = QPushButton("Ukončit")
        btn_exit.setMaximumWidth(150)
        btn_exit.setStyleSheet("""
            QPushButton {
                background-color: #95a5a6;
                color: white;
                border: none;
                border-radius: 5px;
                font-size: 12px;
                padding: 8px 16px;
            }
            QPushButton:hover {
                background-color: #7f8c8d;
            }
        """)
        btn_exit.clicked.connect(self.close)
        exit_layout = QVBoxLayout()
        exit_layout.addWidget(btn_exit, alignment=Qt.AlignmentFlag.AlignRight)
        layout.addLayout(exit_layout)

    def _open_excel_wizard(self):
        """Otevře wizard pro Excel workflow"""
        from gui.wizard import MeasurementGUI

        wizard = MeasurementGUI()
        wizard.exec()

    def _open_word_generator(self):
        """Otevře dialog pro Word generation"""
        try:
            from gui.word_protocol_dialog import WordProtocolGeneratorDialog

            dialog = WordProtocolGeneratorDialog(self)
            dialog.exec()
        except Exception as e:
            from PyQt6.QtWidgets import QMessageBox
            QMessageBox.critical(
                self,
                "Chyba při otevírání dialogu",
                f"Nepodařilo se otevřít dialog pro generování Word protokolů:\n\n{str(e)}\n\n"
                f"Zkuste aplikaci spustit znovu nebo kontaktujte správce."
            )
            print(f"ERROR: {e}")
            import traceback
            traceback.print_exc()
