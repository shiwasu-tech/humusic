"""未実装の機能等"""
# 1. bottom_layout, __init_bottom
#     - メッセージの表示
# 2. play_wave
#     - playsound
# 3. play_midi
#     - play_mid
# 4. update_method
#     - self.convert_methodの更新
# 5. update_prompt_midi
#     - self.prompt_midiの宣言
#     - self.prompt_midiの更新
# 6. update_model
#     - self.modelの更新
#     - jsonの読み込み
# 7. update_gen_midi
#     - self.gen_midiの宣言
#     - self.gen_midiの更新
# 8. record_wave
#     - Recorder
# 9. convert_wave_to_midi
#     - Wave2MidiConverter
# 10. generate_continuation_midi
#     - generate_midi?
# 11. docstringの追加とコメントアウトの整備
# 12. UIの整備
#     - レイアウトの整理
#     - ボタンの色の変更
#     - ボタンのサイズの変更
#     - フォントサイズの変更
#     - フォントの変更

"""実装悩み中のメソッド"""
# def toggle_sound(self):
#     """録音ボタンの状態をトグルする"""
#     if self.record_label.text() == "録音: 録音可能":
#         self.record_button.setText("録音中...")
#         duration = self.rec_sec_slider.value()
#         # durationは録音時間
#         # self.rec_wav_path = record_function(duration)
#         self.record_label.setText("録音: 録音完了")
#         self.record_button.setText("もう一度録音")
#         self.play_label.setText("再生: 再生可能")
#         self.play_button.setText("再生")
#     else:
#         self.record_button.setText("開始")
#         self.record_label.setText("録音: 録音可能")

# ## プロンプトの選択肢のロード
# # リスト形式で選択肢を取得するメソッドに変更するかも
# def load_prompt(self):
#     """JSONファイルからプロンプトを読み込む"""
#     with open('src/application/path_to_resources.json', 'r', encoding='utf-8') as file:
#         data = json.load(file)
#         prompt_key = [key for key in data["prompt"]]
#         self.prompt_combobox.addItems(prompt_key)

# ## プロンプト選択の処理
# def on_prompt_selected(self, text):
#     """プロンプトが選択されたときに呼び出される"""
#     with open('src/application/path_to_resources.json', 'r', encoding='utf-8') as file:
#         data = json.load(file)
#         self.prompt_path = data["prompt"][self.prompt_combobox.currentText()]["prompt_path"]
#     self.prompt_play_label.setText("プロンプト再生: 再生可能")

# ## モデルの選択肢のロード
# # リスト形式で選択肢を取得するメソッドに変更するかも
# def load_models(self):
#     """JSONファイルからモデルを読み込む"""
#     with open('src/application/path_to_resources.json', 'r', encoding='utf-8') as file:
#         data = json.load(file)
#         model_key = [key for key in data["model"]]
#         self.model_combobox.addItems(model_key)

# ## モデル選択の処理
# # モデルのパスを取得するメソッドに変更するかも
# def on_model_selected(self, text):
#     """モデルが選択されたときに呼び出される"""
#     with open('src/application/path_to_resources.json', 'r', encoding='utf-8') as file:
#         data = json.load(file)
#         self.model_path = data["model"][self.model_combobox.currentText()]["model_path"]
#         self.tokenizer_path = data["model"][self.model_combobox.currentText()]["tokenizer_path"]
#     print(self.model_path,self.tokenizer_path)

# ## 生成ボタンが押されたときの処理
# # メソッド自体は新しく作成済み。参考のため置いておく
# def start_generation(self):
#     """生成ボタンが押されたときの処理"""
#     if self.generate_button.text() == "生成":
#         self.generate_button.setText("生成中...")
#         self.generate_button.setStyleSheet("background-color: red; color: white;")
        
#         generate_midi(self.model_path, self.tokenizer_path, self.prompt_path, self.generate_notes)
#         self.generate_button.setText("生成")
#         self.generate_button.setStyleSheet("background-color: orange; color: white;")
        
#     else:
#         self.generate_button.setText("生成")
#         self.generate_button.setStyleSheet("background-color: orange; color: white;")
        
    
#     self.status_label.setText("Status: 生成中...")
#     self.status_label.setText(f"Status: {self.model_combobox.currentText()}で{self.prompt_combobox.currentText()}の続きを生成しました。")
#     print(self.model_path, self.tokenizer_path, self.prompt_path)

# # 再生部分
# # 参考のため置いておく
# ## 生成した続きの選択肢のロード
# def load_generated(self):
#     """JSONファイルから生成した続きを読み込む"""
#     with open('src/application/path_to_resources.json', 'r', encoding='utf-8') as file:
#         data = json.load(file)
#         generated_key = [key for key in data["generated"]]
#         self.generated_combobox.addItems(generated_key)

# ## 生成した続きの選択の処理
# # 日本語がよくわからないが、参考のため置いておく
# def on_generated_selected(self, text):
#     """生成した続きが選択されたときに呼び出される"""
#     with open('src/application/path_to_resources.json', 'r', encoding='utf-8') as file:
#         data = json.load(file)
#         self.gen_midi_path = data["generated"][self.generated_combobox.currentText()]["midi_path"]
#     self.generated_label.setText("生成した続きの再生: 再生可能")

# ## 続きの再生ボタンが押されたときの処理
# # 参考のため置いておく
# def play_generated(self):
#     """続きの再生ボタンが押されたときの処理"""
#     if self.generated_label.text() == "生成した続きの再生: 再生可能":
#         self.generated_label.setText("生成した続きの再生: 再生中")
#         self.generated_play_button.setText("再生中...")
#         self.status_label.setText("Status: 再生中... ターミナルでqを入力すると停止します.")
        
#         play_mid(self.gen_midi_path)
#         self.generated_play_button.setText("もう一度再生")
#         self.generated_label.setText("生成した続きの再生: 再生完了")
#         self.status_label.setText("Status: 再生完了")
        
#     else:
#         self.generated_label.setText("生成した続きの再生: 再生可能")

import sys
import json
from functools import partial
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
_DEFAULT_CONVERT_METHOD = "harvest"
_DEFAULT_NOTE_NUM = 500

_BACKGROUND_COLOR = "black"
_RECORDER_COLOR = "#d65f55"
_PLAYER_COLOR = "#163054"
_CONVERTER_COLOR = "#da9c3d"
_GENERATOR_COLOR = "#92d787"

class MainApp(QWidget):
    def __init__(self):
        super().__init__()
        # 秒数、変換手法、プロンプトのパス、生成モデルのパス，トークナイザーのパス、生成ノーツ数、生成midiのパスを保持するインスタンス変数
        self.rec_time = _DEFAULT_REC_TIME
        self.convert_method = _DEFAULT_CONVERT_METHOD
        self.prompt = _PROMPT_MIDI_PATH
        self.model = _MODEL_PATH
        self.tokenizer = _TOKENIZER_PATH
        self.note_num = _DEFAULT_NOTE_NUM
        self.gen_midi = _GEN_MIDI_PATH
        # メソッド多重呼び出し防止フラグ
        self.is_processing = False
        # layoutのインスタンスオブジェクトを生成
        self.main_layout = QVBoxLayout()
        self.top_layout = QHBoxLayout()
        self.body_layout = QHBoxLayout()
        self.bottom_layout = QHBoxLayout()

        self.recorder_layout = QVBoxLayout()
        self.converter_layout = QVBoxLayout()
        self.generator_layout = QVBoxLayout()
        # uiの初期化
        self.__init_UI()

    
    def __init_UI(self):
        pass
        # 定数の初期化
        WINDOW_X = 100
        WINDOW_Y = 100
        WINDOW_WIDTH = 800
        WINDOW_HEIGHT = 450
        # ウインドウの設定
        self.setWindowTitle(_TITLE)
        self.setGeometry(
            WINDOW_X,
            WINDOW_Y,
            WINDOW_WIDTH,
            WINDOW_HEIGHT
        )
        # 各layoutの初期化
        self.__init_top()
        self.__init_body()
        self.__init_bottom()
        self.main_layout.addLayout(self.top_layout)
        self.main_layout.addWidget(self.__init_line())
        self.main_layout.addLayout(self.body_layout)
        self.main_layout.addWidget(self.__init_line())
        self.main_layout.addLayout(self.bottom_layout)
        # layoutのセット
        self.setLayout(self.main_layout)


    def __init_top(self):
        # 定数の初期化
        LOGO_WIDTH = 50
        LOGO_HEIGHT = 50
        # ロゴの設定
        logo_label = self.__init_pixmap(
            pixmap_path =_LOGO_PATH,
            width = LOGO_WIDTH,
            height = LOGO_HEIGHT
        )
        # タイトルの設定
        title_label = self.__init_label(
            text = _TITLE,
            font_size = 24
        )
        # サブタイトルの設定
        subtitle_label = self.__init_label(
            text = "\n" + _SUBTITLE,
            font_size = 10
        )
        # lineの設定
        line = self.__init_line()

        self.top_layout.addWidget(logo_label)
        self.top_layout.addWidget(title_label)
        self.top_layout.addWidget(subtitle_label)
        # layoutを改行してからlineを追加
        self.top_layout.addStretch()
        self.top_layout.addWidget(line)




    def __init_body(self):
        # 定数の初期化
        # 子のlayoutの初期化
        self.__init_recorder()
        self.__init_converter()
        self.__init_generator()
        # layoutのセット
        self.body_layout.addLayout(self.recorder_layout, stretch=1)
        self.body_layout.addLayout(self.converter_layout, stretch=1)
        self.body_layout.addLayout(self.generator_layout, stretch=1)


    def __init_bottom(self):
        pass
        # 定数の初期化
        # なんかテキストの設定


    def __init_recorder(self):
        # 定数の初期化
        HEAD_FONT_SIZE = 20
        REC_TIME_RANGE = (1, 20)
        # 大きめのラベルの設定
        head_label = self.__init_label(
            text = "録音",
            font_size = HEAD_FONT_SIZE,
            alignment = Qt.AlignCenter
        )
        # 録音時間のスライダーの設定
        rec_time_label = self.__init_label(
            text = f"録音時間: {_DEFAULT_REC_TIME}秒"
        )
        rec_time_slider = self.__init_slider(
            range = REC_TIME_RANGE,
            default_value = _DEFAULT_REC_TIME,
            connect_method = partial(self.__update_rec_time, rec_time_label)
        )
        # 録音ボタンの設定
        rec_button_label = self.__init_label(
            text = "録音ボタン"
        )
        rec_button = self.__init_button(
            text = "録音",
            connect_method = self.__record_wave,
            background_color = _RECORDER_COLOR
        )
        # 再生ボタンの設定
        play_button_label = self.__init_label(
            text = "再生ボタン"
        )
        play_button = self.__init_button(
            text = "再生",
            connect_method = self.__play_wave,
            background_color = _PLAYER_COLOR
        )

        self.recorder_layout.addWidget(head_label)
        self.recorder_layout.addWidget(rec_time_label)
        self.recorder_layout.addWidget(rec_time_slider)
        self.recorder_layout.addWidget(rec_button_label)
        self.recorder_layout.addWidget(rec_button)
        self.recorder_layout.addWidget(play_button_label)
        self.recorder_layout.addWidget(play_button)

    def __init_converter(self):
        # 定数の初期化
        HEAD_FONT_SIZE = 20
        # 大きめのラベルの設定
        head_label = self.__init_label(
            text = "変換",
            font_size = HEAD_FONT_SIZE,
            alignment = Qt.AlignCenter
        )
        # 変換手法の選択コンボボックスの設定
        convert_method_label = self.__init_label(
            text = "ピッチ解析手法"
        )
        convert_method_combobox = self.__init_combobox(
            items = ["harvest", "dio+stonemask"],  # 仮置
            connect_method = self.__update_method
        )
        # 変換ボタンの設定
        convert_button_label = self.__init_label(
            text = "変換ボタン"
        )
        convert_button = self.__init_button(
            text = "変換",
            connect_method = self.__convert_wave_to_midi,
            background_color = _CONVERTER_COLOR
        )
        # 再生ファイル選択コンボボックスの設定
        play_file_label = self.__init_label(
            text = "再生ファイル"
        )
        play_file_combobox = self.__init_combobox(
            items = ["input.mid"],  # 仮置
            connect_method = self.__update_prompt_midi
        )
        # 再生ボタンの設定
        play_button_label = self.__init_label(
            text = "再生ボタン"
        )
        play_button = self.__init_button(
            text = "再生",
            connect_method = self.__play_prompt_midi,
            background_color = _PLAYER_COLOR
        )

        self.converter_layout.addWidget(head_label)
        self.converter_layout.addWidget(convert_method_label)
        self.converter_layout.addWidget(convert_method_combobox)
        self.converter_layout.addWidget(convert_button_label)
        self.converter_layout.addWidget(convert_button)
        self.converter_layout.addWidget(play_file_label)
        self.converter_layout.addWidget(play_file_combobox)
        self.converter_layout.addWidget(play_button_label)
        self.converter_layout.addWidget(play_button)


    def __init_generator(self):
        pass
        # 定数の初期化
        HEAD_FONT_SIZE = 20
        NOTE_NUM_RANGE = (100, 1000)
        # 大きめのラベルの設定
        head_label = self.__init_label(
            text = "生成",
            font_size = HEAD_FONT_SIZE,
            alignment = Qt.AlignCenter
        )
        # 生成モデルの選択コンボボックスの設定
        model_label = self.__init_label(
            text = "生成モデル"
        )
        model_combobox = self.__init_combobox(
            items = ["lstmwithatt"],  # 仮置
            connect_method = self.__update_model
        )
        # 生成ノーツ数のスライダーの設定
        generate_note_label = self.__init_label(
            text = f"生成ノーツ数: {_DEFAULT_NOTE_NUM}"
        )
        generate_note_slider = self.__init_slider(
            range = NOTE_NUM_RANGE,
            default_value = _DEFAULT_NOTE_NUM,
            connect_method = partial(self.__update_note_num, generate_note_label)
        )
        # 生成ボタンの設定
        generate_button_label = self.__init_label(
            text = "生成ボタン"
        )
        generate_button = self.__init_button(
            text = "生成",
            connect_method = self.__generate_continuation_midi,
            background_color = _GENERATOR_COLOR
        )
        # 再生ファイル選択コンボボックスの設定
        play_file_label = self.__init_label(
            text = "再生ファイル"
        )
        play_file_combobox = self.__init_combobox(
            items = ["generated.mid"],  # 仮置
            connect_method = self.__update_gen_midi
        )
        # 再生ボタンの設定
        play_button_label = self.__init_label(
            text = "再生ボタン"
        )
        play_button = self.__init_button(
            text = "再生",
            connect_method = self.__play_gen_midi,
            background_color = _PLAYER_COLOR
        )
        
        self.generator_layout.addWidget(head_label)
        self.generator_layout.addWidget(model_label)
        self.generator_layout.addWidget(model_combobox)
        self.generator_layout.addWidget(generate_note_label)
        self.generator_layout.addWidget(generate_note_slider)
        self.generator_layout.addWidget(generate_button_label)
        self.generator_layout.addWidget(generate_button)
        self.generator_layout.addWidget(play_file_label)
        self.generator_layout.addWidget(play_file_combobox)
        self.generator_layout.addWidget(play_button_label)
        self.generator_layout.addWidget(play_button)


    @staticmethod
    def __init_pixmap(
            pixmap_path: str,
            width: int = None,
            height: int = None
    ) -> QLabel:
        img_label = QLabel()
        pixmap = QPixmap(pixmap_path)
        if width and height:
            img_label.setPixmap(pixmap.scaled(width, height))
        else:
            img_label.setPixmap(pixmap)
        
        return img_label
    

    @staticmethod
    def __init_label(
            text: str,
            font_size: int = None,
            alignment: Qt.AlignmentFlag = None
    ) -> QLabel:
        label = QLabel(text)
        if font_size:
            label.setStyleSheet(f"font-size: {font_size}px;")
        if alignment:
            label.setAlignment(alignment)

        return label


    @staticmethod
    def __init_slider(
            range: tuple[int, int],
            default_value: int,
            connect_method: callable,
            orientation: Qt.Orientation = Qt.Horizontal
    ) -> QSlider:
        slider = QSlider(orientation)
        slider.setRange(*range)
        slider.setValue(default_value)
        slider.valueChanged.connect(connect_method)

        return slider
    

    @staticmethod
    def __init_combobox(
            items: list[str],
            connect_method: callable,
            default_index: int = 0
    ) -> QComboBox:
        combobox = QComboBox()
        combobox.addItems(items)
        combobox.setCurrentIndex(default_index)
        combobox.currentIndexChanged.connect(connect_method)

        return combobox


    @staticmethod
    def __init_button(
            text: str,
            connect_method: callable,
            height: int = 50,
            text_color: str = "#ffffff",
            background_color: str = "#333"
    ) -> QPushButton:
        button = QPushButton(text)
        button.setFixedHeight(height)
        button.setStyleSheet(
            f"color: {text_color}; background-color: {background_color};"
        )
        button.clicked.connect(connect_method)

        return button


    @staticmethod
    def __init_line(
            width: int = 4,
            color: str = "#000",
            orientation: Qt.Orientation = Qt.Horizontal
    ) -> QFrame:
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Sunken)
        line.setLineWidth(width)
        line.setStyleSheet(f"color: {color};")

        return line


    def __update_rec_time(self, label: QLabel, value: int):
        # ラベルの更新
        # valueはスライダーの値
        label.setText(f"録音時間: {value}秒")
        self.rec_time = value


    def __record_wave(self):
        if self.__check_processing():
            return
        # 録音を行う
        # selfから録音時間を取得
        self.__exit_process()

    def __convert_wave_to_midi(self):
        if self.__check_processing():
            return
        # 変換を行う
        # selfから変換手法を取得
        self.__exit_process()

    def __generate_continuation_midi(self):
        if self.__check_processing():
            return
        # 生成を行う
        # selfから生成モデルを取得
        generate_midi(self.model, self.tokenizer, self.prompt, self.note_num)

        self.__exit_process()

    def __play_wave(self):
        if self.__check_processing():
            return
        # 録音した音声を再生する
        self.__exit_process()

    def __play_prompt_midi(self):
        if self.__check_processing():
            return
        # 変換したmidi、プロンプトのmidiを再生する
        play_mid(self.prompt)

        self.__exit_process()

    def __play_gen_midi(self):
        if self.__check_processing():
            return
        # 生成したmidiを再生する
        play_mid(self.gen_midi)

        self.__exit_process()

    def __update_method(self):
        pass
        # コンボボックスの選択肢をselfへ更新

    def __update_prompt_midi(self):
        pass
        # コンボボックスの選択肢をselfへ更新

    def __update_model(self):
        pass
        # コンボボックスの選択肢をselfへ更新

    def __update_note_num(self, label: QLabel, value: int):
        # ラベルの更新
        # valueはスライダーの値
        label.setText(f"生成ノーツ数: {value}")
        self.note_num = value

    def __update_gen_midi(self):
        pass
        # コンボボックスの選択肢をselfへ更新


    def __check_processing(self) -> bool:
        if self.is_processing:
            return True
        else:
            self.is_processing = True
            return False
        
    def __exit_process(self):
        self.is_processing = False


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_app = MainApp()
    main_app.show()
    sys.exit(app.exec())
