"""
Mapování polí z JSON do Excel buněk
"""

# ==================== LSZ ====================
LSZ_MAPPING = {
    "Časový snímek": {
        # Pracovník A (sloupec D)
        "D12": "section4_worker_a.full_name",
        "D14": "section3_additional_data.workers_gender",
        "D15": "section4_worker_a.laterality",
        "D16": "section4_worker_a.age_years",
        "D17": "section4_worker_a.exposure_length_years",
        "D18": "section4_worker_a.height_cm",
        "D19": "section4_worker_a.weight_kg",
        "D20": "section4_worker_a.grip_strength_phk_n",
        "D21": "section4_worker_a.grip_strength_lhk_n",
        "D22": "section4_worker_a.emg_holter",
        "D23": "section4_worker_a.measurement_start",

        # Pracovník B (sloupec K, stejné řádky)
        "K12": "section5_worker_b.full_name",
        "K14": "section3_additional_data.workers_gender",
        "K15": "section5_worker_b.laterality",
        "K16": "section5_worker_b.age_years",
        "K17": "section5_worker_b.exposure_length_years",
        "K18": "section5_worker_b.height_cm",
        "K19": "section5_worker_b.weight_kg",
        "K20": "section5_worker_b.grip_strength_phk_n",
        "K21": "section5_worker_b.grip_strength_lhk_n",
        "K22": "section5_worker_b.emg_holter",
        "K23": "section5_worker_b.measurement_start",
    }
}

# ==================== PP ČAS ====================
PP_CAS_MAPPING = {
    "Časový snímek": {
        "D3": "section2_firma.company",
        "D4": "section2_firma.profession_name",
        "D5": "section4_worker_a.full_name",
        "D6": "section4_worker_a.age_years",
        "D7": "section2_firma.measurement_date",
        "D8": "section2_firma.shift_pattern",
        "D9": "section6_final.measured_by",

        # Pracovník B (sloupec T, jen jméno a věk)
        "T5": "section5_worker_b.full_name",
        "T6": "section5_worker_b.age_years",
    }
}

# ==================== PP KUSY ====================
PP_KUSY_MAPPING = {
    "Časový snímek": {
        "D3": "section2_firma.company",
        "D4": "section2_firma.profession_name",
        "D5": "section4_worker_a.full_name",
        "D6": "section4_worker_a.age_years",
        "D7": "section2_firma.measurement_date",
        "D8": "section2_firma.shift_pattern",
        "D9": "section6_final.measured_by",

        # Pracovník B (sloupec T, jen jméno a věk)
        "T5": "section5_worker_b.full_name",
        "T6": "section5_worker_b.age_years",
    }
}

# ==================== CFZ ====================
CFZ_MAPPING = {
    "Časový snímek A+B": {
        # Pracovník A (sloupec D)
        "D12": "section4_worker_a.full_name",
        "D14": "section3_additional_data.workers_gender",
        "D15": "section4_worker_a.exposure_length_years",
        "D16": "section4_worker_a.age_years",
        "D17": "section4_worker_a.height_cm",
        "D18": "section4_worker_a.weight_kg",

        # Pracovník B (sloupec K, stejné řádky)
        "K12": "section5_worker_b.full_name",
        "K14": "section3_additional_data.workers_gender",
        "K15": "section5_worker_b.exposure_length_years",
        "K16": "section5_worker_b.age_years",
        "K17": "section5_worker_b.height_cm",
        "K18": "section5_worker_b.weight_kg",
    }
}
