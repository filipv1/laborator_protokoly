# LABORATO5 - Project Summary

## 📋 Přehled Projektu

**LABORATO5** je automatizační aplikace pro laboratoř fyzické zátěže, která eliminuje manuální práci při vyplňování Excel souborů a generování protokolů.

**Verze:** 1.0.0 (Prototyp)
**Datum:** 10.01.2025
**Status:** ✅ Prototyp dokončen - základní funkcionalita implementována

---

## 🎯 Co Aplikace Dělá

### Hlavní Funkcionalita
1. **Uživatelské GUI (Wizard)** - 6 kroků pro zadání dat o měření
2. **Automatické generování projektů** - vytváří strukturovanou složku s Excely
3. **Vyplňování Excel souborů** - automaticky vyplňuje data z formuláře do šablon
4. **Export do JSON** - ukládá všechna data v strukturovaném formátu

### Podporované Excel Formáty
- ✅ **LSZ** - Lokální svalová zátěž (.xlsm s makry)
- ✅ **PP ČAS** - Pracovní polohy - ČAS (.xlsx)
- ✅ **PP KUSY** - Pracovní polohy - KUSY (.xlsx)
- ✅ **CFZ** - Celková fyzická zátěž (.xlsx)

---

## 🏗️ Architektura

### Struktura Projektu
```
app/
├── main.py                      # Entry point
├── gui/
│   ├── wizard.py               # Hlavní wizard (6 stránek)
│   └── pages.py                # QWizardPage třídy
├── core/
│   ├── project_manager.py      # Správa projektů
│   └── excel_filler.py         # Vyplňování Excelů
├── config/
│   └── excel_field_mappings.py # JSON → Excel mapping
├── templates/
│   └── excel/                  # Vzorové šablony (LSZ, PP, CFZ)
├── projects/                   # Vygenerované projekty
└── requirements.txt
```

### Tech Stack
- **PyQt6** - GUI framework
- **openpyxl** - Excel manipulace (zachování maker)
- **Python 3.10+**

### Design Patterns
- **Separation of Concerns** - GUI / Core / Config oddělené
- **Mapping Pattern** - JSON → Excel buňky (konfigurovatelné)
- **Factory Pattern** - ExcelFiller pro různé typy Excelů

---

## ✨ Implementované Features

### 1. GUI Wizard (6 kroků)
- **Krok 0:** Výběr souborů k vygenerování (LSZ, PP ČAS, PP KUSY, CFZ)
- **Krok 1:** Základní údaje o firmě (firma, profese, IČO, datum, ...)
- **Krok 2:** Další údaje (norma, typ výrobku, poloha práce, ...)
- **Krok 3:** Pracovník A (jméno, věk, antropometrie, měřící zařízení, ...)
- **Krok 4:** Pracovník B (optional, stejné údaje jako A)
- **Krok 5:** Závěrečné údaje (měření provedl, poznámky)

### 2. Automatické Generování Projektů
- Vytvoří složku: `projects/{evidencni_cislo}_{firma}/`
- Zkopíruje vybrané Excel šablony
- Automaticky vyplní data z formuláře
- Uloží JSON se všemi daty

### 3. Excel Mappings
Implementováno mapování pro:
- **LSZ:** 22 polí (Pracovník A + B)
- **PP ČAS:** 9 polí (základní údaje + 2 pracovníci)
- **PP KUSY:** 9 polí (totožné s PP ČAS)
- **CFZ:** 12 polí (Pracovník A + B)

### 4. Smart Excel Handling
- Automatická detekce maker (.xlsm vs .xlsx)
- `keep_vba=True` jen pro soubory s makry
- Zachování formátování a vzorců

---

## 📊 Výstup Aplikace

### Příklad Struktury Projektu
```
projects/
  001-2024_BOSAL_CR_sro/
    ├── LSZ_001-2024_BOSAL_CR_sro.xlsm      ✅ Vyplněný daty
    ├── PP_001-2024_BOSAL_CR_sro_CAS.xlsx   ✅ Vyplněný daty
    ├── PP_001-2024_BOSAL_CR_sro_KUSY.xlsx  ✅ Vyplněný daty
    ├── CFZ_001-2024_BOSAL_CR_sro.xlsx      ✅ Vyplněný daty
    └── measurement_data.json                JSON se všemi daty
```

### JSON Struktura
```json
{
    "section0_file_selection": { ... },
    "section1_firma": { ... },
    "section2_additional_data": { ... },
    "section3_worker_a": { ... },
    "section4_worker_b": { ... },
    "section5_final": { ... }
}
```

---

## 🚀 Jak Spustit

### Instalace
```bash
cd app
pip install -r requirements.txt
```

### Spuštění
```bash
python main.py
```

### Použití
1. Spusť aplikaci
2. Vyber, které Excely chceš generovat
3. Postupně vyplň 6 kroků wizardu
4. Klikni na "Dokončit"
5. → Projekt se vygeneruje v `projects/`

---

## 📈 Dosažené Výsledky

### Úspora Času
- **Před:** ~1.5-2 hodiny manuálního vyplňování Excelů
- **Po:** ~5-10 minut vyplnění formuláře
- **Úspora:** ~85-90% času na projekt

### Code Quality
- ✅ Separation of Concerns
- ✅ DRY principle (žádná duplicita)
- ✅ Type hints pro všechny funkce
- ✅ Docstrings (Google style)
- ✅ Modular architecture
- ✅ Best practices (viz CODING_GUIDELINES.md)

### Testing Status
- ✅ Manuální test - všechny 4 typy Excelů fungují
- ⏳ Unit testy - zatím neimplementováno
- ⏳ Integration testy - zatím neimplementováno

---

## 🔧 Technické Detaily

### Excel Mappings
Všechny mappings jsou v `config/excel_field_mappings.py`:
- **Tečková notace** pro JSON cesty (`section3_worker_a.full_name`)
- **Buňkové adresy** pro Excel (`D12`, `K15`)
- **Snadné rozšíření** - přidání nových polí = 1 řádek kódu

### Error Handling
- ✅ Kontrola existence šablon
- ✅ Varování při chybějících listech
- ✅ Graceful handling chybějících dat (vrací None)
- ⏳ User-friendly chybové hlášky - TODO

### Bezpečnost
- ✅ Sanitizace názvů složek (odstranění speciálních znaků)
- ✅ UTF-8 encoding pro JSON
- ✅ Path handling přes pathlib (bezpečné)

---

## 📝 Známé Limitace

### Aktuální Verze (1.0.0)
1. **Data Validation** - openpyxl neuchovává dropdown validace v Excelech
2. **Tabulky** - zatím není implementováno kopírování časového snímku (tabulky s řádky)
3. **Validace vstupů** - minimální (jen základní PyQt validace)
4. **Error messages** - jen v console, ne v GUI
5. **Pokročilé mapování** - zatím jen jednoduché buňky, ne tabulky

### Co Není Implementováno
- ⏳ Generování Word protokolů
- ⏳ Generování PDF
- ⏳ Kopírování časového snímku (tabulka z nahraného XLSX)
- ⏳ Kopírování pohybů/poloh (další tabulky)
- ⏳ Načítání existujících projektů
- ⏳ Editace existujících projektů
- ⏳ Pokročilá validace (kontrola IČO, formát dat, ...)
- ⏳ Progress bar při generování
- ⏳ Multi-language podpora
- ⏳ Unit testy

---

## 🎯 Roadmap (Budoucí Vývoj)

### Fáze 2 - Tabulky a Pokročilé Funkce
- [ ] Implementovat kopírování časového snímku z nahraného XLSX
- [ ] Implementovat kopírování tabulek pohybů/poloh
- [ ] Přidat validaci vstupů
- [ ] Error handling v GUI (QMessageBox)
- [ ] Progress bar při generování

### Fáze 3 - Word Protokoly
- [ ] Vytvořit Word šablony s placeholdery (15 variant)
- [ ] Implementovat WordGenerator
- [ ] Načítat data z vyplněných Excelů
- [ ] Generovat Word protokoly

### Fáze 4 - PDF a Finalizace
- [ ] PDF generování z Word protokolů
- [ ] Načítání existujících projektů
- [ ] Editace projektů
- [ ] Export/Import projektů

### Fáze 5 - Polish & Testing
- [ ] Unit testy (>80% coverage)
- [ ] Integration testy
- [ ] User acceptance testing
- [ ] Dokumentace pro end-users

---

## 👥 Vývoj

**Vyvinuto:** Václav (uživatel) + Claude (AI assistant)
**Datum vývoje:** 10.01.2025
**Počet souborů:** 15+ Python modulů, 4 Excel šablony
**Řádky kódu:** ~800 řádků (bez komentářů a prázdných řádků)

### Použité AI Nástroje
- **Claude Code** - implementace, refaktoring, best practices
- **Ultrathink** - architektonická rozhodnutí, debugging

---

## 📄 Licence

Tento projekt je zatím privátní. Licence bude určena později.

---

## 🔗 Související Dokumenty

- `README.md` - Technická dokumentace
- `CODING_GUIDELINES.md` - Coding standards
- `IMPLEMENTACNI_PLAN.md` - Původní plán implementace
- `GUI_DESIGN_COMPLETE.md` - GUI návrh
- `config/README.md` - Jak přidat nové mappings

---

## 🎉 Závěr

**Prototyp je funkční!** Základní funkcionalita pro automatické generování a vyplňování Excelů funguje správě. Aplikace je připravena pro další rozšíření (Word protokoly, PDF, tabulky, ...).

**Status:** ✅ Ready for testing & expansion
