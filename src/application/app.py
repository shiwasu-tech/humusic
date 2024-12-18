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
            _WINDOW_X,
            _WINDOW_Y,
            _WINDOW_WIDTH,
            _WINDOW_HEIGHT
        )

        self.layout_main = QVBoxLayout()

        self.layout_top = QHBoxLayout()
        self.layout_body = QHBoxLayout()
        self.layout_bottom = QHBoxLayout()

        self.layout_recorder = QVBoxLayout()
        self.layout_converter = QVBoxLayout()
        self.layout_generator = QVBoxLayout()
        self.layout_player = QVBoxLayout()

        self.__init_UI()


    def __init_UI(self) -> None:
        self.__init_top()
        self.__init_body()
        self.__init_bottom()

        self.layout_main.addLayout(self.layout_top)
        self.layout_main.addLayout(self.layout_body)
        self.layout_main.addLayout(self.layout_bottom)

        self.setLayout(self.layout_main)


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
        print(pixmap)
        img_label = QLabel(IMG_LABEL)
        img_label.setPixmap(pixmap)
        print(img_label)
        top_label = self.__create_label(
            label_text = _TITLE,
            font_size = TITLE_FONT_SIZE
        )
        index_label = self.__create_label(_SUBTITLE)

        line = self.__create_line(
            width = LINE_WIDTH,
            color = "black"
        )

        self.layout_top.addWidget(img_label)
        self.layout_top.addWidget(top_label)
        self.layout_top.addWidget(index_label)
        self.layout_top.addStretch(STRETCH)
        self.layout_top.addWidget(line)

    
    def __init_body(self) -> None:
        self.__init_recorder()
        self.layout_body.addLayout(self.layout_recorder, stretch=1)

        self.__init_converter()
        self.layout_body.addLayout(self.layout_converter, stretch=1)

        self.__init_generator()
        self.layout_body.addLayout(self.layout_generator, stretch=1)

        # self.__init_player()
        # self.layout_body.addLayout(self.layout_player)


    def __init_recorder(self) -> None:
        REC_LABEL = "録音"
        REC_FONT_SIZE = 20
        REC_SEC_SLIDER_LABEL = f"録音時間: {_DEFAULT_REC_TIME}秒"

        rec_label = self.__create_label(
            label_text = REC_LABEL,
            font_size = REC_FONT_SIZE,
            alignment = Qt.AlignCenter
        )
        rec_sec_slider_label = self.__create_label(REC_SEC_SLIDER_LABEL)
        rec_sec_slider = self.__create_slider(
            orientation = Qt.Horizontal,
            val_range = _DEFALUT_REC_RANGE,
            default_value = _DEFAULT_REC_TIME,
            connect_method = self.__update_rec_sec_slider
        )
        rec_button_label = self.__create_label(label_text = "録音の開始")
        rec_button = self.__create_button(
            text = "開始",
            height = 50,
            button_color = "blue",
            text_color = "white",
            connect_method = self.__start_recording
        )
        preview_button_label = self.__create_label(label_text = "録音した音声の再生")
        preview_button = self.__create_button(
            text = "再生",
            height = 50,
            button_color = "blue",
            text_color = "white",
            connect_method = self.__start_recording
        )

        self.layout_recorder.addWidget(rec_label, alignment=Qt.AlignCenter)
        self.layout_recorder.addWidget(rec_sec_slider_label)
        self.layout_recorder.addWidget(rec_sec_slider)
        self.layout_recorder.addWidget(rec_button_label)
        self.layout_recorder.addWidget(rec_button)
        self.layout_recorder.addWidget(preview_button_label)
        self.layout_recorder.addWidget(preview_button)


    def __update_rec_sec_slider(self) -> None:
        pass


    def __start_recording(self) -> None:
        pass


    def __init_converter(self) -> None:
        CONVERTER_LABEL = "変換"
        CONVERTER_FONT_SIZE = 20
        METHOD_COMBOBOX_LABEL = "変換手法の選択"
        METHODS = ["harvest(default)", "dio+stonemask"]
        PROMPT_COMBOBOX_LABEL = "プロンプトの選択"

        converter_label = self.__create_label(
            label_text = CONVERTER_LABEL,
            font_size = CONVERTER_FONT_SIZE,
            alignment = Qt.AlignCenter
        )
        convert_method_combobox_label = self.__create_label(label_text = METHOD_COMBOBOX_LABEL)
        convert_method_combobox = self.__create_combobox(
            items = METHODS,
            connect_method = self.__update_convert_method
        )
        convert_button = self.__create_button(
            text = "変換",
            height = 50,
            button_color = "blue",
            text_color = "white",
            connect_method = self.__start_converting
        )
        prompt_combobox_label = self.__create_label(label_text = PROMPT_COMBOBOX_LABEL)
        prompt_combobox = self.__create_combobox(
            items = ["default"],
            connect_method = self.__update_convert_method
        )
        player_button = self.__create_button(
            text = "再生",
            height = 50,
            button_color = "blue",
            text_color = "white",
            connect_method = self.__start_converting
        )

        self.layout_converter.addWidget(converter_label, alignment=Qt.AlignCenter)
        self.layout_converter.addWidget(convert_method_combobox_label)
        self.layout_converter.addWidget(convert_method_combobox)
        self.layout_converter.addWidget(convert_button)
        self.layout_converter.addWidget(prompt_combobox_label)
        self.layout_converter.addWidget(prompt_combobox)
        self.layout_converter.addWidget(player_button)
        


    def __update_convert_method(self) -> None:
        pass

    def __start_converting(self) -> None:
        pass


    def __init_generator(self) -> None:
        GENERATOR_LABEL = "生成"
        GENERATOR_FONT_SIZE = 20
        GEN_NOTES_SLIDER_LABEL = f"生成ノート数: {_DEFAULT_GEN_NOTES}"
        GEN_RANGE = (100, 1000)

        generator_label = self.__create_label(
            label_text = GENERATOR_LABEL,
            font_size = GENERATOR_FONT_SIZE,
            alignment = Qt.AlignCenter
        )
        model_combobox_label = self.__create_label(label_text = "モデルの選択")
        model_combobox = self.__create_combobox(
            items = ["default"],
            connect_method = self.__update_gen_notes_slider
        )
        gen_notes_slider_label = self.__create_label(GEN_NOTES_SLIDER_LABEL)
        gen_notes_slider = self.__create_slider(
            orientation = Qt.Horizontal,
            val_range = GEN_RANGE,
            default_value = _DEFAULT_GEN_NOTES,
            connect_method = self.__update_gen_notes_slider
        )
        gen_button = self.__create_button(
            text = "生成",
            height = 50,
            button_color = "blue",
            text_color = "white",
            connect_method = self.__start_generating
        )
        play_data_combobox_label = self.__create_label(label_text = "再生するデータの選択")
        play_data_combobox = self.__create_combobox(
            items = ["default"],
            connect_method = self.__update_gen_notes_slider
        )
        player_button = self.__create_button(
            text = "再生",
            height = 50,
            button_color = "blue",
            text_color = "white",
            connect_method = self.__start_generating
        )

        self.layout_generator.addWidget(generator_label, alignment=Qt.AlignCenter)
        self.layout_generator.addWidget(gen_notes_slider_label)
        self.layout_generator.addWidget(gen_notes_slider)
        self.layout_generator.addWidget(gen_button)
        self.layout_generator.addWidget(model_combobox_label)
        self.layout_generator.addWidget(model_combobox)
        self.layout_generator.addWidget(play_data_combobox_label)
        self.layout_generator.addWidget(play_data_combobox)
        self.layout_generator.addWidget(player_button)

    def __start_generating(self) -> None:
        pass

    def __update_gen_notes_slider(self) -> None:
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
    
    @staticmethod
    def __create_combobox(
        items: list[str],
        connect_method: callable
    ) -> QComboBox:
        combobox = QComboBox()
        combobox.addItems(items)
        combobox.activated.connect(connect_method)
        return combobox
    

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_app = MainApp()
    main_app.show()
    sys.exit(app.exec())