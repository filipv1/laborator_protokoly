"""
Entry point pro LABORATO5 aplikaci
"""
import sys
from PyQt6.QtWidgets import QApplication
from gui import MeasurementGUI


def main():
    """Spustí hlavní aplikaci"""
    app = QApplication(sys.argv)
    window = MeasurementGUI()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
