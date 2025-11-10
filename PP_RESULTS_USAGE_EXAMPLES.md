# PP Results JSON - Příklady použití v šablonách

## Struktura dat

`pp_results.json` nyní používá **číselné klíče jako stringy** (stejně jako `lsz_results.json`), nikoli seznamy.

```json
{
  "excel_type": "PP_CAS",
  "worker_count": 2,
  "what_is_evaluated": "cas",
  "trup": {
    "1": {
      "nazev_polohy": "Předklon trupu větší než 60°",
      "typ_svalove_prace": "Statická",
      "vyskyt_min_a": 0,
      "vyskyt_min_b": 0,
      "prumer_min": 0,
      "typ_pracovni_polohy": "N"
    },
    "2": {
      "nazev_polohy": "Záklon bez opory celého těla",
      ...
    }
  },
  "hlava_krk": {
    "1": {...},
    "2": {...}
  },
  "phk": {...},
  "lhk": {...},
  "dk": {...},
  "ostatni": {...}
}
```

## Přístup k datům v Jinja2 šablonách (docxtpl)

### 1. Přístup k jednomu konkrétnímu řádku

```jinja2
{# Přímý přístup k řádku 1 v sekci trup #}
{{ results.trup["1"].nazev_polohy }}
{{ results.trup["1"].prumer_min }}

{# Přístup k PHK řádku 5 #}
{{ results.phk["5"].vyskyt_min_a }}
```

### 2. Procházení všech řádků v sekci

```jinja2
{# Iterace přes všechny polohy trupu #}
{% for row_num, row_data in results.trup.items() %}
Řádek {{ row_num }}: {{ row_data.nazev_polohy }} - {{ row_data.prumer_min }} min
{% endfor %}
```

### 3. Iterace přes více sekcí

```jinja2
{# Procházení všech sekcí těla #}
{% for row_num, row_data in results.trup.items() %}
  {{ row_data.nazev_polohy }}: {{ row_data.prumer_min }} min
{% endfor %}

{% for row_num, row_data in results.hlava_krk.items() %}
  {{ row_data.nazev_polohy }}: {{ row_data.prumer_min }} min
{% endfor %}
```

### 4. Filtrování podle podmínek

```jinja2
{# Zobraz jen polohy typu "PP" (pracovní poloha) #}
{% for row_num, row_data in results.trup.items() %}
  {% if row_data.typ_pracovni_polohy == "PP" %}
    {{ row_data.nazev_polohy }}
  {% endif %}
{% endfor %}

{# Zobraz jen polohy s výskytem větším než 0 #}
{% for row_num, row_data in results.phk.items() %}
  {% if row_data.prumer_min and row_data.prumer_min > 0 %}
    {{ row_data.nazev_polohy }}: {{ row_data.prumer_min }} min
  {% endif %}
{% endfor %}
```

### 5. Tabulka v Word šabloně

```jinja2
{# Vytvoření tabulky s daty z PP #}
Trup - pracovní polohy:
{% for row_num, row_data in results.trup.items() %}
{{ row_num }} | {{ row_data.nazev_polohy }} | {{ row_data.typ_svalove_prace }} | {{ row_data.prumer_min }}
{% endfor %}
```

## Příklady použití v Python kódu

### Načtení a práce s daty

```python
import json

# Načtení JSON
with open("pp_results.json", "r", encoding="utf-8") as f:
    pp_data = json.load(f)

# Přístup k jednomu řádku
first_trup = pp_data["trup"]["1"]
print(first_trup["nazev_polohy"])  # "Předklon trupu větší než 60°"

# Procházení všech řádků
for row_num, row_data in pp_data["trup"].items():
    print(f"Řádek {row_num}: {row_data['nazev_polohy']}")

# Filtrování
pp_polohy = [
    row_data for row_num, row_data in pp_data["trup"].items()
    if row_data["typ_pracovni_polohy"] == "PP"
]

# Počet řádků v sekci
trup_count = len(pp_data["trup"])
print(f"Počet poloh trupu: {trup_count}")
```

## Srovnání se starým formátem

### STARÉ (seznam) ❌
```json
"trup": [
  {"nazev_polohy": "...", ...},
  {"nazev_polohy": "...", ...}
]
```

```jinja2
{% for row in results.trup %}
  {{ row.nazev_polohy }}
{% endfor %}
```

### NOVÉ (slovník s číselnými klíči) ✅
```json
"trup": {
  "1": {"nazev_polohy": "...", ...},
  "2": {"nazev_polohy": "...", ...}
}
```

```jinja2
{% for row_num, row_data in results.trup.items() %}
  {{ row_num }}: {{ row_data.nazev_polohy }}
{% endfor %}
```

## Výhody nové struktury

1. ✅ **Konzistence s LSZ**: Stejná struktura jako `lsz_results.json`
2. ✅ **Přímý přístup**: Snadný přístup k řádku podle čísla: `results.trup["5"]`
3. ✅ **Čitelnost**: Jednodušší debugování (vidíte číslo řádku)
4. ✅ **Flexibilita**: Snadné přidání/odstranění řádků bez přečíslování indexů

## Sekce v PP Results

| Sekce | Klíč JSON | Počet řádků | Řádky v Excel |
|-------|-----------|-------------|---------------|
| Trup | `trup` | 11 | 4-14 |
| Hlava a krk | `hlava_krk` | 10 | 16-25 |
| PHK | `phk` | 10 | 27-36 |
| LHK | `lhk` | 10 | 38-47 |
| Dolní končetiny | `dk` | 7 | 49-55 |
| Ostatní | `ostatni` | 4 | 57-60 |

**Celkem:** 52 řádků dat
