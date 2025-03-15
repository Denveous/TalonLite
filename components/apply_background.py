import os
import sys
import ctypes
import shutil
from pathlib import Path

""" Utility function to set the wallpaper path for Windows """
def set_wallpaper(image_path):
    try:
        result = ctypes.windll.user32.SystemParametersInfoW(20, 0, image_path, 3)
        if result:
            print("Wallpaper set.")
        else:
            print("Couldn't set wallpaper.")
    except Exception as e:
        print(f"Error setting background: {e}")

""" Utility function to get the installation path for Raven software """
def get_installation_path():
    install_path = Path(os.getenv('APPDATA')) / "ravendevteam"
    install_path.mkdir(parents=True, exist_ok=True)
    return install_path

""" Main function to apply wallpaper """
def main():
    install_path = get_installation_path()
    base_path = os.path.dirname(os.path.abspath(__file__))
    image_path = os.path.join(base_path, r"media\DesktopBackground.png" if "__compiled__" in globals() else r"..\media\DesktopBackground.png")
    shutil.copy(image_path, f"{install_path}\\DesktopBackground.png") # Copy background to HD location for consistency. 
    set_wallpaper(f"{install_path}\\DesktopBackground.png")

if __name__ == "__main__":
    main()
