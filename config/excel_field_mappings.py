"""
Mapování polí z JSON do Excel buněk
"""

# ==================== LSZ ====================
LSZ_MAPPING = {
    "Časový snímek": {
        # Pracovník A (sloupec D)
        "D12": "section3_worker_a.full_name",
        "D14": "section2_additional_data.workers_gender",
        "D15": "section3_worker_a.laterality",
        "D16": "section3_worker_a.age_years",
        "D17": "section3_worker_a.exposure_length_years",
        "D18": "section3_worker_a.height_cm",
        "D19": "section3_worker_a.weight_kg",
        "D20": "section3_worker_a.grip_strength_phk_n",
        "D21": "section3_worker_a.grip_strength_lhk_n",
        "D22": "section3_worker_a.emg_holter",
        "D23": "section3_worker_a.measurement_start",

        # Pracovník B (sloupec K, stejné řádky)
        "K12": "section4_worker_b.full_name",
        "K14": "section2_additional_data.workers_gender",
        "K15": "section4_worker_b.laterality",
        "K16": "section4_worker_b.age_years",
        "K17": "section4_worker_b.exposure_length_years",
        "K18": "section4_worker_b.height_cm",
        "K19": "section4_worker_b.weight_kg",
        "K20": "section4_worker_b.grip_strength_phk_n",
        "K21": "section4_worker_b.grip_strength_lhk_n",
        "K22": "section4_worker_b.emg_holter",
        "K23": "section4_worker_b.measurement_start",
    }
}

# ==================== PP ČAS ====================
PP_CAS_MAPPING = {
    "Časový snímek": {
        "D3": "section1_firma.company",
        "D4": "section1_firma.profession_name",
        "D5": "section3_worker_a.full_name",
        "D6": "section3_worker_a.age_years",
        "D7": "section1_firma.measurement_date",
        "D8": "section1_firma.shift_pattern",
        "D9": "section5_final.measured_by",

        # Pracovník B (sloupec T, jen jméno a věk)
        "T5": "section4_worker_b.full_name",
        "T6": "section4_worker_b.age_years",
    }
}

# ==================== PP KUSY ====================
PP_KUSY_MAPPING = {
    "Časový snímek": {
        "D3": "section1_firma.company",
        "D4": "section1_firma.profession_name",
        "D5": "section3_worker_a.full_name",
        "D6": "section3_worker_a.age_years",
        "D7": "section1_firma.measurement_date",
        "D8": "section1_firma.shift_pattern",
        "D9": "section5_final.measured_by",

        # Pracovník B (sloupec T, jen jméno a věk)
        "T5": "section4_worker_b.full_name",
        "T6": "section4_worker_b.age_years",
    }
}

# ==================== CFZ ====================
CFZ_MAPPING = {
    "Časový snímek A+B": {
        # Pracovník A (sloupec D)
        "D12": "section3_worker_a.full_name",
        "D14": "section2_additional_data.workers_gender",
        "D15": "section3_worker_a.exposure_length_years",
        "D16": "section3_worker_a.age_years",
        "D17": "section3_worker_a.height_cm",
        "D18": "section3_worker_a.weight_kg",

        # Pracovník B (sloupec K, stejné řádky)
        "K12": "section4_worker_b.full_name",
        "K14": "section2_additional_data.workers_gender",
        "K15": "section4_worker_b.exposure_length_years",
        "K16": "section4_worker_b.age_years",
        "K17": "section4_worker_b.height_cm",
        "K18": "section4_worker_b.weight_kg",
    }
}
