# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

LABORATO5 is a PyQt6-based automation tool for a physical workload laboratory. It eliminates manual Excel form-filling by providing a wizard interface that:
1. Collects measurement data through a 6-step GUI wizard
2. Parses Word documents to extract time schedules (using python-docx)
3. Generates project folders with pre-filled Excel files (LSZ, PP, CFZ variants)
4. Copies tabular data (time schedules) into the appropriate Excel sheets

**Current Status:** Prototype v2.0.0 - Core functionality implemented. Excel generation complete. Word protocol generation implemented with conditional text logic for LSZ, PP (ČAS/KUSY), and CFZ protocols. Automatic empty table/row removal implemented.

## Running the Application

```bash
# Install dependencies
cd laborator_protokoly
pip install -r requirements.txt

# Run the application (opens main menu)
python main.py
```

The application opens with a main menu offering two workflows:
1. **Excel Generation** - Create new project with Excel files (LSZ, PP, CFZ)
2. **Word Protocol Generation** - Generate Word protocol from existing project

### Main Menu Features
- **"📊 NOVÝ PROJEKT" button** - Opens the 6-step wizard for collecting measurement data and generating Excel files
- **"📝 GENEROVAT WORD PROTOKOL" button** - Opens dialog to select project folder, Excel file, template, and generate Word protocol
- **Auto-detection** - Word dialog automatically finds `measurement_data.json`, LSZ Excel, and suggests output path
- **Validation** - Both workflows validate inputs and show error messages via QMessageBox
- **ARES API integration** - Automatic company data lookup by IČO (Czech business registry)

## Development Commands

```bash
# Run the application
python main.py

# Test Excel generation (manual testing via GUI)
python main.py
# → Click "Nový projekt" → Complete wizard

# Test Word protocol generation (manual testing via GUI)
python main.py
# → Click "Generovat Word Protokol" → Select files → Generate

# Build standalone EXE for distribution
build_exe.bat

# Test standalone Word generation (without GUI)
python generate_word_from_two_sources.py

# Test conditional text generators
python test_final_all_six_conditions.py

# Test ARES API integration
python test_ares_api.py

# Test gender-based text generation
python test_gender_implementation.py

# Debug Excel reading
python debug_excel.py

# Check if templates exist
ls templates/excel/

# View generated projects
ls projects/

# Debug 11th conditional text (hierarchical load evaluation)
python debug_jedenacta_podminka.py
```

## Architecture

### Core Design Pattern
The application uses **Separation of Concerns** with three main layers:

1. **GUI Layer** (`gui/`)
   - `main_menu.py` - Main menu window with workflow selection (Excel or Word generation)
   - `wizard.py` - QWizard for Excel generation workflow (6-step data collection)
   - `pages.py` - Six QWizardPage classes for measurement data input
   - `word_protocol_dialog.py` - Dialog for Word protocol generation from existing projects

2. **Core Business Logic** (`core/`)
   - `project_manager.py` - Creates project folders, coordinates Excel generation
   - `excel_filler.py` - Fills individual Excel cells using field mappings
   - `table_copier.py` - Copies tabular data (time schedules) into Excel sheets
   - `docx_parser.py` - Extracts time schedule tables from Word documents
   - `text_generator.py` - Generates conditional texts for Word protocols based on measurement results
   - `file_manager.py` - Manages uploaded Word files, temp storage, and cleanup
   - `word_protocol_pipeline.py` - Orchestrates complete Word generation pipeline (Excel→JSON→Word)

3. **Configuration** (`config/`)
   - `excel_field_mappings.py` - Maps JSON paths to Excel cell addresses (e.g., `"section4_worker_a.full_name"` → `"D12"`)
   - `table_mappings.py` - Defines table locations in each Excel type (sheet name, start row, column mappings)

### Data Flow

**Two separate workflows:**

**Workflow 1: Excel Generation (via Wizard)**
```
Main Menu → "Nový projekt" button
  → GUI Wizard (6 pages)
    → Upload Word DOCX (description of work)
    → Word DOCX parser (extracts time schedule table)
    → JSON structure (measurement_data.json)
    → ProjectManager
      → Creates project folder
      → Copies Excel templates
      → ExcelFiller (fills individual fields)
      → TableCopier (fills time schedule table)
```

**Workflow 2: Word Protocol Generation (via Dialog)**
```
Main Menu → "Generovat Word Protokol" button
  → WordProtocolGeneratorDialog
    → User selects: project folder, LSZ Excel, template, output path
    → WordProtocolPipeline orchestrates:
      1. Read measurement_data.json (from project folder)
      2. read_lsz_results.py (Excel → lsz_results.json)
      3. export_charts() (creates chart images in lsz_charts/)
      4. generate_word_from_two_sources.py:
         - TextGenerator (9 conditional texts)
         - docxtpl rendering with two-JSON context
         - Post-processing (highlight selected holters)
    → Output: Word protocol with embedded results
```

### Excel Template System
Four Excel types supported:
- **LSZ** (.xlsm with macros) - Local muscle load (lokální svalová zátěž)
- **PP ČAS** (.xlsx) - Work positions by TIME (pracovní polohy - hodnocení času)
- **PP KUSY** (.xlsx) - Work positions by PIECES (pracovní polohy - hodnocení kusů)
- **CFZ** (.xlsx) - Overall physical load (celková fyzická zátěž)

Each has different:
- Field mappings in `excel_field_mappings.py`
- Table mappings in `table_mappings.py` (sheet name, start row, columns)
- Results readers: `read_lsz_results.py`, `read_pp_results.py` (CFZ pending)
- The mappings are defined per-sheet and specify which JSON fields go to which cells

## Key Implementation Details

### ARES API Integration
The application integrates with the Czech business registry (ARES) for automatic company data lookup:
- **Location:** `gui/pages.py` - `fetch_ares_data()` and `extract_company_data_from_ares()`
- **Trigger:** When user enters IČO (company ID) in the wizard
- **Auto-fills:** Company name, address, house number, city, city district, ZIP code
- **Error handling:** Gracefully handles timeouts, 404 errors, and API failures
- **URL:** `https://ares.gov.cz/ekonomicke-subjekty-v-be/rest/ekonomicke-subjekty/{ico}`

**Implementation:**
```python
def fetch_ares_data(ico: str) -> dict:
    """Fetches company data from ARES API by IČO"""
    ico_clean = ''.join(filter(str.isdigit, str(ico)))
    url = f"https://ares.gov.cz/ekonomicke-subjekty-v-be/rest/ekonomicke-subjekty/{ico_clean}"
    response = requests.get(url, timeout=10)
    return response.json() if response.status_code == 200 else None
```

### Gender-Based Text Generation
Word protocols use gender-specific Czech grammar for proper text generation:
- **Worker gender:** Stored in `measurement_data.json` as "Muž" or "Žena"
- **Text generator:** `core/text_generator.py` contains gender-aware conditional text logic
- **Usage:** Ensures grammatically correct Czech text in Word protocols (e.g., "byl měřen" vs "byla měřena")
- **Filter:** Custom Jinja2 filter `czech_past_tense` for converting verbs based on gender

### Excel Handling with openpyxl
- **Macros:** Only use `keep_vba=True` for `.xlsm` files (checked via `excel_path.suffix`)
- **Limitation:** openpyxl removes Data Validation (dropdowns) when saving - this is documented and unavoidable
- ExcelFiller uses dot notation to traverse JSON: `"section4_worker_a.full_name"` → splits on `.` → traverses dict

### Table Copying System
`TableCopier` has type-specific methods because each Excel type has:
- Different sheet names ("Časový snímek" vs "Časový snímek A+B")
- Different start rows (26 for LSZ, 34 for CFZ, 13 for PP)
- Different column layouts (LSZ has norm calculation column, PP converts minutes→seconds)

The universal `copy_time_schedule()` method dispatches to the correct handler based on `excel_type` parameter.

### Word Document Parsing
`DocxParser.parse_time_schedule_table()`:
- Expects the second table (index 1) in the Word document
- Parses max 20 rows (or 30 for PP variants)
- Returns structured dict: `{"line1": {...}, "line2": {...}, ..., "total": {...}}`
- Handles "Celkem" (total) row detection
- Returns empty structure if parsing fails

### Project Structure
Generated projects follow this pattern:
```
projects/
  {evidence_number}_{company}/
    LSZ_{evidence_number}_{company}.xlsm
    PP_{evidence_number}_{company}_CAS.xlsx
    PP_{evidence_number}_{company}_KUSY.xlsx
    CFZ_{evidence_number}_{company}.xlsx
    measurement_data.json
```

Folder names are sanitized (spaces→underscores, special chars removed) in `ProjectManager._sanitize_folder_name()`.

### Sample Protocols
The `sample_protocols/` directory contains reference Word templates organized by type:
- **Autorizované protokoly pro MUŽE/** - Authorized male protocol templates
- **Autorizované protokoly pro ŽENY/** - Authorized female protocol templates
- **Jeden zaměstnanec/** - Single employee templates
- **Odborné hodnocení - bezpohlavní/** - Gender-neutral expert evaluation templates
- **protokoly v pdf/** - PDF versions of protocols

**Note:** These are reference templates, not the active templates used for generation. Active templates are in `templates/`.

### Temporary File Management
The application handles temporary uploaded files automatically:
- **Upload location:** Temporary files stored in system temp directory
- **Cleanup:** `FileManager.cleanup_temp_uploads()` called on app exit via `atexit.register()`
- **Registration:** Cleanup hook registered in `main.py` entry point
- **Safety:** Ensures no temporary files are left behind after application closes

## JSON Data Structure

### measurement_data.json (Input Data)
The application uses a section-based JSON structure for GUI wizard data:
- `section0_file_selection` - Which Excel files to generate, measurement_days
- `section1_uploaded_docx` - Contains `time_schedule` data parsed from Word, uploaded file path
- `section2_firma` - Company info (company, profession, evidence_number, ico, measurement_date, etc.)
- `section3_additional_data` - Measurement parameters (work_norm, product_type, work_position, etc.)
- `section4_worker_a` - Primary worker data (full_name, age, height, weight, laterality, emg_holter, etc.)
- `section5_worker_b` - Secondary worker data (optional, same structure as worker_a)
- `section6_final` - Final notes and measured_by

See `measurement_data_example.json` for complete structure.

### lsz_results.json (Results Data - LSZ Protocol)
Contains calculated results from Excel files, read by `read_lsz_results.py`:
- **Scalar values:** `Fmax_Phk_Extenzor`, `Fmax_Phk_Flexor`, `Fmax_Lhk_Extenzor`, `Fmax_Lhk_Flexor`
- **Movement counts:** `phk_number_of_movements`, `lhk_number_of_movements`
- **Tables:**
  - `table_somatometrie` - Worker somatometric data
  - `table_B4_I21` - Time schedule with forces (20 rows)
  - `table_W4_Y51` - Hygiene limits lookup table
  - `table_force_distribution` - Force distribution by muscle groups (21 rows)
  - `table_K27_N47` - Additional force data

### pp_results.json (Results Data - PP Protocol)
Contains working position analysis from Excel "Průměr" sheet, read by `read_pp_results.py`:
- **Metadata:** `excel_type` ("PP_CAS" or "PP_KUSY"), `worker_count`, `what_is_evaluated`
- **Body sections** (52 rows total across 6 sections):
  - `trup` - Trunk positions (11 items)
  - `hlava_krk` - Head and neck positions (10 items)
  - `phk` - Right upper limb positions (8 items)
  - `lhk` - Left upper limb positions (8 items)
  - `dk` - Lower limbs positions (9 items)
  - `ostatni` - Other body parts (6 items)
- **Row structure:** Each row contains `nazev_polohy`, `typ_svalove_prace`, `vyskyt_min_a`, `vyskyt_min_b`, `prumer_min`, `typ_pracovni_polohy`

**Critical:** Both JSONs are used together in Word generation:
```python
context = {
    "input": measurement_data,   # From GUI
    "results": results_data       # From Excel (lsz_results.json or pp_results.json)
}
```

## Adding New Excel Mappings

1. **For individual fields:** Add to `config/excel_field_mappings.py`
   ```python
   LSZ_MAPPING = {
       "Sheet Name": {
           "D12": "section4_worker_a.full_name",
           "D13": "section4_worker_a.age_years"
       }
   }
   ```

2. **For tables:** Add to `config/table_mappings.py`
   ```python
   NEW_TABLE_MAPPING = {
       "sheet": "Sheet Name",
       "start_row": 26,
       "columns": {
           "operation": "C",
           "time_min": "F"
       }
   }
   ```

3. **For new table types:** Add method in `TableCopier` and update `copy_time_schedule()` dispatcher

## Word Protocol Generation

**Integration Status:** Word protocol generation is now fully integrated into the GUI via `WordProtocolGeneratorDialog`. Users can generate protocols from existing projects through the main menu.

### Pipeline Architecture
The `WordProtocolPipeline` class orchestrates the complete generation process:
1. Validates project folder (checks for `measurement_data.json`)
2. Detects protocol type (LSZ/PP_CAS/PP_KUSY/CFZ) from Excel filename
3. Reads Excel file and extracts results:
   - LSZ → `read_lsz_results.py` → `lsz_results.json`
   - PP → `read_pp_results.py` → `pp_results.json` (52 rows from "Průměr" sheet)
   - CFZ → Not yet implemented
4. Exports charts from Excel as image files (LSZ only)
5. Generates Word protocol using both JSONs and template
6. Applies post-processing:
   - Holter highlighting (LSZ)
   - Red color highlighting for over-limit values
   - Empty row/table removal (protocol-specific logic)

### Conditional Text System
The application generates Word protocols with dynamic text based on measurement results. This is handled by `core/text_generator.py`:

**Eleven conditional text generators:**
1. **prvni_text_podminka_pocetdni** - Based on measurement days (1 or 2 days)
2. **druhy_text_podminka_limit1** - PHK hygiene limits (4 text variants based on extensor/flexor limits)
3. **treti_text_podminka_limit1** - LHK hygiene limits (4 text variants based on extensor/flexor limits)
4. **ctvrty_text_podminka** - Force distribution ("nejsou", "ojediněle", "pravidelně")
5. **paty_text_podminka** - Over-limit forces (16 text variants for all combinations of 4 muscle groups)
6. **sesty_text_podminka** - Values over 100 check for force_over_70 only ("je" or "není")
7. **sedmy_text_podminka** - Large forces (55-70% Fmax) limit check (full sentence)
8. **osmy_text_podminka** - List of activities with force_over_70 > 100 (comma-separated or empty)
9. **devata_text_podminka** - Detailed text variant with force categories
10. **desata_text_podminka** - Hierarchical evaluation text based on devata_text_podminka results
11. **jedenacta_text_podminka** - Overall load level ("1", "2", or "3") based on all 4 muscle groups vs hygiene limits
   - Returns "1" if ALL muscle groups are below 1/3 of hygiene limit (low load)
   - Returns "2" if at least one is above 1/3 limit but none exceed the full limit (medium load)
   - Returns "3" if at least one exceeds the full hygiene limit (high load, limit exceeded)
   - Evaluates all 4 muscle groups: PHK extensor, PHK flexor, LHK extensor, LHK flexor
   - See `JEDENACTA_PODMINKA_DOKUMENTACE.md` for detailed algorithm and edge cases

**Key function:**
```python
generate_conditional_texts(measurement_data: dict, results_data: dict) -> dict
```
- Reads `measurement_data.json` (GUI input) and `lsz_results.json` (Excel results)
- Returns dictionary with 11 generated text keys
- Uses mathematical rounding (_math_round) for consistency with Excel
- Looks up values in table_W4_Y51 and table_force_distribution
- Calculates work shift-based limits for large forces (55-70% Fmax)
- Analyzes all activities in table_force_distribution to find those with force_over_70 > 100
- Evaluates hierarchical load levels based on hygiene limits (11th condition)

### Word Template Structure
Templates use **docxtpl** (Jinja2 syntax) with two-JSON context:
```python
context = {
    "input": measurement_data,    # From GUI wizard
    "results": results_data        # From Excel calculations
}
```

**Placeholders in templates:**
- Simple values: `{{ input.section2_firma.company }}`
- Results: `{{ results.Fmax_Phk_Extenzor }}`
- Conditional texts: `{{ texts.druhy_text_podminka_limit1 }}`
- Tables: `{% for row in results.table_somatometrie %}...{% endfor %}`

### Post-Processing Steps
Multiple post-processing operations are applied after Word generation:

**1. Holter Highlighting (LSZ only)**
- Maps holter IDs (A-F) to holter numbers (60/16, 65/17, etc.)
- Finds selected holters from measurement_data (worker A and B)
- Bolds corresponding rows in the equipment table
- Uses safe python-docx manipulation (not RichText in docxtpl)

**2. Red Color Highlighting**
- Highlights over-limit force values in red
- Applied to force distribution tables

**3. Empty Row/Table Removal (Protocol-Specific)**
- **LSZ/CFZ:** `remove_empty_activity_rows()` - Removes rows where activity column is "0", "", or "None"
  - Identifies tables by headings: "Výsledky měřených osob – počet pohybů", "síla % Fmax", "rozložení vynakládaných svalových sil"
- **PP:** `remove_empty_pp_rows()` - Removes rows where ALL three values are 0: `vyskyt_min_a == 0 AND vyskyt_min_b == 0 AND prumer_min == 0`
  - Identifies tables by headings: "TRUP", "HLAVA A KRK", "PHK", "LHK", "DOLNÍ KONČETINY", "OSTATNÍ ČÁSTI TĚLA"
  - Additional feature: `remove_empty_pp_tables()` - Removes entire tables that contain only headers (no data rows)
- Both functions use identical XML backend logic, differing only in conditional criteria
- Both iterate rows backwards to avoid index shifting during deletion

**Implementation:**
```python
# In generate_word_protocol_v2()
highlight_selected_holters(output_path, selected_holter_numbers)
highlight_red_colors(output_path)  # Force highlighting
if protocol_type in ["PP_CAS", "PP_KUSY"]:
    remove_empty_pp_rows(output_path)
    remove_empty_pp_tables(output_path)
else:
    remove_empty_activity_rows(output_path)
```

See `PP_EMPTY_ROWS_REMOVAL.md` for detailed PP removal documentation.

### Important Files for Word Generation
- `core/word_protocol_pipeline.py` - Main pipeline class with protocol detection (integrated into GUI)
- `gui/word_protocol_dialog.py` - GUI dialog for Word generation (supports multiple protocols)
- `gui/word_protocol_dialog_v2.py` - Enhanced dialog with multi-protocol checkbox selection
- `generate_word_from_two_sources.py` - Word generation script with post-processing (called by pipeline)
- `read_lsz_results.py` - Reads LSZ results data from Excel files → `lsz_results.json`
- `read_pp_results.py` - Reads PP results data from "Průměr" sheet → `pp_results.json`
- `core/text_generator.py` - All 11 conditional text generators (LSZ-focused)
- `WORD_PLACEHOLDERS_GUIDE.md` - Guide for two-JSON context structure
- `TABLES_ANALYSIS.md` - Analysis of Excel table structures
- `JEDENACTA_PODMINKA_DOKUMENTACE.md` - Documentation for 11th conditional text (hierarchical load evaluation)
- `PP_IMPLEMENTATION_SUMMARY.md` - PP protocol implementation guide and testing instructions
- `PP_EMPTY_ROWS_REMOVAL.md` - Documentation for PP empty row/table removal logic
- `PP_RESULTS_USAGE_EXAMPLES.md` - Examples of using PP results in templates
- Test scripts: `test_word_generation_integration.py`, `test_conditional_texts.py`, `test_jedenacta_text_podminka.py`, etc.

## Building Standalone EXE

The application can be packaged as a standalone Windows executable using PyInstaller:

```bash
# Build EXE (creates dist\LABORATO5\ folder)
build_exe.bat

# Test the built executable
cd dist\LABORATO5
LABORATO5.exe
```

**Important notes about distribution:**
- Distribute the **entire** `dist\LABORATO5\` folder, not just the .exe file
- The folder includes all libraries, templates, and sample protocols
- End users do **NOT** need Python installed
- End users **DO** need Microsoft Excel installed (for xlwings chart export)
- Build size is approximately 500 MB (PyQt6 is large)
- First startup may take ~10 seconds

**Build configuration:**
- Uses `--onedir` mode (folder with dependencies, not single-file)
- Uses `--windowed` mode (no console window)
- Includes `templates/` and `config/` directories
- Sample protocols are copied post-build to avoid encoding issues

See `JAK_VYTVORIT_EXE.md` for detailed build instructions and troubleshooting.

## Known Limitations & Future Work

**Current Limitations:**
- Data Validation (Excel dropdowns) is lost when saving (openpyxl limitation)
- Wizard error handling prints to console; Word dialog uses QMessageBox
- Minimal input validation
- No progress indicators during generation
- xlwings chart export requires Microsoft Excel installation

**Recently Implemented:**
- Word protocol generation with conditional text logic
- Two-JSON context system (measurement_data + results_data)
- File upload and management system
- Conditional text generators (11 variants, including hierarchical load evaluation)
- Holter highlighting in Word tables
- Force highlighting with red colors in Word output
- **GUI integration of Word generation** (via WordProtocolGeneratorDialog)
- **WordProtocolPipeline** for orchestrating complete generation workflow
- **Protocol detection system** - Automatic LSZ/PP_CAS/PP_KUSY/CFZ detection from filename
- **PP protocol support** - Complete PP Excel reading, results JSON generation, Word rendering
- **Multi-protocol dialog** (word_protocol_dialog_v2.py) - Checkbox selection for generating multiple protocols
- **Empty row/table removal** - Protocol-specific logic for cleaning Word output (LSZ vs PP)
- Main menu with workflow selection
- **PyInstaller build system** for standalone EXE distribution
- **11th conditional text** (jedenacta_text_podminka) - hierarchical evaluation of all 4 muscle groups

**Not Yet Implemented (see NEXT_STEPS_ANALYSIS.md):**
- All 15 Word template variants (currently only test templates exist)
- PP-specific conditional text generators (currently using stubs/placeholders)
- CFZ protocol reader (`read_cfz_results.py`) - CFZ Excel reading not yet implemented
- PDF export from Word protocols
- Loading existing projects for editing
- Unit tests
- Advanced validation (IČO format, date ranges)
- Structured logging system

**Priority features (from NEXT_STEPS_ANALYSIS.md):**
1. Copy additional tables (movements, positions) beyond time schedule
2. GUI error dialogs (QMessageBox) instead of console prints
3. Input validation before project generation
4. Progress bar during Excel generation

## Important Files

- `PROJECT_SUMMARY.md` - High-level project overview, features, architecture
- `NEXT_STEPS_ANALYSIS.md` - Detailed analysis of missing features and implementation roadmap
- `measurement_data_example.json` - Example of complete JSON structure
- `config/README.md` - Instructions for adding new Excel mappings
- `WORD_PLACEHOLDERS_GUIDE.md` - Guide for working with two-JSON context in Word templates
- `TABLES_ANALYSIS.md` - Analysis of Excel table structures and data flows
- `JAK_VYTVORIT_EXE.md` - Guide for building standalone executable with PyInstaller
- `generate_word_from_two_sources.py` - Word generation script (now integrated via WordProtocolPipeline)
- `read_lsz_results.py` - Reads results data from Excel files
- `core/word_protocol_pipeline.py` - Pipeline orchestrator for Word generation
- `gui/word_protocol_dialog.py` - GUI dialog for selecting files and generating Word protocols
- `build_exe.bat` - Automated build script for creating Windows executable

## Working with This Codebase

When modifying:
- **Application entry point:** `main.py` launches `MainMenuWindow` which presents two workflow options
- **Workflows:** The app has two independent workflows - Excel generation (wizard) and Word generation (dialog)
- **Excel mappings:** Remember different Excel types have different sheet names and layouts
- **Results readers:** Each protocol type requires its own reader (LSZ: read_lsz_results.py, PP: read_pp_results.py, CFZ: pending)
- **Protocol detection:** Pipeline auto-detects protocol type from Excel filename (LSZ/PP_CAS/PP_KUSY/CFZ pattern)
- **Table copying:** Each Excel type requires specific handling (macros, unit conversions, calculated fields)
- **GUI changes:** The wizard generates JSON on "Finish" - ensure new fields are captured in the correct section
- **Path handling:** Use `pathlib.Path` throughout (already established pattern)
- **Error handling:** Word generation dialog uses QMessageBox for errors; wizard still prints to console
- **Word templates:** Use two-JSON context (`input` and `results`) to separate GUI data from calculated results
- **Conditional texts:** All 11 conditional text generators are in `text_generator.py` - currently LSZ-focused, PP uses stubs
- **Post-processing:** Empty row removal logic differs by protocol type (LSZ vs PP) - see `remove_empty_activity_rows()` vs `remove_empty_pp_rows()`
- **File uploads:** Temporary files are managed by `FileManager` and cleaned up on app exit (via atexit hook)
- **Word pipeline:** `WordProtocolPipeline` orchestrates the complete generation - modify here to change the workflow
- **ARES integration:** Company data lookup is in `gui/pages.py` - modify for additional fields or different APIs
- **Czech language:** Gender-based text generation requires careful handling of Czech grammar rules

## Platform Requirements

**Operating System:**
- **Primary:** Windows (due to pywin32, xlwings, and COM automation)
- **Compatibility:** Code uses `pathlib` for cross-platform paths, but Excel chart export requires Windows + Excel

**External Dependencies:**
- **Microsoft Excel:** Required for xlwings chart export functionality
- **Internet connection:** Optional, only for ARES API company lookup

## Testing Strategy

**GUI Testing:**
```bash
# Test complete Excel generation workflow
python main.py
# → Click "Nový projekt" → Complete wizard

# Test Word protocol generation workflow
python main.py
# → Click "Generovat Word Protokol" → Select files → Generate
```

**Current test files** (standalone scripts, not automated tests):
- `test_word_generation_integration.py` - Full Word generation workflow
- `test_conditional_texts.py` - Tests prvni_text_podminka
- `test_druhy_text_podminka.py` through `test_devata_text_podminka.py` - Individual condition tests
- `test_jedenacta_text_podminka.py` - Tests 11th conditional text (hierarchical load evaluation)
- `test_jedenacta_text_podminka_hranicni_pripady.py` - Tests edge cases for 11th condition
- `test_final_all_six_conditions.py` - Tests multiple conditions together
- `test_all_seven_conditions.py` - Tests seven conditional texts
- `test_subdoc_integration.py` - Subdocument integration tests
- `test_force_highlighting.py` - Tests force highlighting in Word tables
- `test_ares_api.py` - Tests ARES API integration for company data lookup
- `test_gender_implementation.py` - Tests gender-based Czech text generation
- `test_czech_filter.py` - Tests Czech language filters for Jinja2 templates
- `debug_excel.py` - Excel reading and debugging
- `create_simple_test.py` - Creates simple test Word documents
- `verify_red_colors.py` - Verifies red color highlighting in Word output

**Standalone Word generation (without GUI):**
```bash
# Generate Word protocol directly from JSONs
python generate_word_from_two_sources.py

# Test all conditional text generators
python test_final_all_six_conditions.py
```

## Dependencies

```
PyQt6>=6.6.0          # GUI framework
openpyxl>=3.1.0       # Excel manipulation (supports .xlsm macros with keep_vba=True)
python-docx>=1.1.0    # Word document reading/manipulation
docxtpl>=0.16.0       # Word template rendering with Jinja2
xlwings>=0.30.0       # Excel automation for chart export (requires Excel installation)
Pillow>=10.0.0        # Image processing
pywin32>=305          # Windows-specific functionality (COM automation)
requests>=2.31.0      # HTTP requests (for ARES API)
```

**Important notes:**
- **openpyxl limitation:** Data Validation (dropdowns) is lost when saving - this is a known library limitation
- **docxtpl with tables:** Use post-processing with python-docx for complex table formatting (RichText in tables is risky)
- **xlwings:** Requires Excel installation, use only if openpyxl can't handle the task
- **pywin32:** Windows-only dependency for COM automation
