# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

LABORATO5 is a PyQt6-based automation tool for a physical workload laboratory with two workflows:

1. **Excel Generation** - 6-step GUI wizard collects measurement data, parses Word documents for time schedules, generates project folders with pre-filled Excel files (LSZ, PP, CFZ)
2. **Word Protocol Generation** - Reads measurement JSON + Excel results, generates Word reports with conditional texts and post-processing

## Running & Building

```bash
pip install -r requirements.txt
python main.py                    # Run application
build_exe.bat                     # Build standalone EXE (creates dist\LABORATO5\)
```

## Architecture

```
gui/                              # PyQt6 GUI layer
  main_menu.py                    # Main menu with workflow selection
  wizard.py                       # 6-step QWizard for Excel generation
  pages.py                        # QWizardPage classes + ARES API integration
  word_protocol_dialog.py         # Word protocol generation dialog

core/                             # Business logic
  project_manager.py              # Creates project folders, coordinates Excel generation
  excel_filler.py                 # Fills Excel cells using field mappings
  table_copier.py                 # Copies time schedules into Excel (type-specific methods)
  docx_parser.py                  # Extracts tables from Word documents (fuzzy column matching)
  text_generator.py               # 11 LSZ + 3 PP conditional text generators
  word_protocol_pipeline.py       # Orchestrates Word generation (Excel→JSON→Word)

config/                           # Configuration
  excel_field_mappings.py         # JSON path → Excel cell mappings per sheet
  table_mappings.py               # Table locations per Excel type
```

## Critical Concepts

### Two-JSON Context System
Word templates use two data sources combined:
```python
context = {
    "input": measurement_data,    # From GUI wizard (section0-6)
    "results": results_data       # From Excel calculations (lsz_results.json or pp_results.json)
}
```
Template syntax: `{{ input.section2_firma.company }}`, `{{ results.Fmax_Phk_Extenzor }}`, `{{ texts.druhy_text_podminka_limit1 }}`

### Protocol Type Detection
Pipeline auto-detects from Excel filename pattern: `LSZ_*`, `PP_*_CAS`, `PP_*_KUSY`, `CFZ_*`
Each type has different:
- Field mappings and table mappings
- Results reader (`read_lsz_results.py`, `read_pp_results.py`, CFZ pending)
- Post-processing logic (empty row removal criteria differ)
- Conditional text generators

### Excel Type Differences
| Type | Extension | Sheet Name | Start Row | Special Handling |
|------|-----------|------------|-----------|------------------|
| LSZ | .xlsm | "Časový snímek" | 26 | `keep_vba=True`, norm calculation column |
| PP | .xlsx | "Časový snímek A+B" | 13 | Minutes→seconds conversion |
| CFZ | .xlsx | "Časový snímek A+B" | 34 | (Not yet implemented) |

### Single-Worker vs Two-Worker Mode
PP protocols auto-detect: if `section5_worker_b.full_name` is empty, uses `vyskyt_min_a`; otherwise uses `prumer_min` (average).

## Key Gotchas

1. **openpyxl loses Data Validation** - Excel dropdowns are removed when saving. Documented, unavoidable.

2. **Post-processing order matters** - In `generate_word_protocol_v2()`:
   - Holter highlighting (LSZ only)
   - Red color highlighting for over-limit values
   - Empty row removal (LSZ: activity="0"; PP: all three values=0)

3. **Czech grammar handling**:
   - Gender-based text: "Muž"/"Žena" in measurement_data affects verb conjugation
   - Czech declension: `_get_declined_position_name()` converts nominative→genitive for PP positions
   - Custom Jinja2 filters: `|czech` (standard), `|czek` (mandatory decimal), `|nondecimal` (whole numbers only)

4. **Word table parsing** - `DocxParser` expects second table (index 1), uses fuzzy column name matching ("Činnost"/"Operace"/"Popis práce" all work)

5. **xlwings requires Excel** - Chart export only works on Windows with Excel installed

6. **Temporary files** - `FileManager.cleanup_temp_uploads()` registered via `atexit` in main.py

## Adding Excel Mappings

```python
# config/excel_field_mappings.py - individual cells
LSZ_MAPPING = {"Sheet Name": {"D12": "section4_worker_a.full_name"}}

# config/table_mappings.py - table locations
LSZ_TABLE_MAPPING = {"sheet": "Časový snímek", "start_row": 26, "columns": {"operation": "C", "time_min": "F"}}
```

For new table types, add method in `TableCopier` and update `copy_time_schedule()` dispatcher.

## Testing

No automated test suite. Manual testing via GUI or standalone scripts:
```bash
python test_final_all_six_conditions.py   # LSZ conditional texts
python test_pp_kategorizace.py            # PP categorization
python read_lsz_results.py <excel_path>   # Extract results to JSON
```

Test files follow pattern: `test_*.py` for tests, `debug_*.py` for debugging.

## Key Files

- `measurement_data_example.json` - Complete JSON structure reference
- `generate_word_from_two_sources.py` - Standalone Word generation with post-processing
- `read_lsz_results.py` / `read_pp_results.py` - Excel→JSON extraction

## Platform Requirements

- **Windows required** for xlwings/pywin32 COM automation
- **Microsoft Excel required** for chart export
- Internet optional (ARES API for company lookup by IČO)
