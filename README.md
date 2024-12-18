# Humor
## HUMming cOntinuous generatOr

鼻歌を録音し，midiに変換したのち，フリーのmidiを学習させたモデルに鼻歌midinの続きを生成させる．というプロジェクトです．<br>
第2回 C0deハッカソン with pixivにて作成しました．

## 実行方法

uvで一括管理しているので，uvをインストールすると簡単です．<br>
また，pythonの音響系ライブラリを使用しているため，portaudioを事前にインストールしてある必要があります．

上記のが完了した後
```humusic/```ディレクトリ内で，以下のコマンドを実行することで実行環境を構築．
```bash
uv sync
uv add -r requirements.txt
```

```humuic/```ディレクトリ内で，以下のコマンドを実行すれば，アプリケーションが起動します．
```bash
uv run -m /src
```



## ディレクトリ構成
```
humusic/
├─ src/
│├─ hum2midi/
│├─ continuous_generator/
│└─ application/
├─ resources/
├─ model_maker/
├─ README.md
├─ .gitignore
├─ .python-verion
├─ pyproject.toml
├─ reqirements.txt
└─ uv.lock
```




## 使用したデータセットの帰属表示
> ### "Classical Piano Midi"
> Name : Bernd Krueger<br>
> Source : http://www.piano-midi.de<br>
> LICENCE : CC-BY-SA Germaniy License.<br>
> https://creativecommons.org/licenses/by-sa/3.0/de/deed.en

