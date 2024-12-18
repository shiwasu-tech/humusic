import sys
import json
import asyncio
from PySide6.QtWidgets import (
    QApplication, QFrame, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QSlider, QComboBox
)
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QPixmap
from hello import async_function, hello_world

sys.path.append("src")
sys.path.append("src/hum2midi")
sys.path.append("src/application")
from MidPlayer import play_mid

''''''#iitai宛のコメントアウトはこの形式
''''''#下に使用するclassや関数を追加
''''''#インスタンス化はmainapp内で行う方が楽かも
import hum2midi.Recorder as Recorder
from continuous_generator.Generator import generate_midi



class MainApp(QWidget):
    def __init__(self):
        super().__init__()

        # メインウィンドウの設定
        self.setWindowTitle("Humor")
        self.setGeometry(100, 100, 850, 500)
        
        # 背景色の設定
        #self.setStyleSheet("background-color: white;")

        # UI要素の作成
        self.initUI()
        
        # 状態変数
        self.state = "停止"  # 状態管理
        
        
        ''''''#基本的に保存先は以下のパスに追加
        self.rec_wav_path = "rerources/inputs/output.wav"
        self.prompt_path = "resources/inputs/output.mid"
        self.model_path = "resources/models/lstmwithatt_best.pt"
        self.tokenizer_path = "resources/tokenizers/piano1_tokens/tokenizer.json"
        self.gen_midi_path = "resources/generated/generated_best.mid"
        self.record_seconds = 5  # 録音時間の初期値
        self.generate_notes = 500  # 生成する音符数

    def initUI(self):
        """UI要素の初期化"""
        main_layout = QVBoxLayout()  # 全体の縦レイアウト
        # 上部横長のレイアウト
        top_layout = QHBoxLayout()
        
        
        # 画像表示用のラベル
        self.image_label = QLabel("logo")
        pixmap = QPixmap("src/application/logo_1.png")  # 画像ファイルのパスを指定
        scaled_pixmap = pixmap.scaled(50, 50, Qt.KeepAspectRatio)  # 画像のサイズを変更
        self.image_label.setPixmap(scaled_pixmap)
        self.top_label = QLabel("Humor")
        self.top_label.setStyleSheet("font-size: 24px;")  # フォントサイズを24pxに設定
        self.index_label = QLabel("\n--HUMming cOntinuation generatoR--")

        top_layout.addWidget(self.image_label)
        top_layout.addWidget(self.top_label)
        top_layout.addWidget(self.index_label)
        top_layout.addStretch(1)  # 余白を追加
        
        # 線を追加
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Sunken)
        line.setStyleSheet("border: 4px solid black;")  # 線の太さを設定
        
        main_layout.addLayout(top_layout)
        main_layout.addWidget(line)  # 線を追加






        # メインレイアウトに横長のレイアウトと3分割のレイアウトを追加
        main_layout.addLayout(top_layout)  # 横長のレイアウトを追加
        





        
        middle_layout = QHBoxLayout()  # 全体の横レイアウト
        recording_layout = QVBoxLayout()  # 録音部分（左）の縦レイアウト
        prompt_select_layout = QVBoxLayout()  # 変換，プロンプト選択部分（中央左）の縦レイアウト
        generator_layout = QVBoxLayout()  # モデル選択と生成部分（中央右）の縦レイアウト
        player_layout = QVBoxLayout()  # 再生部分（右）の縦レイアウト
        bottom_layout = QVBoxLayout()  # 下部の縦レイアウト

        # Add titles to each section
        recording_title = QLabel("録音")
        prompt_select_title = QLabel("変換")
        generator_title = QLabel("生成")
        player_title = QLabel("再生")

        # Set font size and alignment for titles
        recording_title.setStyleSheet("font-size: 20px; text-align: center;")
        prompt_select_title.setStyleSheet("font-size: 20px; text-align: center;")
        generator_title.setStyleSheet("font-size: 20px; text-align: center;")
        player_title.setStyleSheet("font-size: 20px; text-align: center;")

        recording_layout.addWidget(recording_title, alignment=Qt.AlignCenter)
        prompt_select_layout.addWidget(prompt_select_title, alignment=Qt.AlignCenter)
        generator_layout.addWidget(generator_title, alignment=Qt.AlignCenter)
        player_layout.addWidget(player_title, alignment=Qt.AlignCenter)

        # 録音部分側のUI要素
        self.rec_sec_slider_label = QLabel("録音時間: 5秒")
        self.rec_sec_slider = QSlider(Qt.Horizontal)
        self.rec_sec_slider.setRange(1, 20)
        self.rec_sec_slider.setValue(5)  # 初期値を5に設定
        self.rec_sec_slider.valueChanged.connect(self.update_rec_sec_slider_label)

        self.record_button = QPushButton("開始")
        self.record_button.setFixedHeight(50)  # ボタンの縦を長く設定
        self.record_button.clicked.connect(self.toggle_sound)
        self.record_button.setStyleSheet("background-color: red; color: white;")

        self.play_button = QPushButton("再生")
        self.play_button.setFixedHeight(50)  # ボタンの縦を長く設定
        self.play_button.clicked.connect(self.play_rec_sound)
        self.play_button.setStyleSheet("background-color: gray; color: white;")

        self.record_label = QLabel("録音: 録音可能")
        self.play_label = QLabel("再生: 録音されていません")

        # 録音部分のUI要素の配置
        recording_layout.addWidget(self.rec_sec_slider_label)
        recording_layout.addWidget(self.rec_sec_slider)
        recording_layout.addWidget(self.record_label)
        recording_layout.addWidget(self.record_button)
        recording_layout.addWidget(self.play_label)
        recording_layout.addWidget(self.play_button)
        
        recording_layout.addStretch(10)  # 余白を追加

        # 変換，プロンプト選択部分のUI要素
        self.convert_label = QLabel("音声をmidiに変換: ")
        self.convert_button = QPushButton("変換")
        self.convert_button.setFixedHeight(50)  # ボタンの縦を長く設定
        self.convert_button.clicked.connect(self.convert_rec2mid)
        self.convert_button.setStyleSheet("background-color: purple; color: white;")
        self.prompt_label = QLabel("プロンプト選択:")
        self.prompt_combobox = QComboBox()
        self.prompt_combobox.currentTextChanged.connect(self.on_prompt_selected)
        self.load_prompt()
        self.prompt_play_label = QLabel("プロンプト再生: ")
        self.prompt_play_button = QPushButton("再生")
        self.prompt_play_button.setFixedHeight(50)  # ボタンの縦を長く設定
        self.prompt_play_button.clicked.connect(self.play_prompt)
        self.prompt_play_button.setStyleSheet("background-color: blue; color: white;")

        
        # 変換，プロンプト選択部分のUI要素の配置
        prompt_select_layout.addWidget(self.convert_label)
        prompt_select_layout.addWidget(self.convert_button)
        prompt_select_layout.addWidget(self.prompt_label)
        prompt_select_layout.addWidget(self.prompt_combobox)
        prompt_select_layout.addWidget(self.prompt_play_label)
        prompt_select_layout.addWidget(self.prompt_play_button)
        
        prompt_select_layout.addStretch(10)  # 余白を追加

        # 生成部分のUI要素
        self.model_label = QLabel("モデル選択:")
        self.model_combobox = QComboBox()
        self.model_combobox.currentTextChanged.connect(self.on_model_selected)
        self.load_models()

        self.gen_notes_slider_label = QLabel("生成するノーツ数: 500個")
        self.gen_notes_slider = QSlider(Qt.Horizontal)
        self.gen_notes_slider.setRange(100, 1000)
        self.gen_notes_slider.setValue(500)  # 初期値を5に設定
        self.gen_notes_slider.valueChanged.connect(self.update_gen_notes_slider_label)

        self.generate_button = QPushButton("生成")
        self.generate_button.setFixedHeight(50)  # ボタンの縦を長く設定
        self.generate_button.clicked.connect(self.start_generation)
        self.generate_button.setStyleSheet("background-color: orange; color: white;")


        # 生成部分のUI要素の配置
        generator_layout.addWidget(self.model_label)
        generator_layout.addWidget(self.model_combobox)
        generator_layout.addWidget(self.gen_notes_slider_label)
        generator_layout.addWidget(self.gen_notes_slider)
        generator_layout.addWidget(self.generate_button)
        
        generator_layout.addStretch(10)  # 余白を追加

        # 再生部分のUI要素
        self.generated_select_label = QLabel("生成した続きの選択: ")
        self.generated_combobox = QComboBox()
        self.generated_combobox.currentTextChanged.connect(self.on_generated_selected)
        self.load_generated()
        self.generated_label = QLabel("生成した続きの再生: 未選択")
        self.generated_play_button = QPushButton("再生")
        self.generated_play_button.setFixedHeight(100)  # ボタンの縦を長く設定
        self.generated_play_button.clicked.connect(self.play_generated)
        self.generated_play_button.setStyleSheet("background-color: blue; color: white;")

        # 再生部分のUI要素の配置
        player_layout.addWidget(self.generated_select_label)
        player_layout.addWidget(self.generated_combobox)
        player_layout.addWidget(self.generated_label)
        player_layout.addWidget(self.generated_play_button)

        player_layout.addStretch(10)  # 余白を追加

        self.status_label = QLabel("Status: ---")
        self.explain_label = QLabel("※再生中はターミナルでqを入力すると停止します.")
        bottom_layout.addWidget(self.status_label)
        bottom_layout.addWidget(self.explain_label)
        

        middle_layout.addLayout(recording_layout, 1)  # 左のストレッチファクターを1に設定
        middle_layout.addLayout(prompt_select_layout, 1)  # 中央のストレッチファクターを1に設定
        middle_layout.addLayout(generator_layout, 1)  # 右のストレッチファクターを1に設定
        middle_layout.addLayout(player_layout, 1)  # 右のストレッチファクターを1に設定
        
        main_layout.addLayout(middle_layout)  # 3分割のレイアウトを追加

        # 線を追加
        bottom_line = QFrame()
        bottom_line.setFrameShape(QFrame.HLine)
        bottom_line.setFrameShadow(QFrame.Sunken)
        bottom_line.setStyleSheet("border: 4px solid black;")  # 線の太さを設定
        main_layout.addWidget(bottom_line)  # 線を追加

        main_layout.addLayout(bottom_layout)  # 下部のレイアウトを追加

        self.setLayout(main_layout)

    
    """UI要素の更新"""

    # 録音部分

    def update_rec_sec_slider_label(self, value):
        """録音時間スライダーの値を更新する"""
        self.rec_sec_slider_label.setText(f"録音時間: {value}秒")
        self.record_seconds = value

    ## 録音ボタンが押されたときの処理
    def toggle_sound(self):
        """録音ボタンの状態をトグルする"""
        if self.record_label.text() == "録音: 録音可能":
            self.record_button.setText("録音中...")
            duration = self.rec_sec_slider.value()
            # durationは録音時間
            # self.rec_wav_path = record_function(duration)
            self.record_label.setText("録音: 録音完了")
            self.record_button.setText("もう一度録音")
            self.play_label.setText("再生: 再生可能")
            self.play_button.setText("再生")
        else:
            self.record_button.setText("開始")
            self.record_label.setText("録音: 録音可能")

    ## 再生ボタンが押されたときの処理(wavの再生)
    def play_rec_sound(self):
        """再生ボタンが押されたときの処理"""
        if self.play_label.text() == "再生: 再生可能":
            self.play_label.setText("再生: 再生中")
            self.play_button.setText("再生中...")
            self.status_label.setText("Status: 再生中...")
            
            ''''''#wavの再生関数時間があれば実装
            # ここに再生する関数を入れる
            # playfunction(self.rec_wav_path)

            self.play_button.setText("もう一度再生")
            self.play_label.setText("再生: 再生完了")
        else:
            self.play_label.setText("再生: 再生可能")

    # 変換，プロンプト選択部分
    ## 変換ボタンが押されたときの処理
    def convert_rec2mid(self):
        """録音した音声をmidiに変換する"""

        ''''''#録音した音声をmidiに変換する関数を記入
        #convert_function()
        self.status_label.setText("Status: 音声をmidiに変換しました。")

    ## プロンプトの選択肢のロード
    def load_prompt(self):
        """JSONファイルからプロンプトを読み込む"""
        with open('src/application/path_to_resources.json', 'r', encoding='utf-8') as file:
            data = json.load(file)
            prompt_key = [key for key in data["prompt"]]
            self.prompt_combobox.addItems(prompt_key)
            
    ## プロンプト選択の処理
    def on_prompt_selected(self, text):
        """プロンプトが選択されたときに呼び出される"""
        with open('src/application/path_to_resources.json', 'r', encoding='utf-8') as file:
            data = json.load(file)
            self.prompt_path = data["prompt"][self.prompt_combobox.currentText()]["prompt_path"]
        self.prompt_play_label.setText("プロンプト再生: 再生可能")
        

    ## プロンプト再生ボタンが押された時の処理
    def play_prompt(self):
        """プロンプト再生ボタンが押されたときの処理"""
        if self.prompt_play_label.text() == "プロンプト再生: 再生可能":
            self.status_label.setText("Status: 再生中... ターミナルでqを入力すると停止します.")
            self.prompt_play_label.setText("プロンプト再生: 再生中")
            self.prompt_play_button.setText("再生中...")
            
            play_mid(self.prompt_path)
            self.prompt_play_button.setText("再生")
            self.prompt_play_label.setText("プロンプト再生: 再生完了")
            self.status_label.setText("Status: 再生完了")
        else:
            self.prompt_play_label.setText("プロンプト再生: 再生可能")
            
    # 生成部分
    ## モデルの選択肢のロード
    def load_models(self):
        """JSONファイルからモデルを読み込む"""
        with open('src/application/path_to_resources.json', 'r', encoding='utf-8') as file:
            data = json.load(file)
            model_key = [key for key in data["model"]]
            self.model_combobox.addItems(model_key)

    ## モデル選択の処理
    def on_model_selected(self, text):
        """モデルが選択されたときに呼び出される"""
        with open('src/application/path_to_resources.json', 'r', encoding='utf-8') as file:
            data = json.load(file)
            self.model_path = data["model"][self.model_combobox.currentText()]["model_path"]
            self.tokenizer_path = data["model"][self.model_combobox.currentText()]["tokenizer_path"]
        print(self.model_path,self.tokenizer_path)
        
    ## 生成ノーツ数のスライダーの値を更新する
    def update_gen_notes_slider_label(self, value):
        """生成ノーツ数スライダーの値を更新する"""
        self.gen_notes_slider_label.setText(f"生成するノーツ数: {value}個")
        self.generate_notes = value

    ## 生成ボタンが押されたときの処理
    def start_generation(self):
        """生成ボタンが押されたときの処理"""
        if self.generate_button.text() == "生成":
            self.generate_button.setText("生成中...")
            self.generate_button.setStyleSheet("background-color: red; color: white;")
            
            generate_midi(self.model_path, self.tokenizer_path, self.prompt_path, self.generate_notes)
            self.generate_button.setText("生成")
            self.generate_button.setStyleSheet("background-color: orange; color: white;")
            
        else:
            self.generate_button.setText("生成")
            self.generate_button.setStyleSheet("background-color: orange; color: white;")
            
        
        self.status_label.setText("Status: 生成中...")
        self.status_label.setText(f"Status: {self.model_combobox.currentText()}で{self.prompt_combobox.currentText()}の続きを生成しました。")
        print(self.model_path, self.tokenizer_path, self.prompt_path)

    # 再生部分
    ## 生成した続きの選択肢のロード
    def load_generated(self):
        """JSONファイルから生成した続きを読み込む"""
        with open('src/application/path_to_resources.json', 'r', encoding='utf-8') as file:
            data = json.load(file)
            generated_key = [key for key in data["generated"]]
            self.generated_combobox.addItems(generated_key)
        
    ## 生成した続きの選択の処理
    def on_generated_selected(self, text):
        """生成した続きが選択されたときに呼び出される"""
        with open('src/application/path_to_resources.json', 'r', encoding='utf-8') as file:
            data = json.load(file)
            self.gen_midi_path = data["generated"][self.generated_combobox.currentText()]["midi_path"]
        self.generated_label.setText("生成した続きの再生: 再生可能")
    
    
    ## 続きの再生ボタンが押されたときの処理
    def play_generated(self):
        """続きの再生ボタンが押されたときの処理"""
        if self.generated_label.text() == "生成した続きの再生: 再生可能":
            self.generated_label.setText("生成した続きの再生: 再生中")
            self.generated_play_button.setText("再生中...")
            self.status_label.setText("Status: 再生中... ターミナルでqを入力すると停止します.")
            
            play_mid(self.gen_midi_path)
            self.generated_play_button.setText("もう一度再生")
            self.generated_label.setText("生成した続きの再生: 再生完了")
            self.status_label.setText("Status: 再生完了")
            
        else:
            self.generated_label.setText("生成した続きの再生: 再生可能")


    ##############
    async def start_async_function(self, duration):
        """非同期関数を実行する"""
        await async_function(duration)

        


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainApp()
    window.show()
    sys.exit(app.exec())
