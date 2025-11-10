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
pyinstaller --noconfirm ^
    --onedir ^
    --windowed ^
    --name "LABORATO5" ^
    --add-data "templates;templates" ^
    --add-data "config;config" ^
    --add-data "sample_protocols;sample_protocols" ^
    --collect-data docxcompose ^
    --collect-data docxtpl ^
    main.py

echo.
echo [4/4] Vytvářím projects složku v dist...
if not exist "dist\LABORATO5\projects" mkdir "dist\LABORATO5\projects"
echo   - Projects složka vytvořena

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
echo        - _internal\ (knihovny, Excel + Word sablony)
echo        - projects\ (prazdna slozka pro projekty)
echo.
pause
