# LSZ Template - Dokumentace

**Vytvořeno:** Automaticky z `LSZ_XX_Firma_Pozice_zakomentovano.docx`
**Výstup:** `LSZ_template.docx`
**Stav:** ✅ Připraveno k použití (s několika poznámkami níže)

---

## ✅ Co Bylo Automaticky Nahrazeno

### 1. Základní Údaje (z JSON)

```
✓ Číslo protokolu: LSZ {{measurement_month}}/{{measurement_year}}
✓ Datum vyhotovení: {{measurement_date}}
✓ Firma: {{section2_firma.company}}
✓ IČO: {{section2_firma.ico}}
✓ Profese: {{section2_firma.profession_name}}
✓ Pracoviště: {{section2_firma.workplace}}
✓ Místo měření: {{section2_firma.measurement_location}}
✓ Směnnost: {{section2_firma.shift_pattern}}
✓ Měření provedl: {{section6_final.measured_by}}
```

### 2. Podmíněný Text (1 vs 2 Pracovníci)

```
✓ Rozsah měření:
   "Měřen{{plural_ending}} {{worker_count_text}} pracovní{{plural_worker}} – {{workers_gender}}"

✓ Měřené osoby:
   "Měření se zúčastnil{{plural_ending}} {{worker_count_text}} zapracovan{{plural_adj}} zaměstnan{{plural_noun}}"

✓ Druhý pracovník (všude s podmínkou):
   {% if has_worker_b %}...data pracovníka B...{% endif %}
```

### 3. Údaje o Pracovnících (Tabulky)

**Table 3 - Antropometrické údaje:**
```
✓ Pracovník A:
   {{section4_worker_a.initials}}
   {{section4_worker_a.laterality}}
   {{section4_worker_a.age_years}}
   {{section4_worker_a.exposure_length_years}}
   {{section4_worker_a.height_cm}}
   {{section4_worker_a.weight_kg}}

✓ Pracovník B (podmíněný):
   {% if has_worker_b %}{{section5_worker_b.*}}{% endif %}

✓ Průměrné hodnoty:
   {{workers_age_avg}}
   {{workers_exposure_avg}}
   {{workers_height_avg}}
   {{workers_weight_avg}}
```

### 4. Časový Snímek

**Table 2 bude vyplněna dynamicky z:**
```
{{time_schedule.line1.operation}}
{{time_schedule.line1.time_min}}
{{time_schedule.line1.pieces_count}}
... atd pro line2, line3, ...
{{time_schedule_total.time_min}}
{{time_schedule_total.pieces_count}}
```

### 5. Výsledky z LSZ Excelu

**Přidány placeholdery pro hodnoty z Excelu:**

```
✓ Celkové hodnocení:
   {{excel_lsz.phk_extenzory_avg}} % Fmax
   {{excel_lsz.phk_flexory_avg}} % Fmax
   {{excel_lsz.phk_pohyby_total}}
   {{excel_lsz.lhk_extenzory_avg}} % Fmax
   {{excel_lsz.lhk_flexory_avg}} % Fmax
   {{excel_lsz.lhk_pohyby_total}}

✓ Podmíněné hodnocení:
   {% if excel_lsz.phk_over_limit %}překračují{% else %}nepřekračují{% endif %}
   {% if excel_lsz.high_forces_regular %}pravidelně{% else %}ojediněle{% endif %}
   {% if excel_lsz.extreme_forces %}dochází{% else %}nedochází{% endif %}

✓ Kategorie:
   {{excel_lsz.category}}

✓ EMG hodnoty pro jednotlivé pracovníky:
   {{excel_lsz.worker_a.emg1_avg}}
   {{excel_lsz.worker_a.emg2_avg}}
   {{excel_lsz.worker_a.emg3_avg}}
   {{excel_lsz.worker_a.emg4_avg}}
   {{excel_lsz.worker_a.measurement_time_range}}
   {{excel_lsz.worker_a.measurement_duration}}
```

### 6. Norma vs Čas (Podmíněné Sekce)

```
✓ {% if measurement_type == 'norma' %}
   Text o normě...
   {% endif %}

✓ {% if measurement_type == 'cas' %}
   Text o časovém snímku...
   {% endif %}
```

---

## ⚠️ CO CHYBÍ V JSON A BUDE POTŘEBA DOPLNIT

### 1. Adresní Údaje Firmy

**Aktuálně v šabloně:**
```
{{section2_firma.address_line1}}
{{section2_firma.postal_code}} {{section2_firma.city}}
```

**Řešení:**
Přidat do GUI wizardu (Page2_Firma) pole:
- Adresa (ulice, číslo)
- PSČ
- Město

### 2. Iniciály Pracovníků

**Aktuálně v šabloně:**
```
{{section4_worker_a.initials}}  // např. "F. T."
{{section5_worker_b.initials}}  // např. "S. O."
{{worker_initials}}             // "F. T., S. O." nebo jen "F. T."
```

**Řešení:**
Buď:
- A) Přidat pole "Iniciály" do wizardu
- B) Automaticky generovat z celého jména (Jan Novák → J. N.)

### 3. Popisy Práce (Volné Texty)

**Aktuálně v šabloně:**
```
{{work_description}}              // Popis pracovní činnosti (1. odstavec)
{{work_cycle_description}}        // Popis pracovního cyklu (2. odstavec)
{{workplace_dimensions}}          // Rozměry pracoviště (3. odstavec)
```

**Tyto texty jsou velmi specifické pro každé měření!**

**Možná řešení:**
1. **Nejjednodušší:** Přidat do GUI 3 velká textová pole (QTextEdit)
2. **Alternativa:** Parsovat z nahraného Word dokumentu (pokud tam jsou)
3. **Hybridní:** Načíst z Wordu, ale umožnit editaci v GUI

### 4. Detailní Časové Údaje

**Aktuálně v šabloně:**
```
{{shift_duration}}          // Délka směny (480 min)
{{break_duration}}          // Přestávka (30 min)
{{work_time}}               // Čistá práce (415 min)
{{safety_break}}            // Bezpečnostní přestávky (35 min)
{{work_duration_total}}     // Celková doba výkonu
```

**Řešení:**
Většina lze vypočítat z časového snímku:
```python
shift_duration = 480  # Standard
break_duration = 30   # Z časového snímku (řádek "Přestávka na jídlo")
safety_break = časový snímek["Bezpečnostní přestávky"].time_min
work_time = shift_duration - break_duration - safety_break
work_duration_total = work_time + safety_break
```

### 5. Typ Měření (Norma vs Čas)

**Aktuálně v šabloně:**
```
{% if measurement_type == 'norma' %}...{% endif %}
{% if measurement_type == 'cas' %}...{% endif %}
```

**Řešení:**
Přidat do Page0_VyberSouboru:
```python
measurement_type_combo = QComboBox()
measurement_type_combo.addItems(["Norma", "Čas"])
```

### 6. Průměrné Hodnoty Pracovníků

**Aktuálně v šabloně:**
```
{{workers_age_avg}}
{{workers_exposure_avg}}
{{workers_height_avg}}
{{workers_weight_avg}}
```

**Řešení:**
Vypočítat v Pythonu při přípravě context:
```python
if has_worker_b:
    workers_age_avg = (worker_a.age + worker_b.age) / 2
else:
    workers_age_avg = worker_a.age
```

---

## 📊 VÝSLEDKY Z LSZ EXCELU - CO IDENTIFIKOVAT

**Musíš projít vyplněný LSZ Excel a najít tyto hodnoty:**

### Základní EMG Výsledky

```
excel_lsz.phk_extenzory_avg    → % Fmax (např. 8.1)
excel_lsz.phk_flexory_avg      → % Fmax (např. 9.4)
excel_lsz.lhk_extenzory_avg    → % Fmax (např. 8.6)
excel_lsz.lhk_flexory_avg      → % Fmax (např. 7.8)
```

**Kde v Excelu:**
Nejspíš list "Výsledky" nebo "Vyhodnocení", buňky s průměrnými hodnotami.

### Počty Pohybů

```
excel_lsz.phk_pohyby_total     → Celkový počet pohybů PHK (např. 12 500)
excel_lsz.lhk_pohyby_total     → Celkový počet pohybů LHK (např. 12 200)
```

### Hodnocení (Boolean Flagy)

```
excel_lsz.phk_over_limit       → True/False (překročení limitu PHK)
excel_lsz.lhk_over_limit       → True/False (překročení limitu LHK)
excel_lsz.high_forces_regular  → True/False (pravidelné velké síly)
excel_lsz.high_forces_over_limit → True/False (překročení limitu velkých sil)
excel_lsz.extreme_forces       → True/False (nadlimitní síly >70%)
excel_lsz.extreme_forces_activities → String (při jakých činnostech)
excel_lsz.extreme_forces_regular → True/False (pravidelné nadlimitní síly)
```

### Kategorie

```
excel_lsz.category  → "1" nebo "2" nebo "3" nebo "4"
```

**Kde v Excelu:**
Pravděpodobně list "Vyhodnocení", buňka s textem "Kategorie 2" nebo podobně.

### EMG Hodnoty pro Jednotlivé Pracovníky

```
excel_lsz.worker_a.emg1_avg    → EMG_1 průměr (např. 8.10)
excel_lsz.worker_a.emg2_avg    → EMG_2 průměr (např. 9.40)
excel_lsz.worker_a.emg3_avg    → EMG_3 průměr (např. 8.60)
excel_lsz.worker_a.emg4_avg    → EMG_4 průměr (např. 7.80)
excel_lsz.worker_a.measurement_time_range → "01.02.23 12:27:18 - 13:42:37"
excel_lsz.worker_a.measurement_duration → "00:00:00" (formát h:mm:ss)

excel_lsz.worker_b.*           → Stejné pro pracovníka B (pokud existuje)
```

---

## 📝 TABULKY - CO BUDE DYNAMICKY VYPLNĚNO

### Table 2 - Časový Snímek

**Struktura:**
```
Číslo | Rozpis operací | Čas/směna [min] | Počet ks/směna
------|----------------|-----------------|----------------
  1.  | {{line1.operation}} | {{line1.time_min}} | {{line1.pieces_count}}
  2.  | {{line2.operation}} | {{line2.time_min}} | {{line2.pieces_count}}
 ...  | ...            | ...             | ...
Celkem| Celkem:        | {{total.time_min}} | {{total.pieces_count}}
```

**Data z:**
`section1_uploaded_docx.time_schedule`

### Table 5-8 - Výsledkové Tabulky EMG

**Tyto tabulky obsahují:**
- Síly % Fmax pro jednotlivé operace
- Počty pohybů
- Rozložení vynakládaných sil

**Data z:**
LSZ Excel soubor - detailní hodnoty pro každou operaci a každého pracovníka.

**Řešení:**
Při implementaci `excel_reader.py` bude potřeba načíst celé tabulky z Excelu a vyplnit je do Word šablony.

---

## 🎯 NEXT STEPS - CO TEĎKA UDĚLAT

### 1. Zkontroluj Šablonu

Otevři: `app/templates/word/LSZ_template.docx`

**Zkontroluj:**
- ✅ Jsou placeholdery správně?
- ✅ Nic není rozbité?
- ✅ Formátování je zachováno?

### 2. Identifikuj Výsledky v LSZ Excelu

Otevři: `projects/6969_Fyrma/LSZ_6969_Fyrma.xlsm`

**Vytvoř seznam:**
```
Název výsledku                | List         | Buňka | Příklad hodnoty
------------------------------|--------------|-------|------------------
PHK extenzory průměr          | ???          | ???   | 8.1
PHK flexory průměr            | ???          | ???   | 9.4
LHK extenzory průměr          | ???          | ???   | 8.6
...
Kategorie LSZ                 | ???          | ???   | 2
```

### 3. Rozhodni o Chybějících Polích

**Adresní údaje:**
- Přidat do wizardu? ANO/NE

**Iniciály:**
- Přidat pole do wizardu? ANO
- Nebo generovat automaticky? ANO

**Popisy práce:**
- Přidat textová pole do wizardu? ANO
- Nebo parsovat z Wordu? ANO
- Nebo obojí? ANO

**Typ měření (Norma/Čas):**
- Přidat výběr do wizardu? ANO/NE

### 4. Pošli Feedback

**Až zkontro
luješ šablonu, napiš mi:**
1. ✅ Je šablona OK, nebo něco chybí/je špatně?
2. 📊 Seznam výsledků z LSZ Excelu (buňky)
3. 🎯 Rozhodnutí o chybějících polích (viz bod 3)

**Pak můžu:**
- Doplnit GUI wizard o chybějící pole
- Implementovat `excel_reader.py` pro načítání výsledků
- Implementovat `word_generator.py` pro generování protokolů

---

## 💡 POZNÁMKY

### Pluralizace v Češtině

Pro správnou pluralizaci jsem přidal pomocné proměnné:

```python
plural_ending = "i" if has_worker_b else ""      # Měřeni / Měřen
plural_worker = "ci" if has_worker_b else "k"    # pracovníci / pracovník
plural_adj = "í" if has_worker_b else "ý"        # zapracovaní / zapracovaný
plural_noun = "ci" if has_worker_b else "ec"     # zaměstnanci / zaměstnanec

worker_count_text = "dva" if has_worker_b else "jeden"
```

### Jinja2 Syntax

V šabloně jsou použity Jinja2 konstrukce:
- `{{variable}}` - zobrazení proměnné
- `{% if condition %}...{% endif %}` - podmínka
- `{% for item in list %}...{% endfor %}` - smyčka (pro tabulky)

Tyto budou zpracovány knihovnou `docxtpl` při generování.

### Dynamické Tabulky

Tabulky s proměnným počtem řádků (časový snímek, výsledky) budou vyplněny při generování pomocí `docxtpl` knihovny, která umí:
- Duplikovat řádky tabulky podle dat
- Vyplnit buňky hodnotami
- Zachovat formátování

---

**Šablona je připravena! Co dál? 🚀**
