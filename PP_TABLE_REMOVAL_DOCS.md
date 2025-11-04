# PP Table Removal - Dokumentace nové funkcionality

## Přehled

Rozšíření funkce `remove_empty_pp_rows()` o automatické odstranění celých prázdných tabulek v PP Word protokolech.

## Nová funkcionalita

### Automatické odstranění prázdných tabulek

**Co je nového:**
- Pokud po odstranění prázdných řádků (obsahujících pouze nuly) nezůstane v PP tabulce žádný datový řádek, celá tabulka je automaticky odstraněna z dokumentu
- Tím se zabrání zobrazení prázdných záhlaví tabulek bez dat

### Jak to funguje:

1. **Odstranění prázdných řádků** (původní funkce):
   - Smaže řádky kde `vyskyt_min_a == 0 AND vyskyt_min_b == 0 AND prumer_min == 0`

2. **Detekce prázdné tabulky** (nová funkce):
   - Po odstranění prázdných řádků zkontroluje, zda v tabulce zůstaly datové řádky
   - Datové řádky = všechny kromě:
     - Záhlaví (řádek 0)
     - Sekčních nadpisů (TRUP, HLAVA_KRK, PHK, LHK, atd.)
     - Řádku "OSTATNI" / "Ultrathink"

3. **Odstranění celé tabulky**:
   - Pokud nezůstaly žádné datové řádky, celá tabulka je odstraněna
   - Použití python-docx API: `parent.remove(table._element)`

## Implementace

### Umístění kódu
- **Soubor:** `generate_word_from_two_sources.py`
- **Funkce:** `remove_empty_pp_rows()` (řádky 651-849)

### Klíčové změny:

```python
# Nové proměnné pro sledování tabulek k odstranění
tables_removed = 0
tables_to_remove = []

# Po odstranění prázdných řádků - kontrola zbývajících dat
has_data_rows = False
for row_idx in range(1, len(table.rows)):  # Skip záhlaví
    # ... kontrola jestli řádek obsahuje data ...
    if not (is_empty_or_zero(vyskyt_a) and is_empty_or_zero(vyskyt_b) and is_empty_or_zero(prumer)):
        has_data_rows = True
        break

# Označení tabulky k odstranění pokud nemá data
if not has_data_rows:
    tables_to_remove.append(table)

# Odstranění prázdných tabulek
for table in tables_to_remove:
    parent = table._element.getparent()
    parent.remove(table._element)
```

## Testování

### Testovací skripty

1. **`test_pp_empty_table_creation.py`**
   - Vytvoří testovací dokument s prázdnými a neprázdnými tabulkami
   - Ověří správné odstranění prázdných a zachování neprázdných

2. **`test_pp_edge_cases.py`**
   - Testuje edge cases:
     - Tabulka pouze se záhlavím a OSTATNI
     - Směs různých typů nul (0, 0.0, prázdné)
     - Tabulka s jedním nenulovým řádkem
     - Více section headers v jedné tabulce

### Výsledky testů

Všechny testy prošly úspěšně:
- ✓ Prázdné tabulky jsou správně odstraněny
- ✓ Tabulky s daty jsou zachovány
- ✓ Edge cases fungují správně

## Příklady

### Před úpravou (prázdná tabulka):
```
Nepřijatelná/podmíněně přijatelná pracovní poloha | Svalová práce | MUŽ 1 | MUŽ 2 | Ø | Typ
TRUP
OSTATNI | Ultrathink
```

### Po úpravě:
*Celá tabulka je odstraněna z dokumentu*

### Tabulka která zůstane (obsahuje data):
```
Nepřijatelná/podmíněně přijatelná pracovní poloha | Svalová práce | MUŽ 1 | MUŽ 2 | Ø | Typ
PHK
Elevace paže | Statická | 5 | 0 | 2.5 | PP
OSTATNI | Ultrathink
```

## Integrace

Funkce je automaticky volána při generování PP protokolů:
- V `generate_word_protocol_v2()` na řádku 476
- Podmíněně pro PP protokoly: `if protocol_type in ["PP_CAS", "PP_KUSY"]`

## Výhody

1. **Čistší výstupní dokumenty** - žádné prázdné tabulky
2. **Lepší čitelnost** - dokument obsahuje pouze relevantní data
3. **Profesionálnější vzhled** - odstranění zbytečných elementů
4. **Automatizace** - uživatel nemusí ručně mazat prázdné tabulky

## Poznámky

- Funkce zachovává okolní text a formátování
- Odstranění tabulky neovlivní ostatní prvky dokumentu
- Logování poskytuje informace o počtu odstraněných tabulek