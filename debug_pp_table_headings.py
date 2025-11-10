"""
Debug skript pro zjištění nadpisů PP tabulek v Word dokumentu
"""
from docx import Document
import sys

def find_table_headings(docx_path):
    """Najde všechny nadpisy nad tabulkami"""
    doc = Document(docx_path)

    print(f"Analyzuji dokument: {docx_path}")
    print("="*80)
    print()

    # Projdi všechny elementy v dokumentu
    body = doc._element.body

    for i, element in enumerate(body):
        tag = element.tag.split('}')[-1]  # Odstraň namespace

        if tag == 'p':  # Paragraph
            # Najdi text v paragraphu
            para_text = ""
            for child in element:
                if child.tag.endswith('r'):  # Run
                    for t in child:
                        if t.tag.endswith('t'):  # Text
                            para_text += t.text if t.text else ""

            if para_text.strip():
                # Zkontroluj, jestli následující element je tabulka
                if i + 1 < len(body):
                    next_element = body[i + 1]
                    next_tag = next_element.tag.split('}')[-1]

                    if next_tag == 'tbl':  # Následuje tabulka
                        print(f"NADPIS NAD TABULKOU:")
                        # Safe print - replace problematic chars
                        safe_text = para_text.strip().encode('ascii', 'replace').decode('ascii')
                        print(f"  '{safe_text}'")
                        print(f"  Length: {len(para_text.strip())}")
                        print()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python debug_pp_table_headings.py <word_file.docx>")
        print()
        print("Example:")
        print("  python debug_pp_table_headings.py projects/325_Ascari_sro/PP_325_Ascari_sro_CAS_protokol.docx")
        sys.exit(1)

    docx_path = sys.argv[1]
    find_table_headings(docx_path)
