@echo off
REM Check for required packages and install if not present
pip show tqdm >nul 2>&1 || pip install tqdm
pip show wmi >nul 2>&1 || pip install wmi
pip show pyqt5 >nul 2>&1 || pip install pyqt5
pip show requests >nul 2>&1 || pip install requests
pip show nuitka >nul 2>&1 || pip install nuitka
pip show pywin32 >nul 2>&1 || pip install pywin32
pip show setuptools >nul 2>&1 || pip install setuptools
pip show wheel >nul 2>&1 || pip install wheel
REM Compile the Python script with Nuitka
nuitka --onefile --standalone --enable-plugin=pyqt5 --remove-output --windows-icon-from-ico=media\ICON.ico --windows-console-mode=disable --windows-uac-admin --output-dir=dist --output-filename=TalonX.exe --include-data-dir="components=components" --include-data-dir="media=media" --include-data-dir="components\Win11Debloat=Win11Debloat" --msvc=latest components\init.py
pause
