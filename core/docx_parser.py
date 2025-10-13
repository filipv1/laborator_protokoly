"""
DOCX Parser - parsování Word dokumentů
"""
from pathlib import Path
from typing import Dict, Any, Optional
from docx import Document


class DocxParser:
    """Parsování Word dokumentů pro získání tabulek"""

    @staticmethod
    def parse_time_schedule_table(docx_path: str) -> Dict[str, Any]:
        """
        Naparsuje tabulku "Časové rozložení pracovní směny" z Word dokumentu.

        Args:
            docx_path: Cesta k .docx souboru

        Returns:
            Dictionary s line1...line20 a total
        """
        if not docx_path:
            return DocxParser._get_empty_time_schedule()

        try:
            doc = Document(docx_path)

            # Hledáme druhou tabulku (index 1)
            # Tabulka 1 = informační (místo měření, datum, ...)
            # Tabulka 2 = časové rozložení
            if len(doc.tables) < 2:
                print(f"Varování: Dokument má méně než 2 tabulky")
                return DocxParser._get_empty_time_schedule()

            table = doc.tables[1]  # Druhá tabulka (index 1)

            result = {}
            total_row = None

            # Projdi řádky tabulky (přeskoč header)
            row_count = 0
            for i, row in enumerate(table.rows):
                if i == 0:  # Přeskoč header
                    continue

                cells = row.cells
                if len(cells) < 4:
                    continue

                # Získej text z buněk
                number = cells[0].text.strip()
                operation = cells[1].text.strip()
                time_text = cells[2].text.strip()
                pieces_text = cells[3].text.strip()

                # Detekuj řádek "Celkem"
                if "celkem" in number.lower() or "celkem" in operation.lower():
                    total_row = {
                        "time_min": DocxParser._parse_number(time_text),
                        "pieces_count": DocxParser._parse_number(pieces_text)
                    }
                    continue

                # Normální řádek
                row_count += 1
                if row_count > 20:  # Max 20 řádků
                    break

                result[f"line{row_count}"] = {
                    "number": number,
                    "operation": operation,
                    "time_min": DocxParser._parse_number(time_text),
                    "pieces_count": DocxParser._parse_number(pieces_text)
                }

            # Doplň prázdné řádky do 20
            for i in range(row_count + 1, 21):
                result[f"line{i}"] = {
                    "number": "",
                    "operation": "",
                    "time_min": None,
                    "pieces_count": None
                }

            # Přidej total
            if total_row:
                result["total"] = total_row
            else:
                result["total"] = {"time_min": None, "pieces_count": None}

            return result

        except Exception as e:
            print(f"Chyba při parsování Word dokumentu: {e}")
            return DocxParser._get_empty_time_schedule()

    @staticmethod
    def _parse_number(text: str) -> Optional[int]:
        """
        Převede textový řetězec na číslo.

        Args:
            text: Textový řetězec (např. "415", "-", "")

        Returns:
            Číslo nebo None
        """
        text = text.strip()
        if not text or text == "-":
            return None

        try:
            return int(text)
        except ValueError:
            return None

    @staticmethod
    def _get_empty_time_schedule() -> Dict[str, Any]:
        """
        Vrátí prázdnou strukturu časového snímku.

        Returns:
            Dictionary s prázdnými line1...line20 a total
        """
        result = {}
        for i in range(1, 21):
            result[f"line{i}"] = {
                "number": "",
                "operation": "",
                "time_min": None,
                "pieces_count": None
            }
        result["total"] = {"time_min": None, "pieces_count": None}
        return result
