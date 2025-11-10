"""
Regenerace PP protokolu pro test
"""
import os
from pathlib import Path


def regenerate_pp():
    """Regeneruje PP protokol přes hlavní workflow"""
    project_path = Path("projects/325_Ascari_sro")

    # Změň se do adresáře projektu
    os.chdir(project_path)

    # Spusť generování PP protokolu
    cmd = "python ../../gui/word_protocol_dialog.py"

    # Místo GUI použijeme přímé volání
    import sys
    sys.path.insert(0, "../../")

    from core.word_protocol_pipeline import WordProtocolPipeline

    # Parametry
    project_folder = "."
    excel_file = "PP_325_Ascari_sro_CAS.xlsx"
    template = "../../sample_protocols/Autorizované protokoly pro MUŽE/PP_XX_Firma_Pozice.docx"
    output_path = "PP_325_Ascari_sro_CAS_protokol_TEST.docx"

    # Vytvoř pipeline
    pipeline = WordProtocolPipeline()

    # Generuj protokol
    success, message = pipeline.generate_word_protocol(
        project_folder=project_folder,
        excel_file=excel_file,
        template_path=template,
        output_path=output_path
    )

    if success:
        print(f"✓ PP protokol úspěšně vygenerován: {output_path}")
    else:
        print(f"✗ Chyba: {message}")

    return output_path


if __name__ == "__main__":
    print("REGENERACE PP PROTOKOLU")
    print("="*60)
    output = regenerate_pp()
    print("="*60)
    print(f"Výsledný soubor: {output}")
    print("Otevřete v MS Word pro kontrolu prázdných tabulek.")