from PyQt5.QtWidgets import QApplication, QLabel, QWidget
from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent, QMediaMetaData

import sys

class MovableOverlay(QWidget):
    def __init__(self):
        super().__init__()
        self.setup_overlay()

    def setup_overlay(self):
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint )
        self.setGeometry(100, 100, 400, 100)  # Set initial size and position
        self.setAutoFillBackground(True)
        self.setStyleSheet("background-color: rgba(255, 255, 255, 0);")

        # Example content: a label in the overlay
        label = QLabel('Drag me around!', self)
        label.setStyleSheet("color: white;")
        label.adjustSize()
        label.move(160, 50)

        # Store the mouse press position
        self.drag_position = None

        button = QPushButton("☻", self)
        button.setStyleSheet("color : rgb(76,0,155);")
        # setting geometry of button
        button.setGeometry(10, 10, 30, 30)
        button.clicked.connect(self.make_invisible)


 
    def make_invisible(self):
        # Set window opacity to 0 and make it click-through
        self.setAttribute(Qt.WA_TranslucentBackground);
        self.show()


    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            # Store the position where the mouse was pressed
            self.drag_position = event.globalPos() - self.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event):
        if self.drag_position:
            # Move the window to the new position
            self.move(event.globalPos() - self.drag_position)
            event.accept()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            # Reset drag position when the mouse is released
            self.drag_position = None

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MovableOverlay()
    window.show()
    sys.exit(app.exec_())