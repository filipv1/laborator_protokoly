# NEXT STEPS ANALYSIS - LABORATO5

**Datum analýzy:** 10.01.2025
**Aktuální verze:** 1.0.0 (Prototyp)
**Status:** ✅ Základní funkcionalita funguje, ale chybí kritické features

---

## 🔍 Analýza Současného Stavu

### ✅ Co Funguje
1. **GUI Wizard** - 6 kroků, všechna pole, přepínání mezi stránkami
2. **Projektová struktura** - automatické vytváření složek, sanitizace názvů
3. **Excel vyplňování** - 4 typy (LSZ, PP ČAS, PP KUSY, CFZ) s 52 poli celkem
4. **JSON export** - strukturované uložení všech dat
5. **Smart Excel handling** - keep_vba jen pro .xlsm soubory
6. **Code quality** - modulární, DRY, type hints, docstrings

### ❌ Co NEFUNGUJE / Chybí

#### 🔴 KRITICKÉ MEZERY:
1. **Nahrávání souborů** - uživatel nemůže nahrát časový snímek, pohyby, polohy
2. **Kopírování tabulek** - časový snímek (hlavní tabulka!) se nekopíruje
3. **Validace vstupů** - minimální, aplikace může zhavarovatna špatných datech
4. **Error handling v GUI** - chyby jen v console, ne user-friendly

#### 🟡 DŮLEŽITÉ MEZERY:
5. **Word protokoly** - vůbec neimplementováno (15 šablon + generování)
6. **PDF export** - neimplementováno
7. **Načítání projektů** - nelze otevřít a editovat existující projekt
8. **Progress indikátory** - uživatel neví, co se děje

#### 🟢 NICE TO HAVE:
9. **Unit testy** - žádné testy
10. **Pokročilá validace** - IČO formát, kontrola datumů, rozsahy hodnot
11. **Logging** - jen print(), ne strukturovaný logging
12. **Multi-projekt management** - nelze spravovat více projektů najednou

---

## 🎯 PRIORITIZOVANÉ NEXT STEPS

### 🔴 PRIORITA 1 - KRITICKÉ (Bez toho aplikace není použitelná!)

#### 1.1. Nahrávání Souborů v GUI
**Proč kritické:** Podle původního návrhu (GUI_DESIGN_COMPLETE.md) má uživatel nahrát:
- Časový snímek (.xlsx/.xls)
- Počítání pohybů (.xlsx)
- Pracovní polohy (.xlsx)

**Implementace:**
- Přidat do wizardu novou page (nebo rozšířit stávající)
- `QFileDialog` pro výběr souborů
- Validace nahraných souborů (správná struktura, požadované sloupce)
- Uložení cest do JSON

**Odhadovaná doba:** 2-3 hodiny

**Dopady:**
- Umožní uživateli dodat data, která nejsou v GUI
- Nutnost pro next step (kopírování tabulek)

---

#### 1.2. Kopírování Časového Snímku
**Proč kritické:** Časový snímek je **HLAVNÍ TABULKA** v protokolech! Bez něj jsou Excely neúplné.

**Co je časový snímek:**
- Tabulka s řádky činností (např. "Obsluha stroje", "Přestávka", ...)
- Obsahuje sloupce: Činnost, Čas začátku, Čas konce, Trvání, Počet kusů, ...
- Desítky až stovky řádků

**Implementace:**
```python
# Nový modul: core/table_copier.py

class TableCopier:
    def copy_time_snapshot(self, source_xlsx: Path, target_workbooks: Dict[str, Path]):
        """
        Zkopíruje časový snímek z nahraného XLSX do všech generovaných Excelů.

        Args:
            source_xlsx: Cesta k nahranému časovému snímku
            target_workbooks: {"lsz": Path, "cfz": Path, ...}
        """
        # 1. Načti data z source_xlsx
        # 2. Pro každý target Excel:
        #    - Najdi správný list
        #    - Najdi startovní řádek (kde začíná tabulka)
        #    - Zkopíruj řádek po řádku
        #    - Zachovej formátování (pokud možno)
```

**Challenges:**
- Různé Excely mají časový snímek na různých místech
- Různý formát tabulek (počet sloupců, názvy)
- Musíme zachovat vzorce (pokud jsou)

**Odhadovaná doba:** 4-6 hodin

**Dopady:**
- Excely budou kompletní a použitelné
- Hlavní funkcionalita aplikace

---

#### 1.3. Validace Vstupů
**Proč kritické:** Špatná data = aplikace havaruje nebo generuje neplatné Excely.

**Co validovat:**
- **Povinná pole:** firma, profese, evidenční číslo, jméno pracovníka A
- **Formáty:** datum, IČO (8 číslic), čísla (věk, výška, hmotnost)
- **Rozsahy:** věk (18-99), výška (100-250 cm), hmotnost (30-200 kg)
- **Logika:** pokud je pracovník B, musí být vyplněno jméno

**Implementace:**
- Přidat `core/validators.py`
- Přidat `registerField()` a `validatePage()` v QWizardPage
- User-friendly error messages v GUI

**Odhadovaná doba:** 3-4 hodiny

---

#### 1.4. Error Handling v GUI
**Proč kritické:** Uživatel nerozumí console outputu. Potřebuje vidět chyby v GUI.

**Implementace:**
- Nahradit všechny `print()` v core modulech za logging
- Přidat `QMessageBox` pro:
  - Úspěšné dokončení (s cestou k projektu)
  - Chyby (chybějící šablona, špatná data, ...)
  - Varování (Data Validation bude ztracena, ...)
- Progress dialog během generování

**Odhadovaná doba:** 2-3 hodiny

---

### 🟡 PRIORITA 2 - VELMI DŮLEŽITÉ (Pro plnou funkcionalitu)

#### 2.1. Kopírování Tabulek Pohybů a Poloh
**Podobné jako časový snímek, ale pro další tabulky.**

**Implementace:**
- Rozšířit `TableCopier` o další metody
- `copy_movements()` - pohyby pracovníků
- `copy_positions()` - pracovní polohy

**Odhadovaná doba:** 4-5 hodin

---

#### 2.2. Progress Bar / Indikátory
**Proč důležité:** Generování Excelů trvá několik sekund. Uživatel potřebuje feedback.

**Implementace:**
- `QProgressDialog` během generování
- Steps: "Vytváření složky...", "Kopírování LSZ...", "Vyplňování dat...", "Hotovo!"

**Odhadovaná doba:** 1-2 hodiny

---

#### 2.3. Načítání Existujících Projektů
**Proč důležité:** Uživatel může chtít editovat projekt (opravit překlep, přidat poznámku).

**Implementace:**
- Tlačítko "Otevřít existující projekt" v main menu
- Načíst `measurement_data.json`
- Předvyplnit wizard daty z JSONu
- Možnost upravit a znovu generovat Excely

**Odhadovaná doba:** 3-4 hodiny

---

### 🟢 PRIORITA 3 - DŮLEŽITÉ (Rozšíření funkcionality)

#### 3.1. Word Šablony (15 variant)
**Největší úkol!** Podle IMPLEMENTACNI_PLAN.md: 10-15 hodin práce.

**Co je potřeba:**
1. Vytvořit 15 Word šablon s placeholdery:
   - CFZ: muž/žena × 1/2 pracovníci = 5 variant
   - LSZ: muž/žena × 1/2 pracovníci = 5 variant
   - PP: muž/žena × 1/2 pracovníci = 5 variant

2. Použít **docxtpl** (Jinja2 syntax):
   ```
   Firma: {{firma.nazev}}
   Profese: {{profese}}

   {% for row in casovy_snimek %}
   {{row.cinnost}} | {{row.cas}} | {{row.kusy}}
   {% endfor %}
   ```

**Výzva:** Získat vzorové protokoly od laboratoře!

**Odhadovaná doba:** 10-15 hodin

---

#### 3.2. Word Generování
**Implementace:**
```python
# Nový modul: core/word_generator.py

class WordGenerator:
    def generate_protocol(self, protocol_type: str, project_data: dict, excel_data: dict):
        """
        Vygeneruje Word protokol z šablony.

        Args:
            protocol_type: "CFZ", "LSZ", "PP"
            project_data: Data z measurement_data.json
            excel_data: Data načtená z vyplněného Excelu (výsledky měření)
        """
        # 1. Vyber správnou šablonu (word_template_selector.py už máme!)
        # 2. Načti Excel data (výsledky, kategorie)
        # 3. Kombinuj project_data + excel_data
        # 4. Renderuj pomocí docxtpl
        # 5. Ulož Word protokol
```

**Odhadovaná doba:** 5-7 hodin

---

#### 3.3. PDF Export
**Implementace:**
- Použít **python-docx2pdf** nebo **LibreOffice headless**
- Konvertovat vygenerované Word protokoly na PDF

**Odhadovaná doba:** 2-3 hodiny

---

### 🔵 PRIORITA 4 - NICE TO HAVE (Polish & Quality)

#### 4.1. Unit Testy
**Moduly k testování:**
- `excel_filler.py` - testovat vyplňování buněk
- `project_manager.py` - testovat vytváření projektů
- `validators.py` - testovat validační logiku
- `table_copier.py` - testovat kopírování tabulek

**Cíl:** 80%+ code coverage

**Odhadovaná doba:** 8-10 hodin

---

#### 4.2. Pokročilá Validace
- IČO: kontrola formátu (8 číslic) + kontrolní součet
- Datum: logické rozsahy (ne budoucnost, ne příliš starý)
- Cross-field validace (např. datum narození vs. věk)

**Odhadovaná doba:** 2-3 hodiny

---

#### 4.3. Logging System
**Nahradit všechny print() za strukturovaný logging:**
```python
import logging

logger = logging.getLogger(__name__)
logger.info("Projekt vytvořen: {path}")
logger.warning("Data Validation bude ztracena")
logger.error("Chyba při vyplňování: {error}")
```

**Odhadovaná doba:** 2-3 hodiny

---

## 📊 Časový Odhad

| Priorita | Úkoly | Čas |
|----------|-------|-----|
| 🔴 P1 - Kritické | Upload souborů, kopírování tabulek, validace, error handling | 11-16h |
| 🟡 P2 - Velmi důležité | Pohyby/polohy, progress bar, načítání projektů | 8-11h |
| 🟢 P3 - Důležité | Word šablony, generování, PDF | 17-25h |
| 🔵 P4 - Nice to have | Testy, pokročilá validace, logging | 12-16h |
| **CELKEM** | | **48-68 hodin** |

**Realistický odhad:** 6-9 pracovních dnů (full-time)

---

## 🎯 DOPORUČENÉ POŘADÍ IMPLEMENTACE

### Sprint 1 (Kritické) - 2-3 dny
1. ✅ Nahrávání souborů v GUI
2. ✅ Kopírování časového snímku
3. ✅ Základní validace vstupů
4. ✅ Error handling v GUI

**Výsledek:** Aplikace je plně použitelná pro generování Excelů.

---

### Sprint 2 (Důležité) - 2-3 dny
5. ✅ Kopírování pohybů a poloh
6. ✅ Progress bar
7. ✅ Načítání existujících projektů

**Výsledek:** Aplikace je uživatelsky přívětivá a flexibilní.

---

### Sprint 3 (Word protokoly) - 3-4 dny
8. ✅ Vytvoření 15 Word šablon (NEJDELŠÍ!)
9. ✅ Word generování
10. ✅ PDF export

**Výsledek:** Kompletní workflow od zadání dat po finální PDF protokoly.

---

### Sprint 4 (Quality) - 2-3 dny
11. ✅ Unit testy (>80% coverage)
12. ✅ Pokročilá validace
13. ✅ Logging system
14. ✅ User acceptance testing

**Výsledek:** Production-ready aplikace.

---

## 🚨 Kritická Rozhodnutí

### 1. Kde vzít Word šablony?
**Problém:** Potřebuješ 15 vzorových Word protokolů od laboratoře.

**Řešení:**
- **Varianta A:** Laboratoř ti poskytne všechny varianty → Jen přidáš placeholdery
- **Varianta B:** Máš jen 1 protokol → Musíš vytvořit 14 dalších variant ručně
- **Varianta C:** Použiješ AI (ChatGPT/Claude) na generování variant

**Doporučení:** Zjisti, jaké protokoly laboratoř má. Bez nich nemůžeš pokračovat na Word generování.

---

### 2. Struktura časového snímku
**Problém:** Každý Excel může očekávat jiný formát časového snímku.

**Řešení:**
- **Varianta A:** Definovat jednotný formát → uživatel musí nahrát soubor v tomto formátu
- **Varianta B:** Podporovat více formátů → složitější parsování
- **Varianta C:** Nechat uživatele ručně mapovat sloupce v GUI

**Doporučení:** Začni s Varianta A (jednotný formát). Později rozšířit na B.

---

### 3. Data Validation Warning
**Problém:** openpyxl odstraní Data Validation (dropdown menu) z Excelů.

**Řešení:**
- Informovat uživatele (QMessageBox při prvním spuštění)
- Dokumentovat v README
- Případně přidat checkbox "Zobrazit toto varování příště"

**Není řešitelné** - omezení openpyxl knihovny.

---

## 💡 Architektorická Doporučení

### Nové Moduly (které budou potřeba):

```
app/
├── core/
│   ├── table_copier.py        # Kopírování tabulek z XLSX
│   ├── word_generator.py      # Generování Word protokolů
│   ├── pdf_exporter.py        # PDF export
│   ├── validators.py          # Validace vstupů
│   └── project_loader.py      # Načítání existujících projektů
├── gui/
│   ├── upload_page.py         # Stránka pro upload souborů
│   └── dialogs.py             # Custom dialogy (error, progress, ...)
├── templates/
│   └── word/                  # 15 Word šablon
└── tests/
    ├── test_excel_filler.py
    ├── test_table_copier.py
    └── test_validators.py
```

### Config pro Tabulky:
```python
# config/table_mappings.py

TABLE_MAPPINGS = {
    "LSZ": {
        "time_snapshot": {
            "sheet": "Časový snímek",
            "start_row": 25,  # Kde začíná tabulka
            "columns": ["Činnost", "Čas začátku", "Čas konce", "Trvání"]
        }
    },
    "CFZ": {
        "time_snapshot": {
            "sheet": "Časový snímek A+B",
            "start_row": 30,
            ...
        }
    }
}
```

---

## 🎯 Závěr a Akční Plán

### IMMEDIATE NEXT STEP (Zítra):
**Rozhodnutí #1:** Potřebuješ od laboratoře:
- ✅ Vzorové Word protokoly (všechny varianty, pokud existují)
- ✅ Vyplněný časový snímek (příklad XLSX souboru)
- ✅ Vyplněné tabulky pohybů/poloh
- ✅ Potvrzení, že formát Excelů je správný

**Bez těchto dat nemůžeš pokračovat na Sprint 1!**

---

### Pokud máš data → START SPRINT 1:
1. Implementuj nahrávání souborů (2-3h)
2. Implementuj kopírování časového snímku (4-6h)
3. Přidej validaci (3-4h)
4. Přidej error handling (2-3h)

**= 11-16 hodin = cca 2-3 dny práce**

---

### Pokud nemáš data → Mezitím:
- Vylepši dokumentaci
- Přidej unit testy pro stávající kód
- Refaktoruj (pokud je co)
- Zjisti požadavky na Word protokoly

---

## 📈 Metriky Úspěchu

### Po Sprint 1:
- ✅ Aplikace generuje **kompletní** Excely s časovým snímkem
- ✅ Uživatel vidí chyby v GUI (ne v console)
- ✅ Validace chrání před špatnými daty

### Po Sprint 2:
- ✅ Uživatel může načíst a editovat projekty
- ✅ Progress bar poskytuje feedback
- ✅ Všechny tabulky (časový snímek, pohyby, polohy) se kopírují

### Po Sprint 3:
- ✅ Aplikace generuje Word protokoly
- ✅ Aplikace exportuje PDF
- ✅ **KOMPLETNÍ WORKFLOW**: GUI → Excel → Word → PDF

### Po Sprint 4:
- ✅ 80%+ test coverage
- ✅ Zero critical bugs
- ✅ Production-ready

---

**Status:** 📊 Analýza dokončena - čeká na rozhodnutí o next steps

**Autor:** Claude + Václav
**Datum:** 10.01.2025
