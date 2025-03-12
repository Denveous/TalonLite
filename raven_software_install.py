""" Import the necessary modules for the program to work """
import os
import sys
import json
import logging
import platform
import subprocess
import zipfile
from pathlib import Path
from tqdm import tqdm

""" Set up logging """
def log(message):
    logging.info(message)

""" Utility function to fetch the packages.json file """
def get_packages_json():
    try:
        with open('packages.json', 'r') as f:
            return json.load(f)
    except Exception as e:
        log(f"Error loading packages.json: {e}")
        return None

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
def download_file(path, destination, desc="Copying"):
    try:
        import shutil
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
def install_package(package, install_dir):
    platform_name = platform.system()
    if platform_name != "Windows":
        log(f"Package {package['name']} is not available for {platform_name}")
        return False
    
    package_dir = install_dir / package["name"]
    package_dir.mkdir(parents=True, exist_ok=True)
    
    path = package["path"]
    file_name = path.split("/")[-1]
    download_path = package_dir / file_name

    log(f"Installing {package['name']} v{package['version']}...")

    if not download_file(path, download_path, f"Copying {package['name']}"):
        return False

    if not extract_zip(download_path, package_dir):
        return False

    if package["shortcut"]:
        create_shortcut(package_dir, package["name"])

    log(f"Successfully installed {package['name']}")
    return True

""" Begin the process of fetching the package list then installing them """
def run_toolbox():
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    log("Fetching package list...")
    packages_data = get_packages_json()
    if not packages_data:
        log("Failed to fetch packages data")
        return False

    install_dir = get_installation_path()
    install_dir.mkdir(parents=True, exist_ok=True)

    success = True
    for package in packages_data["packages"]:
        if not install_package(package, install_dir):
            success = False
            log(f"Failed to install {package['name']}")
        else:
            log(f"Successfully installed {package['name']}")

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
