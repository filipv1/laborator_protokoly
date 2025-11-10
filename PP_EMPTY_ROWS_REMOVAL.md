# PP Empty Rows Removal - Dokumentace

## Přehled

Implementace odstranění prázdných řádků z PP Word protokolů. Používá **stejnou backend logiku** jako LSZ protokoly, ale s upraveným podmínkovým kritériem.

## Implementované funkce

### `remove_empty_pp_rows(docx_path)`

**Umístění:** `generate_word_from_two_sources.py` (řádek 646)

**Účel:** Smaže řádky z PP tabulek, kde všechny tři sloupce obsahují hodnotu 0 nebo jsou prázdné.

**Kritérium pro odstranění:**
```python
vyskyt_min_a == 0 AND vyskyt_min_b == 0 AND prumer_min == 0
```

Řádek se smaže POUZE pokud VŠECHNY tři hodnoty jsou 0 (nebo prázdné).

### Struktura PP tabulky

```
Sloupec | Index | Název              | JSON klíč
--------|-------|--------------------|--------------
A       | 0     | Název polohy       | nazev_polohy
B       | 1     | Typ svalové práce  | typ_svalove_prace
C       | 2     | Výskyt min A       | vyskyt_min_a ✓
D       | 3     | Výskyt min B       | vyskyt_min_b ✓
E       | 4     | Průměr min         | prumer_min   ✓
F       | 5     | Typ pracovní polohy| typ_pracovni_polohy
```

✓ = Kontrolované sloupce pro rozhodnutí o odstranění

## Srovnání s LSZ logikou

### LSZ: `remove_empty_activity_rows()`
- **Kontroluje:** 1 sloupec (activity)
- **Kritérium:** `activity == "0" OR activity == "" OR activity == "None"`
- **Tabulky:** Identifikuje podle nadpisů:
  - "Výsledky měřených osob – počet pohybů/jednotka:"
  - "Výsledky měřených osob – síla % Fmax:"
  - "Výsledky měřených osob – rozložení vynakládaných svalových sil ve směně:"

### PP: `remove_empty_pp_rows()`
- **Kontroluje:** 3 sloupce (vyskyt_min_a, vyskyt_min_b, prumer_min)
- **Kritérium:** `vyskyt_min_a == 0 AND vyskyt_min_b == 0 AND prumer_min == 0`
- **Tabulky:** Identifikuje podle nadpisů (case-insensitive):
  - "TRUP" / "Trup"
  - "HLAVA A KRK" / "Hlava a krk"
  - "PHK" / "Pravá horní končetina"
  - "LHK" / "Levá horní končetina"
  - "DOLNÍ KONČETINY" / "Dolní končetiny"
  - "OSTATNÍ ČÁSTI TĚLA" / "Ostatní části těla"
  - "Pracovní polohy"
  - "Hodnocení pracovních poloh"

### Společná logika (identická implementace)

Obě funkce používají **totožnou XML backend logiku**:

1. **Hledání tabulek:**
   ```python
   para_element = para._element
   parent = para_element.getparent()
   para_position = parent.index(para_element)

   # Hledej následující element typu table
   for i in range(para_position + 1, len(parent)):
       next_element = parent[i]
       if next_element.tag.endswith('tbl'):
           # Nalezena tabulka
   ```

2. **Procházení řádků ODZADU:**
   ```python
   for row_idx in range(len(table.rows) - 1, 0, -1):  # Skip row 0 (header)
   ```
   - Důvod: Při mazání řádků se indexy neposunují

3. **Odstranění řádku (XML operace):**
   ```python
   table._element.remove(table.rows[row_idx]._element)
   ```

4. **Uložení dokumentu pouze při změnách:**
   ```python
   if total_deleted > 0:
       doc.save(docx_path)
   ```

## Integrace do pipeline

### V `generate_word_protocol_v2()`

**Podmíněné volání podle typu protokolu:**

```python
# POST-PROCESSING: Odstraň prázdné řádky z tabulek
print(f"  → Odstraňuji prázdné řádky z tabulek...")
if protocol_type in ["PP_CAS", "PP_KUSY"]:
    # PP: Odstraň řádky kde vyskyt_min_a, vyskyt_min_b, prumer_min jsou všechny 0
    remove_empty_pp_rows(output_path)
else:
    # LSZ/CFZ: Odstraň řádky kde activity = "0"
    remove_empty_activity_rows(output_path)
```

**Umístění:** Řádek 472-479 v `generate_word_from_two_sources.py`

**Pořadí post-processing kroků:**
1. Zvýraznění vybraných holterů
2. Červené zvýraznění nadlimitních hodnot (force_distribution)
3. **→ Odstranění prázdných řádků** (LSZ nebo PP podle typu)

## Příklady

### Řádek BUDE smazán (PP)

```
| Předklon trupu | Statická | 0 | 0 | 0 | N |
```
✓ Všechny tři hodnoty jsou 0 → SMAŽE SE

### Řádek NEBUDE smazán (PP)

```
| Předklon trupu | Statická | 5 | 0 | 2.5 | N |
```
❌ Alespoň jedna hodnota je nenulová → ZŮSTANE

```
| Záklon trupu | Statická | 0 | 10 | 5 | PP |
```
❌ vyskyt_min_b = 10 (nenulové) → ZŮSTANE

## Testování

### Manuální test PP protokolu

```bash
# 1. Vygeneruj PP Excel s některými nulovými řádky
python main.py
# → Vyber "Nový projekt" → Vyplň data → Vygeneruj PP_CAS

# 2. Vygeneruj Word protokol
python main.py
# → Vyber "Generovat Word Protokol" → Vyber PP Excel → Vygeneruj

# 3. Zkontroluj výstup
# → Otevři vygenerovaný Word dokument
# → Zkontroluj PP tabulky (Trup, Hlava, PHK, LHK, DK, Ostatní)
# → Ověř, že řádky se všemi nulovými hodnotami byly odstraněny
```

### Co sledovat v konzoli

```
Generuji Word protokol pro: PP_CAS
...
  → Odstraňuji prázdné řádky z tabulek...
  → Nalezena PP tabulka pod nadpisem: Trup
  ✓ Smazáno 3 prázdných řádků z PP tabulky
  → Nalezena PP tabulka pod nadpisem: PHK
  ✓ Smazáno 5 prázdných řádků z PP tabulky
  ✓ Celkem smazáno 8 prázdných PP řádků z 2 tabulek
```

## Poznámky k implementaci

1. **Nadpisy tabulek:** Seznam nadpisů v `target_headings` je potřeba upravit podle skutečných PP Word šablon. Aktuálně obsahuje nejčastější varianty.

2. **Case-insensitive match:** Použito `heading.lower() in para_text.lower()` pro robustní matching.

3. **Bezpečnost:** Funkce používá `try-except` pro IndexError, pokud řádek nemá dostatečný počet buněk.

4. **Prázdné hodnoty:** Funkce `is_empty_or_zero()` kontroluje:
   - `"0"`, `"0.0"` (string nula)
   - `""` (prázdný string)
   - `"None"`, `"null"` (textové reprezentace null)
   - `not value` (falsy hodnoty)

## Budoucí vylepšení

1. **Konfigurovatelné nadpisy:** Přesunout `target_headings` do config souboru
2. **Konfigurovatelné sloupce:** Možnost zadat indexy sloupců jako parametr
3. **Debug mode:** Volitelný výpis všech kontrolovaných hodnot před smazáním
4. **Unit testy:** Automatické testy pro různé kombinace hodnot

## Related Files

- `generate_word_from_two_sources.py` - Implementace obou funkcí
- `PP_IMPLEMENTATION_SUMMARY.md` - PP protokol implementace
- `PP_RESULTS_USAGE_EXAMPLES.md` - Příklady použití PP results
- `read_pp_results.py` - Čtení PP Excel dat
