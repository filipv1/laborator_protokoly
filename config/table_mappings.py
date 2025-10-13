"""
Mapování pro kopírování tabulkových dat do Excelů
"""

# ==================== CFZ ====================
CFZ_TABLE_MAPPING = {
    "sheet": "Časový snímek A+B",
    "start_row": 34,
    "end_row": 53,  # 20 řádků (34-53)
    "columns": {
        "operation": "C",      # Rozpis pracovních operací
        "time_min": "F",       # Čas/směna [min]
        "notes": "J"           # Poznámky
    }
}

# ==================== LSZ ====================
LSZ_TABLE_MAPPING = {
    "sheet": "Časový snímek",
    "start_row": 26,
    "end_row": 45,  # 20 řádků (26-45)
    "columns": {
        "operation": "C",      # Rozpis
        "time_min": "F",       # Čas/směna [min]
        "norm_pcs_hour": "J",  # Norma [ks/hod] - vypočítá se z pieces_count a time_min
        "notes": "M"           # Poznámky
    }
}

# ==================== PP ČAS ====================
PP_CAS_TABLE_MAPPING = {
    "sheet": "Časový snímek",
    "start_row": 13,
    "end_row": 42,  # 30 řádků (13-42)
    "columns": {
        "operation": "C",      # Rozpis
        "time_sec": "D",       # Čas [s] - konvertuje z minut na sekundy
        "notes": "L"           # Poznámky
    }
}

# ==================== PP KUSY ====================
PP_KUSY_TABLE_MAPPING = {
    "sheet": "Časový snímek",
    "start_row": 13,
    "end_row": 42,  # 30 řádků (13-42)
    "columns": {
        "operation": "C",      # Rozpis
        "time_sec": "D",       # Čas [s] - konvertuje z minut na sekundy
        "notes": "L"           # Poznámky
    }
}
