# ULTRATHINK: Analýza tabulek v read_lsz_results.py

## 🔍 ODPOVĚĎ: "table_B4_I21" NENÍ hardcoded!

Název je matoucí, ale logika je **DYNAMICKÁ** s automatickou detekcí počtu řádků.

---

## 📊 DETAILNÍ ANALÝZA VŠECH TABULEK

### ❌ HARDCODED (fixní pozice):

#### 1. **table_W4_Y51** (read_lsz_results.py:102-113)
```python
# Tabulka W4-Y51 (hardcoded)
for row in ws.iter_rows(min_row=4, max_row=51, min_col=23, max_col=25):
    # Čte VŽDY řádky 4-51, sloupce W-Y
```
**Problém:** Pokud má tabulka jiný počet řádků, načte i prázdné řádky nebo odřízne data
**Název:** Správný - odpovídá fixní oblasti

---

#### 2. **table_somatometrie** (read_lsz_results.py:53-84)
```python
for row in ws.iter_rows(min_row=20, max_row=24, min_col=2, max_col=8):
    # Čte VŽDY řádky 20-24, sloupce B-H
```
**Problém:** Pokud je víc než 5 řádků dat (20-24), odřízne je
**Název:** Správný - odpovídá fixní oblasti B19:H24

---

### ✅ DYNAMICKÉ (automatická detekce):

#### 3. **table_B4_I21** (read_lsz_results.py:115-143)
```python
# KROK 1: Najdi začátek tabulky (hledá text "Činnost")
for row_idx, row in enumerate(ws.iter_rows(min_row=1, max_row=30, min_col=2, max_col=2)):
    if row[0] and "Činnost" in str(row[0]):
        table2_start_row = row_idx + 3  # Začni 3 řádky pod "Činnost"
        break

# KROK 2: Čti data až do prvního prázdného řádku
if table2_start_row:
    for row in ws.iter_rows(min_row=table2_start_row, max_row=table2_start_row + 50, ...):
        # BREAK na prázdném řádku!
        if not row[0] and row[0] != 0:
            break  # <--- TADY SE ZASTAVÍ AUTOMATICKY

        table2.append({...})
```

**Jak to funguje:**
1. **Hledá nadpis** "Činnost" v sloupci B (řádky 1-30)
2. **Přeskočí 3 řádky** (hlavičky)
3. **Čte max 50 řádků**, ALE...
4. **ZASTAVÍ SE** na prvním prázdném řádku!

**Výhoda:** Funguje pro **LIBOVOLNÝ počet řádků** (1-50)
**Název:** ŠPATNÝ - mělo by být `table_activities` nebo `table_time_schedule`

---

#### 4. **table_movements_per_unit** (read_lsz_results.py:145-167)
```python
# Hledá: "pohyb" AND "jednotka"
for row_idx, row in enumerate(ws.iter_rows(min_row=1, max_row=100, ...)):
    if row[0] and "pohyb" in str(row[0]).lower() and "jednotka" in str(row[0]).lower():
        table3_start_row = row_idx + 5
        break

# Break na prázdném řádku
if not row[0] and row[0] != 0:
    break
```

**Dynamické:** ✅ Hledá nadpis, zastavuje se na prázdném řádku
**Max řádků:** 50

---

#### 5. **table_time_weighted_average** (read_lsz_results.py:169-197)
```python
# Hledá: "časově" AND "průměr"
if (not row[0] and not row[1]) or (row[0] and "Výsledky" in str(row[0])):
    break  # <--- DVOJE BREAK PODMÍNKA!
```

**Dynamické:** ✅ Hledá nadpis, zastavuje se na prázdném řádku NEBO na dalším nadpisu "Výsledky"
**Max řádků:** 20

---

#### 6. **table_force_distribution** (read_lsz_results.py:199-228)
```python
# Hledá: "rozložení" AND "svalových sil"
if not row[0] and row[0] != 0:
    break
```

**Dynamické:** ✅ Hledá nadpis, zastavuje se na prázdném řádku
**Max řádků:** 50

---

## 🎯 SOUHRN

| Tabulka | Typ | Max řádků | Break podmínka | Správný název? |
|---------|-----|-----------|----------------|----------------|
| table_W4_Y51 | ❌ HARDCODED | 48 (4-51) | žádná | ✅ Ano |
| table_somatometrie | ❌ HARDCODED | 5 (20-24) | žádná | ✅ Ano |
| table_B4_I21 | ✅ DYNAMICKÁ | 50 | prázdný řádek | ❌ Matoucí |
| table_movements_per_unit | ✅ DYNAMICKÁ | 50 | prázdný řádek | ✅ Popisný |
| table_time_weighted_average | ✅ DYNAMICKÁ | 20 | prázdný NEBO "Výsledky" | ✅ Popisný |
| table_force_distribution | ✅ DYNAMICKÁ | 50 | prázdný řádek | ✅ Popisný |

---

## 💡 ODPOVĚĎ NA TVOU OTÁZKU

### "Je table_B4_I21 hardcoded?"

**NE!** Je **plně dynamická** s těmito vlastnostmi:

✅ **Automaticky najde začátek** (hledá text "Činnost")
✅ **Přizpůsobí se počtu řádků** (break na prázdném řádku)
✅ **Funguje pro 1-50 řádků dat**
❌ **Špatný název** - "B4_I21" vypadá jako hardcoded pozice

### Příklad:
```
Excel má 5 řádků dat → načte 5 řádků
Excel má 15 řádků dat → načte 15 řádků
Excel má 80 řádků dat → načte prvních 50 řádků (limit)
```

---

## ⚠️ SKUTEČNÉ PROBLÉMY

### 1. **table_W4_Y51** - SKUTEČNĚ hardcoded!
```python
for row in ws.iter_rows(min_row=4, max_row=51, ...):
```
❌ Pokud má míň/víc řádků, selže

### 2. **table_somatometrie** - SKUTEČNĚ hardcoded!
```python
for row in ws.iter_rows(min_row=20, max_row=24, ...):
```
❌ Pokud je víc než 5 pracovníků, odřízne data

---

## 🔧 DOPORUČENÍ

### Oprav HARDCODED tabulky na dynamické:

#### table_W4_Y51:
```python
# PŘED (hardcoded):
for row in ws.iter_rows(min_row=4, max_row=51, ...):

# PO (dynamické):
for row in ws.iter_rows(min_row=4, max_row=200, ...):
    if not any(row):  # Prázdný řádek
        break
```

#### table_somatometrie:
```python
# PŘED (hardcoded):
for row in ws.iter_rows(min_row=20, max_row=24, ...):

# PO (dynamické):
for row in ws.iter_rows(min_row=20, max_row=100, ...):
    if all(cell is None or cell == '' for cell in row):
        break
```

---

## 📝 PŘEJMENUJ MATOUCÍ NÁZEV

```python
# PŘED:
results["table_B4_I21"] = table2

# PO (lepší názvy):
results["table_time_schedule"] = table2
# nebo
results["table_activities"] = table2
# nebo
results["table_worker_activities"] = table2
```
