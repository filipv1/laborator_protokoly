# LSZ Word Šablona - Průvodce Placeholdery

Tento dokument ti pomůže vytvořit Word šablonu pro LSZ protokol.

## 📋 PLACEHOLDERY - DATA Z JSON

### HLAVIČKA PROTOKOLU
```
{{section2_firma.evidence_number}}      - Evidenční číslo (např. "6969")
{{section2_firma.measurement_date}}     - Datum měření (např. "13.10.2025")
```

### 1. ÚDAJE O FIRMĚ
```
{{section2_firma.company}}              - Název firmy (např. "BOSAL CR s.r.o.")
{{section2_firma.profession_name}}      - Název profese (např. "Obsluha lisu")
{{section2_firma.ico}}                  - IČO firmy (např. "12345678")
{{section2_firma.workplace}}            - Pracoviště (např. "Hala 1")
{{section2_firma.measurement_location}} - Místo měření (např. "Říčany")
```

### 2. ÚDAJE O MĚŘENÍ
```
{{section2_firma.shift_pattern}}               - Směnnost (např. "Denní")
{{section3_additional_data.set_standard}}      - Stanovená norma (např. "5")
{{section3_additional_data.product_type}}      - Typ výrobku (např. "Výfuk")
{{section3_additional_data.work_performed}}    - Práce vykonávaná (stoj/sed/chůze)
{{section3_additional_data.work_plane_height}} - Výška pracovní roviny (např. "150 cm")
{{section3_additional_data.manual_load_min_kg}} - Min. hmotnost břemen (kg)
{{section3_additional_data.manual_load_max_kg}} - Max. hmotnost břemen (kg)
```

### 3. ÚDAJE O PRACOVNÍKOVI
```
{{section4_worker_a.full_name}}           - Jméno a příjmení (např. "Jan Novák")
{{section4_worker_a.age_years}}           - Věk v letech (např. 35)
{{section4_worker_a.exposure_length_years}} - Délka expozice v letech (např. 5)
{{section4_worker_a.height_cm}}           - Výška v cm (např. 180)
{{section4_worker_a.weight_kg}}           - Váha v kg (např. 85.5)
{{section4_worker_a.laterality}}          - Lateralita (pravostranná/levostranná)
{{section4_worker_a.grip_strength_phk_n}} - Síla stisku PHK v N (např. 450.0)
{{section4_worker_a.grip_strength_lhk_n}} - Síla stisku LHK v N (např. 420.0)
```

### 4. MĚŘÍCÍ ZAŘÍZENÍ
```
{{section4_worker_a.emg_holter}}         - EMG Holter (A/B/C/D/E/F)
{{section4_worker_a.polar}}              - Polar (1-8)
{{section4_worker_a.chest_strap_number}} - Číslo hrudního pásu (např. "1")
{{section4_worker_a.measurement_start}}  - Začátek měření (např. "08:00")
{{section4_worker_a.work_duration}}      - Doba výkonu práce v min (např. "480")
{{section4_worker_a.breaks}}             - Přestávky v min (např. "30")
{{section4_worker_a.code}}               - Kód (pokud se používá)
```

### 5. ČASOVÝ SNÍMEK (TABULKA)

**Pro tabulku použij Jinja2 loop:**

```
{% for line in time_schedule %}
{{line.number}} | {{line.operation}} | {{line.time_min}} min | {{line.pieces_count or '-'}} ks
{% endfor %}

CELKEM: {{time_schedule_total.time_min}} min | {{time_schedule_total.pieces_count}} ks
```

**Nebo pokud chceš jednotlivé řádky:**
```
{{time_schedule.line1.number}}        - Číslo řádku 1
{{time_schedule.line1.operation}}     - Operace (např. "Zakládání")
{{time_schedule.line1.time_min}}      - Čas v minutách (např. 415)
{{time_schedule.line1.pieces_count}}  - Počet kusů (např. 180)
// ... line2, line3, atd.

{{time_schedule.total.time_min}}      - Celkový čas
{{time_schedule.total.pieces_count}}  - Celkový počet kusů
```

### 6. ZÁVĚR
```
{{section6_final.measured_by}}  - Měření provedl (např. "Ing. Novák")
{{section6_final.notes}}        - Poznámky (volný text)
```

---

## 🔴 PLACEHOLDERY - VÝSLEDKY Z LSZ EXCELU

**DŮLEŽITÉ:** Tyto hodnoty jsou ve vyplněném LSZ Excel souboru!
Musíš projít Excel a určit, v kterých buňkách jsou následující výsledky:

### VÝSLEDKY MĚŘENÍ LSZ
```
{{excel_lsz.category}}              - Kategorie LSZ (např. "Kategorie 1")
                                      → Buňka v Excelu: _________

{{excel_lsz.emg_phk_avg}}          - EMG PHK průměr (např. "45.2 %MVC")
                                      → Buňka v Excelu: _________

{{excel_lsz.emg_lhk_avg}}          - EMG LHK průměr (např. "42.1 %MVC")
                                      → Buňka v Excelu: _________

{{excel_lsz.emg_phk_max}}          - EMG PHK maximum (např. "78.5 %MVC")
                                      → Buňka v Excelu: _________

{{excel_lsz.emg_lhk_max}}          - EMG LHK maximum (např. "75.3 %MVC")
                                      → Buňka v Excelu: _________

{{excel_lsz.recommendation}}        - Doporučení (např. "Práce je přípustná")
                                      → Buňka v Excelu: _________

// Přidej další výsledky, které chceš v protokolu
```

---

## 📋 CHECKLIST - CO UDĚLAT PŘI VYTVÁŘENÍ ŠABLONY

1. **Otevři vzorový LSZ Word protokol od laboratoře**
   - [ ] Máš vzorový protokol?
   - [ ] Je vyplněný daty (abys viděl, co kam patří)?

2. **Nahraď statické texty placeholdery**
   ```
   Bylo:  Firma: BOSAL CR s.r.o.
   Bude:  Firma: {{section2_firma.company}}
   ```

3. **Pro časový snímek vytvoř tabulku**
   - [ ] V Wordu vytvoř tabulku (Číslo | Operace | Čas | Kusy)
   - [ ] Do řádků vlož Jinja2 loop (viz výše)

4. **Identifikuj výsledky v LSZ Excel souboru**
   - [ ] Otevři vyplněný LSZ Excel
   - [ ] Najdi list s výsledky (např. "Vyhodnocení")
   - [ ] Zapiš si buňky s výsledky (M15, N20, atd.)
   - [ ] Vytvoř seznam: název výsledku → buňka

5. **Přidej placeholdery pro výsledky**
   ```
   Kategorie LSZ: {{excel_lsz.category}}
   EMG PHK průměr: {{excel_lsz.emg_phk_avg}} %MVC
   ```

6. **Ulož jako LSZ_template.docx**
   - [ ] Ulož do: `app/templates/word/LSZ_template.docx`

---

## 🎯 PŘÍKLAD - JAK BY MOHLA VYPADAT ČÁST ŠABLONY

```
PROTOKOL O MĚŘENÍ LOKÁLNÍ SVALOVÉ ZÁTĚŽE

Evidenční číslo: {{section2_firma.evidence_number}}
Datum měření: {{section2_firma.measurement_date}}

===============================================

1. IDENTIFIKAČNÍ ÚDAJE

Firma:          {{section2_firma.company}}
IČO:            {{section2_firma.ico}}
Profese:        {{section2_firma.profession_name}}
Pracoviště:     {{section2_firma.workplace}}
Místo měření:   {{section2_firma.measurement_location}}

===============================================

2. ÚDAJE O MĚŘENÍ

Směnnost:              {{section2_firma.shift_pattern}}
Typ výrobku:           {{section3_additional_data.product_type}}
Práce vykonávaná:      {{section3_additional_data.work_performed}}
Výška pracovní roviny: {{section3_additional_data.work_plane_height}} cm

===============================================

3. PRACOVNÍK

Jméno:              {{section4_worker_a.full_name}}
Věk:                {{section4_worker_a.age_years}} let
Délka expozice:     {{section4_worker_a.exposure_length_years}} let
Antropometrie:      {{section4_worker_a.height_cm}} cm / {{section4_worker_a.weight_kg}} kg
Lateralita:         {{section4_worker_a.laterality}}

Síla stisku ruky:
- PHK: {{section4_worker_a.grip_strength_phk_n}} N
- LHK: {{section4_worker_a.grip_strength_lhk_n}} N

Měřící zařízení:
- EMG Holter:       {{section4_worker_a.emg_holter}}
- Polar:            {{section4_worker_a.polar}}
- Hrudní pás č.:    {{section4_worker_a.chest_strap_number}}

===============================================

4. ČASOVÝ SNÍMEK PRACOVNÍ SMĚNY

[TABULKA]
Číslo | Operace/Činnost | Čas [min] | Počet kusů
------|-----------------|-----------|------------
{% for line in time_schedule %}
{{line.number}} | {{line.operation}} | {{line.time_min}} | {{line.pieces_count or '-'}}
{% endfor %}
------|-----------------|-----------|------------
CELKEM | | {{time_schedule_total.time_min}} | {{time_schedule_total.pieces_count}}

===============================================

5. VÝSLEDKY MĚŘENÍ

Kategorie LSZ: {{excel_lsz.category}}

EMG - Pravá horní končetina (PHK):
- Průměr: {{excel_lsz.emg_phk_avg}} %MVC
- Maximum: {{excel_lsz.emg_phk_max}} %MVC

EMG - Levá horní končetina (LHK):
- Průměr: {{excel_lsz.emg_lhk_avg}} %MVC
- Maximum: {{excel_lsz.emg_lhk_max}} %MVC

Doporučení: {{excel_lsz.recommendation}}

===============================================

6. ZÁVĚR

Měření provedl: {{section6_final.measured_by}}

Poznámky:
{{section6_final.notes}}
```

---

## 🔧 JAK PRACOVAT S EXCEL VÝSLEDKY

### Krok 1: Identifikuj Buňky v LSZ Excel

Otevři vyplněný `LSZ_6969_Fyrma.xlsm` a najdi:

**Příklad (předpokládám):**
```
List: "Vyhodnocení" nebo "Výsledky"

Buňka M15: Kategorie LSZ = "Kategorie 1"
Buňka N20: EMG PHK průměr = 45.2
Buňka N21: EMG PHK max = 78.5
Buňka O20: EMG LHK průměr = 42.1
Buňka O21: EMG LHK max = 75.3
Buňka P25: Doporučení = "Práce je přípustná"
```

### Krok 2: Vytvoř Config Soubor

Až identifikuješ buňky, vytvoříme:
```python
# config/excel_results_mappings.py

LSZ_RESULTS_MAPPING = {
    "sheet": "Vyhodnocení",  # Název listu
    "results": {
        "category": "M15",
        "emg_phk_avg": "N20",
        "emg_phk_max": "N21",
        "emg_lhk_avg": "O20",
        "emg_lhk_max": "O21",
        "recommendation": "P25"
    }
}
```

---

## ✅ TVŮJ AKČNÍ PLÁN

### FÁZE 1: Příprava Šablony (děláš TY)

1. **Vezmi vzorový LSZ protokol od laboratoře**
   - Pokud nemáš → vytvoř podle struktury výše

2. **Identifikuj všechny variabilní části**
   - Firma, pracovník, data, výsledky

3. **Nahraď je placeholdery**
   - Použij naming convention výše
   - `{{section2_firma.company}}`
   - `{{excel_lsz.category}}`

4. **Ulož jako `LSZ_template.docx`**
   - Ulož do: `app/templates/word/`

5. **Projdi LSZ Excel a identifikuj výsledky**
   - Vytvoř seznam: výsledek → buňka
   - Pošli mi tento seznam

### FÁZE 2: Implementace (dělám JÁ)

6. **Vytvořím `config/excel_results_mappings.py`**
   - Podle tvého seznamu buněk

7. **Implementujem `core/excel_reader.py`**
   - Načítání výsledků z LSZ Excelu

8. **Implementujem `core/word_generator.py`**
   - Generování LSZ Word protokolu

9. **Implementujem `gui/word_dialog.py`**
   - GUI pro spuštění generování

10. **Rozšířím `main.py`**
    - Tlačítko "Generovat LSZ protokol"

### FÁZE 3: Testování

11. **Otestujem na projektu `6969_Fyrma`**
12. **Opravím chyby**
13. **Dokončím LSZ → pak přidáme CFZ, PP**

---

## 📞 CO OD TEBE TEĎKA POTŘEBUJU

1. ✅ **Vzorový LSZ Word protokol**
   - Pošli mi soubor (pokud máš)
   - Nebo popis struktury

2. ✅ **Seznam výsledků z LSZ Excelu**
   ```
   Název výsledku          | List         | Buňka | Příklad hodnoty
   ------------------------|--------------|-------|------------------
   Kategorie LSZ           | Vyhodnocení  | M15   | "Kategorie 1"
   EMG PHK průměr          | Vyhodnocení  | N20   | 45.2
   ...
   ```

3. ✅ **Potvrzení struktury JSON**
   - Je výše uvedená JSON struktura správně?
   - Chybí nějaká data?

---

**Jakmile vytvoříš Word šablonu a identifikuješ výsledky v Excelu, můžeme začít implementovat!**

Chceš, abych ti pomohl s něčím konkrétním při tvorbě šablony?