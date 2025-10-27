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
echo POZOR: Vzorove protokoly NEBUDOU zabaleny do EXE (problem s diakritikou)
pyinstaller --noconfirm ^
    --onedir ^
    --console ^
    --name "LABORATO5_DEBUG" ^
    --add-data "templates;templates" ^
    --add-data "config;config" ^
    --collect-data docxcompose ^
    --collect-data docxtpl ^
    main.py

echo.
echo [4/4] Kopiruji Vzorove protokoly do dist...
if exist "Vzorové protokoly" (
    xcopy "Vzorové protokoly" "dist\LABORATO5_DEBUG\Vzorové protokoly\" /E /I /Y
    echo   - Vzorove protokoly zkopirovany
)
if exist "Vzor popis práce 2024" (
    xcopy "Vzor popis práce 2024" "dist\LABORATO5_DEBUG\Vzor popis práce 2024\" /E /I /Y
    echo   - Vzor popis prace zkopirovany
)

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
