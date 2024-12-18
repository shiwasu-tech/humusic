import sys
import json
from PySide6.QtWidgets import (
    QApplication,
    QFrame,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QLabel,
    QSlider,
    QComboBox
)
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QPixmap

from MidPlayer import play_mid
sys.path.append("src")
sys.path.append("src/hum2midi")
from hum2midi.Recorder import Recorder
from hum2midi.Wave2MidiConverter import Wave2MidiConverter
from continuous_generator.Generator import generate_midi

_TITLE = "Humor"
_SUBTITLE = "--HUMming cOntinuation generatoR--"

_WAVE_PATH = "resources/inputs/input.wav"
_PROMPT_MIDI_PATH = "resources/inputs/input.mid"
_MODEL_PATH = "resources/models/lstmwithatt_best.pt"
_TOKENIZER_PATH = "resources/tokenizers/piano1_tokens/tokenizer.json"
_GEN_MIDI_PATH = "resources/generated/generated_best.mid"

_LOGO_PATH = "src/application/logo_1.png"

_DEFAULT_REC_TIME = 5
_DEFAULT_GEN_NOTES = 500

_WINDOW_X = 100
_WINDOW_Y = 100
_WINDOW_WIDTH = 850
_WINDOW_HEIGHT = 500

class MainApp(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle(_TITLE)
        self.setGeometry(
            x = _WINDOW_X,
            y = _WINDOW_Y,
            w = _WINDOW_WIDTH,
            h = _WINDOW_HEIGHT
        )

        self.layout_main = QVBoxLayout()
        self.layout_top = QHBoxLayout()
        self.layout_bottom = QHBoxLayout()
        self.layout_bottom_left = QVBoxLayout()
        self.layout_bottom_center = QHBoxLayout()
        self.layout_bottom_right = QVBoxLayout()


    def __init_UI(self) -> None:
        self.__init_top()
        self.layout_main.addLayout(self.layout_top)

        self.__init_bottom()
        self.layout_main.addLayout(self.layout_bottom)


    def __init_top(self) -> None:
        IMG_LABEL = "logo"
        IMG_WIDTH = 50
        IMG_HEIGHT = 50
        TITLE_FONT_SIZE = 24
        STRETCH = 1
        LINE_WIDTH = 4

        pixmap = QPixmap(_LOGO_PATH).scaled(
            IMG_WIDTH,
            IMG_HEIGHT,
            Qt.KeepAspectRatio
        )
        img_label = QLabel(IMG_LABEL).setPixmap(pixmap)
        top_label = QLabel(_TITLE).setStyleSheet(
            f"font-size: {TITLE_FONT_SIZE}px;"
        )
        index_label = QLabel(_SUBTITLE)

        line = QFrame().setStyleSheet(
            f"border: {LINE_WIDTH}px solid black;"
            )
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Sunken)

        self.layout_top.addWidget(img_label)
        self.layout_top.addWidget(top_label)
        self.layout_top.addWidget(index_label)
        self.layout_top.addStretch(STRETCH)
        self.layout_top.addWidget(line)

        

        



    def __init_bottom(self) -> None:
        pass

