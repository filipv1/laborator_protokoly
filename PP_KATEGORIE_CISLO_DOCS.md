# PP - Číslo kategorie (Placeholder)

## Název placeholderu
```
{{ texts.pp_kategorie_cislo }}
```

## Co obsahuje
**Číslo nejvyšší kategorie** pracovních poloh jako string: `"1"`, `"2"`, nebo `"3"`

## Logika určení kategorie

### Kategorie 1 (výsledek: "1")
- **Všechny** pracovní polohy **NEPŘEKROČILY** limit kategorie 1
- Pracovní prostředí je v pořádku

### Kategorie 2 (výsledek: "2")
- **Alespoň jedna** pracovní poloha **PŘEKROČILA** limit kategorie 1
- **Žádná** pracovní poloha **NEPŘEKROČILA** limit kategorie 2

### Kategorie 3 (výsledek: "3")
- **Alespoň jedna** pracovní poloha **PŘEKROČILA** limit kategorie 2
- Nejvyšší úroveň překročení

## Datový typ
**POZOR:** Vrací **STRING** (`"1"`, `"2"`, `"3"`), ne integer!

V podmínkách v Jinja2 šablonách používej porovnání se stringem:
```jinja
{% if texts.pp_kategorie_cislo == '1' %}  ✅ SPRÁVNĚ (string)
{% if texts.pp_kategorie_cislo == 1 %}    ❌ ŠPATNĚ (integer)
```

## Příklady použití v Word šabloně

### Varianta 1: Přímé zobrazení čísla
```jinja
Pracovní polohy jsou zařazeny do kategorie {{ texts.pp_kategorie_cislo }}.
```

**Výstup:**
```
Pracovní polohy jsou zařazeny do kategorie 2.
```

---

### Varianta 2: Podmínka podle kategorie
```jinja
{% if texts.pp_kategorie_cislo == '1' %}
Všechny pracovní polohy jsou v kategorii 1 (bez problémů).
{% elif texts.pp_kategorie_cislo == '2' %}
Některé pracovní polohy překročily limit kategorie 1.
{% else %}
POZOR: Pracovní polohy překročily limit kategorie 2!
{% endif %}
```

---

### Varianta 3: Dynamický text s číslem překročené kategorie
```jinja
Celková doba zaujímání nepřijatelných pracovních poloh překročila přípustný limit kategorie
{% if texts.pp_kategorie_cislo == '3' %}2{% else %}1{% endif %}.
```

**Výstup (kategorie 3):**
```
Celková doba zaujímání nepřijatelných pracovních poloh překročila přípustný limit kategorie 2.
```

**Výstup (kategorie 2):**
```
Celková doba zaujímání nepřijatelných pracovních poloh překročila přípustný limit kategorie 1.
```

---

### Varianta 4: V tabulce
```jinja
| Parametr | Hodnota |
|----------|---------|
| Výsledná kategorie | {{ texts.pp_kategorie_cislo }} |
| Stav | {% if texts.pp_kategorie_cislo == '1' %}V pořádku{% else %}Překročení{% endif %} |
```

---

### Varianta 5: Kombinace s dalšími placeholdery
```jinja
Výsledná kategorie: {{ texts.pp_kategorie_cislo }}

{% if texts.pp_kategorie_cislo != '1' %}
Problematické polohy: {{ texts.pp_problematicke_polohy_seznam }}
{% endif %}
```

**Výstup (kategorie 2):**
```
Výsledná kategorie: 2

Problematické polohy: dynamické předklon trupu, statické otočení hlavy
```

---

### Varianta 6: Barevné označení podle kategorie
```jinja
Kategorie: {{ texts.pp_kategorie_cislo }}
{% if texts.pp_kategorie_cislo == '3' %}
🔴 VYSOKÉ RIZIKO
{% elif texts.pp_kategorie_cislo == '2' %}
🟡 STŘEDNÍ RIZIKO
{% else %}
🟢 NÍZKÉ RIZIKO
{% endif %}
```

## Vztah k ostatním PP placeholderům

| Placeholder | Obsah | Příklad |
|-------------|-------|---------|
| `pp_kategorie_cislo` | **Číslo kategorie** | `"2"` |
| `pp_problematicke_polohy_seznam` | **Seznam poloh** | `"dynamické předklon trupu, statické otočení hlavy"` |
| `prvni_pp_podminka_kategorie` | **Kompletní text** | `"Celková doba zaujímání nepřijatelných pracovních poloh a podmíněně přijatelných poloh překročila v průměru přípustný limit kategorie 1 pro dynamické předklon trupu, statické otočení hlavy."` |

## Kdy použít který placeholder

### Použij `pp_kategorie_cislo` když:
- Potřebuješ **podmínku** v šabloně (if/elif/else)
- Chceš zobrazit **jen číslo** bez textu
- Potřebuješ **dynamicky měnit text** podle kategorie
- Chceš číslo **v tabulce** nebo seznamu

### Použij `pp_problematicke_polohy_seznam` když:
- Potřebuješ **seznam problematických poloh** bez celého textu
- Chceš **vlastní formulaci** s výčtem poloh

### Použij `prvni_pp_podminka_kategorie` když:
- Chceš **automatický kompletní text**
- Stačí ti standardní formulace podle NV 361/2007

## Implementace

### Funkce
```python
def _get_pp_max_category(
    results_data: Dict[str, Any],
    category_limits: Dict[str, Any]
) -> int
```

**Soubor:** `core/text_generator.py`

### Algoritmus
1. Projde všechny sekce (trup, hlava_krk, phk, lhk, dk, ostatni)
2. Pro každou polohu určí kategorii (1, 2, nebo 3) podle `prumer_min` a typu
3. Sleduje nejvyšší nalezenou kategorii
4. Vrátí max kategorii jako integer (1, 2, nebo 3)
5. V `generate_conditional_texts()` se převede na string

### Kategoriální limity

**Standardní směna (480 min):**
- PP kategorie 1: 0-100 min
- PP kategorie 2: 101-160 min
- PP kategorie 3: 161+ min
- N kategorie 1: 0-20 min
- N kategorie 2: 21-30 min
- N kategorie 3: 31+ min

**Nestandardní směny:**
- Limity se upravují koeficientem podle délky směny
- Viz `PP_KATEGORIE_LIMITY_DOKUMENTACE.md`

## Testování

### Test s různými kategoriemi
```bash
python test_pp_kategorie_cislo.py
```

Tento test demonstruje:
- Kategorii 1 (vše OK)
- Kategorii 2 (překročena kat1)
- Kategorii 3 (překročena kat2)
- Příklady použití v šablonách

## Časté chyby

### ❌ ŠPATNĚ - Porovnání s integerem
```jinja
{% if texts.pp_kategorie_cislo == 1 %}
```

### ✅ SPRÁVNĚ - Porovnání se stringem
```jinja
{% if texts.pp_kategorie_cislo == '1' %}
```

### ❌ ŠPATNĚ - Matematické operace
```jinja
{{ texts.pp_kategorie_cislo + 1 }}  <!-- Chyba: nelze sčítat string -->
```

### ✅ SPRÁVNĚ - Použití filtru nebo podmínky
```jinja
{% if texts.pp_kategorie_cislo == '2' %}
Překročena kategorie 1
{% elif texts.pp_kategorie_cislo == '3' %}
Překročena kategorie 2
{% endif %}
```

## Příklady reálného použití

### Protokol s výsledky
```jinja
Odborné hodnocení pracovních poloh
======================================

Výsledná kategorie: {{ texts.pp_kategorie_cislo }}

{% if texts.pp_kategorie_cislo == '1' %}
✅ Hodnocení: Pracovní prostředí je v pořádku. Všechny pracovní polohy
jsou v kategorii 1 podle NV 361/2007.

{% elif texts.pp_kategorie_cislo == '2' %}
⚠ Hodnocení: Byly zjištěny pracovní polohy v kategorii 2.

Problematické polohy: {{ texts.pp_problematicke_polohy_seznam }}

Doporučení: Prověřit možnosti organizačních opatření ke snížení
expozice problematickým polohám.

{% else %}
🔴 Hodnocení: Byly zjištěny pracovní polohy v kategorii 3.

Problematické polohy: {{ texts.pp_problematicke_polohy_seznam }}

Doporučení: Urgentn­ě prověřit možnosti technických a organizačních
opatření. Pracovní prostředí vyžaduje úpravu.
{% endif %}
```

## Související dokumentace
- `PP_KATEGORIE_LIMITY_DOKUMENTACE.md` - Dokumentace limitů a koeficientů
- `PP_SEZNAM_PROBLEMATICKYCH_POLOH_DOCS.md` - Dokumentace seznamu poloh
- `PP_IMPLEMENTATION_SUMMARY.md` - Implementace PP protokolů
- `core/text_generator.py` - Zdrojový kód
