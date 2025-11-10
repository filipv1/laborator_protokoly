# PP - Seznam problematických poloh (Placeholder)

## Název placeholderu
```
{{ texts.pp_problematicke_polohy_seznam }}
```

## Co obsahuje
**Čárkou oddělený seznam pracovních poloh**, které překročily nejvyšší naměřenou kategorii.

- **Kategorie 2:** Vypíše VŠECHNY polohy, které překročily kategorii 1
- **Kategorie 3:** Vypíše POUZE polohy, které překročily kategorii 2 (nejhorší)
- **Kategorie 1:** Prázdný string (žádné problémy)

## Formát výstupu
```
"dynamické předklon trupu, statické otočení hlavy, dynamické zvedání paže nad horizontálu"
```

- Typ svalové práce (dynamické/statické) je vždy součástí
- Názvy poloh lowercase (kromě prvního písmene po typu)
- Odděleno čárkami a mezerami

## Příklady použití v Word šabloně

### Varianta 1: Přímé zobrazení seznamu
```jinja
Pracovní polohy s překročením limitů: {{ texts.pp_problematicke_polohy_seznam }}
```

**Výstup:**
```
Pracovní polohy s překročením limitů: dynamické předklon trupu, statické otočení hlavy
```

---

### Varianta 2: S podmínkou (kontrola, zda jsou nějaké problémy)
```jinja
{% if texts.pp_problematicke_polohy_seznam %}
POZOR: Byly zjištěny překročení limitů u následujících poloh:
{{ texts.pp_problematicke_polohy_seznam }}
{% else %}
Všechny pracovní polohy jsou v kategorii 1 (bez problémů).
{% endif %}
```

**Výstup (s problémy):**
```
POZOR: Byly zjištěny překročení limitů u následujících poloh:
dynamické předklon trupu, statické otočení hlavy
```

**Výstup (bez problémů):**
```
Všechny pracovní polohy jsou v kategorii 1 (bez problémů).
```

---

### Varianta 3: Vlastní formulace podle kategorie
```jinja
Celková doba zaujímání nepřijatelných poloh překročila přípustný limit kategorie
{% if texts.pp_problematicke_polohy_seznam contains 'kategorie 3' %}
2
{% else %}
1
{% endif %}
 pro: {{ texts.pp_problematicke_polohy_seznam }}
```

---

### Varianta 4: V tabulce
```jinja
| Překročené polohy | {{ texts.pp_problematicke_polohy_seznam or "žádné" }} |
```

## Rozdíl oproti `prvni_pp_podminka_kategorie`

| Placeholder | Obsah | Příklad |
|-------------|-------|---------|
| `prvni_pp_podminka_kategorie` | **Kompletní text** s kategorizací | "Celková doba zaujímání nepřijatelných pracovních poloh a podmíněně přijatelných poloh překročila v průměru přípustný limit kategorie 1 pro dynamické předklon trupu, statické otočení hlavy." |
| `pp_problematicke_polohy_seznam` | **Pouze seznam** poloh | "dynamické předklon trupu, statické otočení hlavy" |

## Kdy použít který placeholder

### Použij `prvni_pp_podminka_kategorie` když:
- Chceš **automatický kompletní text** s gramatikou
- Nechceš psát vlastní formulace
- Stačí ti standardní text podle NV 361/2007

### Použij `pp_problematicke_polohy_seznam` když:
- Chceš **vlastní formulaci** textu
- Potřebuješ seznam někde uprostřed věty
- Chceš seznam v tabulce nebo seznamu
- Potřebuješ podmínku (if/else) podle toho, zda jsou problémy

## Implementace

### Funkce
```python
def _get_pp_problematic_positions_list(
    results_data: Dict[str, Any],
    category_limits: Dict[str, Any]
) -> str
```

**Soubor:** `core/text_generator.py`

### Algoritmus
1. Projde všechny sekce (trup, hlava_krk, phk, lhk, dk, ostatni)
2. Pro každou polohu určí kategorii (1, 2, nebo 3) podle `prumer_min` a typu
3. Sbírá problematické polohy do dvou seznamů:
   - `category_2_problems` - polohy v kategorii 2+
   - `category_3_problems` - polohy v kategorii 3
4. Vrátí seznam podle nejvyšší kategorie:
   - Max kategorie 3 → vrátí `category_3_problems`
   - Max kategorie 2 → vrátí `category_2_problems`
   - Max kategorie 1 → vrátí `""` (prázdný string)

### Formátování názvů
Používá funkci `_format_pp_position_name()`:
- Vstup: `typ_svalove_prace="Dynamická"`, `nazev_polohy="Předklon trupu"`
- Výstup: `"dynamické předklon trupu"`

## Testování

### Test 1: Reálná data
```bash
python test_pp_seznam_problematickych_poloh.py
```

### Test 2: Simulovaná data s problémy
```bash
python test_pp_seznam_s_problemy.py
```

## Kategoriální limity

Limity se upravují podle délky směny (koeficient):

**Standardní směna (480 min, koef. 1.000):**
- PP kategorie 1: 0-100 min
- PP kategorie 2: 101-160 min
- PP kategorie 3: >161 min
- N kategorie 1: 0-20 min
- N kategorie 2: 21-30 min
- N kategorie 3: >31 min

**Delší směna (500 min, koef. 1.025):**
- PP kategorie 1: 0-102 min
- PP kategorie 2: 103-164 min
- PP kategorie 3: >165 min
- N kategorie 1: 0-21 min
- N kategorie 2: 22-31 min
- N kategorie 3: >32 min

## Související dokumentace
- `PP_KATEGORIE_LIMITY_DOKUMENTACE.md` - Dokumentace kategorizace a koeficientů
- `PP_IMPLEMENTATION_SUMMARY.md` - Implementace PP protokolů
- `core/text_generator.py` - Zdrojový kód
