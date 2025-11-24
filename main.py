"""
Entry point pro LABORATO5 aplikaci
"""
import sys
import atexit
from PyQt6.QtWidgets import QApplication
from gui import MainMenuWindow
from core import FileManager
from core.system_check import verify_system_compatibility


def cleanup_on_exit():
    """Vyčistí temp soubory při zavření aplikace"""
    file_manager = FileManager()
    file_manager.cleanup_temp_uploads()
    print("Temp soubory vyčištěny")


def main():
    """Spustí hlavní aplikaci"""
    # Verify system compatibility before starting GUI
    # This checks Python version, required packages, and optional services
    if not verify_system_compatibility():
        sys.exit(1)

    # Registruj cleanup funkci pro volání při ukončení
    atexit.register(cleanup_on_exit)

    app = QApplication(sys.argv)
    window = MainMenuWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
