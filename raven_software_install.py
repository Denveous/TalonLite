""" Import the necessary modules for the program to work """
import os
import sys
import logging
import platform
import subprocess
import zipfile
from pathlib import Path
import shutil

""" Set up logging """
def log(message):
    logging.info(message)

""" Add exclusions for Raven software to Windows Defender """
def add_defender_exclusion(path):
    try:
        subprocess.run(
            ['powershell', '-Command', 
             f'Add-MpPreference -ExclusionPath "{path}"'],
            check=True,
            capture_output=True
        )
        log(f"Added Windows Defender exclusion for: {path}")
        return True
    except Exception as e:
        log(f"Failed to add Windows Defender exclusion: {e}")
        return False

""" Utility function to get the installation path for Raven software """
def get_installation_path():
    install_path = Path(os.getenv('APPDATA')) / "ravendevteam"
    install_path.mkdir(parents=True, exist_ok=True)
    add_defender_exclusion(str(install_path))
    return install_path

""" Utility function to copy a file """
def download_file(path, destination):
    try:
        shutil.copy(path, destination)
        log(f"Copied {path} to {destination}")
        return True
    except Exception as e:
        log(f"Copy error: {e}")
        return False

""" Extract ZIP file to the target directory """
def extract_zip(zip_path, extract_to):
    try:
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(extract_to)
        log(f"Extracted {zip_path} to {extract_to}")
        return True
    except Exception as e:
        log(f"Failed to extract {zip_path}: {e}")
        return False

""" Utility function to create a shortcut to the first EXE file found """
def create_shortcut(target_dir, shortcut_name):
    try:
        desktop = os.path.join(os.path.expanduser("~"), "Desktop")
        shortcut_path = os.path.join(desktop, f"{shortcut_name}.lnk")

        exe_files = list(target_dir.glob("*.exe"))
        if not exe_files:
            log(f"No EXE file found in {target_dir}, skipping shortcut creation")
            return False

        exe_file = exe_files[0]
        os.system(f'cmd /c mklink "{shortcut_path}" "{exe_file}"')
        log(f"Created shortcut for {shortcut_name}")
        return True
    except Exception as e:
        log(f"Failed to create shortcut: {e}")
        return False

""" Install the specified package """
def install_package(zip_name, install_dir):
    platform_name = platform.system()
    if platform_name != "Windows":
        log(f"Package {zip_name} is not available for {platform_name}")
        return False
    
    package_dir = install_dir / zip_name.replace('.zip', '')
    package_dir.mkdir(parents=True, exist_ok=True)

    if hasattr(sys, '_MEIPASS'):
        temp_dir = Path(sys._MEIPASS)
    else:
        log("Not running in a bundled environment.")
        return False

    zip_path = temp_dir / zip_name

    log(f"Installing {zip_name} from {zip_path}...")

    if not zip_path.exists():
        log(f"Zip file {zip_path} not found.")
        return False

    if not download_file(zip_path, install_dir / zip_name):
        return False

    if not extract_zip(install_dir / zip_name, package_dir):
        return False

    create_shortcut(package_dir, zip_name.replace('.zip', ''))

    log(f"Successfully installed {zip_name}")
    return True

""" Begin the process of installing hardcoded packages """
def run_toolbox():
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    log("Fetching package list...")

    # Hardcoded list of zip file names, because fuck using a json.
    zip_files = [
        "scratchpad.zip",
        "redact.zip",
        "filediff.zip",
        "resmon.zip"
    ]

    install_dir = get_installation_path()
    install_dir.mkdir(parents=True, exist_ok=True)

    success = True
    for zip_name in zip_files:
        if not install_package(zip_name, install_dir):
            success = False
            log(f"Failed to install {zip_name}")
        else:
            log(f"Successfully installed {zip_name}")

    log("Installation process completed" + (" successfully" if success else " with some failures"))
    return success

def main():
    try:
        success = run_toolbox()
        return success
   
    except KeyboardInterrupt:
        log("\nInstallation cancelled by user")
        return False
    except Exception as e:
        log(f"Unexpected error: {e}")
        return False

""" Run the program """
if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

