"""
Text Generator - generování podmínkových textů pro Word protokoly
"""
import math
from typing import Dict, Any, Optional


def _math_round(value: float) -> int:
    """
    Klasické matematické zaokrouhlování (ne Python banker's rounding).

    Args:
        value: Číslo k zaokrouhlení

    Returns:
        Zaokrouhlené celé číslo
    """
    return math.floor(value + 0.5)


def _find_in_table_W4_Y51(table: Dict[str, Dict], fmax_rounded: int) -> Optional[Dict[str, Any]]:
    """
    Najde řádek v table_W4_Y51, kde fmax odpovídá zaokrouhlené hodnotě.

    Args:
        table: table_W4_Y51 z results_data
        fmax_rounded: Zaokrouhlená hodnota Fmax

    Returns:
        Řádek z tabulky {"fmax": ..., "phk": ..., "lhk": ...} nebo None
    """
    # Projdi tabulku (skip header na indexu "1")
    for key, row in table.items():
        if key == "1":  # Skip header
            continue

        # Porovnej fmax
        if row.get("fmax") == fmax_rounded:
            return row

    return None


def _calculate_druhy_text_podminka_limit1(results_data: Dict[str, Any]) -> str:
    """
    Vypočítá text pro druhy_text_podminka_limit1 na základě překročení hygienických limitů.

    Args:
        results_data: Data z lsz_results.json

    Returns:
        Vygenerovaný text podle podmínek
    """
    # Definice textových variant
    TEXTS = {
        (1, 1): "překračují průměrné hygienické limity počtu pohybů pro naměřené vynakládané svalové síly extenzorů a flexorů předloktí pravé horní končetiny.",
        (1, 0): "překračují průměrné hygienické limity počtu pohybů pro naměřené vynakládané svalové síly extenzorů předloktí pravé horní končetiny. Pro flexory byl hygienický limit zachován.",
        (0, 1): "překračují průměrné hygienické limity počtu pohybů pro naměřené vynakládané svalové síly flexorů předloktí pravé horní končetiny. Pro extenzory byl hygienický limit zachován.",
        (0, 0): "nepřekračují průměrné hygienické limity počtu pohybů pro naměřené vynakládané svalové síly extenzorů a flexorů předloktí pravé horní končetiny."
    }

    # Načti data
    fmax_ext = results_data.get("Fmax_Phk_Extenzor")
    fmax_flex = results_data.get("Fmax_Phk_Flexor")
    phk_movements = results_data.get("phk_number_of_movements")
    table = results_data.get("table_W4_Y51", {})

    # Fallback pokud chybí data
    if fmax_ext is None or fmax_flex is None or phk_movements is None or not table:
        return TEXTS[(0, 0)]

    # VĚTEV 1: Extenzory
    fmax_ext_rounded = _math_round(fmax_ext)
    row_ext = _find_in_table_W4_Y51(table, fmax_ext_rounded)

    if row_ext is None:
        extenzor_flag = 0
    else:
        limit_ext = row_ext.get("phk", 0)
        extenzor_flag = 1 if phk_movements > limit_ext else 0

    # VĚTEV 2: Flexory
    fmax_flex_rounded = _math_round(fmax_flex)
    row_flex = _find_in_table_W4_Y51(table, fmax_flex_rounded)

    if row_flex is None:
        flexor_flag = 0
    else:
        limit_flex = row_flex.get("phk", 0)
        flexor_flag = 1 if phk_movements > limit_flex else 0

    # Vybrat text podle kombinace
    return TEXTS[(extenzor_flag, flexor_flag)]


def _calculate_treti_text_podminka_limit1(results_data: Dict[str, Any]) -> str:
    """
    Vypočítá text pro treti_text_podminka_limit1 na základě překročení hygienických limitů pro LHK.

    Args:
        results_data: Data z lsz_results.json

    Returns:
        Vygenerovaný text podle podmínek
    """
    # Definice textových variant
    TEXTS = {
        (1, 1): "překračují průměrné hygienické limity počtu pohybů pro naměřené vynakládané svalové síly extenzorů a flexorů předloktí levé horní končetiny.",
        (1, 0): "překračují průměrné hygienické limity počtu pohybů pro naměřené vynakládané svalové síly extenzorů předloktí levé horní končetiny. Pro flexory byl hygienický limit zachován.",
        (0, 1): "překračují průměrné hygienické limity počtu pohybů pro naměřené vynakládané svalové síly flexorů předloktí levé horní končetiny. Pro extenzory byl hygienický limit zachován.",
        (0, 0): "nepřekračují průměrné hygienické limity počtu pohybů pro naměřené vynakládané svalové síly extenzorů a flexorů předloktí levé horní končetiny."
    }

    # Načti data
    fmax_ext = results_data.get("Fmax_Lhk_Extenzor")
    fmax_flex = results_data.get("Fmax_Lhk_Flexor")
    lhk_movements = results_data.get("lhk_number_of_movements")
    table = results_data.get("table_W4_Y51", {})

    # Fallback pokud chybí data
    if fmax_ext is None or fmax_flex is None or lhk_movements is None or not table:
        return TEXTS[(0, 0)]

    # VĚTEV 1: Extenzory
    fmax_ext_rounded = _math_round(fmax_ext)
    row_ext = _find_in_table_W4_Y51(table, fmax_ext_rounded)

    if row_ext is None:
        extenzor_flag = 0
    else:
        limit_ext = row_ext.get("lhk", 0)
        extenzor_flag = 1 if lhk_movements > limit_ext else 0

    # VĚTEV 2: Flexory
    fmax_flex_rounded = _math_round(fmax_flex)
    row_flex = _find_in_table_W4_Y51(table, fmax_flex_rounded)

    if row_flex is None:
        flexor_flag = 0
    else:
        limit_flex = row_flex.get("lhk", 0)
        flexor_flag = 1 if lhk_movements > limit_flex else 0

    # Vybrat text podle kombinace
    return TEXTS[(extenzor_flag, flexor_flag)]


def _calculate_ctvrty_text_podminka(results_data: Dict[str, Any], worker_count: int = 2) -> str:
    """
    Vypočítá text pro ctvrty_text_podminka na základě rozložení svalových sil.

    Args:
        results_data: Data z lsz_results.json
        worker_count: Počet pracovníků (1 nebo 2)

    Returns:
        "nejsou" | "ojediněle" | "pravidelně"
    """
    # Načti tabulku force_distribution
    table = results_data.get("table_force_distribution", {})

    # Vyber správný řádek Celkem podle počtu pracovníků
    # Pro 1 pracovníka: řádek 7 (Celkem 1. měřené osoby)
    # Pro 2 pracovníky: řádek 21 (časově vážený průměr)
    celkem_row_key = "7" if worker_count == 1 else "21"
    row = table.get(celkem_row_key, {})

    # Pokud řádek neexistuje, fallback na "nejsou"
    if not row:
        return "nejsou"

    # Načti všechny 8 hodnot
    values = [
        row.get("force_55_70_phk_extenzory"),
        row.get("force_55_70_phk_flexory"),
        row.get("force_55_70_lhk_extenzory"),
        row.get("force_55_70_lhk_flexory"),
        row.get("force_over_70_phk_extenzory"),
        row.get("force_over_70_phk_flexory"),
        row.get("force_over_70_lhk_extenzory"),
        row.get("force_over_70_lhk_flexory")
    ]

    # Konvertuj None na 0 (fallback)
    values = [v if v is not None else 0 for v in values]

    # Podmínky (v tomto pořadí!)
    if all(v == 0 for v in values):
        return "nejsou"
    elif all(v >= 1 for v in values):
        return "pravidelně"
    else:
        return "ojediněle"


def _calculate_paty_text_podminka(results_data: Dict[str, Any], worker_count: int = 2) -> str:
    """
    Vypočítá text pro paty_text_podminka na základě nadlimitních svalových sil (nad 70% Fmax).

    Args:
        results_data: Data z lsz_results.json
        worker_count: Počet pracovníků (1 nebo 2)

    Returns:
        Text podle kombinace 4 hodnot force_over_70
    """
    # Načti tabulku force_distribution
    table = results_data.get("table_force_distribution", {})

    # Vyber správný řádek Celkem podle počtu pracovníků
    # Pro 1 pracovníka: řádek 7 (Celkem 1. měřené osoby)
    # Pro 2 pracovníky: řádek 21 (časově vážený průměr)
    celkem_row_key = "7" if worker_count == 1 else "21"
    row = table.get(celkem_row_key, {})

    # Pokud řádek neexistuje, fallback
    if not row:
        return "Při provádění práce nedochází k vynakládání nadlimitních svalových sil u všech měřených svalových skupin rukou a předloktí (nad 70 % Fmax)."

    # Načti 4 hodnoty (nadlimitní síly nad 70%)
    values = [
        row.get("force_over_70_phk_extenzory", 0),
        row.get("force_over_70_phk_flexory", 0),
        row.get("force_over_70_lhk_extenzory", 0),
        row.get("force_over_70_lhk_flexory", 0)
    ]

    # Konvertuj None na 0 (fallback)
    values = [v if v is not None else 0 for v in values]

    # Konvertuj na flags (>= 1 → 1, jinak 0)
    flags = tuple(1 if v >= 1 else 0 for v in values)

    # KOMPLETNÍ MAPPING VŠECH 16 KOMBINACÍ (2^4 = 16)
    PATTERNS = {
        (0, 0, 0, 0): "Při provádění práce nedochází k vynakládání nadlimitních svalových sil u všech měřených svalových skupin rukou a předloktí (nad 70 % Fmax).",

        (0, 0, 0, 1): "Při provádění práce dochází k vynakládání nadlimitních svalových sil u flexorů LHK (nad 70 % Fmax).",
        (0, 0, 1, 0): "Při provádění práce dochází k vynakládání nadlimitních svalových sil u extenzorů LHK (nad 70 % Fmax).",
        (0, 0, 1, 1): "Při provádění práce dochází k vynakládání nadlimitních svalových sil u měřených svalových skupin levé ruky a předloktí (nad 70 % Fmax).",

        (0, 1, 0, 0): "Při provádění práce dochází k vynakládání nadlimitních svalových sil u flexorů PHK (nad 70 % Fmax).",
        (0, 1, 0, 1): "Při provádění práce dochází k vynakládání nadlimitních svalových sil u měřených flexorových svalových skupin rukou a předloktí (nad 70 % Fmax).",
        (0, 1, 1, 0): "Při provádění práce dochází k vynakládání nadlimitních svalových sil u flexorů PHK a extenzorů LHK (nad 70 % Fmax).",
        (0, 1, 1, 1): "Při provádění práce dochází k vynakládání nadlimitních svalových sil u flexorů PHK, extenzorů LHK a flexorů LHK (nad 70 % Fmax).",

        (1, 0, 0, 0): "Při provádění práce dochází k vynakládání nadlimitních svalových sil u extenzorů PHK (nad 70 % Fmax).",
        (1, 0, 0, 1): "Při provádění práce dochází k vynakládání nadlimitních svalových sil u extenzorů PHK a flexorů LHK (nad 70 % Fmax).",
        (1, 0, 1, 0): "Při provádění práce dochází k vynakládání nadlimitních svalových sil u měřených extenzorových svalových skupin rukou a předloktí (nad 70 % Fmax).",
        (1, 0, 1, 1): "Při provádění práce dochází k vynakládání nadlimitních svalových sil u extenzorů PHK, extenzorů LHK a flexorů LHK (nad 70 % Fmax).",

        (1, 1, 0, 0): "Při provádění práce dochází k vynakládání nadlimitních svalových sil u měřených svalových skupin pravé ruky a předloktí (nad 70 % Fmax).",
        (1, 1, 0, 1): "Při provádění práce dochází k vynakládání nadlimitních svalových sil u extenzorů PHK, flexorů PHK a flexorů LHK (nad 70 % Fmax).",
        (1, 1, 1, 0): "Při provádění práce dochází k vynakládání nadlimitních svalových sil u extenzorů PHK, flexorů PHK a extenzorů LHK (nad 70 % Fmax).",
        (1, 1, 1, 1): "Při provádění práce dochází k vynakládání nadlimitních svalových sil u extenzorů PHK, flexorů PHK, extenzorů LHK a flexorů LHK (nad 70 % Fmax)."
    }

    return PATTERNS.get(flags, "Při provádění práce nedochází k vynakládání nadlimitních svalových sil u všech měřených svalových skupin rukou a předloktí (nad 70 % Fmax).")  # fallback pokud pattern neexistuje


def _calculate_sesty_text_podminka(results_data: Dict[str, Any], worker_count: int = 2) -> str:
    """
    Vypočítá text pro sesty_text_podminka na základě hodnot > 100.

    POUZE pro nadlimitní síly nad 70% Fmax (force_over_70_*).

    Args:
        results_data: Data z lsz_results.json
        worker_count: Počet pracovníků (1 nebo 2)

    Returns:
        Celá věta o pravidelnosti vynakládání nadlimitních svalových sil
    """
    # Načti tabulku force_distribution
    table = results_data.get("table_force_distribution", {})

    # Vyber správný řádek Celkem podle počtu pracovníků
    # Pro 1 pracovníka: řádek 7 (Celkem 1. měřené osoby)
    # Pro 2 pracovníky: řádek 21 (časově vážený průměr)
    celkem_row_key = "7" if worker_count == 1 else "21"
    row = table.get(celkem_row_key, {})

    # Pokud řádek neexistuje, fallback
    if not row:
        return "Vynakládání nadlimitních svalových sil není pravidelnou součástí výkonu prováděné práce."

    # Načti POUZE 4 hodnoty force_over_70 (nadlimitní síly nad 70%)
    values = [
        row.get("force_over_70_phk_extenzory", 0),
        row.get("force_over_70_phk_flexory", 0),
        row.get("force_over_70_lhk_extenzory", 0),
        row.get("force_over_70_lhk_flexory", 0)
    ]

    # Konvertuj None na 0 (fallback)
    values = [v if v is not None else 0 for v in values]

    # Pokud jakákoliv hodnota > 100
    if any(v > 100 for v in values):
        return "Vynakládání nadlimitních svalových sil je pravidelnou součástí výkonu prováděné práce."
    else:
        return "Vynakládání nadlimitních svalových sil není pravidelnou součástí výkonu prováděné práce."


def _calculate_sedmy_text_podminka(measurement_data: Dict[str, Any], results_data: Dict[str, Any], worker_count: int = 2) -> str:
    """
    Vypočítá text pro sedmy_text_podminka na základě překročení limitu pro velké svalové síly (55-70% Fmax).

    Logika:
    - Načti délku směny (work_duration v minutách)
    - Vypočti limit = (work_duration / 2) + 360
    - Sečti 4 hodnoty force_55_70_* z řádku Celkem
    - Pokud součet > limit → "překračuje u měřených svalových skupin..."
    - Jinak → "nepřekračuje u žádné z měřených svalových skupin..."

    Args:
        measurement_data: Data z measurement_data.json
        results_data: Data z lsz_results.json
        worker_count: Počet pracovníků (1 nebo 2)

    Returns:
        Celá věta o překročení/nepřekročení hygienického limitu
    """
    # Načti délku směny v minutách
    work_duration = measurement_data.get("section4_worker_a", {}).get("work_duration")

    # Pokud work_duration chybí, fallback
    if work_duration is None:
        return "Celosměnový počet těchto sil nepřekračuje u žádné z měřených svalových skupin rukou a předloktí daný hygienický limit."

    # Konvertuj na číslo (může být string z JSON)
    try:
        work_duration = float(work_duration)
    except (ValueError, TypeError):
        # Pokud konverze selže, fallback
        return "Celosměnový počet těchto sil nepřekračuje u žádné z měřených svalových skupin rukou a předloktí daný hygienický limit."

    # Vypočti limit podle vzorce: limit = (work_duration / 2) + 360
    limit = (work_duration / 2) + 360

    # Načti tabulku force_distribution
    table = results_data.get("table_force_distribution", {})

    # Vyber správný řádek Celkem podle počtu pracovníků
    # Pro 1 pracovníka: řádek 7 (Celkem 1. měřené osoby)
    # Pro 2 pracovníky: řádek 21 (časově vážený průměr)
    celkem_row_key = "7" if worker_count == 1 else "21"
    row = table.get(celkem_row_key, {})

    # Pokud řádek neexistuje, fallback
    if not row:
        return "Celosměnový počet těchto sil nepřekračuje u žádné z měřených svalových skupin rukou a předloktí daný hygienický limit."

    # Načti 4 hodnoty force_55_70_* (velké svalové síly 55-70% Fmax)
    suma_55_70 = (
        row.get("force_55_70_phk_extenzory", 0) +
        row.get("force_55_70_phk_flexory", 0) +
        row.get("force_55_70_lhk_extenzory", 0) +
        row.get("force_55_70_lhk_flexory", 0)
    )

    # Porovnej s limitem
    if suma_55_70 > limit:
        return "Celosměnový počet těchto sil překračuje u měřených svalových skupin rukou a předloktí daný hygienický limit."
    else:
        return "Celosměnový počet těchto sil nepřekračuje u žádné z měřených svalových skupin rukou a předloktí daný hygienický limit."


def _calculate_osmy_text_podminka(results_data: Dict[str, Any], worker_count: int = 2) -> str:
    """
    Vypočítá text pro osmy_text_podminka - seznam činností s force_over_70 > 100.

    Logika:
    - Pokud sesty_text_podminka = "není" → prázdný string
    - Pokud sesty_text_podminka = "je":
      - Projdi všechny řádky table_force_distribution (kromě "Celkem")
      - Pro každý řádek zkontroluj 4 hodnoty force_over_70_*
      - Pokud jakákoliv > 100 → přidej activity do seznamu
      - Vrať seznam oddělený čárkami

    Args:
        results_data: Data z lsz_results.json
        worker_count: Počet pracovníků (1 nebo 2)

    Returns:
        Seznam činností oddělený čárkami, nebo prázdný string
    """
    # Nejdřív zkontroluj sesty_text_podminka
    sesty = _calculate_sesty_text_podminka(results_data, worker_count)

    # Pokud sesty = "není", vrať prázdný string
    if sesty == "není":
        return ""

    # Sesty = "je", najdi konkrétní činnosti
    table = results_data.get("table_force_distribution", {})

    if not table:
        return ""

    activities = []

    # Projdi všechny řádky kromě "Celkem" řádků
    for key, row in table.items():
        # Načti activity
        activity = row.get("activity")
        if not activity:
            continue

        # Skip všechny řádky s "Celkem" (pro 1 pracovníka = 1 řádek, pro 2 = 3 řádky)
        if activity == "Celkem":
            continue

        # Zkontroluj 4 hodnoty force_over_70
        force_values = [
            row.get("force_over_70_phk_extenzory", 0),
            row.get("force_over_70_phk_flexory", 0),
            row.get("force_over_70_lhk_extenzory", 0),
            row.get("force_over_70_lhk_flexory", 0)
        ]

        # Konvertuj None na 0 (fallback pro null hodnoty z JSON)
        force_values = [v if v is not None else 0 for v in force_values]

        # Pokud jakákoliv > 100, přidej activity
        if any(v > 100 for v in force_values):
            activities.append(activity)

    # Vrať seznam oddělený čárkami (nebo prázdný string)
    if activities:
        return ", ".join(activities)
    else:
        return ""


def _calculate_devata_text_podminka(results_data: Dict[str, Any]) -> Dict[str, str]:
    """
    Vypočítá hodnoty pro tabulku hygienických limitů (devátá podmínka).

    Používá stejnou logiku jako druhá a třetí podmínka, ale vrací strukturovaná data
    pro všechny 4 svalové skupiny: PHK extenzory, PHK flexory, LHK extenzory, LHK flexory.

    Args:
        results_data: Data z lsz_results.json

    Returns:
        Dictionary s hodnotami pro tabulku:
        {
            "phk_extenzory": "Nad limitem" | "Pod limitem",
            "phk_flexory": "Nad limitem" | "Pod limitem",
            "lhk_extenzory": "Nad limitem" | "Pod limitem",
            "lhk_flexory": "Nad limitem" | "Pod limitem"
        }
    """
    # Default fallback hodnoty (všechno pod limitem)
    result = {
        "phk_extenzory": "Pod limitem",
        "phk_flexory": "Pod limitem",
        "lhk_extenzory": "Pod limitem",
        "lhk_flexory": "Pod limitem"
    }

    # Načti tabulku W4_Y51 a počty pohybů
    table = results_data.get("table_W4_Y51", {})
    if not table:
        return result

    phk_movements = results_data.get("phk_number_of_movements")
    lhk_movements = results_data.get("lhk_number_of_movements")

    # === PHK EXTENZORY ===
    fmax_phk_ext = results_data.get("Fmax_Phk_Extenzor")

    if fmax_phk_ext is not None and phk_movements is not None:
        fmax_rounded = _math_round(fmax_phk_ext)
        row = _find_in_table_W4_Y51(table, fmax_rounded)
        if row is not None:
            limit = row.get("phk", 0)
            if phk_movements > limit:
                result["phk_extenzory"] = "Nad limitem"

    # === PHK FLEXORY ===
    fmax_phk_flex = results_data.get("Fmax_Phk_Flexor")

    if fmax_phk_flex is not None and phk_movements is not None:
        fmax_rounded = _math_round(fmax_phk_flex)
        row = _find_in_table_W4_Y51(table, fmax_rounded)
        if row is not None:
            limit = row.get("phk", 0)
            if phk_movements > limit:
                result["phk_flexory"] = "Nad limitem"

    # === LHK EXTENZORY ===
    fmax_lhk_ext = results_data.get("Fmax_Lhk_Extenzor")

    if fmax_lhk_ext is not None and lhk_movements is not None:
        fmax_rounded = _math_round(fmax_lhk_ext)
        row = _find_in_table_W4_Y51(table, fmax_rounded)
        if row is not None:
            limit = row.get("lhk", 0)
            if lhk_movements > limit:
                result["lhk_extenzory"] = "Nad limitem"

    # === LHK FLEXORY ===
    fmax_lhk_flex = results_data.get("Fmax_Lhk_Flexor")

    if fmax_lhk_flex is not None and lhk_movements is not None:
        fmax_rounded = _math_round(fmax_lhk_flex)
        row = _find_in_table_W4_Y51(table, fmax_rounded)
        if row is not None:
            limit = row.get("lhk", 0)
            if lhk_movements > limit:
                result["lhk_flexory"] = "Nad limitem"

    return result


def _get_shift_duration_text(work_duration_minutes: float) -> str:
    """
    Převede délku směny v minutách na slovní vyjádření v češtině.

    Args:
        work_duration_minutes: Délka směny v minutách (240-840)

    Returns:
        Slovní vyjádření ve tvaru "(osmihodinovou)" nebo "(sedmi a půl hodinovou)"
    """
    # Mapování minut → text (4h až 14h, po půlhodinových incrementech)
    SHIFT_DURATION_MAP = {
        240: "(čtyřhodinovou)",
        270: "(čtyři a půl hodinovou)",
        300: "(pětihodinovou)",
        330: "(pět a půl hodinovou)",
        360: "(šestihodinovou)",
        390: "(šest a půl hodinovou)",
        420: "(sedmihodinovou)",
        450: "(sedmi a půl hodinovou)",
        480: "(osmihodinovou)",
        510: "(osmi a půl hodinovou)",
        540: "(devítihodinovou)",
        570: "(devíti a půl hodinovou)",
        600: "(desetihodinovou)",
        630: "(deseti a půl hodinovou)",
        660: "(jedenáctihodinovou)",
        690: "(jedenácti a půl hodinovou)",
        720: "(dvanáctihodinovou)",
        750: "(dvanácti a půl hodinovou)",
        780: "(třináctihodinovou)",
        810: "(třinácti a půl hodinovou)",
        840: "(čtrnáctihodinovou)"
    }

    # Zaokrouhli na nejbližších 30 minut
    rounded_minutes = round(work_duration_minutes / 30) * 30

    # Vrať text nebo fallback
    return SHIFT_DURATION_MAP.get(int(rounded_minutes), "(osmihodinovou)")


def _calculate_hygiene_limits(results_data: Dict[str, Any]) -> Dict[str, int]:
    """
    Vypočítá hygienické limity pro všechny 4 Fmax hodnoty z table_W4_Y51.

    Args:
        results_data: Data z lsz_results.json

    Returns:
        Dictionary s limity: {"phk_extenzor": 12500, "phk_flexor": 13000, ...}
    """
    table = results_data.get("table_W4_Y51", {})
    result = {}

    # PHK Extenzory
    fmax_phk_ext = results_data.get("Fmax_Phk_Extenzor")
    if fmax_phk_ext is not None:
        fmax_rounded = _math_round(fmax_phk_ext)
        row = _find_in_table_W4_Y51(table, fmax_rounded)
        if row is not None:
            result["phk_extenzor"] = row.get("phk", 0)

    # PHK Flexory
    fmax_phk_flex = results_data.get("Fmax_Phk_Flexor")
    if fmax_phk_flex is not None:
        fmax_rounded = _math_round(fmax_phk_flex)
        row = _find_in_table_W4_Y51(table, fmax_rounded)
        if row is not None:
            result["phk_flexor"] = row.get("phk", 0)

    # LHK Extenzory
    fmax_lhk_ext = results_data.get("Fmax_Lhk_Extenzor")
    if fmax_lhk_ext is not None:
        fmax_rounded = _math_round(fmax_lhk_ext)
        row = _find_in_table_W4_Y51(table, fmax_rounded)
        if row is not None:
            result["lhk_extenzor"] = row.get("lhk", 0)

    # LHK Flexory
    fmax_lhk_flex = results_data.get("Fmax_Lhk_Flexor")
    if fmax_lhk_flex is not None:
        fmax_rounded = _math_round(fmax_lhk_flex)
        row = _find_in_table_W4_Y51(table, fmax_rounded)
        if row is not None:
            result["lhk_flexor"] = row.get("lhk", 0)

    return result


def _calculate_desata_text_podminka(devata_data: Dict[str, str]) -> str:
    """
    Vypočítá text pro desatou podmínku - celkové překročení limitu.

    Zkontroluje všechny 4 hodnoty z devátého textu (phk_extenzory, phk_flexory,
    lhk_extenzory, lhk_flexory). Pokud je ALESPOŇ JEDNA "Nad limitem",
    vrátí "Nad limitem", jinak "Pod limitem".

    Args:
        devata_data: Výstup z _calculate_devata_text_podminka
                    {"phk_extenzory": "Nad limitem" | "Pod limitem", ...}

    Returns:
        "Nad limitem" | "Pod limitem"
    """
    # Zkontroluj všechny 4 hodnoty
    values = [
        devata_data.get("phk_extenzory", "Pod limitem"),
        devata_data.get("phk_flexory", "Pod limitem"),
        devata_data.get("lhk_extenzory", "Pod limitem"),
        devata_data.get("lhk_flexory", "Pod limitem")
    ]

    # Pokud je alespoň jedna hodnota "Nad limitem", vrať "Nad limitem"
    if any(v == "Nad limitem" for v in values):
        return "Nad limitem"
    else:
        return "Pod limitem"


def _calculate_jedenacta_text_podminka(results_data: Dict[str, Any]) -> str:
    """
    Vypočítá text pro jedenáctou podmínku - hierarchické vyhodnocení zatížení všech svalových skupin.

    Vyhodnotí všechny 4 svalové skupiny (PHK extenzory, PHK flexory, LHK extenzory, LHK flexory)
    vzhledem k jejich hygienickým limitům.

    HIERARCHIE (priorita od nejvyšší):
    3. Alespoň jeden sval překračuje hygienický limit (počet pohybů > limit)
    2. Alespoň jeden sval je nad 1/3 hygienického limitu, ale žádný nepřekračuje celý limit
    1. Žádný sval není nad 1/3 hygienického limitu

    Args:
        results_data: Data z lsz_results.json

    Returns:
        "1" - žádný sval není nad 1/3 hygienického limitu
        "2" - alespoň jeden sval je nad 1/3 limitu, ale žádný nepřekračuje limit
        "3" - alespoň jeden sval překračuje hygienický limit
    """
    table = results_data.get("table_W4_Y51", {})
    phk_movements = results_data.get("phk_number_of_movements")
    lhk_movements = results_data.get("lhk_number_of_movements")

    # Fallback pokud chybí data
    if not table or phk_movements is None or lhk_movements is None:
        return "1"

    # Flagy pro vyhodnocení
    over_limit = False  # Alespoň jeden sval > limit
    over_one_third = False  # Alespoň jeden sval > 1/3 limitu

    # === PHK EXTENZORY ===
    fmax_phk_ext = results_data.get("Fmax_Phk_Extenzor")
    if fmax_phk_ext is not None:
        fmax_rounded = _math_round(fmax_phk_ext)
        row = _find_in_table_W4_Y51(table, fmax_rounded)
        if row is not None:
            limit = row.get("phk", 0)
            one_third_limit = limit / 3

            if phk_movements > limit:
                over_limit = True
            elif phk_movements > one_third_limit:
                over_one_third = True

    # === PHK FLEXORY ===
    fmax_phk_flex = results_data.get("Fmax_Phk_Flexor")
    if fmax_phk_flex is not None:
        fmax_rounded = _math_round(fmax_phk_flex)
        row = _find_in_table_W4_Y51(table, fmax_rounded)
        if row is not None:
            limit = row.get("phk", 0)
            one_third_limit = limit / 3

            if phk_movements > limit:
                over_limit = True
            elif phk_movements > one_third_limit:
                over_one_third = True

    # === LHK EXTENZORY ===
    fmax_lhk_ext = results_data.get("Fmax_Lhk_Extenzor")
    if fmax_lhk_ext is not None:
        fmax_rounded = _math_round(fmax_lhk_ext)
        row = _find_in_table_W4_Y51(table, fmax_rounded)
        if row is not None:
            limit = row.get("lhk", 0)
            one_third_limit = limit / 3

            if lhk_movements > limit:
                over_limit = True
            elif lhk_movements > one_third_limit:
                over_one_third = True

    # === LHK FLEXORY ===
    fmax_lhk_flex = results_data.get("Fmax_Lhk_Flexor")
    if fmax_lhk_flex is not None:
        fmax_rounded = _math_round(fmax_lhk_flex)
        row = _find_in_table_W4_Y51(table, fmax_rounded)
        if row is not None:
            limit = row.get("lhk", 0)
            one_third_limit = limit / 3

            if lhk_movements > limit:
                over_limit = True
            elif lhk_movements > one_third_limit:
                over_one_third = True

    # Hierarchické vyhodnocení (priorita: 3 > 2 > 1)
    if over_limit:
        return "3"
    elif over_one_third:
        return "2"
    else:
        return "1"


def generate_conditional_texts(measurement_data: Dict[str, Any], results_data: Optional[Dict[str, Any]] = None) -> Dict[str, str]:
    """
    Vygeneruje podmínkové texty na základě dat z measurement_data.json a results_data.

    Args:
        measurement_data: Data z measurement_data.json (celý JSON)
        results_data: Data z lsz_results.json (celý JSON), volitelné

    Returns:
        Dictionary s vygenerovanými texty:
        {
            "prvni_text_podminka_pocetdni": "...",
            "druhy_text_podminka_limit1": "...",
            "treti_text_podminka_limit1": "...",
            "ctvrty_text_podminka": "...",
            "paty_text_podminka": "...",
            "sesty_text_podminka": "...",
            "sedmy_text_podminka": "...",
            "osmy_text_podminka": "...",
            "devata_text_podminka": {...}  (dictionary s hodnotami tabulky)
        }
    """
    texts = {}

    # PODMÍNKA 1: Počet dnů měření + pohlaví + počet pracovníků
    section0 = measurement_data.get("section0_file_selection", {})
    section2 = measurement_data.get("section2_firma", {})
    measurement_days = section2.get("measurement_days", 1)  # Z section2_firma
    gender = section0.get("workers_gender", "muži")          # Z section0_file_selection
    worker_count = section0.get("worker_count", 2)           # Z section0_file_selection

    # Matice všech kombinací (2 dny × 2 worker_count × 2 pohlaví = 8 variant)
    prvni_text_varianty = {
        # 1 pracovník, 1 den
        (1, 1, "muži"): "Měření probíhalo v jednom dni, v jedné průměrné směně. Měřen byl 1 pracovník – muž.",
        (1, 1, "ženy"): "Měření probíhalo v jednom dni, v jedné průměrné směně. Měřena byla 1 pracovnice – žena.",

        # 1 pracovník, 2 dny
        (2, 1, "muži"): "Měření probíhalo ve dvou dnech, ve dvou průměrných směnách. Měřen byl 1 pracovník – muž.",
        (2, 1, "ženy"): "Měření probíhalo ve dvou dnech, ve dvou průměrných směnách. Měřena byla 1 pracovnice – žena.",

        # 2 pracovníci, 1 den
        (1, 2, "muži"): "Měření probíhalo v jednom dni, v jedné průměrné směně. Měřeni byli 2 pracovníci – muži.",
        (1, 2, "ženy"): "Měření probíhalo v jednom dni, v jedné průměrné směně. Měřeny byly 2 pracovnice – ženy.",

        # 2 pracovníci, 2 dny
        (2, 2, "muži"): "Měření probíhalo ve dvou dnech, ve dvou průměrných směnách. Měřeni byli 2 pracovníci – muži.",
        (2, 2, "ženy"): "Měření probíhalo ve dvou dnech, ve dvou průměrných směnách. Měřeny byly 2 pracovnice – ženy.",
    }

    texts["prvni_text_podminka_pocetdni"] = prvni_text_varianty.get((measurement_days, worker_count, gender), prvni_text_varianty[(1, 2, "muži")])

    # PODMÍNKA 2: Hygienické limity PHK (pouze pokud jsou k dispozici results_data)
    if results_data is not None:
        texts["druhy_text_podminka_limit1"] = _calculate_druhy_text_podminka_limit1(results_data)

    # PODMÍNKA 3: Hygienické limity LHK (pouze pokud jsou k dispozici results_data)
    if results_data is not None:
        texts["treti_text_podminka_limit1"] = _calculate_treti_text_podminka_limit1(results_data)

    # PODMÍNKA 4: Rozložení svalových sil (pouze pokud jsou k dispozici results_data)
    if results_data is not None:
        texts["ctvrty_text_podminka"] = _calculate_ctvrty_text_podminka(results_data, worker_count)

    # PODMÍNKA 5: Nadlimitní svalové síly nad 70% Fmax (pouze pokud jsou k dispozici results_data)
    if results_data is not None:
        texts["paty_text_podminka"] = _calculate_paty_text_podminka(results_data, worker_count)

    # PODMÍNKA 6: Hodnoty > 100 (pouze pokud jsou k dispozici results_data)
    if results_data is not None:
        texts["sesty_text_podminka"] = _calculate_sesty_text_podminka(results_data, worker_count)

    # PODMÍNKA 7: Překročení limitu pro velké svalové síly 55-70% Fmax (vyžaduje measurement_data i results_data)
    if results_data is not None:
        texts["sedmy_text_podminka"] = _calculate_sedmy_text_podminka(measurement_data, results_data, worker_count)

    # PODMÍNKA 8: Seznam činností s force_over_70 > 100 (pouze pokud jsou k dispozici results_data)
    if results_data is not None:
        texts["osmy_text_podminka"] = _calculate_osmy_text_podminka(results_data, worker_count)

    # PODMÍNKA 9: Tabulka hygienických limitů (Nad limitem / Pod limitem pro všechny 4 svalové skupiny)
    if results_data is not None:
        texts["devata_text_podminka"] = _calculate_devata_text_podminka(results_data)

    # PODMÍNKA 10: Celkové překročení limitu (pokud je alespoň jedna svalová skupina nad limitem)
    if results_data is not None:
        devata_data = texts.get("devata_text_podminka", {})
        texts["desata_text_podminka"] = _calculate_desata_text_podminka(devata_data)

    # PODMÍNKA 11: Hierarchické vyhodnocení zatížení (1/3 limitu vs celý limit)
    if results_data is not None:
        texts["jedenacta_text_podminka"] = _calculate_jedenacta_text_podminka(results_data)

    # HYGIENICKÉ LIMITY: Číselné hodnoty limitů z table_W4_Y51
    if results_data is not None:
        texts["hygiene_limits"] = _calculate_hygiene_limits(results_data)

    # HYGIENICKÝ LIMIT PRO 55-70% FMAX: Vypočítané číslo podle délky směny
    work_duration = measurement_data.get("section4_worker_a", {}).get("work_duration")
    if work_duration is not None:
        try:
            work_duration = float(work_duration)
            texts["hygiene_limit_55_70"] = int((work_duration / 2) + 360)
            texts["shift_duration_text"] = _get_shift_duration_text(work_duration)
        except (ValueError, TypeError):
            texts["hygiene_limit_55_70"] = 600  # Fallback pro 8h směnu
            texts["shift_duration_text"] = "(osmihodinovou)"
    else:
        texts["hygiene_limit_55_70"] = 600  # Fallback pro 8h směnu
        texts["shift_duration_text"] = "(osmihodinovou)"

    # PODMÍNĚNÉ PLACEHOLDERY: Vypíší text pouze pokud je překročení
    # Sesty text - pokud DOCHÁZÍ k pravidelným nadlimitním silám (> 100)
    if results_data is not None:
        sesty = texts.get("sesty_text_podminka", "")
        if "je pravidelnou součástí" in sesty:
            texts["sesty_text_if_true"] = texts["sesty_text_podminka"]
        else:
            texts["sesty_text_if_true"] = ""

    # Sedmy text - pokud PŘEKRAČUJE limit pro 55-70% Fmax
    if results_data is not None:
        sedmy = texts.get("sedmy_text_podminka", "")
        if "překračuje" in sedmy and "nepřekračuje" not in sedmy:
            texts["sedmy_text_if_true"] = texts["sedmy_text_podminka"]
        else:
            texts["sedmy_text_if_true"] = ""

    return texts


# ============================================================================
# HOLTER FORMATTING - Zvýraznění vybraných holterů ve Word tabulce
# ============================================================================

# Mapování holter ID → číslo holteru v textu
HOLTER_MAPPING = {
    "A": "60/16",
    "B": "65/17",
    "C": "84/19",
    "D": "85/19",
    "E": "86/20",
    "F": "87/20"
}


def get_selected_holter_numbers(measurement_data: Dict[str, Any]) -> list:
    """
    Zjistí vybraná čísla holterů z measurement_data.

    Args:
        measurement_data: Data z measurement_data.json (celý JSON)

    Returns:
        List čísel holterů (např. ["65/17", "85/19"])
    """
    selected = []

    # Pracovník A
    holter_a = measurement_data.get("section4_worker_a", {}).get("emg_holter")
    if holter_a and holter_a in HOLTER_MAPPING:
        selected.append(HOLTER_MAPPING[holter_a])

    # Pracovník B
    holter_b = measurement_data.get("section5_worker_b", {}).get("emg_holter")
    if holter_b and holter_b in HOLTER_MAPPING:
        selected.append(HOLTER_MAPPING[holter_b])

    return selected


def highlight_selected_holters(docx_path: str, selected_holter_numbers: list) -> None:
    """
    Zvýrazní tučně řádky s vybranými holtry v tabulce měřících přístrojů.

    BEZPEČNÝ PŘÍSTUP: Post-processing po vyrendrování šablony.
    Nepoužívá RichText v tabulkách (riskantní), ale upravuje hotový dokument.

    Args:
        docx_path: Cesta k vygenerovanému Word dokumentu
        selected_holter_numbers: List čísel holterů (např. ["65/17", "85/19"])

    Returns:
        None (upravuje dokument in-place)
    """
    from docx import Document

    # Pokud nejsou vybrané holteru, není co zvýrazňovat
    if not selected_holter_numbers:
        return

    # Otevři dokument
    doc = Document(docx_path)

    # Najdi správnou tabulku (ta s nadpisem "Typ" v prvním sloupci)
    for table in doc.tables:
        if len(table.rows) == 0:
            continue

        # Zkontroluj první buňku prvního řádku (hlavička)
        first_cell_text = table.rows[0].cells[0].text.strip()

        # Pokud obsahuje "Typ", je to správná tabulka
        if "Typ" in first_cell_text:
            # Projdi všechny řádky kromě hlavičky
            for row_idx, row in enumerate(table.rows[1:], start=1):
                cell_text = row.cells[0].text

                # Pokud řádek obsahuje vybraný holter
                if any(holter_num in cell_text for holter_num in selected_holter_numbers):
                    # Nastav bold pro všechny runs v prvním sloupci
                    for paragraph in row.cells[0].paragraphs:
                        for run in paragraph.runs:
                            run.bold = True

            # Tabulku jsme našli a zpracovali, můžeme skončit
            break

    # Ulož změny (přepíše originální soubor)
    doc.save(docx_path)


# ============================================================================
# FORCE DISTRIBUTION HIGHLIGHTING - Červené zvýraznění nadlimitních hodnot
# ============================================================================

def highlight_force_distribution_values(docx_path: str, measurement_data: Dict[str, Any], results_data: Dict[str, Any]) -> None:
    """
    Červeně zvýrazní nadlimitní hodnoty v tabulce force_distribution.

    DVOJE KRITÉRIA:
    1. force_over_70_* > 100 → červeně
    2. force_55_70_* > hygienický limit → červeně
       - Limit = (work_duration / 2) + 360 (stejná logika jako sedmá podmínka)

    BEZPEČNÝ PŘÍSTUP: Post-processing po vyrendrování šablony.
    Nepoužívá RichText v tabulkách (riskantní), ale upravuje hotový dokument.

    Args:
        docx_path: Cesta k vygenerovanému Word dokumentu
        measurement_data: Data z measurement_data.json (pro work_duration)
        results_data: Data z lsz_results.json (pro table_force_distribution)

    Returns:
        None (upravuje dokument in-place)
    """
    from docx import Document
    from docx.shared import RGBColor

    # Vypočti hygienický limit pro force_55_70 (stejná logika jako sedmá podmínka)
    work_duration = measurement_data.get("section4_worker_a", {}).get("work_duration")

    if work_duration is None:
        # Fallback - pokud není work_duration, použij výchozí 8h směnu
        limit_55_70 = 600
    else:
        try:
            work_duration = float(work_duration)
            limit_55_70 = (work_duration / 2) + 360
        except (ValueError, TypeError):
            limit_55_70 = 600  # Fallback

    # Načti tabulku force_distribution
    table_force_dist = results_data.get("table_force_distribution", {})
    if not table_force_dist:
        return  # Není co zvýrazňovat

    # Otevři dokument
    doc = Document(docx_path)

    # Najdi správnou tabulku - tabulka force_distribution
    # Identifikace:
    # - 9 sloupců (activity + 8 hodnot)
    # - Obsahuje "Výskyt sil" nebo "Rozpis" v hlavičce
    target_table = None
    for table_idx, table in enumerate(doc.tables):
        if len(table.rows) < 2:
            continue

        # Zkontroluj hlavičku
        header_row = table.rows[0]

        # Musí mít 9 sloupců
        if len(header_row.cells) != 9:
            continue

        header_text = " ".join([cell.text for cell in header_row.cells]).lower()

        # Musí obsahovat klíčová slova
        if ("výskyt sil" in header_text or "vyskyt sil" in header_text) and \
           ("rozpis" in header_text or "innost" in header_text or "activity" in header_text):
            target_table = table
            break

    if target_table is None:
        return  # Tabulka nenalezena

    # Identifikuj indexy sloupců (force_over_70 a force_55_70)
    # Struktura tabulky (podle TABLES_ANALYSIS.md):
    # Sloupec 0: activity
    # Sloupec 1-4: force_55_70 (PHK ext, PHK flex, LHK ext, LHK flex)
    # Sloupec 5-8: force_over_70 (PHK ext, PHK flex, LHK ext, LHK flex)

    force_55_70_columns = [1, 2, 3, 4]  # PHK ext, PHK flex, LHK ext, LHK flex
    force_over_70_columns = [5, 6, 7, 8]  # PHK ext, PHK flex, LHK ext, LHK flex

    # Projdi všechny řádky
    for row_idx, row in enumerate(target_table.rows):
        # Zpracuj VŠECHNY řádky včetně "Celkem" a "Časově vážený průměr"
        # Skip pouze řádky hlavičky - pozná se tak, že sloupec 5 není číslo

        # Zkontroluj, jestli je to hlavička (sloupec 5 není číslo)
        try:
            test_value = row.cells[5].text.strip()
            float(test_value)  # Pokud to selže, je to hlavička
        except (ValueError, IndexError):
            continue  # Skip hlavičku

        # === FORCE_OVER_70: Zkontroluj hodnoty > 100 ===
        for col_idx in force_over_70_columns:
            if col_idx >= len(row.cells):
                continue

            cell = row.cells[col_idx]
            cell_text = cell.text.strip()

            try:
                value = float(cell_text)
                if value > 100:
                    # Obarvi červeně - MUSÍME PŘEPSAT OBSAH, NE JEN MĚNIT BARVU
                    # Docxtpl může vytvářet speciální run strukturu, která se neobarvuje správně

                    # Smaž všechny paragraphy
                    for paragraph in cell.paragraphs:
                        p = paragraph._element
                        p.getparent().remove(p)

                    # Vytvoř nový paragraph s červeným runem
                    new_para = cell.add_paragraph()
                    run = new_para.add_run(cell_text)
                    run.font.color.rgb = RGBColor(255, 0, 0)
            except (ValueError, TypeError):
                pass  # Není číslo, skip

        # === FORCE_55_70: Zkontroluj hodnoty > limit ===
        for col_idx in force_55_70_columns:
            if col_idx >= len(row.cells):
                continue

            cell = row.cells[col_idx]
            cell_text = cell.text.strip()

            try:
                value = float(cell_text)
                if value > limit_55_70:
                    # Obarvi červeně - MUSÍME PŘEPSAT OBSAH, NE JEN MĚNIT BARVU

                    # Smaž všechny paragraphy
                    for paragraph in cell.paragraphs:
                        p = paragraph._element
                        p.getparent().remove(p)

                    # Vytvoř nový paragraph s červeným runem
                    new_para = cell.add_paragraph()
                    run = new_para.add_run(cell_text)
                    run.font.color.rgb = RGBColor(255, 0, 0)
            except (ValueError, TypeError):
                pass  # Není číslo, skip

    # Ulož změny (přepíše originální soubor)
    doc.save(docx_path)
