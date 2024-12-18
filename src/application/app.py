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

_DEFALUT_REC_RANGE = (1, 20)
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
        self.layout_body = QHBoxLayout()
        self.layout_bottom = QHBoxLayout()

        self.layout_recorder = QVBoxLayout()
        self.layout_converter = QVBoxLayout()
        self.layout_generator = QVBoxLayout()
        self.layout_player = QVBoxLayout()



    def __init_UI(self) -> None:
        self.__init_top()
        self.__init_body()
        self.__init_bottom()

        self.layout_main.addLayout(self.layout_top)
        self.layout_main.addLayout(self.layout_body)
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

    
    def __init_body(self) -> None:
        self.__init_recorder()
        self.layout_body.addLayout(self.layout_recorder)

        self.__init_converter()
        self.layout_body.addLayout(self.layout_converter)

        self.__init_generator()
        self.layout_body.addLayout(self.layout_generator)

        self.__init_player()
        self.layout_body.addLayout(self.layout_player)


    def __init_recorder(self) -> None:
        REC_LABEL = "録音"
        REC_FONT_SIZE = 20
        REC_SEC_SLIDER_LABEL = f"録音時間: {_DEFAULT_REC_TIME}秒"

        rec_label = QLabel(REC_LABEL).setStyleSheet(
            f"font-size: {REC_FONT_SIZE}px; text-align: center;"
        )

        rec_sec_slider_label = QLabel(REC_SEC_SLIDER_LABEL)
        rec_sec_slider = QSlider(Qt.Horizontal)
        rec_sec_slider.setRange(*_DEFALUT_REC_RANGE)
        rec_sec_slider.setValue(_DEFAULT_REC_TIME)
        rec_sec_slider.valueChanged.connect(
            self.__update_rec_sec_slider
        )

        self.layout_recorder.addWidget(rec_label, alignment=Qt.AlignCenter)


    def __update_rec_sec_slider(self) -> None:
        pass


    def __init_converter(self) -> None:
        pass


    def __init_generator(self) -> None:
        pass


    def __init_player(self) -> None:
        pass


    def __init_bottom(self) -> None:
        pass

    @staticmethod
    def __create_label(
        label_text: str,
        font_size: int = None,
        alignment: Qt.AlignmentFlag = None,

    ) -> QLabel:
        label = QLabel(label_text)
        if font_size:
            label.setStyleSheet(f"font-size: {font_size}px;")
        if alignment:
            label.setAlignment(alignment)
        return label
    
    @staticmethod
    def __create_slider(
        orientation: Qt.Orientation,
        val_range: tuple[int, int],
        default_value: int,
        connect_method: callable
    ) -> QSlider:
        slider = QSlider(orientation)
        slider.setRange(*val_range)
        slider.setValue(default_value)
        slider.valueChanged.connect(connect_method)
        return slider
    
    @staticmethod
    def __create_button(
        text: str,
        height: int,
        button_color: str,
        text_color: str,
        connect_method: callable
    ) -> QPushButton:
        button = QPushButton(text)
        button.setFixedHeight(height)
        button.clicked.connect(connect_method)
        button.setStyleSheet(
            f"background-color: {button_color}; color: {text_color};"
        )
        return button

    @staticmethod
    def __create_line(width: int, color: str) -> QFrame:
        line = QFrame()
        line.setStyleSheet(f"border: {width}px solid {color};")
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Sunken)
        return line