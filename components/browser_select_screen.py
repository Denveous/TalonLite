from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QGraphicsDropShadowEffect, QSpacerItem, QSizePolicy
)
from PyQt5.QtGui import QColor, QFont, QFontDatabase, QPixmap
from PyQt5.QtCore import Qt, QPropertyAnimation, QEasingCurve
import os
import sys
import logging

""" Set up the log file """
LOG_FILE = "talon.txt"
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

""" Utility function to log outputs """
def log(message):
    logging.info(message)
    print(message)

class AnimatedButton(QPushButton):
    def __init__(self, text, color, hover_color=None, is_firefox=False):
        super().__init__(text)
        self.default_color = color
        self.hover_color = hover_color if hover_color else color
        self.is_firefox = is_firefox
        self.default_text_color = QColor(0, 0, 0)
        self.hover_text_color = QColor(255, 255, 255) if is_firefox else self.default_text_color
        text_color = QColor(255, 255, 255) if self.is_firefox else self.default_text_color
        self.setStyleSheet(f"background-color: {self.default_color.name()}; color: {text_color.name()}; border: none;")
        self.setFont(QFont("Chakra Petch", 14, QFont.Bold))
        self.setFixedSize(240, 40)
        self.shadow_effect = QGraphicsDropShadowEffect()
        self.shadow_effect.setBlurRadius(80)
        self.shadow_effect.setColor(self.default_color.darker(200))
        self.shadow_effect.setOffset(0, 0)
        self.setGraphicsEffect(self.shadow_effect)
        self.animation = QPropertyAnimation(self.shadow_effect, b"blurRadius")
        self.animation.setDuration(800)
        self.animation.setEasingCurve(QEasingCurve.InOutQuad)

    def enterEvent(self, event):
        self.animation.stop()
        self.animation.setStartValue(self.shadow_effect.blurRadius())
        self.animation.setEndValue(200)
        self.animation.start()
        text_color = self.hover_text_color.name() if self.is_firefox else self.default_text_color.name()
        self.setStyleSheet(f"background-color: {self.hover_color.name()}; color: {text_color}; border: none;")
        super().enterEvent(event)

    def leaveEvent(self, event):
        self.animation.stop()
        self.animation.setStartValue(self.shadow_effect.blurRadius())
        self.animation.setEndValue(80)
        self.animation.start()
        text_color = QColor(255, 255, 255) if self.is_firefox else self.default_text_color
        self.setStyleSheet(f"background-color: {self.default_color.name()}; color: {text_color.name()}; border: none;")
        super().leaveEvent(event)

class BrowserSelectScreen(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Browser Selector")
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.showFullScreen()
        self.setStyleSheet("background-color: black;")
        self.load_chakra_petch_font()
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)
        layout.setContentsMargins(0, 0, 0, 0)

        title_layout = QVBoxLayout()
        title_label = QLabel("Welcome. Please select a web browser")
        title_label.setStyleSheet("color: white; font-weight: bold;")
        title_label.setFont(QFont("Chakra Petch", 24, QFont.Bold))
        title_label.setAlignment(Qt.AlignCenter)
        title_layout.addWidget(title_label)
        title_layout.setStretch(0, 1)
        layout.addLayout(title_layout)

        image_label = QLabel(self)
        base_path = os.path.dirname(os.path.abspath(__file__))
        image_path = os.path.join(base_path, "media\\browser_selection.png" if "__compiled__" in globals() else "..\\media\\browser_selection.png")

        log(f"Image path browser: {image_path}")
        pixmap = QPixmap(image_path)
        scaled_pixmap = pixmap.scaledToWidth(int(1920 * 0.6), Qt.SmoothTransformation)
        image_label.setPixmap(scaled_pixmap)
        image_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(image_label)

        browsers = {
            "Chrome": QColor(255, 255, 255),
            "Brave": QColor(255, 255, 255), 
            "Firefox": QColor(34, 139, 34),
            "Librewolf": QColor(255, 255, 255),
        }
        self.selected_browser = None
        button_layout = QHBoxLayout()
        button_layout.setSpacing(20)
        button_layout.setAlignment(Qt.AlignCenter)
        button_columns = []

        for browser, color in browsers.items():
            column_layout = QVBoxLayout()
            column_layout.setAlignment(Qt.AlignTop)
            button = AnimatedButton(browser, color, is_firefox=(browser == "Firefox"))
            button.setFixedWidth(350)
            button.clicked.connect(lambda _, b=browser: self.select_browser(b))
            column_layout.addWidget(button)

            if browser == "Firefox":
                label = QLabel("Recommended Browser")
                label.setStyleSheet("color: rgb(34, 139, 34); font-weight: bold; background: transparent;")
                label.setAlignment(Qt.AlignCenter)
                label.setFixedWidth(button.width())
                label.setFont(QFont("Chakra Petch", 15, QFont.Bold))
                column_layout.addWidget(label)
                spacer = QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Expanding)
                column_layout.addItem(spacer)

            button_columns.append(column_layout)

        for column in button_columns:
            button_layout.addLayout(column)

        layout.addLayout(button_layout)

        skip_warning_layout = QVBoxLayout()
        skip_warning_layout.setAlignment(Qt.AlignCenter)
        skip_warning_layout.setContentsMargins(0, 22, 0, 0)  

        skip_button = QPushButton("Skip Browser Installation")
        skip_button.setStyleSheet("background-color: gray; color: white; border: none; font-size: 16px;")
        skip_button.setFixedSize(240, 40)
        skip_button.clicked.connect(self.skip_browser_selection)
        skip_warning_layout.addWidget(skip_button, alignment=Qt.AlignCenter)

        warning_label = QLabel("Note: Microsoft Edge will be removed in the process.")
        warning_label.setStyleSheet("color: red; font-weight: bold;")
        warning_label.setAlignment(Qt.AlignCenter)
        skip_warning_layout.addWidget(warning_label, alignment=Qt.AlignCenter)

        layout.addLayout(skip_warning_layout)

        self.setLayout(layout)

    def load_chakra_petch_font(self):
        try:
            base_path = os.path.dirname(os.path.abspath(__file__))
            font_path = os.path.join(base_path, "media\\ChakraPetch-Regular.ttf" if "__compiled__" in globals() else "..\\media\\ChakraPetch-Regular.ttf")
            log(f"Font check: {font_path}")

            font_id = QFontDatabase.addApplicationFont(font_path)
            if font_id == -1:
                print("Failed to load font.")
            else:
                print("Font loaded successfully.")
        except Exception as e:
            print(f"Error loading font: {e}")

    def select_browser(self, browser_name):
        self.selected_browser = browser_name
        print(f"Selected browser: {self.selected_browser}")
        self.close()
        return self.selected_browser

    def skip_browser_selection(self):
        print("Browser installation skipped.")
        self.selected_browser = "skip"
        self.close()

