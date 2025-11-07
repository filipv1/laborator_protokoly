# PP Kategorie Limity - Dokumentace

## Přehled

Implementace přepočtu limitních hodnot pro kategorizaci pracovních poloh (PP a N) podle NV 361/2007, Tabulka č.8.

**Účel:** Pro nestandardní délky směn (≠ 480 min) aplikovat koeficient přepočtu na base limity kategorií.

## Base limity (standardní směna 480 min)

### Typ "PP" (pracovní poloha)
- **Kategorie 1:** 0 - 100 min
- **Kategorie 2:** 101 - 160 min
- **Kategorie 3:** >160 min

### Typ "N" (nepříznivá poloha)
- **Kategorie 1:** 0 - 20 min
- **Kategorie 2:** 21 - 30 min
- **Kategorie 3:** >30 min

## Koeficient přepočtu (NV 361/2007, Tabulka č.8)

### Vzorec

**Pro delší směny (>480 min):**
```python
if difference < 30:
    intervals = 1  # 481-509 min
else:
    intervals = ((difference - 30) // 30) + 2  # 510-539, 540-569, ...

koeficient = 1.0 + (intervals * 0.025)
koeficient = min(koeficient, 1.2)  # Max cap
```

**Pro kratší směny (<480 min):**
```python
abs_diff = abs(difference)
intervals = ((abs_diff - 1) // 30) + 1  # 1-30→1, 31-60→2, ...

koeficient = 1.0 - (intervals * 0.025)
koeficient = max(koeficient, 0.8)  # Min floor
```

### Tabulka koeficientů

| Doba výkonu práce [min] | Limitní hodnota [%] | Koeficient |
|-------------------------|---------------------|------------|
| >689                    | 20                  | 1.200      |
| 660-689                 | 17,5                | 1.175      |
| 630-659                 | 15                  | 1.150      |
| 600-629                 | 12,5                | 1.125      |
| 570-599                 | 10                  | 1.100      |
| 540-569                 | 7,5                 | 1.075      |
| 510-539                 | 5                   | 1.050      |
| 481-509                 | 2,5                 | 1.025      |
| **480 (standard)**      | **0**               | **1.000**  |
| 450-479                 | -2,5                | 0.975      |
| 420-449                 | -5                  | 0.950      |
| 390-419                 | -7,5                | 0.925      |
| 360-389                 | -10                 | 0.900      |
| 330-359                 | -12,5               | 0.875      |
| 300-329                 | -15                 | 0.850      |
| 270-299                 | -17,5               | 0.825      |
| 240-269                 | -20                 | 0.800      |
| <240                    | -20                 | 0.800      |

## Výpočet limitů

**Funkce:** `_calculate_pp_category_limits(coefficient: float) -> dict`

**Vzorec:**
```python
# Aplikovat koeficient na base limity
pp_limit1 = _math_round(100 * coefficient)
pp_limit2 = _math_round(160 * coefficient)
n_limit1 = _math_round(20 * coefficient)
n_limit2 = _math_round(30 * coefficient)

# Vytvořit boundaries
pp_kat1: 0 - pp_limit1
pp_kat2: (pp_limit1 + 1) - pp_limit2
pp_kat3: >(pp_limit2 + 1)

n_kat1: 0 - n_limit1
n_kat2: (n_limit1 + 1) - n_limit2
n_kat3: >(n_limit2 + 1)
```

**Zaokrouhlení:** Používá `_math_round()` (floor(x + 0.5)) pro konzistenci s Excel výpočty.

## Příklady

### Příklad 1: Standardní směna (480 min)
```
work_duration_min = 480
→ koeficient = 1.000

PP limity:
  Kategorie 1: 0 - 100 min
  Kategorie 2: 101 - 160 min
  Kategorie 3: >160 min

N limity:
  Kategorie 1: 0 - 20 min
  Kategorie 2: 21 - 30 min
  Kategorie 3: >30 min
```

### Příklad 2: Delší směna (510 min)
```
work_duration_min = 510
difference = 510 - 480 = 30
intervals = ((30 - 30) // 30) + 2 = 2
→ koeficient = 1.0 + (2 * 0.025) = 1.050

PP limity:
  Kategorie 1: 0 - 105 min  (100 * 1.05 = 105)
  Kategorie 2: 106 - 168 min  (160 * 1.05 = 168)
  Kategorie 3: >168 min

N limity:
  Kategorie 1: 0 - 21 min  (20 * 1.05 = 21)
  Kategorie 2: 22 - 32 min  (30 * 1.05 = 31.5 → 32)
  Kategorie 3: >32 min
```

### Příklad 3: Kratší směna (420 min)
```
work_duration_min = 420
difference = 420 - 480 = -60
abs_diff = 60
intervals = ((60 - 1) // 30) + 1 = 2
→ koeficient = 1.0 - (2 * 0.025) = 0.950

PP limity:
  Kategorie 1: 0 - 95 min  (100 * 0.95 = 95)
  Kategorie 2: 96 - 152 min  (160 * 0.95 = 152)
  Kategorie 3: >152 min

N limity:
  Kategorie 1: 0 - 19 min  (20 * 0.95 = 19)
  Kategorie 2: 20 - 29 min  (30 * 0.95 = 28.5 → 29)
  Kategorie 3: >29 min
```

### Příklad 4: Maximální koeficient (720 min)
```
work_duration_min = 720
difference = 720 - 480 = 240
intervals = ((240 - 30) // 30) + 2 = 9
→ koeficient = 1.0 + (9 * 0.025) = 1.225
→ koeficient = min(1.225, 1.2) = 1.200 (cap)

PP limity:
  Kategorie 1: 0 - 120 min  (100 * 1.2 = 120)
  Kategorie 2: 121 - 192 min  (160 * 1.2 = 192)
  Kategorie 3: >192 min

N limity:
  Kategorie 1: 0 - 24 min  (20 * 1.2 = 24)
  Kategorie 2: 25 - 36 min  (30 * 1.2 = 36)
  Kategorie 3: >36 min
```

## Výstup do Word šablon

Limity jsou přidány do `texts` dictionary a dostupné v Word šablonách jako placeholdery:

```jinja2
PP kategorie:
- Kategorie 1: 0 - {{ texts.pp_kat1_max }} min
- Kategorie 2: {{ texts.pp_kat2_min }} - {{ texts.pp_kat2_max }} min
- Kategorie 3: >{{ texts.pp_kat3_min }} min

N kategorie:
- Kategorie 1: 0 - {{ texts.n_kat1_max }} min
- Kategorie 2: {{ texts.n_kat2_min }} - {{ texts.n_kat2_max }} min
- Kategorie 3: >{{ texts.n_kat3_min }} min
```

## Použití v dalších podmínkách

Tyto limity budou použity v následujících PP podmínkách pro kategorizaci jednotlivých pracovních poloh:

```python
# Příklad použití
for section in ["trup", "hlava_krk", "phk", "lhk", "dk", "ostatni"]:
    for row_id, row in pp_results[section].items():
        prumer_min = row["prumer_min"]
        typ = row["typ_pracovni_polohy"]  # "PP" nebo "N"

        # Kategorizace
        if typ == "PP":
            if prumer_min <= texts["pp_kat1_max"]:
                kategorie = 1
            elif prumer_min <= texts["pp_kat2_max"]:
                kategorie = 2
            else:
                kategorie = 3
        else:  # typ == "N"
            if prumer_min <= texts["n_kat1_max"]:
                kategorie = 1
            elif prumer_min <= texts["n_kat2_max"]:
                kategorie = 2
            else:
                kategorie = 3
```

## Edge Cases

### work_duration_min chybí
- **Fallback:** 480 min (standardní směna)
- **Koeficient:** 1.0
- **Chování:** Base limity beze změn

### Extrémně krátká směna (<240 min)
- **Koeficient:** Limitován na 0.8 (min floor)
- **PP kat1:** 0-80 min
- **N kat1:** 0-16 min

### Extrémně dlouhá směna (>689 min)
- **Koeficient:** Limitován na 1.2 (max cap)
- **PP kat1:** 0-120 min
- **N kat1:** 0-24 min

## Implementační detaily

### Soubory
- **Hlavní logika:** `core/text_generator.py`
  - `_calculate_pp_work_shift_coefficient(work_duration_min)` - Výpočet koeficientu
  - `_calculate_pp_category_limits(coefficient)` - Výpočet limitů
  - `generate_conditional_texts()` - Integrace do PP větve

### Unit testy
- **Soubor:** `test_pp_coefficient_and_limits.py`
- **Coverage:**
  - Koeficient pro směny 240-720 min
  - Limity pro koeficienty 0.8-1.2
  - Edge cases (zaokrouhlení, max/min caps)

### Testovací skripty
- `test_pp_limits_real_data.py` - Test na reálných projektech
- Debug výpis v konzoli při generování PP protokolu

## Reference

- **NV 361/2007:** [https://www.zakonyprolidi.cz/cs/2007-361#f7804228](https://www.zakonyprolidi.cz/cs/2007-361#f7804228)
- **Tabulka č.8:** Přepočet limitních hodnot podle doby výkonu práce
