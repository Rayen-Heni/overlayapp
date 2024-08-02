from PyQt5.QtWidgets import QApplication, QLabel, QWidget, QPushButton, QSlider, QVBoxLayout
from PyQt5.QtCore import Qt, QPoint
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from comtypes import CLSCTX_ALL
import sys

class MovableOverlay(QWidget):
    def __init__(self):
        super().__init__()
        self.setup_overlay()
        self.init_audio_control()
        self.is_translucent = False  # Track the current state

    def setup_overlay(self):
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)
        self.setGeometry(100, 100, 400, 100)  # Set initial size and position
        self.setAutoFillBackground(True)
        self.setStyleSheet("background-color: rgba(0, 0, 0, 100);")

        # Example content: a label in the overlay
        label = QLabel('Volume Slider!', self)
        label.setStyleSheet("color: white;")
        label.adjustSize()
        label.move(160, 10)
        label.setAttribute(Qt.WA_TranslucentBackground)

        # Store the mouse press position
        self.drag_position = None

        button = QPushButton("☻", self)
        button.setStyleSheet("color : rgb(76,0,155);")
        button.setGeometry(10, 10, 30, 30)
        button.clicked.connect(self.toggle_transparency)
        button.setAttribute(Qt.WA_TranslucentBackground) 

        # Slider for volume control
        self.slider = QSlider(Qt.Horizontal, self)
        self.slider.setGeometry(50, 60, 300, 30)
        self.slider.setRange(0, 100)
        self.slider.valueChanged.connect(self.set_volume)
        self.slider.setAttribute(Qt.WA_TranslucentBackground)

    def init_audio_control(self):
        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        self.volume_control = interface.QueryInterface(IAudioEndpointVolume)
        current_volume = self.volume_control.GetMasterVolumeLevelScalar()
        self.slider.setValue(int(current_volume * 100))

    def set_volume(self, value):
        self.volume_control.SetMasterVolumeLevelScalar(value / 100, None)

    def toggle_transparency(self):
        if self.is_translucent:
            self.setAttribute(Qt.WA_TranslucentBackground, False)
            self.setStyleSheet("background-color: rgba(255, 255, 255, 255);")  # Opaque background
        else:
            self.setAttribute(Qt.WA_TranslucentBackground, True)
            self.setStyleSheet("background-color: rgba(255, 255, 255, 0);")  # Translucent background
        self.is_translucent = not self.is_translucent
        self.show()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drag_position = event.globalPos() - self.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event):
        if self.drag_position:
            self.move(event.globalPos() - self.drag_position)
            event.accept()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drag_position = None

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MovableOverlay()
    window.show()
    sys.exit(app.exec_())