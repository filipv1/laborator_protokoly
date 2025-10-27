@echo off
REM ===================================
REM LABORATO5 - Build EXE
REM ===================================

echo.
echo [1/4] Instaluji PyInstaller...
pip install pyinstaller

echo.
echo [2/4] Cistim stare buildy...
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist

echo.
echo [3/4] Sestavuji EXE...
echo POZOR: Vzorove protokoly NEBUDOU zabaleny do EXE (problem s diakritikou)
pyinstaller --noconfirm ^
    --onedir ^
    --windowed ^
    --name "LABORATO5" ^
    --add-data "templates;templates" ^
    --add-data "config;config" ^
    --collect-data docxcompose ^
    --collect-data docxtpl ^
    main.py

echo.
echo [4/4] Kopiruji Vzorove protokoly do dist...
if exist "Vzorové protokoly" (
    xcopy "Vzorové protokoly" "dist\LABORATO5\Vzorové protokoly\" /E /I /Y
    echo   - Vzorove protokoly zkopirovany
)
if exist "Vzor popis práce 2024" (
    xcopy "Vzor popis práce 2024" "dist\LABORATO5\Vzor popis práce 2024\" /E /I /Y
    echo   - Vzor popis prace zkopirovany
)

echo.
echo ========================================
echo EXE vytvoren v: dist\LABORATO5\
echo Spustitelny soubor: dist\LABORATO5\LABORATO5.exe
echo ========================================
echo.
echo POZOR: Pred predanim kolegum zkopiruj CELOU slozku dist\LABORATO5\
echo        (Ne jen .exe soubor!)
echo        Obsahuje:
echo        - LABORATO5.exe
echo        - _internal\ (knihovny)
echo        - templates\ (Excel sablony)
echo        - Vzorove protokoly\ (Word sablony)
echo.
pause
