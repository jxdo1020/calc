@echo off
setlocal
py -m pip install -r requirements-dev.txt || exit /b 1
py -m pytest || exit /b 1
py -m PyInstaller --noconfirm --clean --onefile --windowed --name OpenClassPad --collect-all sympy run.py || exit /b 1
echo Portable executable: dist\OpenClassPad.exe
