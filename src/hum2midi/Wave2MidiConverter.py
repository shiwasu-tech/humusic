import numpy as np
from mido import MidiFile, MidiTrack, Message, MetaMessage, bpm2tempo

class Wave2MidiConverter:
    """録音した音声データをMIDIデータに変換するクラス

    録音した音声データを解析し、MIDIデータに変換する
    ピッチとBPMの情報から、ピッチを32分音符間隔で分割し、各平均値をノート番号に変換する
    隣接するノート番号が連続している場合、同じノート番号の長さを加算する

    Attributes:
        bpm (float): BPM
        velocity (int): ノートオン時のベロシティ
        output_path (str): 保存するMIDIファイル
        midi (MidiFile): MIDIファイルオブジェクト
        track (MidiTrack): MIDIトラックオブジェクト
    """

    def __init__(
            self,
            bpm: float,
            velocity: int = 100,
            output_path: str = "resources/output.mid"
    ):
        """コンストラクタ

        Args:
            bpm (float): BPM
            velocity (int, optional): 音量. Defaults to 80.
            output_path (str, optional): 保存するMIDIファイルのパス. Defaults to "resources/output.mid".
        """

        self.bpm = bpm
        self.velocity = velocity
        self.output_path = output_path

        self.midi = MidiFile()
        self.track = MidiTrack()
        self.__track_setup()

        
    def __track_setup(self):
        """MIDIトラックの設定を行うメソッド"""

        self.midi.tracks.append(self.track)
        self.track.append(MetaMessage('set_tempo', tempo=bpm2tempo(self.bpm)))


    def create_midi(self, f0_list: np.ndarray, time: float):
        """MIDIデータを作成するメソッド

        Args:
            f0_list (np.ndarray): ピッチのリスト
            time (float): ピッチの時間軸
        """

        notes = self._make_notes(f0_list, time)
        joined_notes = self._join_notes(notes)
        self._joined_notes_to_midi(joined_notes)


    def _make_notes(self, f0_list: np.ndarray, time: float) -> list:
        """ピッチのリストからノート番号のリストを作成するメソッド

        Args:
            f0_list (np.ndarray): ピッチのリスト
            time (float): ピッチの時間軸

        Returns:
            list: ノート番号のリスト
        """

        start_point = 0
        for s, f0 in enumerate(f0_list):
            if f0 != 0:
                start_point = s
                break

        FRAME = int((7.5 / self.bpm) * (1 / time))
        separated_f0_list = np.array_split(
            f0_list[start_point:],
            len(f0_list[start_point:]) // FRAME
        )

        notes = []
        for f0s in separated_f0_list:
            notes.append(self.__f0_to_note_number(np.mean(f0s)))
        
        return notes


    def __f0_to_note_number(self, f0: float) -> int:
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


    def _join_notes(self, notes: list) -> list:
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


    def _joined_notes_to_midi(self, joined_notes: list):
        """結合されたノート番号のリストをMIDIデータに変換するメソッド

        MIDIデータはMIDIファイルとして保存される

        Args:
            joined_notes (list): 結合されたノート番号の辞書型リスト{ノート番号, 長さ}
        """

        for note in joined_notes:
            if note["note"] != -1:
                self.track.append(Message(
                    "note_on",
                    note=note["note"],
                    velocity=self.velocity,
                    time=0
                ))
                self.track.append(Message(
                    "note_off",
                    note=note["note"],
                    velocity=self.velocity,
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
