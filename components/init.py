""" Import necessary modules for the program to work """
import sys
import os
import ctypes
import subprocess
import threading
import logging
from PyQt5.QtWidgets import QApplication
from defender_check import DefenderCheck
from install_screen import InstallScreen
import debloat_windows
import windows_check
import apply_background
import time
from PyQt5.QtCore import QTimer
import platform
import winreg
import tempfile
import shutil

""" Establish the version of TalonLite """
TALONLITE_VERSION = "0.2.2 (1.1.4 Talon Base)"

""" Set up the log file """
LOG_FILE = "TalonLite.txt"
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

""" Utility function to obtain information about Windows """
def get_windows_info():
    try:
        windows_version = platform.win32_ver()
        reg = winreg.ConnectRegistry(None, winreg.HKEY_LOCAL_MACHINE)
        key = winreg.OpenKey(reg, r"SOFTWARE\Microsoft\Windows NT\CurrentVersion")
        
        build_number = winreg.QueryValueEx(key, "CurrentBuildNumber")[0]
        product_name = winreg.QueryValueEx(key, "ProductName")[0]
        display_version = winreg.QueryValueEx(key, "DisplayVersion")[0]
        
        return {
            'version': windows_version[0],
            'build': build_number,
            'product_name': product_name,
            'display_version': display_version
        }
    except Exception as e:
        logging.error(f"Error getting Windows information: {e}")
        return None

""" Utility function to check if the program is being ran as administrator """
def is_running_as_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin() != 0
    except Exception as e:
        logging.error(f"Error checking admin privileges: {e}")
        return False

""" If the program is not being ran as administrator, elevate """
def restart_as_admin():
    try:
        script = sys.argv[0]
        params = ' '.join(sys.argv[1:])
        logging.info("Restarting with admin privileges...")
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, f'"{script}" {params}', None, 1)
        sys.exit()
    except Exception as e:
        logging.error(f"Error restarting as admin: {e}")

""" Cleanup old Nuitka folders """
def clean_nuitka_temp_folders():
    temp_directory = tempfile.gettempdir()
    for item in os.listdir(temp_directory):  # Corrected indentation
        item_path = os.path.join(temp_directory, item)
        if os.path.isdir(item_path) and item.lower().startswith('onefile_'):
            print(f"Removing nuitka folder: {item_path}")
            shutil.rmtree(item_path)

""" Main function to begin TalonLite installation """
def main():
    logging.info("Starting TalonLite Installer")
    logging.info(f"TalonLite Version: {TALONLITE_VERSION}")
    windows_info = get_windows_info()
    if windows_info:
        logging.info(f"Windows Version: {windows_info['product_name']}")
        logging.info(f"Build Number: {windows_info['build']}")
        logging.info(f"Display Version: {windows_info['display_version']}")
    app = QApplication(sys.argv)
    if not is_running_as_admin():
        logging.warning("Program is not running as admin. Restarting with admin rights...")
        restart_as_admin()
    try:
        loggin.info("Cleaning up previous temp files...")
        clean_nuitka_temp_folders()
    except Exception as e:
        logging.error(f"Error during clean up: {e}")
    try:
        logging.info("Starting Defender check...")
        defender_check_window = DefenderCheck()
        defender_check_window.defender_disabled_signal.connect(defender_check_window.close)
        defender_check_window.show()
        while defender_check_window.isVisible():
            app.processEvents()
        logging.info("Defender is disabled, proceeding with the rest of the program.")
    except Exception as e:
        logging.error(f"Error during Defender check: {e}")
    try:
        logging.info("Running Windows 11 and fresh install check...")
        windows_check.check_system()
        logging.info("System check passed.")
    except Exception as e:
        logging.error(f"System check failed: {e}")
    try:
        logging.info("Displaying installation screen...")
        install_screen = InstallScreen()
        install_screen.show()
    except Exception as e:
        logging.error(f"Error during installation screen setup: {e}")

    """ Run the installation process """
    def perform_installation():
        try:
            logging.info("Applying background settings...")
            apply_background.main()
            logging.info("Background settings applied successfully.")
        except Exception as e:
            logging.error(f"Error applying background settings: {e}")
        
        try:
            logging.info("Removing Microsoft Edge...")
            debloat_windows.run_edge_vanisher()
            logging.info("Microsoft Edge removal complete.")
        except Exception as e:
            logging.error(f"Error removing Microsoft Edge: {e}")
        
        logging.info("All installations and configurations completed.")
        install_screen.close()
        logging.info("Installation complete. Restarting system...")
        debloat_windows.finalize_installation()

    try:
        logging.info("Starting installation process in a separate thread...")
        install_thread = threading.Thread(target=perform_installation)
        install_thread.start()
        while install_thread.is_alive():
            app.processEvents()
            time.sleep(0.05)            
    except Exception as e:
        logging.error(f"Error starting installation thread: {e}")
    
    app.exec_()

""" Start the program """
if __name__ == "__main__":
    main()
    print("Executable path:", sys.executable)
