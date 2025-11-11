# Flexibilní parsování tabulek z Word dokumentů

## 📋 Přehled změn

**Datum:** 2025-11-10
**Soubor:** `core/docx_parser.py`
**Verze:** 2.0.0 - Flexibilní načítání

## 🎯 Problém

Původní implementace vyžadovala **přesně 4 sloupce** v tabulce časového snímku:
- Č. (číslo)
- Činnost
- Čas (min)
- Počet kusů

**Co se stávalo když sloupec chyběl:**
- ❌ Celý řádek se přeskočil (`if len(cells) < 4: continue`)
- ❌ Tabulka se vůbec nenačetla
- ❌ Uživatel nemohl pokračovat ve wizardu

**Reálné případy:**
- Uživatel nemá v popisu práce sloupec "Počet kusů"
- Uživatel nemá sloupec "Čas (min)"
- Různá pořadí sloupců
- Různé názvy sloupců (Činnost vs Popis práce)

---

## ✅ Řešení

### Nová funkcionalita:
1. **Fuzzy matching názvů sloupců** - Rozpozná různé varianty názvů
2. **Flexibilní načítání** - Funguje i když některé sloupce chybí
3. **Artificiální doplnění** - Chybějící sloupce → `None` hodnoty
4. **Debug výpisy** - Uživatel vidí co bylo detekováno
5. **Fallback na default pořadí** - Pokud header nelze detekovat

### Podporované varianty názvů:

**Činnost:**
- "činnost", "operace", "operation", "popis", "práce", "aktivita", "cinnost"

**Čas:**
- "čas", "time", "min", "minut", "trvání", "doba", "cas"

**Počet kusů:**
- "počet", "kusy", "pieces", "ks", "count", "množství", "pocet", "mnozstvi"

**Číslo:**
- "č.", "číslo", "number", "#", "pořadí", "por.", "c."

---

## 🔧 Implementace

### Nové helper funkce:

#### 1. `_normalize_column_name(name: str)`
Normalizuje název sloupce pro matching:
- Lowercase
- Odstraní diakritiku (č→c, š→s)
- Odstraní speciální znaky
- Redukuje mezery

```python
"Čas (min)" → "cas min"
"Popis práce" → "popis prace"
```

#### 2. `_detect_column_mapping(header_cells)`
Detekuje mapování `column_type → column_index`:
- Fuzzy matching podle COLUMN_PATTERNS
- Prioritní pořadí: operation > time_min > pieces_count > number
- Tracking už přiřazených sloupců (žádné duplikáty)

```python
Header: ["Č.", "Činnost", "Čas (min)"]
→ {
    "number": 0,
    "operation": 1,
    "time_min": 2,
    "pieces_count": None  # Chybí
}
```

#### 3. `_safe_get_cell_value(cells, column_index)`
Bezpečně získá hodnotu buňky:
- Vrací `None` pokud index neexistuje
- Vrací `None` pokud `column_index` je `None`

---

## 📊 Testované scénáře

### ✅ Scénář 1: Plná tabulka (4 sloupce)
```
Č. | Činnost | Čas (min) | Počet kusů
1  | Montáž  | 45        | 120
```
**Výsledek:** Všechny hodnoty načteny ✓

---

### ✅ Scénář 2: Bez sloupce "Počet kusů"
```
Č. | Činnost | Čas (min)
1  | Montáž  | 45
```
**Výsledek:**
```python
{
  "operation": "Montáž",
  "time_min": 45,
  "pieces_count": None  # ✓ Artificiálně doplněno
}
```

**Použití:**
- LSZ: Norma se nevypočítá (OK - není potřeba)
- CFZ/PP: Nepotřebují pieces_count

---

### ✅ Scénář 3: Bez sloupce "Čas"
```
Č. | Činnost | Počet kusů
1  | Montáž  | 120
```
**Výsledek:**
```python
{
  "operation": "Montáž",
  "time_min": None,  # ✓ Artificiálně doplněno
  "pieces_count": 120
}
```

**Použití:**
- Excel: time_min buňka zůstane prázdná (editovatelná v GUI)

---

### ✅ Scénář 4: Jen činnosti
```
Č. | Činnost
1  | Montáž
```
**Výsledek:**
```python
{
  "operation": "Montáž",
  "time_min": None,
  "pieces_count": None
}
```

---

### ✅ Scénář 5: Jiné pořadí sloupců
```
Činnost | Čas (min) | Č.
Montáž  | 45        | 1
```
**Výsledek:** ✓ Fuzzy matching detekuje správně bez ohledu na pořadí

---

### ✅ Scénář 6: Různé názvy sloupců
```
Popis práce | Doba [min] | Kusy
Montáž      | 45         | 120
```
**Výsledek:** ✓ Fuzzy matching rozpozná varianty názvů

---

### ✅ Scénář 7: Čísla jako text (edge case)
```
Č. | Činnost | Čas (min)
1  | Montáž  | třicet    ← text místo čísla
```
**Výsledek:** `time_min: None` (fallback funguje) ✓

---

## 🛡️ Backward Compatibility

### ✅ Zachováno:
1. **JSON struktura** - Identická jako dřív
2. **Existující projekty** - Budou fungovat bez změn
3. **Excel export** - `TableCopier` už správně zachází s `None`
4. **GUI** - Prázdné buňky budou editovatelné

### Test na 27 existujících projektech:
```
✓ Všechny projekty mají správnou JSON strukturu
✓ Žádné breaking changes
```

---

## 🔍 Debug výpisy

### Příklad konzole výstupu:
```
✓ Detekované sloupce v časovém snímku:
   • Činnost: sloupec 1
   • Čas: sloupec 2
   ⚠ Počet kusů: chybí (bude None)
✓ Načteno 3 řádků z časového snímku
```

### Když header chybí:
```
⚠ Varování: Nepodařilo se detekovat názvy sloupců, používám default pořadí
   Předpokládám: [Č., Činnost, Čas, Počet kusů]
```

### Když činnost chybí:
```
❌ CHYBA: Sloupec 'Činnost' nebyl nalezen! Tabulka se nenačte.
```

---

## ⚙️ Validační pravidla

### MUSÍ existovat:
- **operation** (Činnost) - řádek bez činnosti se přeskočí

### VOLITELNÉ:
- **number** (Č.) - pokud chybí → prázdný string
- **time_min** (Čas) - pokud chybí → `None`
- **pieces_count** (Počet kusů) - pokud chybí → `None`

### Přeskočení řádku:
- Řádek se přeskočí POUZE pokud `operation` je prázdné/None
- Řádek "Celkem" se detekuje a ukládá do `total`

---

## 📦 Změněné soubory

### `core/docx_parser.py`
**Přidáno:**
- `COLUMN_PATTERNS` - Konstantní patterns pro matching
- `_normalize_column_name()` - Normalizace názvů
- `_detect_column_mapping()` - Detekce sloupců
- `_safe_get_cell_value()` - Bezpečné čtení buněk

**Upraveno:**
- `parse_time_schedule_table()` - Kompletní refaktoring
  - Header detection
  - Flexible column mapping
  - Debug výpisy
  - Fallback na default

**Nezměněno:**
- `_parse_number()` - Zůstává stejné (s fallback na None)
- `_get_empty_time_schedule()` - Zůstává stejné
- Výstupní JSON struktura

---

## 🧪 Testování

### Automatické testy:
```bash
# Vytvoří 7 testovacích Word dokumentů a otestuje všechny scénáře
python test_flexible_docx_parsing.py

# Otestuje backward compatibility s existujícími projekty
python test_backward_compatibility.py
```

### Testovací dokumenty:
Vytvořeny v `test_docx_flexible/`:
- `test_full_table.docx` - Plná tabulka (4 sloupce)
- `test_no_pieces.docx` - Bez počtu kusů
- `test_no_time.docx` - Bez času
- `test_operations_only.docx` - Jen činnosti
- `test_different_order.docx` - Jiné pořadí sloupců
- `test_different_names.docx` - Různé názvy sloupců
- `test_numbers_as_text.docx` - Edge case s textem místo čísel

---

## 🚀 Použití v GUI

### Workflow:
1. Uživatel nahraje Word dokument v wizardu
2. `DocxParser.parse_time_schedule_table()` načte tabulku
3. Debug výpisy zobrazí co bylo detekováno
4. Data se uloží do `measurement_data.json`
5. Excel soubory se vygenerují s None hodnotami tam kde sloupec chybí
6. Uživatel může hodnoty doplnit v GUI (buňky jsou editovatelné)

### Výhody pro uživatele:
- ✅ Nemusí mít všechny sloupce v tabulce
- ✅ Může používat různé názvy sloupců
- ✅ Může mít sloupce v libovolném pořadí
- ✅ Vidí co bylo detekováno (debug výpisy)
- ✅ Může doplnit chybějící hodnoty v GUI

---

## 📚 Příklady použití

### Před (nefungovalo):
```python
# Word dokument s 3 sloupci (bez Počet kusů)
table = [
    ["Č.", "Činnost", "Čas (min)"],
    ["1", "Montáž", "45"]
]
result = DocxParser.parse_time_schedule_table(docx_path)
# → Řádek se přeskočil (len(cells) < 4)
# → line1 = {"operation": "", "time_min": None, ...}
```

### Po (funguje):
```python
# Stejný Word dokument
result = DocxParser.parse_time_schedule_table(docx_path)
# → Debug: "✓ Činnost: sloupec 1"
# → Debug: "✓ Čas: sloupec 2"
# → Debug: "⚠ Počet kusů: chybí (bude None)"
# → line1 = {"operation": "Montáž", "time_min": 45, "pieces_count": None}
```

---

## 🔮 Budoucí vylepšení

### Možná rozšíření:
1. **UI warning** - QMessageBox když sloupec chybí
2. **Konfigurovatelné patterns** - Uživatel může přidat vlastní názvy sloupců
3. **Multi-table support** - Načtení více tabulek z jednoho dokumentu
4. **Auto-fill** - Automatické doplnění chybějících hodnot z předchozích řádků

---

## 🐛 Known Issues

### Žádné známé problémy

---

## ✍️ Autor

**Implementace:** Claude Code + Filip Václavík
**Datum:** 2025-11-10
**Testováno:** 7 scénářů + 27 existujících projektů
**Status:** ✅ Production ready

---

## 📝 Changelog

### v2.0.1 (2025-11-10) - HOTFIX
- 🔧 **OPRAVA**: Common prefix matching pro české skloňování
- ✅ Problém: "operaci" vs "operace" se nematchoval kvůli stejné délce
- ✅ Řešení: Porovnání common prefix (bez posledních 2 znaků = koncovky)
- ✅ Testováno na 3 reálných souborech s názvem "Rozpis pracovních operací"
- ✅ Všechny 3 soubory úspěšně načteny
- ✅ Backward compatibility zachována (27 projektů)

### v2.0.0 (2025-11-10)
- ✅ Přidán fuzzy matching názvů sloupců
- ✅ Flexibilní načítání s chybějícími sloupci
- ✅ Debug výpisy pro lepší UX
- ✅ Fallback na default pořadí
- ✅ Backward compatibility zachována
- ✅ 7 testovacích scénářů
- ✅ Testováno na 27 existujících projektech
