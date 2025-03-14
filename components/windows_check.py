""" Import necessary modules for the program to work """
import sys
import platform
import os
import time
from PyQt5.QtWidgets import QApplication, QMessageBox
from PyQt5.QtCore import Qt, QTimer



""" Utility function to check if the system is Windows 11 """
def is_windows_11():
    version = platform.version()
    return version.startswith("10.0") and int(platform.release()) >= 10



""" Utility function to display a UI pop-up """
def show_popup(title, message, is_error=False, delay_ok=False, exit_on_error=False):
    app = QApplication.instance() or QApplication(sys.argv)
    msg_box = QMessageBox()
    msg_box.setWindowTitle(title)
    msg_box.setTextFormat(Qt.RichText)
    msg_box.setText(f"<span style='font-size:12pt;'>{message}</span>")
    msg_box.setIcon(QMessageBox.Critical if is_error else QMessageBox.Warning)
    ok_button = msg_box.addButton(QMessageBox.Ok)
    if delay_ok:
        ok_button.setEnabled(False)
        QTimer.singleShot(3000, lambda: ok_button.setEnabled(True))
    msg_box.exec_()
    if exit_on_error:
        os._exit(1)




""" Check if the system is Windows 11 """
def check_system():
    if not is_windows_11():
        show_popup(
            "Talon Installation Failure",
            "You are currently on Windows 10 or older. <b>Talon is designed to only work on freshly installed Windows 11 systems</b>. Please update to a fresh installation of Windows 11 before attempting to use Talon again.",
            is_error=True,
            exit_on_error=True
        )
    show_popup(
        "Talon Installation Warning",
        """
        Talon is designed to be used on <b>freshly installed Windows 11 systems</b>. Running this program on an already in-use system could result in data loss, apps stopping working, or even corruption.<br><br>
        
        <b>For the best results, please ensure you are on a fresh installation of the latest version of Windows 11 Home or Professional.</b>
        """,
        is_error=False,
        delay_ok=True
    )




""" Start the program if running as a standalone script """
if __name__ == "__main__":
    check_system()
