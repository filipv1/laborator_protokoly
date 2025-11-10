# GUI Redesign Plan - Multi-Protocol Support

## Cíl
Umožnit uživateli generovat více Word protokolů najednou (LSZ, PP, CFZ) podle toho, jaké Excel soubory má ve složce projektu.

## Nový UI Layout

```
╔═════════════════════════════════════════════════════════════════╗
║           GENEROVÁNÍ WORD PROTOKOLŮ                             ║
╠═════════════════════════════════════════════════════════════════╣
║                                                                 ║
║ 1️⃣ Složka projektu                                              ║
║ [C:\...\projects\001-2024_Firma]  [Vybrat složku...]           ║
║ ✓ measurement_data.json nalezen                                ║
║                                                                 ║
║ ─────────────────────────────────────────────────────────────── ║
║                                                                 ║
║ 2️⃣ Dostupné protokoly (vyberte, které chcete generovat)        ║
║                                                                 ║
║ ☑ LSZ - Lokální svalová zátěž                                  ║
║   Excel: LSZ_001-2024_Firma.xlsm ✓                             ║
║   Template: [lsz_placeholdery_v2.docx ▼]                       ║
║   Výstup: LSZ_protokol.docx                                    ║
║                                                                 ║
║ ☑ PP - Pracovní polohy (ČAS)                                   ║
║   Excel: PP_001-2024_Firma_CAS.xlsx ✓                          ║
║   Template: [PP_placeholdery_v2.docx ▼]                        ║
║   Výstup: PP_CAS_protokol.docx                                 ║
║                                                                 ║
║ ☐ PP - Pracovní polohy (KUSY)                                  ║
║   Excel: PP_001-2024_Firma_KUSY.xlsx ✓                         ║
║   Template: [PP_placeholdery_v2.docx ▼]                        ║
║   Výstup: PP_KUSY_protokol.docx                                ║
║                                                                 ║
║ ☐ CFZ - Celková fyzická zátěž                                  ║
║   Excel: CFZ_001-2024_Firma.xlsx ✓                             ║
║   Template: [CFZ_placeholdery_v2.docx ▼]                       ║
║   Výstup: CFZ_protokol.docx                                    ║
║                                                                 ║
║ ─────────────────────────────────────────────────────────────── ║
║                                                                 ║
║                                      [Zrušit]  [Generovat (2)]  ║
║                                                                 ║
╚═════════════════════════════════════════════════════════════════╝
```

## Klíčové změny

### 1. Detekce Excel souborů ve složce
```python
def _detect_available_protocols(self):
    """Detekuje, jaké Excel soubory jsou ve složce"""
    protocols = {}

    # LSZ
    lsz_files = list(self.project_folder.glob("LSZ_*.xlsm"))
    if lsz_files:
        protocols["LSZ"] = lsz_files[0]

    # PP ČAS
    pp_cas_files = list(self.project_folder.glob("PP_*_CAS.xlsx"))
    if pp_cas_files:
        protocols["PP_CAS"] = pp_cas_files[0]

    # PP KUSY
    pp_kusy_files = list(self.project_folder.glob("PP_*_KUSY.xlsx"))
    if pp_kusy_files:
        protocols["PP_KUSY"] = pp_kusy_files[0]

    # CFZ
    cfz_files = list(self.project_folder.glob("CFZ_*.xlsx"))
    if cfz_files:
        protocols["CFZ"] = cfz_files[0]

    return protocols
```

### 2. Dynamické vytvoření UI pro každý protokol
```python
def _create_protocol_section(self, protocol_type, excel_path, worker_count, gender):
    """Vytvoří UI sekci pro jeden protokol"""
    section = QWidget()
    layout = QVBoxLayout(section)

    # Checkbox pro enable/disable
    checkbox = QCheckBox(self._get_protocol_name(protocol_type))
    checkbox.setChecked(True)  # Default: checked

    # Excel path (readonly)
    excel_label = QLabel(f"Excel: {excel_path.name}")

    # Template dropdown
    template_combo = QComboBox()
    templates = self._get_templates_for_protocol(protocol_type, worker_count, gender)
    for tmpl_name, tmpl_path in templates:
        template_combo.addItem(tmpl_name, tmpl_path)

    # Output path
    output_label = QLabel(f"Výstup: {self._suggest_output_name(protocol_type)}")

    layout.addWidget(checkbox)
    layout.addWidget(excel_label)
    layout.addWidget(template_combo)
    layout.addWidget(output_label)

    return section, checkbox, template_combo
```

### 3. Template mapping pro všechny protokoly
```python
def _get_templates_for_protocol(self, protocol_type, worker_count, gender):
    """Vrátí dostupné templates pro daný protokol"""

    # Mapping: (protocol, worker_count, gender) → [(display_name, path), ...]
    template_map = {
        ("LSZ", 2, "muži"): [
            ("LSZ - 2 muži (standard)", Path("sample_protocols/.../lsz_placeholdery_v2.docx")),
        ],
        ("PP_CAS", 2, "muži"): [
            ("PP ČAS - 2 muži", Path("sample_protocols/.../PP_CAS_placeholdery_v2.docx")),
        ],
        # ... další kombinace
    }

    key = (protocol_type, worker_count, gender)
    return template_map.get(key, [])
```

### 4. Generování více protokolů najednou
```python
def _generate(self):
    """Spustí generování pro všechny zaškrtnuté protokoly"""

    protocols_to_generate = []

    # Projdi všechny protocol checkboxy
    for protocol_type, (checkbox, template_combo, excel_path) in self.protocol_widgets.items():
        if checkbox.isChecked():
            template_path = template_combo.currentData()
            protocols_to_generate.append((protocol_type, excel_path, template_path))

    if not protocols_to_generate:
        QMessageBox.warning(self, "Chyba", "Vyberte alespoň jeden protokol!")
        return

    # Progress dialog
    progress = QProgressDialog(
        f"Generuji {len(protocols_to_generate)} protokol(ů)...",
        None, 0, len(protocols_to_generate), self
    )

    # Generuj postupně
    for i, (protocol_type, excel_path, template_path) in enumerate(protocols_to_generate):
        progress.setValue(i)
        progress.setLabelText(f"Generuji {protocol_type}...")

        # Detekuj typ protokolu
        pipeline = WordProtocolPipeline(self.project_folder)

        output_path = self.project_folder / f"{protocol_type}_protokol.docx"

        success, message = pipeline.generate_protocol(
            excel_path,
            template_path,
            output_path
        )

        if not success:
            QMessageBox.critical(self, f"Chyba při {protocol_type}", message)
            return

    progress.setValue(len(protocols_to_generate))
    QMessageBox.information(
        self,
        "Úspěch",
        f"Úspěšně vygenerovány {len(protocols_to_generate)} protokoly!"
    )
    self.accept()
```

## Implementační kroky

1. **Refaktor `_browse_project_folder()`**
   - Přidat `_detect_available_protocols()`
   - Pro každý nalezený protokol vytvořit UI sekci

2. **Přidat `ProtocolSection` widget**
   - Samostatný widget pro každý typ protokolu
   - Obsahuje: checkbox, excel label, template dropdown, output label

3. **Upravit `_generate()`**
   - Iterovat přes zaškrtnuté protokoly
   - Pro každý spustit pipeline

4. **Template system**
   - Rozšířit mapping o PP a CFZ templates
   - Hledat templates podle protokolu

## Výhody tohoto řešení

- ✅ **Čisté**: Každý protokol má vlastní sekci
- ✅ **Flexibilní**: Snadné přidání nových typů
- ✅ **User-friendly**: Jasně viditelné, co se bude generovat
- ✅ **Zpětně kompatibilní**: LSZ funguje stejně jako předtím
- ✅ **Best practices**: Separation of concerns, DRY principle
