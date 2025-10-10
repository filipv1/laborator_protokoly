# Excel Field Mappings

Tato složka obsahuje mapování mezi JSON daty a Excel buňkami.

## Jak přidat mapping pro další Excel

### 1. Otevři `excel_field_mappings.py`

### 2. Přidej nový mapping podle vzoru:

```python
CFZ_MAPPING = {
    "Název_listu_v_excelu": {
        "A1": "section1_firma.company",
        "B2": "section3_worker_a.age_years",
        "C3": "section2_additional_data.work_performed",
        # ... další buňky
    },
    "Další_list": {
        # ... další buňky
    }
}
```

### 3. Exportuj v `__init__.py`:

```python
from .excel_field_mappings import LSZ_MAPPING, CFZ_MAPPING

__all__ = ['LSZ_MAPPING', 'CFZ_MAPPING']
```

### 4. Použij v `project_manager.py`:

```python
from config import CFZ_MAPPING

# V metodě _fill_excel_data:
if "cfz" in copied_files:
    cfz_filler = ExcelFiller(CFZ_MAPPING)
    cfz_filler.fill_excel(copied_files["cfz"], project_data)
```

## Dostupné JSON cesty

Viz `measurement_data_example.json` v root složce pro kompletní seznam.

Příklady:
- `section1_firma.company`
- `section3_worker_a.full_name`
- `section2_additional_data.workers_gender`

## Formát

**Klíč:** Přesný název listu v Excelu (case-sensitive!)
**Hodnota:** Dictionary s mappingem `"buňka": "json.path"`
