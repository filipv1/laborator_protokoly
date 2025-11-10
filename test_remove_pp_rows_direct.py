"""
Přímý test remove_empty_pp_rows() na existujícím Word dokumentu
"""
import sys
import shutil
from pathlib import Path
from generate_word_from_two_sources import remove_empty_pp_rows

if len(sys.argv) < 2:
    print("Usage: python test_remove_pp_rows_direct.py <word_file.docx>")
    print()
    print("Example:")
    print("  python test_remove_pp_rows_direct.py projects/325_Ascari_sro/PP_325_Ascari_sro_CAS_protokol.docx")
    sys.exit(1)

word_file = Path(sys.argv[1])

if not word_file.exists():
    print(f"ERROR Soubor nenalezen: {word_file}")
    sys.exit(1)

# Vytvoř zálohu
backup_file = word_file.with_name(word_file.stem + "_BACKUP.docx")
shutil.copy(word_file, backup_file)
print(f"Zalohováno do: {backup_file}")
print()

# Spusť funkci
print(f"Odstraňuji prázdné PP řádky z: {word_file}")
print("="*80)
remove_empty_pp_rows(str(word_file))
print("="*80)
print()
print(f"OK Hotovo! Zkontroluj výsledek v: {word_file}")
print(f"Záloha: {backup_file}")
