@echo off

REM Check for required packages and install if not present
pip show tqdm >nul 2>&1 || pip install tqdm
pip show wmi >nul 2>&1 || pip install wmi
pip show pyqt5 >nul 2>&1 || pip install pyqt5
pip show requests >nul 2>&1 || pip install requests

REM Compile the Python script with Nuitka
nuitka --onefile --standalone --enable-plugin=pyqt5 --remove-output --windows-icon-from-ico=media\ICON.ico --windows-console-mode=disable --windows-uac-admin --output-dir=dist --output-filename=talon.exe ^
--include-data-files="media\ChakraPetch-Regular.ttf=ChakraPetch-Regular.ttf" ^
--include-data-files="media\browser_selection.png=browser_selection.png" ^
--include-data-files="media\additional_software_offer.png=additional_software_offer.png" ^
--include-data-files="components\barebones.json=barebones.json" ^
--include-data-files="media\DesktopBackground.png=DesktopBackground.png" ^
--include-data-files="media\scratchpad.zip=scratchpad.zip" ^
--include-data-files="media\redact.zip=redact.zip" ^
--include-data-files="media\filediff.zip=filediff.zip" ^
--include-data-files="media\resmon.zip=resmon.zip" ^
--include-data-files="components\run_debloat.ps1=run_debloat.ps1" ^
--include-data-files="components\update_policy_changer.ps1=update_policy_changer.ps1" ^
--include-data-files="components\uninstall_oo.ps1=uninstall_oo.ps1" ^
--include-data-files="components\edge_vanisher.ps1=edge_vanisher.ps1" ^
--include-data-dir="components\Win11Debloat=Win11Debloat" ^
--include-data-dir="components\Win11Debloat\Assets=Win11Debloat\Assets" ^
--include-data-dir="components\Win11Debloat\Regfiles=Win11Debloat\Regfiles" ^
--include-data-dir="components\Win11Debloat\Start=Win11Debloat\Start" ^
--msvc=latest init.py

pause
