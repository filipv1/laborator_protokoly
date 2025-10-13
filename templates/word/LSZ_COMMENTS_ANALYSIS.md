# LSZ Template - Analýza Word Komentářů

**Nalezeno:** 31 komentářů od Licha Simona
**Datum:** 2025-10-09
**Závěr:** Komentáře obsahují VELMI komplexní logiku a podmínky!

---

## 🔴 VAROVÁNÍ: VYSOKÁ KOMPLEXITA

Komentáře odhalily, že LSZ protokol vyžaduje:
- ✅ Základní placeholdery (již implementováno)
- ⚠️ **Složité podmíněné fráze** (4-5 variant podle hodnot)
- ⚠️ **Dynamické výpočty** (hygienické limity podle směny)
- ⚠️ **Červené formátování** podle překročení limitů
- ⚠️ **Komplexní logické stromy** (nadlimitní síly)
- ⚠️ **Frekvenční analýzy** (až 10 obrázků z FASO)

**Odhad implementace:** 15-20 hodin místo původních 8-12 hodin!

---

## 📊 KATEGORIE KOMENTÁŘŮ

### Kategorie A: JEDNODUCHÉ (Již Implementováno)
- Komentář 1: Datum vypracování ✅
- Komentář 4, 6: Data z wordu ✅
- Komentář 7, 10: Data z excelu SOMATOMETRIE ✅
- Komentář 9: Vyplývá z informací ✅

### Kategorie B: STŘEDNÍ SLOŽITOST (Vyžaduje Podmínky)
- Komentář 2: Měření 1 nebo 2 dny
- Komentář 5: Čas vs Norma
- Komentář 12: Poznámky podle operací
- Komentář 28-31: Data z FASO a popisu práce

### Kategorie C: VYSOKÁ SLOŽITOST (Vyžaduje Logiku + Excel Data)
- Komentář 14: Počet pohybů podle kusy/čas
- Komentář 15: Hygienický limit - výpočet
- Komentář 17: Červené formátování
- Komentář 19-20: Fráze s 4 variantami
- Komentář 21: Velké síly - 3 varianty
- Komentář 22-23: Nadlimitní síly - složitý strom
- Komentář 27: Kategorizace podle limitů

---

## 📝 DETAILNÍ ANALÝZA KOMENTÁŘŮ

### Komentář 2: Měření 1 vs 2 Dny
**Text:** "Měření probíhalo v jednom dni / ve dvou dnech..."

**Logika:**
```python
if measurement_days == 1:
    text = "Měření probíhalo v jednom dni, v jedné průměrné směně."
else:
    text = "Měření probíhalo ve dvou dnech, ve dvou průměrných směnách."

text += f" Měřen{'i byli' if worker_count == 2 else ' byl'} {worker_count_text} pracovník{'i' if worker_count > 1 else ''} – {gender}."
```

**Placeholder:**
```
{% if measurement_days == 1 %}Měření probíhalo v jednom dni, v jedné průměrné směně.{% else %}Měření probíhalo ve dvou dnech, ve dvou průměrných směnách.{% endif %} Měřen{{plural_ending}} {{worker_count_text}} pracovník{{plural_worker}} – {{workers_gender}}.
```

**Potřeba v JSON:**
```json
"measurement_days": 1  // nebo 2
```

---

### Komentář 3: EMG Holter - Tučné Označení
**Text:** "Holtr použit při měření je vyznačen na první straně excelu LSZ. Označit použitý holtr tučně"

**Logika:**
- V tabulce přístrojů (Table 0) označit použitý EMG Holter tučně
- Data jsou v excelu LSZ (první strana)

**Implementace:**
```python
# Při vyplňování Table 0:
for row in table.rows:
    if row.cells[0].text.contains(used_emg_holter):
        # Označit tučně
        for paragraph in row.cells[0].paragraphs:
            for run in paragraph.runs:
                run.font.bold = True
```

**Potřeba:**
```python
excel_lsz.used_emg_holter = "EMG Holter č. 60/16"  # Z excelu LSZ
```

---

### Komentář 5: Čas vs Norma
**Text:** "Pokud na ČAS – fráze zůstává stejná. Pokud na NORMA – mění se počet kusů dle časového snímku"

**Již implementováno:**
```jinja
{% if measurement_type == 'norma' %}
Průměrná směna odpovídala stanovené normě...
V den měření byla norma na lince stanovena na {{time_schedule_total.pieces_count}} ks/směna.
{% endif %}

{% if measurement_type == 'cas' %}
Průměrná směna vychází z časového snímku...
{% endif %}
```

---

### Komentář 12: Poznámky Podle Operací
**Text:** "Pokud bezpečnostní přestávka – změnit čas... Pokud operace co se neměřila – změnit název operace..."

**Logika:**
```python
notes = []
for operation in time_schedule:
    if operation.name.lower() == "bezpečnostní přestávky":
        notes.append(f"Pozn.: Bezpečnostní přestávky v trvání {operation.time_min} minut, v časovém vážení počítáno se 3 % Fmax.")
    elif operation.unmeasured:  # např. úklid
        notes.append(f"Pozn.: Pracovní činnost \"{operation.name}\" nebyla měřena, v časovém vážení počítáno se 7 % Fmax.")
```

**Placeholder:**
```jinja
{% for note in operation_notes %}
{{note}}
{% endfor %}
```

---

### Komentář 14: Počet Pohybů - Kusy vs Čas
**Text:** "Pokud se hodnotily kusy – data v excelu LSZ PracovníkA/A tabulka pohyby kusy. Pokud se hodnotil čas – data v excelu LSZ PracovníkA/A tabulka pohyby čas"

**Logika:**
- Excel LSZ má 2 tabulky: "pohyby kusy" a "pohyby čas"
- Podle `measurement_type` načíst správnou tabulku

**Implementace v excel_reader.py:**
```python
if measurement_type == "norma":
    movements_table = excel_lsz.sheet["PracovníkA/A"].table["pohyby kusy"]
else:
    movements_table = excel_lsz.sheet["PracovníkA/A"].table["pohyby čas"]
```

---

### Komentář 15: Hygienický Limit - Výpočet
**Text:** "Hygienický limit = zaokrouhlené číslo %Fmax pro danou svalovou skupinu × kontrola snížení/navýšení hygienického limitu × vložení hodnoty ze sloupce na listu CELKOVÉ VÝSLEDKY"

**Logika:**
```python
# Základní limity podle směny
shift_limits = {
    480: 600,   # 8h
    450: 585,   # 7.5h
    # atd podle trojčlenky
}

# Upravený limit podle snížení/navýšení
hygiene_limit_adjustment = 0  # -2.5% nebo +2.5%
adjusted_limit = shift_limits[shift_duration] * (1 + hygiene_limit_adjustment / 100)

# Pro každou svalovou skupinu
for muscle_group in ['phk_extenzory', 'phk_flexory', 'lhk_extenzory', 'lhk_flexory']:
    fmax_percent = excel_lsz[f"{muscle_group}_avg"]  # např. 8.1

    # Hygienický limit z tabulky
    hygiene_limit_fmax = excel_lsz[f"{muscle_group}_hygiene_limit"]  # z excelu

    # Finální limit
    final_limit = round(hygiene_limit_fmax * adjusted_limit)
```

**Potřeba:**
```python
shift_duration = 480  # minuty
hygiene_limit_adjustment = 0  # % (-2.5, 0, +2.5)
```

---

### Komentář 17: Červené Formátování Při Překročení
**Text:** "Pokud HODNOTY Výskyt sil > 70 % Fmax PŘEVYŠUJE hodnotu 100 → Hodnotu dát červeně. Pokud HODNOTY Výskyt sil 55-70 % Fmax PŘEVYŠUJE hygienický limit → Hodnotu dát červeně"

**Logika:**
```python
def format_cell_red_if_over_limit(cell, value, limit):
    """Formátuj buňku červeně, pokud hodnota překračuje limit"""
    cell.text = str(value)
    if value > limit:
        for paragraph in cell.paragraphs:
            for run in paragraph.runs:
                run.font.color.rgb = RGBColor(255, 0, 0)  # Červená
                run.font.bold = True
```

**V tabulkách:**
- Table 8: Výskyt sil 55-70% a >70%
- Pokud > limit → červeně + tučně

---

### Komentář 19-20: Fráze Pro Překročení Limitů - 4 VARIANTY!
**Text:** "FRÁZE: nepřekračují... / překračují... / překračují extenzory, flexory zachován / překračují flexory, extenzory zachován"

**Logika:**
```python
def get_limit_phrase(phk_ext_over, phk_flex_over, limb="pravé"):
    """Vrátí správnou frázi podle toho, co překračuje limit"""

    if not phk_ext_over and not phk_flex_over:
        return f"nepřekračují průměrné hygienické limity počtu pohybů pro naměřené vynakládané svalové síly extenzorů a flexorů předloktí {limb} horní končetiny."

    elif phk_ext_over and phk_flex_over:
        return f"překračují průměrné hygienické limity počtu pohybů pro naměřené vynakládané svalové síly extenzorů a flexorů předloktí {limb} horní končetiny."

    elif phk_ext_over and not phk_flex_over:
        return f"překračují průměrné hygienické limity počtu pohybů pro naměřené vynakládané svalové síly extenzorů předloktí {limb} horní končetiny. Pro flexory byl hygienický limit zachován."

    elif not phk_ext_over and phk_flex_over:
        return f"překračují průměrné hygienické limity počtu pohybů pro naměřené vynakládané svalové síly flexorů předloktí {limb} horní končetiny. Pro extenzory byl hygienický limit zachován."
```

**Použití:**
```jinja
Průměrné počty pohybů PHK ({{excel_lsz.phk_pohyby_total}}) {{phk_limit_phrase}}
Průměrné počty pohybů LHK ({{excel_lsz.lhk_pohyby_total}}) {{lhk_limit_phrase}}
```

---

### Komentář 21: Velké Svalové Síly - 3 VARIANTY!
**Text:** "nejsou / ojediněle / pravidelně podle hodnot v tabulce rozložení sil"

**Logika:**
```python
def determine_high_forces_frequency(forces_55_70_table):
    """
    Určí frekvenci velkých svalových sil
    forces_55_70_table = [ext_phk, flex_phk, ext_lhk, flex_lhk] pro řádek "Celkem"
    """

    # Pokud všechny 0 → nejsou
    if all(f == 0 for f in forces_55_70_table):
        return "nejsou"

    # Pokud jen 1 nebo 2 nenulové → ojediněle
    non_zero_count = sum(1 for f in forces_55_70_table if f > 0)
    if non_zero_count <= 2:
        return "ojediněle"

    # Pokud většina nebo všechny nenulové → pravidelně
    return "pravidelně"
```

**Fráze:**
```jinja
V hodnocené průměrné směně {% if high_forces_freq == 'nejsou' %}nejsou při provádění práce vynakládány{% elif high_forces_freq == 'ojediněle' %}jsou při provádění práce ojediněle vynakládány{% else %}jsou při provádění práce pravidelně vynakládány{% endif %} velké svalové síly u měřených svalových skupin rukou a předloktí (55–70 % Fmax).
```

---

### Komentář 22: Překročení Velkých Sil
**Text:** "překračuje Když velké svalové síly 55–70 % Fmax jsou více než 600 (8h) / 585 (7.5h)... Méně = nepřekračuje"

**Logika:**
```python
# Limit podle směny
shift_limits = {
    480: 600,
    450: 585,
    # Trojčlenka pro ostatní: limit = 600 * (shift_duration / 480)
}

limit = shift_limits.get(shift_duration, 600 * (shift_duration / 480))

# Kontrola pro každou svalovou skupinu
high_forces_over_limit = any(
    excel_lsz.forces_55_70_total[muscle] > limit
    for muscle in ['phk_ext', 'phk_flex', 'lhk_ext', 'lhk_flex']
)

phrase = "překračuje" if high_forces_over_limit else "nepřekračuje"
```

---

### Komentář 23: Nadlimitní Síly >70% - VELMI SLOŽITÉ!
**Text:** "nedochází Když poslední 4 hodnoty jsou 0 0 0 0... Když dochází tak vypsat kde..."

**Příklady fráze:**
```
0 0 0 0 → "nedochází k vynakládání nadlimitních svalových sil"
1 1 0 0 → "dochází k vynakládání nadlimitních svalových sil u pravé ruky a předloktí"
0 0 1 1 → "dochází k vynakládání nadlimitních svalových sil u levé ruky a předloktí"
1 0 1 0 → "dochází k vynakládání nadlimitních svalových sil u extenzorů"
0 1 0 1 → "dochází k vynakládání nadlimitních svalových sil u flexorů"
0 1 1 0 → "dochází k vynakládání nadlimitních svalových sil u flexorů PHK a extenzorů LHK"
```

**Logika:**
```python
def get_extreme_forces_phrase(forces_over_70):
    """
    forces_over_70 = [ext_phk, flex_phk, ext_lhk, flex_lhk] (hodnoty celkem)
    Returns: text fráze
    """
    ext_phk, flex_phk, ext_lhk, flex_lhk = forces_over_70

    # Žádné nadlimitní síly
    if all(f == 0 for f in forces_over_70):
        return "Při provádění práce nedochází k vynakládání nadlimitních svalových sil u všech měřených svalových skupin rukou a předloktí (nad 70 % Fmax)."

    affected = []

    # PHK (obě)
    if ext_phk > 0 and flex_phk > 0:
        affected.append("pravé ruky a předloktí")
    # LHK (obě)
    elif ext_lhk > 0 and flex_lhk > 0:
        affected.append("levé ruky a předloktí")
    # Extenzory obě
    elif ext_phk > 0 and ext_lhk > 0:
        affected.append("extenzorových svalových skupin rukou a předloktí")
    # Flexory obě
    elif flex_phk > 0 and flex_lhk > 0:
        affected.append("flexorových svalových skupin rukou a předloktí")
    # Kombinace specifické
    else:
        parts = []
        if ext_phk > 0:
            parts.append("extenzorů PHK")
        if flex_phk > 0:
            parts.append("flexorů PHK")
        if ext_lhk > 0:
            parts.append("extenzorů LHK")
        if flex_lhk > 0:
            parts.append("flexorů LHK")

        affected.append(" a ".join(parts))

    return f"Při provádění práce dochází k vynakládání nadlimitních svalových sil u {affected[0]} (nad 70 % Fmax)."
```

---

### Komentář 27: Kategorizace
**Text:** "1, 2, 3 nad limit = kategorie 3. Pokud jsou pohyby pod od 1/3 hygienického limitu = kategorie 1"

**Logika:**
```python
def determine_category(movements_data, hygiene_limits):
    """
    Určí kategorii LSZ na základě pohybů a limitů
    """

    over_limit_count = 0
    under_third_limit_count = 0

    for muscle in ['phk_ext', 'phk_flex', 'lhk_ext', 'lhk_flex']:
        movements = movements_data[muscle]
        limit = hygiene_limits[muscle]

        if movements > limit:
            over_limit_count += 1
        elif movements < limit / 3:
            under_third_limit_count += 1

    # Kategorie 3: 1 nebo více nad limitem
    if over_limit_count >= 1:
        return "3"

    # Kategorie 1: Všechny pod 1/3 limitu
    if under_third_limit_count == 4:
        return "1"

    # Jinak kategorie 2
    return "2"
```

---

### Komentář 29-31: Frekvenční Analýzy (FASO)
**Text:** "Z frekvenční analýzy ve wordu Název je obvykle FASO... FREKVENČNÍCH ANALÝZ MŮŽE BÝT AŽ 10"

**Problém:** Obrázky z FASO Word dokumentu!

**Řešení:**
1. **Varianta A:** Uživatel nahraje FASO.docx při vytváření projektu
2. **Varianta B:** Uživatel manuálně přidá obrázky do vygenerovaného protokolu
3. **Varianta C:** Parsovat FASO.docx a extrahovat obrázky automaticky

**Implementace (Varianta C):**
```python
def extract_images_from_faso(faso_docx_path):
    """Extrahuj obrázky z FASO Word dokumentu"""
    doc = Document(faso_docx_path)
    images = []

    for rel in doc.part.rels.values():
        if "image" in rel.target_ref:
            image_part = rel.target_part
            images.append({
                'data': image_part.blob,
                'filename': rel.target_ref.split('/')[-1]
            })

    return images[:10]  # Max 10 obrázků
```

---

## 🎯 ROZHODNUTÍ CO IMPLEMENTOVAT

### FÁZE 1: ZÁKLADNÍ (✅ Již Hotovo)
- Základní placeholdery
- Podmínky pro 1 vs 2 pracovníky
- Data z JSON a časového snímku

### FÁZE 2: STŘEDNÍ SLOŽITOST (⚠️ Vyžaduje Rozhodnutí)
- [ ] Měření 1 vs 2 dny (přidat do JSON?)
- [ ] EMG Holter tučné označení
- [ ] Poznámky podle operací (dynamicky generovat)
- [ ] Typ měření (Norma/Čas) - přidat do wizardu

### FÁZE 3: VYSOKÁ SLOŽITOST (❌ Velmi Časově Náročné)
- [ ] Červené formátování při překročení
- [ ] Fráze s 4 variantami (překročení limitů)
- [ ] Velké síly - 3 varianty
- [ ] Nadlimitní síly - složitý strom
- [ ] Hygienický limit - výpočty
- [ ] Kategorizace podle limitů
- [ ] FASO obrázky (10 variant)

---

## 📋 DOPORUČENÍ

### Option A: MINIMÁLNÍ IMPLEMENTACE
**Co implementovat:**
- ✅ Základní placeholdery (hotovo)
- ✅ Podmínky 1/2 pracovníci (hotovo)
- ➕ Typ měření (Norma/Čas)
- ➕ Měření 1/2 dny

**Co nechat manuální:**
- Červené formátování → uživatel udělá v Wordu
- Složité fráze → uživatel vybere správnou variantu
- FASO obrázky → uživatel přidá manuálně

**Odhadovaný čas:** +2-3 hodiny
**Výhoda:** Rychlá implementace
**Nevýhoda:** Uživatel musí dost doplňovat ručně

---

### Option B: STŘEDNÍ IMPLEMENTACE (DOPORUČUJI)
**Co implementovat:**
- ✅ Vše z Option A
- ➕ Podmíněné poznámky podle operací
- ➕ EMG Holter tučné označení
- ➕ Základní výpočty hygienických limitů
- ➕ Jednoduché červené formátování (boolean flagy)

**Co nechat manuální:**
- Složité fráze s 4 variantami → poskytnou se 2-3 nejčastější
- FASO obrázky → manuálně
- Velmi složité logické stromy

**Odhadovaný čas:** +8-12 hodin
**Výhoda:** Vyvážený poměr automatizace vs. čas
**Nevýhoda:** Některé pokročilé funkce chybí

---

### Option C: PLNÁ IMPLEMENTACE
**Co implementovat:**
- ✅ Vše z Option B
- ➕ Všechny 4 varianty frází
- ➕ Složité logické stromy pro nadlimitní síly
- ➕ Automatická kategorizace
- ➕ FASO obrázky parser
- ➕ Pokročilé červené formátování všude

**Odhadovaný čas:** +20-30 hodin!
**Výhoda:** Téměř plná automatizace
**Nevýhoda:** Velmi časově náročné, riziko chyb v logice

---

## 🤔 CO TEĎKA?

**Rozhodní, kterou Option chceš:**

**Option A:** Rychle a jednoduše, hodně manuální práce
**Option B:** Vyvážené, rozumný čas implementace ⭐ DOPORUČUJI
**Option C:** Plná automatizace, hodně práce

**Pak ti:**
1. Aktualizuji šablonu podle zvolené Option
2. Vytvořím config soubory s potřebnými mappings
3. Implementuji potřebnou logiku

**Nebo:**
- Můžeš nejdřív začít s Option A
- Postupně přidávat funkce z Option B/C podle potřeby
- Iterativní přístup = bezpečnější

---

**Tvoje volba?** 🎯
