"""
Utility pro správu nahraných souborů
"""
from pathlib import Path
from datetime import datetime
import shutil


class FileManager:
    """Správa nahraných Word souborů - ukládání do temp a cleanup"""

    def __init__(self):
        """Inicializace FileManageru s temp upload složkou"""
        self.temp_uploads_dir = Path("projects/_temp/uploads")
        self.temp_uploads_dir.mkdir(parents=True, exist_ok=True)

    def save_uploaded_docx(self, source_path: str) -> Path:
        """
        Zkopíruje nahraný Word do temp složky s timestampem.

        Args:
            source_path: Cesta k nahranému souboru (z QFileDialog)

        Returns:
            Absolutní Path k zkopírovanému souboru v temp složce
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"popis_prace_upload_{timestamp}.docx"
        dest_path = self.temp_uploads_dir / filename

        shutil.copy2(source_path, dest_path)
        return dest_path.resolve()

    def cleanup_temp_uploads(self):
        """Smaže všechny temp soubory při zavření aplikace"""
        if self.temp_uploads_dir.exists():
            shutil.rmtree(self.temp_uploads_dir)
            self.temp_uploads_dir.mkdir(parents=True, exist_ok=True)
