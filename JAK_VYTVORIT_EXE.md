# JAK VYTVOŘIT EXE SOUBOR PRO LABORATO5

## 🚀 Rychlý postup (3 kroky)

### 1. Nainstaluj závislosti
```bash
pip install -r requirements.txt
```

### 2. Spusť build script
```bash
build_exe.bat
```

### 3. Předej kolegům
Zkopíruj **CELOU** složku `dist\LABORATO5\` kolegům.
Spustitelný soubor: `dist\LABORATO5\LABORATO5.exe`

---

## ⚠️ DŮLEŽITÉ

### Před předáním kolegům:
1. **Zkopíruj CELOU složku** `dist\LABORATO5\`, ne jen .exe soubor!
2. V té složce je `.exe` + všechny potřebné knihovny
3. Kolega jen klikne na `LABORATO5.exe` a aplikace se spustí

### Testování před předáním:
1. Po buildu jdi do `dist\LABORATO5\`
2. Dvojklik na `LABORATO5.exe`
3. Otestuj, že aplikace funguje (vytvoř testovací projekt)

---

## 📦 Co je zabaleno v EXE?

- ✅ Celý Python runtime
- ✅ Všechny knihovny (PyQt6, openpyxl, python-docx, docxtpl, xlwings)
- ✅ Excel templaty (`templates/excel/`)
- ✅ Konfigurace (`config/`)
- ✅ Celý kód aplikace

Kolega **NEPOTŘEBUJE** nainstalovaný Python!

---

## 🐛 Řešení problémů

### Build selže na PyInstaller
```bash
pip install --upgrade pyinstaller
```

### EXE nefunguje na cizím PC
- Ujisti se, že jsi předal **celou složku** `dist\LABORATO5\`, ne jen .exe
- Na cizím PC může chybět **Excel** (xlwings vyžaduje instalovaný Excel)

### xlwings nefunguje
- xlwings vyžaduje **nainstalovaný Microsoft Excel**
- Pokud ho kolega nemá, funkce exportu grafů nebude fungovat
- (Grafy jsou nyní zakomentované, takže by to mělo být OK)

---

## 📝 Poznámky

- Build vytvoří **~500 MB** složku (PyQt6 je velké)
- První spuštění může trvat ~10 sekund (rozbalení knihoven)
- EXE funguje pouze na **Windows** (PyQt6 + xlwings jsou Windows-only v tomto setupu)

---

## 🔧 Pokročilé: Ruční build

Pokud nechceš použít `build_exe.bat`, můžeš použít příkaz přímo:

```bash
pyinstaller --onedir --windowed --name "LABORATO5" --add-data "templates;templates" --add-data "config;config" main.py
```

**Parametry vysvětlené:**
- `--onedir` = vytvoří složku s .exe + knihovnami (jednodušší než --onefile)
- `--windowed` = žádný console terminál (pouze GUI)
- `--name "LABORATO5"` = název .exe souboru
- `--add-data "templates;templates"` = zahrnout Excel šablony
- `--add-data "config;config"` = zahrnout konfigurační soubory

---

## ✅ Checklist před předáním

- [ ] Build úspěšně dokončen
- [ ] Otestoval jsem `LABORATO5.exe` na svém PC
- [ ] Vytvořil jsem testovací projekt a zkontroloval Excel výstup
- [ ] Připravil jsem ZIP se složkou `LABORATO5\`
- [ ] Informoval jsem kolegy, že potřebují **Microsoft Excel** nainstalovaný
