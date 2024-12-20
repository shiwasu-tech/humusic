import numpy as np
import sys
from mido import MidiFile, MidiTrack, Message, MetaMessage, bpm2tempo
sys.path.append("src/hum2midi")
from src.hum2midi.WaveAnalyzer import WaveAnalyzer

class Wave2MidiConverter:
    """録音した音声データをMIDIデータに変換するクラス

    録音した音声データを解析し、MIDIデータに変換する
    ピッチとBPMの情報から、ピッチを32分音符間隔で分割し、各平均値をノート番号に変換する
    隣接するノート番号が連続している場合、同じノート番号の長さを加算する

    Attributes:
        wave_path (str): 解析する音声データのパス
        method (str): 解析手法の指定. "harvest"か"dio"を指定
        output_path (str): 保存するMIDIファイルのパス
        f0_list (np.ndarray): ピッチのリスト
        time (float): ピッチの時間軸の間隔
        bpm (float): BPM
        midi (MidiFile): MIDIファイル
        track (MidiTrack): MIDIトラック
    """

    def __init__(
            self,
            wave_path: str,
            method: str = "harvest",
            output_path: str = "resources/output.mid"
    ):
        """コンストラクタ

        初期化の際、WaveAnalyzerを用いてピッチとBPMを取得する

        Args:
            wave_path (str): 解析する音声データのパス
            method (str, optional): 解析手法の指定. "harvest"か"dio"を指定. Defaults to "harvest".
            output_path (str, optional): 保存するMIDIファイルのパス. Defaults to "resources/output.mid".
        """
        print("Initializing Wave2MidiConverter...")
        self.wave_path = wave_path
        self.method = method
        self.output_path = output_path

        analyzer = WaveAnalyzer(self.wave_path, self.method)
        f0_list, time, bpm = analyzer.analyze_pitch_and_bpm()
        self.f0_list = f0_list
        self.time = time
        self.bpm = bpm

        self.midi = MidiFile()
        self.track = MidiTrack()
        self.__track_setup()
        print("Wave2MidiConverter initialized")

        
    def __track_setup(self):
        """MIDIトラックの設定を行うメソッド"""
        self.midi.tracks.append(self.track)
        self.track.append(MetaMessage('set_tempo', tempo=bpm2tempo(self.bpm)))


    def create_midi(self, velocity: int = 100):
        """MIDIデータを作成するメソッド

        Args:
            velocity (int, optional): ノートのベロシティ. Defaults to 100.
        """
        print("Creating MIDI data...")
        notes = self._make_notes()
        joined_notes = self._join_notes(notes)
        self._joined_notes_to_midi(joined_notes, velocity)


    def _make_notes(self) -> list:
        """ノート番号のリストを作成するメソッド

        ピッチをノート番号に変換することで、ノート番号のリストを作成する

        Returns:
            list: ノート番号のリスト
        """
        start_point = 0
        for s, f0 in enumerate(self.f0_list):
            if f0 != 0:
                start_point = s
                break

        FRAME = int((7.5 / self.bpm) * (1 / self.time))
        separated_f0_list = np.array_split(
            self.f0_list[start_point:],
            len(self.f0_list[start_point:]) // FRAME
        )

        notes = []
        for f0s in separated_f0_list:
            notes.append(self.__f0_to_note_number(np.mean(f0s)))
        
        return notes


    @staticmethod
    def __f0_to_note_number(f0: float) -> int:
        """ピッチをノート番号に変換するメソッド

        無音の場合はノート番号を-1とする

        Args:
            f0 (float): ピッチ

        Returns:
            int: ノート番号
        """
        if f0 == 0:
            return -1
        else:
            return int(69 + 12 * np.log2(f0 / 440))

    @staticmethod
    def _join_notes(notes: list) -> list:
        """同じノード番号の連続した音符を結合するメソッド

        Args:
            notes (list): ノート番号のリスト

        Returns:
            list: 結合されたノート番号の辞書型リスト{ノート番号, 長さ}
        """
        joined_notes = []
        prev_note = -1

        for note in notes:
            if not (prev_note <= note <= prev_note + 1):
                joined_notes.append({"note": note, "length": 1})
                prev_note = note
            else:
                joined_notes[-1]["length"] += 1
        
        return joined_notes


    def _joined_notes_to_midi(self, joined_notes: list, velocity: int):
        """結合されたノート番号のリストをMIDIデータに変換するメソッド

        MIDIデータはMIDIファイルとして保存される

        Args:
            joined_notes (list): 結合されたノート番号の辞書型リスト{ノート番号, 長さ}
            velocity (int): ノートのベロシティ
        """
        for note in joined_notes:
            if note["note"] != -1:
                self.track.append(Message(
                    "note_on",
                    note=note["note"],
                    velocity=velocity,
                    time=0
                ))
                self.track.append(Message(
                    "note_off",
                    note=note["note"],
                    velocity=velocity,
                    time=note["length"]*60
                ))
            else:
                self.track.append(Message(
                    "note_off",
                    note=0,
                    velocity=0,
                    time=note["length"]*60
                ))

        self.midi.save(self.output_path)
        print(f"Saved as {self.output_path}")


    def set_wave_path(self, wave_path: str):
        """音声データのパスを設定するメソッド

        音声データに依存する情報も再取得する

        Args:
            wave_path (str): 音声データのパス
        """
        self.wave_path = wave_path
        analyzer = WaveAnalyzer(self.wave_path)
        f0_list, time, bpm = analyzer.analyze_pitch_and_bpm()
        self.f0_list = f0_list
        self.time = time
        self.bpm = bpm

if __name__ == "__main__":
    wave2midi = Wave2MidiConverter("resources/inputs/input.wav")
    wave2midi.create_midi()