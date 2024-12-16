import sys
import json
import asyncio
from PySide6.QtWidgets import (
    QApplication, QFrame, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QSlider, QComboBox
)
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QPixmap
from hello import async_function, hello_world

class MainApp(QWidget):
    def __init__(self):
        super().__init__()

        # メインウィンドウの設定
        self.setWindowTitle("Humor")
        self.setGeometry(100, 100, 750, 200)
        
        # 背景色の設定
        #self.setStyleSheet("background-color: white;")

        # UI要素の作成
        self.initUI()
        
        # 状態変数
        self.state = "停止"  # 状態管理

    def initUI(self):
        main_layout = QVBoxLayout()  # 全体の縦レイアウト
        # 上部横長のレイアウト
        top_layout = QHBoxLayout()
        
        
        # 画像表示用のラベル
        self.image_label = QLabel("logo")
        pixmap = QPixmap("logo_1.png")  # 画像ファイルのパスを指定
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
        
        bottom_layout = QHBoxLayout()  # 全体の横レイアウト
        left_layout = QVBoxLayout()  # 左側の縦レイアウト
        middle_layout = QVBoxLayout()  # 中央の縦レイアウト
        right_layout = QVBoxLayout()  # 右側の縦レイアウト

        # 左側のUI要素
        self.slider_label = QLabel("録音時間: 5秒")
        self.slider = QSlider(Qt.Horizontal)
        self.slider.setRange(1, 20)
        self.slider.setValue(5)  # 初期値を5に設定
        self.slider.valueChanged.connect(self.update_slider_label)

        self.record_button = QPushButton("開始")
        self.record_button.clicked.connect(self.toggle_sound)
        self.record_button.setStyleSheet("background-color: red; color: white;")

        self.play_button = QPushButton("再生")
        self.play_button.clicked.connect(self.play_sound)
        self.play_button.setStyleSheet("background-color: black; color: white;")

        self.record_label = QLabel("録音: 録音可能")
        self.play_label = QLabel("再生: 録音されていません")

        # 左側のUI要素の配置
        left_layout.addWidget(self.slider_label)
        left_layout.addWidget(self.slider)
        left_layout.addWidget(self.record_label)
        left_layout.addWidget(self.record_button)
        left_layout.addWidget(self.play_label)
        left_layout.addWidget(self.play_button)
        
        left_layout.addStretch(10)  # 余白を追加

        # 中央のUI要素
        self.prompt_label = QLabel("プロンプト選択:")
        self.prompt_combobox = QComboBox()
        self.load_prompt()
        
        self.model_label = QLabel("モデル選択:")
        self.model_combobox = QComboBox()
        self.load_models()


        self.generate_button = QPushButton("生成")
        self.generate_button.setFixedHeight(50)  # ボタンの縦を長く設定
        self.generate_button.clicked.connect(self.start_generation)
        self.generate_button.setStyleSheet("background-color: black; color: white;")

        self.result_label = QLabel("結果: ---")

        # 中央のUI要素の配置
        middle_layout.addWidget(self.prompt_label)
        middle_layout.addWidget(self.prompt_combobox)
        middle_layout.addWidget(self.model_label)
        middle_layout.addWidget(self.model_combobox)
        middle_layout.addWidget(self.generate_button)
        middle_layout.addWidget(self.result_label)
        
        middle_layout.addStretch(10)  # 余白を追加

        # 右側のUI要素
        self.continue_label = QLabel("生成した続きの再生: ")
        self.continue_button = QPushButton("再生")
        self.continue_button.setFixedHeight(130)  # ボタンの縦を長く設定
        self.continue_button.setStyleSheet("background-color: black; color: white;")

        # 右側のUI要素の配置
        right_layout.addWidget(self.continue_label)
        right_layout.addWidget(self.continue_button)
        
        right_layout.addStretch(10)  # 余白を追加
        

        bottom_layout.addLayout(left_layout, 1)  # 左のストレッチファクターを1に設定
        bottom_layout.addLayout(middle_layout, 1)  # 中央のストレッチファクターを1に設定
        bottom_layout.addLayout(right_layout, 1)  # 右のストレッチファクターを1に設定
        
        main_layout.addLayout(bottom_layout)  # 3分割のレイアウトを追加

        self.setLayout(main_layout)
    
    def load_prompt(self):
        """JSONファイルからプロンプトを読み込む"""
        with open('src/application/prompts.json', 'r', encoding='utf-8') as file:
            data = json.load(file)
            prompts = [prompt['name'] for prompt in data]
            self.prompt_combobox.addItems(prompts)

    def load_models(self):
        """JSONファイルからモデルを読み込む"""
        with open('src/application/models.json', 'r', encoding='utf-8') as file:
            data = json.load(file)
            models = [model['name'] for model in data]
            self.model_combobox.addItems(models)

    def update_slider_label(self, value):
        """スライダーの値を更新する"""
        self.slider_label.setText(f"録音秒数: {value}秒")

    def toggle_sound(self):
        """録音ボタンの状態をトグルする"""
        if self.record_label.text() == "録音: 録音可能":
            self.record_button.setText("録音中")
            duration = self.slider.value()
            #record_function(duration)
            self.record_label.setText("録音: 録音完了")
            self.record_button.setText("もう一度録音")
            self.play_label.setText("再生: 再生可能")
            self.play_button.setText("再生")
        else:
            self.record_button.setText("開始")
            self.record_label.setText("録音: 録音可能")

    async def start_async_function(self, duration):
        """非同期関数を実行する"""
        await async_function(duration)

    def play_sound(self):
        """再生ボタンが押されたときの処理"""
        if self.play_label.text() == "再生: 再生可能":
            self.play_label.setText("再生: 再生中")
            self.play_button.setText("再生中")
            #playfunction()
            self.play_button.setText("もう一度再生")
            self.play_label.setText("再生: 再生完了")

        else:
            self.play_label.setText("再生: 再生可能")


    def start_generation(self):
        """生成ボタンが押されたときの処理"""
        self.result_label.setText("結果: 生成中...")
        self.result_label.setText(f"結果: {self.model_combobox.currentText()}で{self.prompt_combobox.currentText()}の続きを生成しました。")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainApp()
    window.show()
    sys.exit(app.exec())
