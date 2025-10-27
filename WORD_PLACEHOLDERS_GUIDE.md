# Průvodce Word placeholdery - práce se dvěma JSONy

## 📋 Struktura dat

### measurement_data.json (VSTUPNÍ DATA)
```json
{
  "section1_firma": {
    "company": "BOSAL ČR s.r.o.",
    "ico": "12345678",
    "measurement_date": "10.10.2024"
  },
  "section3_worker_a": {
    "full_name": "Jan Novák",
    "age_years": 35,
    "height_cm": 178
  }
}
```

### lsz_results.json (VÝSLEDKOVÁ DATA)
```json
{
  "Fmax_Phk_Extenzor": 5.5,
  "Fmax_Phk_Flexor": 7.5,
  "table_somatometrie": [
    {
      "datum": "2024-10-15",
      "inicialy": "JN",
      "vek_roky": 35,
      "vyska_cm": 178
    }
  ]
}
```

---

## VARIANTA 1: Vnořená struktura (DOPORUČENÁ) ✅

### Použití v Python:
```python
context = {
    "input": measurement_data,
    "results": results_data
}
```

### Placeholdery v Word:

**Jednoduché hodnoty:**
```
Firma: {{ input.section1_firma.company }}
IČO: {{ input.section1_firma.ico }}
Datum měření: {{ input.section1_firma.measurement_date }}

Pracovník: {{ input.section3_worker_a.full_name }}
Věk: {{ input.section3_worker_a.age_years }} let

Fmax PHK Extenzor: {{ results.Fmax_Phk_Extenzor }} N
Fmax PHK Flexor: {{ results.Fmax_Phk_Flexor }} N
```

**Tabulka somatometrie:**
```jinja2
| Datum | Iniciály | Věk | Výška |
|-------|----------|-----|-------|
{% for row in results.table_somatometrie -%}
| {{ row.datum }} | {{ row.inicialy }} | {{ row.vek_roky }} | {{ row.vyska_cm }} |
{% endfor %}
```

**Časový snímek (table_B4_I21):**
```jinja2
{% for row in results.table_B4_I21 -%}
{{ loop.index }}. {{ row.activity }} - {{ row.time_min }} minut
   PHK extenzory: {{ row.phk_extenzory }} N
   LHK extenzory: {{ row.lhk_extenzory }} N
{% endfor %}
```

**Výhody:**
- ✅ Jasná separace zdrojů dat
- ✅ Žádné kolize klíčů
- ✅ Snadná údržba

**Nevýhody:**
- ⚠️ Delší placeholdery

---

## VARIANTA 2: Plochá struktura

### Použití v Python:
```python
context = {**measurement_data, **results_data}
```

### Placeholdery v Word:

**Jednoduché hodnoty:**
```
Firma: {{ section1_firma.company }}
IČO: {{ section1_firma.ico }}

Fmax PHK Extenzor: {{ Fmax_Phk_Extenzor }} N
```

**Tabulka somatometrie:**
```jinja2
{% for row in table_somatometrie -%}
| {{ row.datum }} | {{ row.inicialy }} | {{ row.vek_roky }} |
{% endfor %}
```

**Výhody:**
- ✅ Kratší placeholdery
- ✅ Jednodušší syntaxe

**Nevýhody:**
- ❌ Riziko kolize klíčů (pokud mají oba JSONy stejný klíč)
- ❌ Není jasné, odkud data pocházejí

---

## VARIANTA 3: Prefixovaná struktura

### Použití v Python:
```python
context = {
    "m": measurement_data,  # m = measurement
    "r": results_data       # r = results
}
```

### Placeholdery v Word:

**Jednoduché hodnoty:**
```
Firma: {{ m.section1_firma.company }}
IČO: {{ m.section1_firma.ico }}

Fmax PHK Extenzor: {{ r.Fmax_Phk_Extenzor }} N
```

**Tabulka somatometrie:**
```jinja2
{% for row in r.table_somatometrie -%}
| {{ row.datum }} | {{ row.inicialy }} | {{ row.vek_roky }} |
{% endfor %}
```

**Výhody:**
- ✅ Krátké prefixy
- ✅ Jasná separace
- ✅ Žádné kolize

**Nevýhody:**
- ⚠️ Musíš si pamatovat, co znamená 'm' a 'r'

---

## 🎯 DOPORUČENÍ

Pro tvůj projekt doporučuji **VARIANTU 1 (vnořená struktura)** protože:

1. **Jasné oddělení zdrojů** - okamžitě vidíš, jestli data jsou vstupní nebo výsledková
2. **Žádné kolize** - můžeš mít stejné klíče v obou JSONech
3. **Snadná údržba** - když přidáš nové pole, hned víš, kam patří
4. **Škálovatelnost** - později můžeš přidat třetí zdroj (např. "calculations")

---

## 📝 PŘÍKLAD: Kompletní Word sekce

```
PROTOKOL O MĚŘENÍ LOKÁLNÍ SVALOVÉ ZÁTĚŽE

Firma: {{ input.section1_firma.company }}
IČO: {{ input.section1_firma.ico }}
Pracoviště: {{ input.section1_firma.workplace }}
Datum měření: {{ input.section1_firma.measurement_date }}

MĚŘENÁ OSOBA A:
Jméno: {{ input.section3_worker_a.full_name }}
Věk: {{ input.section3_worker_a.age_years }} let
Výška: {{ input.section3_worker_a.height_cm }} cm
Lateralita: {{ input.section3_worker_a.laterality }}

VÝSLEDKY MĚŘENÍ:
Fmax PHK Extenzor: {{ results.Fmax_Phk_Extenzor }} N
Fmax PHK Flexor: {{ results.Fmax_Phk_Flexor }} N
Počet pohybů PHK: {{ results.phk_number_of_movements }}

SOMATOMETRICKÁ DATA:
| Datum | Iniciály | Lateralita | Věk | Expozice | Výška | Hmotnost |
|-------|----------|------------|-----|----------|-------|----------|
{% for row in results.table_somatometrie -%}
| {{ row.datum }} | {{ row.inicialy }} | {{ row.lateralita }} | {{ row.vek_roky }} | {{ row.expozice_roky }} | {{ row.vyska_cm }} | {{ row.hmotnost_kg }} |
{% endfor %}

ČASOVÝ SNÍMEK:
{% for row in results.table_B4_I21 -%}
{% if row.activity != 0 -%}
Činnost: {{ row.activity }}
Čas: {{ row.time_min }} min
PHK extenzory: {{ row.phk_extenzory }} N, flexory: {{ row.phk_flexory }} N
LHK extenzory: {{ row.lhk_extenzory }} N, flexory: {{ row.lhk_flexory }} N

{% endif -%}
{% endfor %}
```

---

## 🔄 PODMÍNKOVÉ TEXTY (Conditional Texts)

Aplikace generuje dynamické texty na základě naměřených dat a výsledků. Tyto texty jsou dostupné v `texts` objektu v Word šabloně.

### Dostupné conditional texts:

**1. prvni_text_podminka_pocetdni** - Počet dnů měření
```jinja2
{{ texts.prvni_text_podminka_pocetdni }}
```
Výstup: "Měření probíhalo v jednom dni..." nebo "...ve dvou dnech..."

**2. druhy_text_podminka_limit1** - PHK hygienické limity
```jinja2
{{ texts.druhy_text_podminka_limit1 }}
```
Výstup: Text o překročení/dodržení limitů pro extenzory a flexory PHK

**3. treti_text_podminka_limit1** - LHK hygienické limity
```jinja2
{{ texts.treti_text_podminka_limit1 }}
```
Výstup: Text o překročení/dodržení limitů pro extenzory a flexory LHK

**4. ctvrty_text_podminka** - Rozložení svalových sil
```jinja2
{{ texts.ctvrty_text_podminka }}
```
Výstup: "nejsou" | "ojediněle" | "pravidelně"

**5. paty_text_podminka** - Nadlimitní síly (nad 70% Fmax)
```jinja2
{{ texts.paty_text_podminka }}
```
Výstup: Komplexní text podle kombinace nadlimitních sil ve 4 svalových skupinách

**6. sesty_text_podminka** - Kontrola hodnot nad 100 (pouze force_over_70)
```jinja2
{{ texts.sesty_text_podminka }}
```
Výstup: "je" nebo "není"

**Logika výpočtu:**
- Kontroluje POUZE 4 hodnoty `force_over_70_*` z řádku 21 (Celkem)
- Pokud jakákoliv z těchto hodnot > 100 → "je"
- Pokud všechny hodnoty ≤ 100 → "není"
- IGNORUJE hodnoty `force_55_70_*` (ty se neberou v úvahu)

**7. sedmy_text_podminka** - Limit velkých sil (55-70% Fmax) ⭐ NOVÉ
```jinja2
{{ texts.sedmy_text_podminka }}
```

**Výstupy (celé věty):**
- ✅ `"nepřekračuje u žádné z měřených svalových skupin rukou a předloktí daný hygienický limit."`
- ⚠️ `"překračuje u měřených svalových skupin rukou a předloktí daný hygienický limit."`

**Logika výpočtu:**
- limit = (délka_směny_v_minutách / 2) + 360
- součet = suma 4 hodnot force_55_70_* z řádku 21 (Celkem)
- pokud součet > limit → věta s "překračuje"
- pokud součet ≤ limit → věta s "nepřekračuje"

**⚙️ Technické detaily:**
- Bezpečná konverze work_duration (zpracovává string i číslo)
- Error handling pro neplatné hodnoty → fallback na "nepřekračuje"

**Příklad použití v Word šabloně:**
```
Velké svalové síly (55-70% Fmax) {{ texts.sedmy_text_podminka }}
```

**Výsledek v dokumentu:**
```
Velké svalové síly (55-70% Fmax) nepřekračuje u žádné z měřených svalových
skupin rukou a předloktí daný hygienický limit.
```

**8. osmy_text_podminka** - Seznam činností s force_over_70 > 100 ⭐ NOVÉ
```jinja2
{{ texts.osmy_text_podminka }}
```

**Výstupy:**
- Prázdný string (`""`) - pokud sesty_text_podminka = "není"
- Prázdný string (`""`) - pokud sesty = "je" ale žádná konkrétní činnost nemá >100
- Seznam činností oddělený čárkami - např. `"Zakládání, Bezpečnostní přestávka"`

**Logika výpočtu:**
1. Zkontroluj `sesty_text_podminka` (force_over_70 v řádku 21 "Celkem")
2. Pokud "není" → prázdný string
3. Pokud "je":
   - Projdi všechny řádky table_force_distribution (kromě "21")
   - Pro každý řádek zkontroluj 4 hodnoty force_over_70_*
   - Pokud jakákoliv > 100 → přidej `activity` do seznamu
   - Vrať seznam oddělený čárkami

**Příklad použití v Word šabloně:**
```jinja2
{% if texts.osmy_text_podminka %}
Konkrétně se jedná o tyto činnosti: {{ texts.osmy_text_podminka }}.
{% endif %}
```

**Výsledek v dokumentu:**
```
Konkrétně se jedná o tyto činnosti: Zakládání, Bezpečnostní přestávka.
```

Nebo pokud je prázdný:
```
(nic se nevypíše)
```

### Jak jsou texty generovány:

V Python kódu (`generate_word_from_two_sources.py`):
```python
from core.text_generator import generate_conditional_texts

# Generuj conditional texts
texts = generate_conditional_texts(measurement_data, results_data)

# Vytvoř kontext pro šablonu
context = {
    "input": measurement_data,
    "results": results_data,
    "texts": texts  # ← Tady jsou conditional texts
}
```

V Word šabloně:
```jinja2
Měření probíhalo: {{ texts.prvni_text_podminka_pocetdni }}

Hygienické limity: {{ texts.druhy_text_podminka_limit1 }}

Limit velkých sil: {{ texts.sedmy_text_podminka }}
```

---

## 🚀 JAK TO POUŽÍT

1. **Vyber variantu** v `generate_word_from_two_sources.py`
2. **Uprav Word šablonu** podle vybrané varianty
3. **Spusť generování:**
   ```bash
   python generate_word_from_two_sources.py
   ```
4. **Zkontroluj výsledek** v `LSZ_vyplneny.docx`
