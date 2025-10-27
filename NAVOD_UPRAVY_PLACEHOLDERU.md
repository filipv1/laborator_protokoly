# NÁVOD: Jak upravit placeholdery v Word šablonách

Tento návod ti ukáže, jak přepsat placeholdery v Word šablonách, aby fungovaly nový univerzální filtr pro formátování čísel.

---

## 📋 CO SE ZMĚNILO (POŽADAVKY 3, 4, 5, 7)

### ✅ Nové funkcionality:

**JEDEN UNIVERZÁLNÍ FILTR `|czech` pro všechna čísla!**

1. **Zaokrouhlení na 1 des. místo** → automaticky
2. **Čárka místo tečky** (8.9 → 8,9) → automaticky
3. **Mezery pro tisíce** (2222 → 2 222) → automaticky
4. **Auto-detekce** celé vs desetinné číslo → automaticky
5. **Dnešní datum** → placeholder `{{ today_date }}`

---

## 🎯 JEDEN FILTR PRO VŠECHNO: `|czech`

### Výhody:

- ✅ **Auto-detekce:** Automaticky pozná, jestli je číslo celé nebo desetinné
- ✅ **Univerzální:** Funguje pro VŠECHNA čísla (malá i velká, celá i desetinná)
- ✅ **Jednoduché:** Nemusíš přemýšlet, který filtr použít

### Jak to funguje:

```
{{ 8.55|czech }}         → "8,6"        (desetinné, zaokrouhleno)
{{ 450|czech }}          → "450"        (celé, bez mezer)
{{ 2222|czech }}         → "2 222"      (celé, s mezerami)
{{ 12345.67|czech }}     → "12 345,7"   (desetinné + mezery!)
{{ 5.0|czech }}          → "5"          (celé, i když float)
```

---

## 🔧 JAK UPRAVIT PLACEHOLDERY V WORD ŠABLONĚ

### PRAVIDLO 1: Všechna čísla → přidat `|czech`

**Platí pro:** Všechna čísla z Excelu (Fmax, počty pohybů, hodnoty v tabulkách, atd.).

#### Příklad 1: Fmax hodnoty (desetinné)
```
PŘED:  {{ Fmax_Phk_Flexor }} % Fmax
PO:    {{ Fmax_Phk_Flexor|czech }} % Fmax
```

**Výsledek:**
- `8.55` → `8,6`
- `11.899999` → `11,9`
- `7.2` → `7,2`

#### Příklad 2: Počty pohybů (celé)
```
PŘED:  PHK ({{ phk_number_of_movements }})
PO:    PHK ({{ phk_number_of_movements|czech }})
```

**Výsledek:**
- `450` → `450` (bez mezer)
- `2222` → `2 222` (s mezerami)
- `33333` → `33 333`

#### Příklad 3: Velké desetinné číslo
```
PŘED:  {{ table_row.some_value }}
PO:    {{ table_row.some_value|czech }}
```

**Výsledek:**
- `12345.67` → `12 345,7` (mezery + čárka!)

---

### PRAVIDLO 2: Texty → PONECHAT BEZ ZMĚNY

**Platí pro:** Všechny textové placeholdery (názvy, adresy, podmíněné texty atd.).

```
{{ section2_firma.company }}  ← BEZ ZMĚNY
{{ section_generated_texts.druhy_text_podminka_limit1 }}  ← BEZ ZMĚNY
```

---

### PRAVIDLO 3: Dnešní datum → použít `{{ today_date }}`

**Nový placeholder:**
```
Datum vytvoření protokolu: {{ today_date }}
```

**Výsledek:**
- Automaticky se vloží dnešní datum ve formátu `dd.mm.yyyy`
- Příklad: `27.10.2025`

---

## 📝 KOMPLETNÍ PŘÍKLAD ÚPRAVY

### Původní text v šabloně:
```
{{Fmax_Phk_Flexor}} % Fmax. Průměrné počty pohybů PHK ({{phk_number_of_movements}}) {{section_generated_texts.druhy_text_podminka_limit1}}
```

### Upravený text v šabloně:
```
{{Fmax_Phk_Flexor|czech}} % Fmax. Průměrné počty pohybů PHK ({{phk_number_of_movements|czech}}) {{section_generated_texts.druhy_text_podminka_limit1}}
```

### Výsledek ve vygenerovaném Wordu:
```
PŘED: 8.55 % Fmax. Průměrné počty pohybů PHK (2222) překračují...
PO:   8,6 % Fmax. Průměrné počty pohybů PHK (2 222) překračují...
```

---

## 🔍 SEZNAM PLACEHOLDERŮ, KTERÉ MUSÍŠ UPRAVIT

### Všechna čísla (přidat `|czech`):

**Skalární hodnoty:**
```
{{ Fmax_Phk_Extenzor|czech }}
{{ Fmax_Phk_Flexor|czech }}
{{ Fmax_Lhk_Extenzor|czech }}
{{ Fmax_Lhk_Flexor|czech }}
{{ phk_number_of_movements|czech }}
{{ lhk_number_of_movements|czech }}
```

**V tabulkách (for loop):**
```
{% for row in table_somatometrie %}
  Výška: {{ row.vyska_cm|czech }}
  Váha: {{ row.hmotnost_kg|czech }}
  Věk: {{ row.vek_roky|czech }}
{% endfor %}

{% for row in table_B4_I21 %}
  Čas: {{ row.time_min|czech }}
  PHK Ext: {{ row.phk_extenzory|czech }}
  PHK Flex: {{ row.phk_flexory|czech }}
  LHK Ext: {{ row.lhk_extenzory|czech }}
  LHK Flex: {{ row.lhk_flexory|czech }}
{% endfor %}

{% for row in table_force_distribution %}
  Pohyby 55-70% PHK Ext: {{ row.force_55_70_phk_extenzory|czech }}
  Pohyby >70% PHK Ext: {{ row.force_over_70_phk_extenzory|czech }}
  (atd. pro všechny číselné sloupce)
{% endfor %}
```

### Texty (PONECHAT BEZ ZMĚNY):

```
{{ section2_firma.company }}
{{ section2_firma.address }}
{{ section4_worker_a.full_name }}
{{ section_generated_texts.prvni_text_podminka_pocetdni }}
{{ section_generated_texts.druhy_text_podminka_limit1 }}
{{ section_generated_texts.sedmy_text_podminka }}
```

---

## ⚙️ POSTUP ÚPRAVY

1. **Otevři Word šablonu** (např. `lsz_placeholdery_v2.docx`)

2. **Stiskni `Ctrl+F`** (najít a nahradit)

3. **Najdi placeholder:**
   - Hledej: `{{ Fmax_Phk_Flexor }}`

4. **Přepiš na:**
   - `{{ Fmax_Phk_Flexor|round1 }}`

5. **Opakuj pro všechny placeholdery** podle seznamu výše

6. **Ulož šablonu**

---

## 🧪 JAK OTESTOVAT

1. Vygeneruj Word protokol přes GUI
2. Otevři vygenerovaný Word dokument
3. Zkontroluj:
   - ✅ Desetinná čísla mají 1 des. místo a čárku (např. `8,6`)
   - ✅ Velká čísla mají mezery (např. `2 222`)
   - ✅ Datum je správně (např. `27.10.2025`)

---

## ❓ FAQ

**Q: Co když zapomenu přidat filtr `|czech`?**
A: Číslo se vypíše v původním formátu (např. `8.55` místo `8,6`).

**Q: Můžu použít filtr v podmínkách (`{% if %}`)?**
A: Ano! Např. `{% if Fmax_Phk_Extenzor|czech > "5" %}`

**Q: Co když filtr aplikuji na text?**
A: Filtr vrátí hodnotu beze změny (žádná chyba).

**Q: Musím rozlišovat desetinná a celá čísla?**
A: **NE!** Filtr `|czech` automaticky detekuje typ čísla a aplikuje správné formátování.

**Q: Funguje to i pro velká desetinná čísla?**
A: **ANO!** Např. `12345.67|czech` → `"12 345,7"` (mezery + čárka).

**Q: Co když mám číslo jako `5.0` (float, ale celé)?**
A: Filtr automaticky pozná, že je to celé číslo → `"5"` (bez desetinné části).

---

## 📦 DALŠÍ INFO

- Filtr je implementovaný v `generate_word_from_two_sources.py`
- Funkce: `format_czech_number()` (jedna univerzální funkce!)
- Automaticky se registruje před renderingem šablony
- **34 automatických testů** zajišťuje správnou funkčnost

---

## 🎯 RYCHLÝ PŘEHLED

### CO MUSÍŠ UDĚLAT:

1. **Otevři Word šablonu**
2. **Najdi všechny číselné placeholdery** (Ctrl+F: `{{ F`, `{{ phk`, `{{ lhk`, atd.)
3. **Přidej `|czech` za každý placeholder s číslem:**
   - `{{ Fmax_Phk_Extenzor }}` → `{{ Fmax_Phk_Extenzor|czech }}`
   - `{{ phk_number_of_movements }}` → `{{ phk_number_of_movements|czech }}`
4. **Textové placeholdery PONECHAT BEZ ZMĚNY:**
   - `{{ section2_firma.company }}` → **BEZE ZMĚNY**
5. **Přidej dnešní datum (volitelně):**
   - `{{ today_date }}`
6. **Ulož šablonu**
7. **Otestuj generování!**

### JEDNODUCHÁ PRAVIDLA:

- ✅ **Číslo?** → Přidej `|czech`
- ✅ **Text?** → Nech beze změny
- ✅ **Datum?** → Použij `{{ today_date }}`

**Jedna funkce pro všechno = méně chyb!** 🚀

---

✅ **Hotovo! Nyní můžeš začít upravovat placeholdery v Word šablonách.**
