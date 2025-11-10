@echo off
REM ===================================
REM LABORATO5 - DEBUG Build EXE
REM ===================================
REM Tato verze ZOBRAZÍ console okno s chybovými hláškami!

echo.
echo [DEBUG BUILD] - Uvidíš všechny chyby v console okně
echo.
echo [1/4] Instaluji PyInstaller...
pip install pyinstaller

echo.
echo [2/4] Cistim stare buildy...
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist

echo.
echo [3/4] Sestavuji DEBUG EXE (s console oknem)...
pyinstaller --noconfirm ^
    --onedir ^
    --console ^
    --name "LABORATO5_DEBUG" ^
    --add-data "templates;templates" ^
    --add-data "config;config" ^
    --add-data "sample_protocols;sample_protocols" ^
    --collect-data docxcompose ^
    --collect-data docxtpl ^
    main.py

echo.
echo [4/4] Vytvářím projects složku v dist...
if not exist "dist\LABORATO5_DEBUG\projects" mkdir "dist\LABORATO5_DEBUG\projects"
echo   - Projects složka vytvořena

echo.
echo ========================================
echo DEBUG EXE vytvoren v: dist\LABORATO5_DEBUG\
echo Spustitelny soubor: dist\LABORATO5_DEBUG\LABORATO5_DEBUG.exe
echo ========================================
echo.
echo POZOR: Tato verze UKÁŽE console okno s chybovými hláškami!
echo        Použij ji pro debugging, ne pro kolegy.
echo.
pause
