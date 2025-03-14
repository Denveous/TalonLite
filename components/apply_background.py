import os
import sys
import ctypes

def set_wallpaper(image_path):
    try:
        result = ctypes.windll.user32.SystemParametersInfoW(20, 0, image_path, 3)
        if result:
            print("Task completed.")
        else:
            print("Task failed.")
    except Exception as e:
        print(f"Error setting background: {e}")

def main():
    if hasattr(sys, "_MEIPASS"):
        image_path = os.path.join(sys._MEIPASS, "media/DesktopBackground.png")
    else:
        image_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "media/DesktopBackground.png"))
    set_wallpaper(image_path)

if __name__ == "__main__":
    main()
