"""
Word Protocol Generator - načítá data ze dvou oddělených JSONů
- measurement_data.json = vstupní data (GUI wizard)
- lsz_results.json = výsledková data (načtená z Excel)
"""
import json
import sys
import argparse
from docxtpl import DocxTemplate, InlineImage
from docx.shared import Mm
from pathlib import Path
from PIL import Image
from core.text_generator import generate_conditional_texts, get_selected_holter_numbers, highlight_selected_holters, highlight_force_distribution_values

# Fix Windows console encoding
sys.stdout.reconfigure(encoding='utf-8')


def normalize_png(png_path):
    """
    Konvertuje PNG do standardního formátu, který python-docx rozpozná.
    xlwings občas exportuje PNG v nestandardním formátu.
    """
    try:
        img = Image.open(png_path)
        # Konvertuj do RGB (pokud je RGBA nebo jiný režim)
        if img.mode not in ('RGB', 'L'):
            img = img.convert('RGB')
        # Ulož zpět jako standardní PNG
        img.save(png_path, 'PNG')
        return True
    except Exception as e:
        print(f"⚠ Chyba při normalizaci PNG: {e}")
        return False


def generate_word_protocol_v1(measurement_json, results_json, template_path, output_path):
    """
    VARIANTA 1: Vnořená struktura
    V Word šabloně používáš: {{ input.section1_firma.company }} a {{ results.Fmax_Phk_Extenzor }}
    """
    # Získej projekt folder (parent measurement_json)
    project_folder = Path(measurement_json).parent

    # Načti oba JSONy
    with open(measurement_json, encoding='utf-8') as f:
        input_data = json.load(f)

    with open(results_json, encoding='utf-8') as f:
        results_data = json.load(f)

    # Vygeneruj podmínkové texty a přidej do input_data
    conditional_texts = generate_conditional_texts(input_data, results_data)
    input_data["section_generated_texts"] = conditional_texts

    # Konvertuj tabulky z dict na list (pro indexování v Jinja2)
    # Vytvoř 1-indexed list (s dummy elementem na indexu 0)
    # Padded až do indexu 50 pro Word template placeholders
    MAX_ROWS = 50
    for key, value in results_data.items():
        if isinstance(value, dict) and value and all(k.isdigit() for k in value.keys()):
            # Převeď slovník s číselnými klíči na list (1-indexed)
            # Padded s prázdnými daty pro template placeholders
            results_data[key] = [None] + [value.get(str(i), {}) for i in range(1, MAX_ROWS + 1)]

    # Vytvoř vnořenou strukturu
    context = {
        "input": input_data,
        "results": results_data
    }

    # Vygeneruj Word
    doc = DocxTemplate(template_path)

    # ZAKOMENTOVÁNO: Vkládání grafů zakázáno
    # # Přidat grafy jako obrázky (z project folder) - PNG formát
    # graf1_path = project_folder / "lsz_charts" / "graf1.png"
    # graf2_path = project_folder / "lsz_charts" / "graf2.png"
    #
    # if graf1_path.exists():
    #     context["graf1"] = InlineImage(doc, str(graf1_path), width=Mm(150))
    # else:
    #     context["graf1"] = ""
    #
    # if graf2_path.exists():
    #     context["graf2"] = InlineImage(doc, str(graf2_path), width=Mm(150))
    # else:
    #     context["graf2"] = ""

    doc.render(context)
    doc.save(output_path)

    # POST-PROCESSING: Zvýrazni vybrané holteru tučně
    selected_holters = get_selected_holter_numbers(input_data)
    if selected_holters:
        print(f"  → Zvýrazňuji holteru: {selected_holters}")
        highlight_selected_holters(output_path, selected_holters)
        print(f"  ✓ Zvýraznění dokončeno")
    else:
        print(f"  ⚠ Žádné holteru k zvýraznění")

    # POST-PROCESSING: Červeně zvýrazni nadlimitní hodnoty v force_distribution
    print(f"  → Zvýrazňuji nadlimitní hodnoty v tabulce force_distribution...")
    highlight_force_distribution_values(output_path, input_data, results_data)
    print(f"  ✓ Červené zvýraznění dokončeno")

    print(f"[OK] Word vygenerován (VNOŘENÁ STRUKTURA): {output_path}")
    print(f"  - Vstupní sekce: {list(input_data.keys())}")
    print(f"  - Výsledkové tabulky: {len([k for k in results_data.keys() if k.startswith('table_')])}")
    print()
    print("V Word šabloně používej:")
    print("  {{ input.section1_firma.company }}")
    print("  {{ results.Fmax_Phk_Extenzor }}")
    print("  {% for row in results.table_somatometrie %}")


def generate_word_protocol_v2(measurement_json, results_json, template_path, output_path):
    """
    VARIANTA 2: Plochá struktura (flat merge)
    V Word šabloně používáš: {{ section1_firma.company }} a {{ Fmax_Phk_Extenzor }}
    UPOZORNĚNÍ: Pokud mají oba JSONy stejné klíče, dojde ke kolizi!
    """
    # Získej projekt folder (parent measurement_json)
    project_folder = Path(measurement_json).parent

    # Načti oba JSONy
    with open(measurement_json, encoding='utf-8') as f:
        input_data = json.load(f)

    with open(results_json, encoding='utf-8') as f:
        results_data = json.load(f)

    # Vygeneruj podmínkové texty a přidej do input_data
    conditional_texts = generate_conditional_texts(input_data, results_data)
    input_data["section_generated_texts"] = conditional_texts

    # Přejmenuj klíče pro kompatibilitu s Word template
    key_mapping = {
        "section1_firma": "section2_firma",
        "section2_additional_data": "section3_additional_data",
        "section3_worker_a": "section4_worker_a",
        "section4_worker_b": "section5_worker_b",
        "section5_final": "section6_final"
    }

    for old_key, new_key in key_mapping.items():
        if old_key in input_data:
            input_data[new_key] = input_data.pop(old_key)

    # Konvertuj tabulky z dict na list (pro indexování v Jinja2)
    # Vytvoř 1-indexed list (s dummy elementem na indexu 0)
    # Padded až do indexu 50 pro Word template placeholders
    MAX_ROWS = 50
    for key, value in results_data.items():
        if isinstance(value, dict) and value and all(k.isdigit() for k in value.keys()):
            # Převeď slovník s číselnými klíči na list (1-indexed)
            # Padded s prázdnými daty pro template placeholders
            results_data[key] = [None] + [value.get(str(i), {}) for i in range(1, MAX_ROWS + 1)]

    # Slouč do jedné úrovně
    context = {**input_data, **results_data}

    # Načti cestu k Word souboru z JSON
    copied_docx_path = input_data.get("section1_uploaded_docx", {}).get("copied_file_path")

    # Vytvoř template pro přístup k new_subdoc metodě
    tpl = DocxTemplate(template_path)

    # Přidat subdoc do contextu
    if copied_docx_path and Path(copied_docx_path).exists():
        subdoc = tpl.new_subdoc(copied_docx_path)
        context["popisprace"] = subdoc
        print(f"✓ Subdokument načten: {Path(copied_docx_path).name}")
    else:
        print("⚠ Varování: Popis práce nebyl nalezen, placeholder zůstane prázdný")
        context["popisprace"] = ""

    # ZAKOMENTOVÁNO: Vkládání grafů zakázáno
    # # Přidat grafy jako obrázky (z project folder) - PNG formát
    # graf1_path = project_folder / "lsz_charts" / "graf1.png"
    # graf2_path = project_folder / "lsz_charts" / "graf2.png"
    #
    # if graf1_path.exists():
    #     context["graf1"] = InlineImage(tpl, str(graf1_path), width=Mm(150))
    #     print(f"✓ Graf 1 přidán do Word")
    # else:
    #     print(f"⚠ Graf 1 nenalezen: {graf1_path}")
    #     context["graf1"] = ""
    #
    # if graf2_path.exists():
    #     context["graf2"] = InlineImage(tpl, str(graf2_path), width=Mm(150))
    #     print(f"✓ Graf 2 přidán do Word")
    # else:
    #     print(f"⚠ Graf 2 nenalezen: {graf2_path}")
    #     context["graf2"] = ""

    # Vygeneruj Word (použít již vytvořený tpl objekt!)
    tpl.render(context)
    tpl.save(output_path)

    # POST-PROCESSING: Zvýrazni vybrané holteru tučně
    selected_holters = get_selected_holter_numbers(input_data)
    if selected_holters:
        print(f"  → Zvýrazňuji holteru: {selected_holters}")
        highlight_selected_holters(output_path, selected_holters)
        print(f"  ✓ Zvýraznění dokončeno")
    else:
        print(f"  ⚠ Žádné holteru k zvýraznění")

    # POST-PROCESSING: Červeně zvýrazni nadlimitní hodnoty v force_distribution
    print(f"  → Zvýrazňuji nadlimitní hodnoty v tabulce force_distribution...")
    highlight_force_distribution_values(output_path, input_data, results_data)
    print(f"  ✓ Červené zvýraznění dokončeno")

    print(f"[OK] Word vygenerován (PLOCHÁ STRUKTURA): {output_path}")
    print(f"  - Celkový počet klíčů: {len(context)}")
    print()
    print("V Word šabloně používej:")
    print("  {{ section1_firma.company }}")
    print("  {{ Fmax_Phk_Extenzor }}")
    print("  {% for row in table_somatometrie %}")


def generate_word_protocol_v3(measurement_json, results_json, template_path, output_path):
    """
    VARIANTA 3: Prefixovaná struktura
    V Word šabloně používáš: {{ m.section1_firma.company }} a {{ r.Fmax_Phk_Extenzor }}
    Krátké prefixy, jasná separace
    """
    # Získej projekt folder (parent measurement_json)
    project_folder = Path(measurement_json).parent

    # Načti oba JSONy
    with open(measurement_json, encoding='utf-8') as f:
        input_data = json.load(f)

    with open(results_json, encoding='utf-8') as f:
        results_data = json.load(f)

    # Vygeneruj podmínkové texty a přidej do input_data
    conditional_texts = generate_conditional_texts(input_data, results_data)
    input_data["section_generated_texts"] = conditional_texts

    # Konvertuj tabulky z dict na list (pro indexování v Jinja2)
    # Vytvoř 1-indexed list (s dummy elementem na indexu 0)
    # Padded až do indexu 50 pro Word template placeholders
    MAX_ROWS = 50
    for key, value in results_data.items():
        if isinstance(value, dict) and value and all(k.isdigit() for k in value.keys()):
            # Převeď slovník s číselnými klíči na list (1-indexed)
            # Padded s prázdnými daty pro template placeholders
            results_data[key] = [None] + [value.get(str(i), {}) for i in range(1, MAX_ROWS + 1)]

    # Vytvoř prefixovanou strukturu
    context = {
        "m": input_data,
        "r": results_data
    }

    # Vygeneruj Word
    doc = DocxTemplate(template_path)

    # ZAKOMENTOVÁNO: Vkládání grafů zakázáno
    # # Přidat grafy jako obrázky (z project folder) - PNG formát
    # graf1_path = project_folder / "lsz_charts" / "graf1.png"
    # graf2_path = project_folder / "lsz_charts" / "graf2.png"
    #
    # if graf1_path.exists():
    #     context["graf1"] = InlineImage(doc, str(graf1_path), width=Mm(150))
    # else:
    #     context["graf1"] = ""
    #
    # if graf2_path.exists():
    #     context["graf2"] = InlineImage(doc, str(graf2_path), width=Mm(150))
    # else:
    #     context["graf2"] = ""

    doc.render(context)
    doc.save(output_path)

    # POST-PROCESSING: Zvýrazni vybrané holteru tučně
    selected_holters = get_selected_holter_numbers(input_data)
    if selected_holters:
        print(f"  → Zvýrazňuji holteru: {selected_holters}")
        highlight_selected_holters(output_path, selected_holters)
        print(f"  ✓ Zvýraznění dokončeno")
    else:
        print(f"  ⚠ Žádné holteru k zvýraznění")

    # POST-PROCESSING: Červeně zvýrazni nadlimitní hodnoty v force_distribution
    print(f"  → Zvýrazňuji nadlimitní hodnoty v tabulce force_distribution...")
    highlight_force_distribution_values(output_path, input_data, results_data)
    print(f"  ✓ Červené zvýraznění dokončeno")

    print(f"[OK] Word vygenerován (PREFIXOVANÁ STRUKTURA): {output_path}")
    print()
    print("V Word šabloně používej:")
    print("  {{ m.section1_firma.company }}")
    print("  {{ r.Fmax_Phk_Extenzor }}")
    print("  {% for row in r.table_somatometrie %}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Generuje Word protokol ze dvou JSON souborů')
    parser.add_argument('measurement_json', help='Cesta k measurement_data JSON souboru')
    parser.add_argument('results_json', help='Cesta k lsz_results JSON souboru')
    parser.add_argument('template_path', help='Cesta k Word šabloně (.docx)')
    parser.add_argument('output_path', help='Cesta k výstupnímu Word souboru')
    parser.add_argument('--variant', choices=['v1', 'v2', 'v3'], default='v2',
                        help='Varianta generování (v1=vnořená, v2=plochá, v3=prefixovaná)')

    args = parser.parse_args()

    # Spusť vybranou variantu
    if args.variant == 'v1':
        generate_word_protocol_v1(args.measurement_json, args.results_json,
                                  args.template_path, args.output_path)
    elif args.variant == 'v2':
        generate_word_protocol_v2(args.measurement_json, args.results_json,
                                  args.template_path, args.output_path)
    elif args.variant == 'v3':
        generate_word_protocol_v3(args.measurement_json, args.results_json,
                                  args.template_path, args.output_path)
