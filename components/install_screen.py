""" Import necessary modules for the program to work """
import sys
import os
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QFrame, QHBoxLayout
)
from PyQt5.QtGui import QFont, QFontDatabase, QPainter, QColor, QPen
from PyQt5.QtCore import Qt, QTimer



""" Create a class for the installation UI """
class InstallScreen(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("TalonX Installer")
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.showFullScreen()
        self.setStyleSheet("background-color: black;")
        self.setAttribute(Qt.WA_ShowWithoutActivating)
        self.setWindowState(Qt.WindowFullScreen | Qt.WindowActive)
        self.load_chakra_petch_font()
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)
        layout.setContentsMargins(0, 0, 0, 0)
        title_label = QLabel("Installing TalonX...")
        title_label.setStyleSheet("color: white; font-weight: bold;")
        title_label.setFont(QFont("Chakra Petch", 24, QFont.Bold))
        title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(title_label)
        body_label = QLabel("This may take a few minutes. Do not turn your PC off.")
        body_label.setStyleSheet("color: white;")
        body_label.setFont(QFont("Chakra Petch", 18))
        body_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(body_label)
        layout.addSpacing(30)
        spinner_layout = QHBoxLayout()
        spinner_layout.setAlignment(Qt.AlignCenter)
        self.spinner = LoadingSpinner()
        spinner_layout.addWidget(self.spinner)
        self.spinner.start_spinning()
        layout.addLayout(spinner_layout)
        self.setLayout(layout)

    """ Load the Chakra Petch font, which is used for the UI """
    def load_chakra_petch_font(self):
        try:
            base_path = os.path.dirname(os.path.abspath(__file__))
            font_path = os.path.join(base_path, "media\\ChakraPetch-Regular.ttf" if "__compiled__" in globals() else "..\\media\\ChakraPetch-Regular.ttf")
            font_id = QFontDatabase.addApplicationFont(font_path)
            if font_id == -1:
                print("Failed to load font.")
            else:
                print("Font loaded successfully.")
        except Exception as e:
            print(f"Error loading font: {e}")



""" Create a class for the loading spinner in the UI """
class LoadingSpinner(QFrame):

    """ Initialization """
    def __init__(self):
        super().__init__()
        self.setFixedSize(100, 100)
        self.setStyleSheet("background-color: transparent;")
        self.angle = 0
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update)
        self.timer.start(30)

    """ Use QPainter to draw the spinner """
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        pen = QPen(QColor(255, 255, 255))
        pen.setWidth(6)
        painter.setPen(pen)
        painter.setBrush(Qt.transparent)
        rect = self.rect()
        painter.drawArc(rect.adjusted(10, 10, -10, -10), self.angle * 16, 100 * 16)

    """ Begin spinning """
    def start_spinning(self):
        self.angle = 0
        self.update()

    """ Update the spinner to spin """
    def update(self):
        self.angle -= 5
        if self.angle <= -360:
            self.angle = 0
        super().update()