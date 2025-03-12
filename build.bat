@echo off

REM Check for required packages and install if not present
pip show tqdm >nul 2>&1 || pip install tqdm
pip show wmi >nul 2>&1 || pip install wmi
pip show pyqt5 >nul 2>&1 || pip install pyqt5
pip show requests >nul 2>&1 || pip install requests

REM Compile the Python script with Nuitka
nuitka --onefile --standalone --enable-plugin=pyqt5 --remove-output --windows-icon-from-ico=ICON.ico --windows-console-mode=disable --windows-uac-admin --output-dir=dist --output-filename=talon.exe --follow-imports ^
--include-data-files="ChakraPetch-Regular.ttf=ChakraPetch-Regular.ttf" ^
--include-data-files="browser_selection.png=browser_selection.png" ^
--include-data-files="additional_software_offer.png=additional_software_offer.png" ^
--include-data-files="barebones.json=barebones.json" ^
--include-data-files="DesktopBackground.png=DesktopBackground.png" ^
--include-data-files="packages.json=packages.json" ^
--include-data-files="scratchpad.zip=scratchpad.zip" ^
--include-data-files="redact.zip=redact.zip" ^
--include-data-files="filediff.zip=filediff.zip" ^
--include-data-files="resmon.zip=resmon.zip" ^
--include-data-files="Win11Debloat-master.zip=Win11Debloat-master.zip" ^
--msvc=latest init.py

pause
