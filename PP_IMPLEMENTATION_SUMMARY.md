# PP Protocol Implementation - Summary

## ✅ CO BYLO IMPLEMENTOVÁNO

### 1. GUI - Multi-Protocol Support
**Soubor:** `gui/word_protocol_dialog_v2.py`
- ✅ Automatická detekce Excel souborů ve složce (LSZ, PP_CAS, PP_KUSY, CFZ)
- ✅ Dynamické zobrazení protokolů s checkboxy
- ✅ Template výběr pro každý protokol
- ✅ Generování více protokolů najednou

### 2. PP Excel Reader
**Soubor:** `read_pp_results.py`
- ✅ Načítá data z listu "Průměr"
- ✅ Mapuje 6 sekcí těla (trup, hlava_krk, phk, lhk, dk, ostatni)
- ✅ Celkem 52 řádků (42 poloh + metadata)
- ✅ Vytváří `pp_results.json` ve structure (číselné klíče jako stringy, stejně jako LSZ):
```json
{
  "excel_type": "PP_CAS",
  "worker_count": 2,
  "what_is_evaluated": "cas",
  "trup": {
    "1": {"nazev_polohy": "...", "typ_svalove_prace": "...", ...},
    "2": {...},
    ...
  },
  "hlava_krk": {
    "1": {...},
    ...
  },
  "phk": {...},
  "lhk": {...},
  "dk": {...},
  "ostatni": {...}
}
```

### 3. Pipeline - Protocol Detection
**Soubor:** `core/word_protocol_pipeline.py`
- ✅ Nová metoda `_detect_protocol()` - detekuje LSZ/PP/CFZ z názvu souboru
- ✅ Dispatcher pro správný reader:
  - LSZ → `read_lsz_results()` → `lsz_results.json`
  - PP → `read_pp_results()` → `pp_results.json`
- ✅ Předává `protocol_type` do Word generátoru

### 4. Word Generator - Protocol Support
**Soubor:** `generate_word_from_two_sources.py`
- ✅ Nový parametr `protocol_type` (default="LSZ")
- ✅ Předává `protocol_type` do `generate_conditional_texts()`

### 5. Text Generator - PP Stub
**Soubor:** `core/text_generator.py`
- ✅ Nový parametr `protocol_type` (default="LSZ")
- ✅ PP stub implementace:
  - Generuje `prvni_text_podminka_pocetdni` (generická podmínka)
  - Ostatní PP podmínky: placeholder pro budoucí implementaci

---

## 🧪 JAK TESTOVAT

### Testovací Data
**Projekt:** `projects/_fjfjfe`
- ✅ LSZ__fjfjfe.xlsm
- ✅ PP__fjfjfe_CAS.xlsx ← **TENTO POUŽIJ PRO TEST**
- ✅ PP__fjfjfe_KUSY.xlsx
- ✅ CFZ__fjfjfe.xlsx

**PP Template:** `sample_protocols/Autorizované protokoly pro MUŽE/PP_XX_Firma_Pozice.docx`

### Kroky testování:

1. **Spusť aplikaci:**
   ```bash
   python main.py
   ```

2. **Klikni "📝 GENEROVAT WORD PROTOKOL"**

3. **Vyber složku projektu:**
   - Navigate to: `projects/_fjfjfe`
   - Klikni "Vybrat složku"

4. **Měl bys vidět 4 protokoly:**
   ```
   ☑ LSZ - Lokální svalová zátěž
   ☑ PP - Pracovní polohy (ČAS)    ← TENTO ZAŠKRTNI
   ☐ PP - Pracovní polohy (KUSY)
   ☐ CFZ - Celková fyzická zátěž
   ```

5. **Vyber jen PP ČAS:**
   - Zaškrtni checkbox u "PP - Pracovní polohy (ČAS)"
   - Odškrtni ostatní

6. **Zkontroluj template:**
   - Template by měl být: `PP_XX_Firma_Pozice.docx`

7. **Klikni "Generovat"**

8. **Co se stane:**
   - Pipeline detekuje `PP_CAS` z názvu souboru
   - Spustí `read_pp_results.py` → vytvoří `pp_results.json`
   - Vygeneruje Word protokol s placeholdery z `measurement_data.json`

---

## 📊 CO FUNGUJE

### End-to-End Flow
```
GUI (dialog V2)
  ↓ (vyber PP_CAS Excel)
  ↓
Pipeline (_detect_protocol)
  ↓ (detekuje "PP_CAS")
  ↓
read_pp_results.py
  ↓ (načte 52 řádků z Průměr)
  ↓
pp_results.json (uložen do project folder)
  ↓
generate_word_from_two_sources.py
  ↓ (protocol_type="PP_CAS")
  ↓
text_generator (PP stub)
  ↓ (vygeneruje prvni_text_podminka)
  ↓
Word Protocol (PP_XX_Firma_Pozice.docx)
  ↓
✓ PP__fjfjfe_CAS_protokol.docx
```

---

## 🔍 CO ZKONTROLOVAT V OUTPUTS

### 1. Console Output (měl bys vidět):
```
Detekovan protocol: PP_CAS
Nacitam data z Excel: PP__fjfjfe_CAS.xlsx
Pouzivam list: Prumer
  Nacitam sekci: trup (radky 4-14)
    OK Nacteno 11 polozek
  Nacitam sekci: hlava_krk (radky 16-25)
    OK Nacteno 10 polozek
  ... (další sekce)
OK pp_results.json vytvoren
Generuji Word protokol pro: PP_CAS
Generuji PP podminkove texty (stub)
OK Word protokol vygenerovan
```

### 2. Soubory ve složce `projects/_fjfjfe/`:
```
✓ measurement_data.json (existující)
✓ pp_results.json (NOVÝ - vygenerovaný)
✓ PP__fjfjfe_CAS_protokol.docx (NOVÝ - Word výstup)
```

### 3. Word Protokol (PP__fjfjfe_CAS_protokol.docx):
**Měl by obsahovat:**
- ✅ Základní placeholdery z `measurement_data.json` (firma, IČO, datum, ...)
- ✅ `prvni_text_podminka_pocetdni` (generovaný text o počtu dnů/pracovníků)
- ✅ Tabulky s daty z `pp_results.json` (pokud jsou v template)
- ⚠️ PP-specific podmínky budou "TODO" (stub implementace)

---

## ⚠️ ZNÁMÉ LIMITACE (PRO SOUČASNÝ TEST)

1. **PP conditional texts jsou stub:**
   - Pouze `prvni_text_podminka_pocetdni` funguje
   - Ostatní PP podmínky vrací placeholder
   - **Řešení:** Implementovat `text_generator_pp.py` později

2. **Template může obsahovat LSZ placeholdery:**
   - Pokud template obsahuje LSZ-specific placeholdery (např. `Fmax_Phk_Extenzor`), zůstanou prázdné
   - **Řešení:** Aktualizovat template s PP-specific placeholdery

3. **CFZ není implementován:**
   - Pokud zkusíš vybrat CFZ, pipeline vrátí error
   - **Řešení:** Implementovat `read_cfz_results.py` později

---

## 🎯 OČEKÁVANÝ VÝSLEDEK TESTU

**Pokud vše funguje:**
1. ✅ PP protokol se vygeneruje bez chyb
2. ✅ `pp_results.json` obsahuje 52 řádků dat
3. ✅ Word dokument obsahuje základní data z `measurement_data.json`
4. ✅ `prvni_text_podminka_pocetdni` obsahuje správný text

**Pokud selže:**
- Zkontroluj console output pro error traceback
- Zkontroluj, jestli všechny soubory existují
- Ověř, že PP template existuje na správné cestě

---

## 🔜 DALŠÍ KROKY (PO ÚSPĚŠNÉM TESTU)

1. **Implementovat PP conditional texts:**
   - Vytvořit `text_generator_pp.py` s PP-specific podmínkami
   - Integrovat do `generate_conditional_texts()` dispatcher

2. **Aktualizovat PP template:**
   - Přidat PP-specific placeholdery
   - Přidat tabulky z `pp_results.json`
   - Přidat PP podmínkové texty

3. **Vytvořit PP dokumentaci:**
   - Zdokumentovat PP results JSON strukturu
   - Zdokumentovat PP placeholdery v template
   - Vytvořit příklady PP podmínkových textů

---

## 📝 NOTES

- Celý flow je **zpětně kompatibilní** - LSZ protokoly fungují beze změn
- Architecture je **extensible** - snadné přidání CFZ protokolu
- Code je **clean** - separace LSZ/PP/CFZ logiky
- Vše je **type-safe** - s Literal type hints pro protocol types
