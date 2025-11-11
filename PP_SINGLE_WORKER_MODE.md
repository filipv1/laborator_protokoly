# PP Single-Worker Mode - Dokumentace

## Prehled

PP protokoly podporuji dva rezimy pro vypocet kategorizace pracovnich poloh:

1. **Two-worker mode** (vychozi) - Pouziva `prumer_min` (prumer pracovniku A a B)
2. **Single-worker mode** - Pouziva `vyskyt_min_a` (pouze pracovnik A)

## Detekce rezimu

Rezim se automaticky detekuje z `measurement_data.json`:

```python
# Single-worker pokud worker_b nema vyplnene jmeno
worker_b = measurement_data.get("section5_worker_b", {})
is_single = not bool(worker_b.get("full_name", "").strip())
```

**Priklad measurement_data.json (single-worker):**
```json
{
    "section5_worker_b": {
        "full_name": "",
        "age_years": 0
    }
}
```

## Pouziti v kodu

### Helper funkce
```python
def _is_single_worker_protocol(measurement_data: Dict[str, Any]) -> bool:
    """Detekuje single-worker protokol"""
    worker_b = measurement_data.get("section5_worker_b", {})
    full_name = worker_b.get("full_name", "")
    return not bool(full_name.strip() if full_name else False)
```

### PP funkce s parametrem use_worker_a_only

```python
# 1. Maximalni kategorie
def _get_pp_max_category(
    results_data: Dict[str, Any],
    category_limits: Dict[str, Any],
    use_worker_a_only: bool = False  # NOVY PARAMETR
) -> int:
    # Vyber hodnoty podle modu
    if use_worker_a_only:
        comparison_value = row_data.get("vyskyt_min_a", 0)
    else:
        comparison_value = row_data.get("prumer_min", 0)
```

Stejna logika plati pro:
- `_get_pp_problematic_positions_list()`
- `_calculate_prvni_pp_podminka_kategorie()`

### Integrace v generate_conditional_texts()

```python
if protocol_type in ("PP_CAS", "PP_KUSY"):
    # Detekovat single-worker mod
    is_single_worker = _is_single_worker_protocol(measurement_data)

    # Predavat do vsech PP funkci
    texts["prvni_pp_podminka_kategorie"] = _calculate_prvni_pp_podminka_kategorie(
        results_data,
        category_limits,
        use_worker_a_only=is_single_worker  # PREDAT PARAMETR
    )
```

## Testovani

### Unit test: Detekce
```bash
python test_pp_single_worker_detection.py
```

### Unit test: Porovnani logiky
```bash
python test_pp_single_vs_dual_worker_logic.py
```

### Integracni test
```bash
python test_pp_single_worker_integration.py
```

## Priklad vysledku

**Testovaci data:**
- `vyskyt_min_a` = 130 min (prekroci kat1=100)
- `prumer_min` = 65 min (NEprekroci kat1=100)

**Single-worker rezim (vyskyt_min_a=130):**
```
Celkova doba...prekrocila...prisustny limit kategorie 1
pro dynamicky predklon trupu.

pp_kategorie_cislo: "2"
```

**Two-worker rezim (prumer_min=65):**
```
Celkova doba...NEprekrocila...prisustny limit kategorie 1.

pp_kategorie_cislo: "1"
```

## Soubory

**Implementace:**
- `core/text_generator.py` - Vsechny PP funkce a detekce

**Testy:**
- `test_pp_single_worker_detection.py` - Test detekce
- `test_pp_single_vs_dual_worker_logic.py` - Porovnani modu
- `test_pp_single_worker_integration.py` - Integracni test

**Testovaci data:**
- `projects/test_single_worker_PP/measurement_data.json`
- `projects/test_single_worker_PP/pp_results.json`

## Poznamky

- Detekce je 100% spolehliiva (kontroluje full_name v worker_b)
- Backward compatible - existujici two-worker protokoly funguj beze zmen
- Debug printy ukazuji aktivni rezim v console outputu
