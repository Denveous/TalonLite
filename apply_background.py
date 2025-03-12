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
    if getattr(sys, 'frozen', False):
        script_dir = sys._MEIPASS
    else:
        script_dir = os.path.dirname(os.path.abspath(__file__))
    image_path = os.path.join(script_dir, "DesktopBackground.png")
    set_wallpaper(image_path)

if __name__ == "__main__":
    main()
