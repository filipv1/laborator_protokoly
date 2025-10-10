# LABORATO5 - Aplikace

## Struktura projektu

```
app/
├── main.py              # Entry point (spustitelný soubor)
├── gui/
│   ├── __init__.py     # Package init (exportuje MeasurementGUI)
│   ├── wizard.py       # Hlavní QWizard třída
│   └── pages.py        # Všechny QWizardPage třídy (6 stránek)
├── core/
│   ├── __init__.py     # Core package init
│   ├── project_manager.py  # Správa projektů
│   └── excel_filler.py     # Vyplňování dat do Excelů
├── config/
│   ├── __init__.py     # Config package init
│   └── excel_field_mappings.py  # Mapování JSON → Excel buňky
├── templates/
│   └── excel/          # Vzorové Excel soubory (LSZ, PP, CFZ)
├── projects/           # Vygenerované projekty (složky s Excely)
├── requirements.txt     # Python závislosti
└── README.md           # Tento soubor
```

## Instalace

```bash
cd C:\Users\vaclavik\Desktop\laborato5\app
pip install -r requirements.txt
```

## Spuštění

```bash
python main.py
```

## Moduly

### `main.py`
Entry point aplikace. Vytvoří QApplication a zobrazí hlavní wizard.

### `gui/wizard.py`
Obsahuje hlavní třídu `MeasurementGUI` (QWizard), která spojuje všechny stránky.

**Funkcionalita:**
- Při kliknutí na "Dokončit" automaticky vygeneruje `measurement_data.json`
- JSON obsahuje všechna vyplněná data z formuláře
- Klíče v angličtině bez diakritiky, hodnoty v češtině

### `gui/pages.py`
Obsahuje všechny QWizardPage třídy:
- `Page0_VyberSouboru` - Výběr Excel souborů k vygenerování (LSZ, PP čas, PP kusy, CFZ)
- `Page1_Firma` - Základní údaje o firmě
- `Page2_DalsiUdaje` - Další údaje o měření
- `Page3_PracovnikA` - Údaje o pracovníkovi A
- `Page4_PracovnikB` - Údaje o pracovníkovi B (optional)
- `Page5_Zaverecne` - Závěrečné údaje

### `measurement_data_example.json`
Příklad struktury výstupního JSON souboru.

### `core/project_manager.py`
Obsahuje `ProjectManager` třídu pro správu projektů.

**Funkcionalita:**
- Vytváření složek projektů podle evidenčního čísla a firmy
- Kopírování Excel šablon podle výběru uživatele
- **Vyplňování dat do Excelů** pomocí `ExcelFiller`
- Sanitizace názvů složek (odstranění speciálních znaků)

**Struktura vytvořeného projektu:**
```
projects/
  001-2024_BOSAL_CR_sro/
    LSZ_001-2024_BOSAL_CR_sro.xlsm        ← Vyplněný daty!
    PP_001-2024_BOSAL_CR_sro_CAS.xlsx     ← Vyplněný daty!
    PP_001-2024_BOSAL_CR_sro_KUSY.xlsx    ← Vyplněný daty!
    CFZ_001-2024_BOSAL_CR_sro.xlsx        ← Vyplněný daty!
    measurement_data.json
```

### `core/excel_filler.py`
Obsahuje `ExcelFiller` třídu pro vyplňování dat do Excelů.

**Funkcionalita:**
- Načte Excel soubor (s makry pomocí `keep_vba=True`)
- Podle mappingu z `config/excel_field_mappings.py` vyplní buňky
- Uloží zpět zachovává makra

### `config/excel_field_mappings.py`
Mapování JSON cest na Excel buňky.

**Aktuální stav:**
- ✅ LSZ_MAPPING - Pracovník A (D12-D23), Pracovník B (K12-K23)
- ✅ PP_CAS_MAPPING - Základní údaje (D3-D9), Pracovník B (T5-T6)
- ✅ PP_KUSY_MAPPING - Základní údaje (D3-D9), Pracovník B (T5-T6)
- ✅ CFZ_MAPPING - Pracovník A (D12-D18), Pracovník B (K12-K18)

## Proč rozdělení do více souborů?

### Best practices:
1. **Separation of Concerns** - každý modul má jasnou zodpovědnost
2. **Maintainability** - snadnější najít a upravit specifickou část
3. **Testability** - jednotlivé komponenty lze testovat samostatně
4. **Scalability** - připraveno na budoucí rozšíření (validace, ukládání, generování Excelů)
5. **Readability** - kratší soubory = přehlednější kód

### Struktura podle best practices:
- **Entry point oddělený** - `main.py` je jen bootstrapping
- **GUI v samostatném package** - `gui/` obsahuje UI logiku
- **Stránky v jednom modulu** - `pages.py` obsahuje všechny formuláře (protože jsou si podobné)
- **Wizard samostatně** - `wizard.py` orchestruje stránky

## Budoucí rozšíření

Připravená struktura pro:
```
app/
├── main.py
├── gui/
│   ├── wizard.py
│   └── pages.py
├── core/              # (budoucí) Business logika
│   ├── validators.py
│   └── generators.py
├── config/            # (budoucí) Konfigurace
│   └── mappings.py
└── utils/             # (budoucí) Helper funkce
    └── file_helpers.py
```
