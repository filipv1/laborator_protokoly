# Jedenáctá podmínka - Hierarchické vyhodnocení zatížení

## Účel
Vyhodnotí celkový stav všech 4 svalových skupin (PHK extenzory, PHK flexory, LHK extenzory, LHK flexory) vzhledem k jejich hygienickým limitům a vrátí číselný indikátor (1, 2, nebo 3).

## Výstupy

### "1" - Nízké zatížení
Žádný ze 4 svalů není nad 1/3 hygienického limitu.
- **Podmínka:** Všechny svaly mají `počet_pohybů ≤ (hygienický_limit / 3)`

### "2" - Střední zatížení
Alespoň jeden sval je nad 1/3 hygienického limitu, ale žádný nepřekračuje celý hygienický limit.
- **Podmínka:**
  - Alespoň jeden sval: `počet_pohybů > (hygienický_limit / 3)`
  - Všechny svaly: `počet_pohybů ≤ hygienický_limit`

### "3" - Vysoké zatížení (překročení limitu)
Alespoň jeden sval překračuje hygienický limit.
- **Podmínka:** Alespoň jeden sval: `počet_pohybů > hygienický_limit`

## Hierarchie vyhodnocení
Podmínka je hierarchická - vyšší priorita má přednost:
1. **Priorita 1 (nejvyšší):** Překročení limitu → "3"
2. **Priorita 2:** Nad 1/3 limitu → "2"
3. **Priorita 3 (nejnižší):** Pod 1/3 limitu → "1"

## 4 svalové skupiny

| Svalová skupina | Fmax hodnota | Počet pohybů | Limit z tabulky |
|-----------------|--------------|--------------|-----------------|
| PHK extenzory   | Fmax_Phk_Extenzor | phk_number_of_movements | table_W4_Y51[row]["phk"] |
| PHK flexory     | Fmax_Phk_Flexor   | phk_number_of_movements | table_W4_Y51[row]["phk"] |
| LHK extenzory   | Fmax_Lhk_Extenzor | lhk_number_of_movements | table_W4_Y51[row]["lhk"] |
| LHK flexory     | Fmax_Lhk_Flexor   | lhk_number_of_movements | table_W4_Y51[row]["lhk"] |

## Algoritmus

Pro každou ze 4 svalových skupin:
1. Najdi hygienický limit v `table_W4_Y51` podle zaokrouhlené hodnoty Fmax
2. Vypočítej `one_third_limit = limit / 3`
3. Zkontroluj:
   - Je `počet_pohybů > limit`? → nastav flag `over_limit = True`
   - Jinak je `počet_pohybů > one_third_limit`? → nastav flag `over_one_third = True`

Finální vyhodnocení:
- Pokud `over_limit == True` → vrať "3"
- Jinak pokud `over_one_third == True` → vrať "2"
- Jinak → vrať "1"

## Použití v Word šabloně

```django
{{ section_generated_texts.jedenacta_text_podminka }}
```

**Vrací:** `"1"`, `"2"` nebo `"3"`

## Příklady

### Příklad 1: Nízké zatížení (output "1")
```
PHK limit: 12000, počet pohybů: 3000
LHK limit: 13000, počet pohybů: 3000

1/3 PHK limitu: 4000 → 3000 ≤ 4000 ✓
1/3 LHK limitu: 4333 → 3000 ≤ 4333 ✓

→ Všechny svaly pod 1/3 limitu → Output: "1"
```

### Příklad 2: Střední zatížení (output "2")
```
PHK limit: 12000, počet pohybů: 8000
LHK limit: 13000, počet pohybů: 3000

PHK: 8000 > 4000 (1/3 limitu) ✓, ale 8000 ≤ 12000 (limit) ✓
LHK: 3000 ≤ 4333 (1/3 limitu) ✓

→ Alespoň jeden sval nad 1/3 limitu, ale pod limitem → Output: "2"
```

### Příklad 3: Vysoké zatížení (output "3")
```
PHK limit: 12000, počet pohybů: 3000
LHK limit: 13000, počet pohybů: 15000

PHK: 3000 ≤ 4000 (1/3 limitu) ✓
LHK: 15000 > 13000 (limit) ✗ PŘEKROČEN

→ Alespoň jeden sval překračuje limit → Output: "3"
```

## Hraniční případy

### Hodnota ROVNA 1/3 limitu
```
Počet pohybů: 4000
Limit: 12000
1/3 limitu: 4000

4000 > 4000? Ne → Není nad 1/3 limitu
→ Output: "1" (pokud všechny ostatní svaly také pod 1/3)
```

### Hodnota ROVNA limitu
```
Počet pohybů: 12000
Limit: 12000
1/3 limitu: 4000

12000 > 12000? Ne → Limit NENÍ překročen
12000 > 4000? Ano → Je nad 1/3 limitu
→ Output: "2"
```

### Hodnota TĚSNĚ nad limitem
```
Počet pohybů: 12001
Limit: 12000

12001 > 12000? Ano → Limit JE překročen
→ Output: "3"
```

## Testování

Byly vytvořeny dva testovací soubory:

### 1. `test_jedenacta_text_podminka.py`
Testuje základní scénáře:
- Test 1: Všechny svaly pod 1/3 limitu → "1" ✓
- Test 2: Alespoň jeden nad 1/3, ale pod limitem → "2" ✓
- Test 3: Alespoň jeden nad limitem → "3" ✓

### 2. `test_jedenacta_text_podminka_hranicni_pripady.py`
Testuje hraniční případy:
- Hodnota ROVNA 1/3 limitu → "1" ✓
- Hodnota ROVNA limitu → "2" ✓
- Hodnota TĚSNĚ nad limitem → "3" ✓

**Všechny testy prošly úspěšně!**

## Implementace

Funkce je implementována v `core/text_generator.py`:
- `_calculate_jedenacta_text_podminka(results_data)` - vypočítá výstup
- Automaticky volána v `generate_conditional_texts()` při generování Word protokolů

## Poznámky

- Používá matematické zaokrouhlování (`_math_round`) pro konzistenci s Excelem
- Fallback hodnota při chybějících datech: `"1"`
- Podmínka vyhodnocuje PHK extenzory a flexory proti **stejnému** počtu pohybů (`phk_number_of_movements`)
- Podmínka vyhodnocuje LHK extenzory a flexory proti **stejnému** počtu pohybů (`lhk_number_of_movements`)
