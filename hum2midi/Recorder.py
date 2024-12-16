import pyaudio as pa
import wave

class Recorder:
    """鼻歌を録音するクラス

    PyAudioオブジェクトで開いたstreamを使って録音を行う
    録音したlist型のデータをwavファイルとして保存する
    
    Attributes:
        channels (int): 録音する音声のチャンネル数
        fs (int): 録音する音声のサンプリング周波数
        chunk (int): 録音する音声のフレーム数
        format (int): 録音する音声のフォーマット
        record_sec (int): 録音する時間（秒）
        output_path (str): 録音した音声を保存するパス
    """

    def __init__(
            self,
            channels: int = 1,
            fs: int = 44100,
            chunk: int = 1024,
            format: int = pa.paInt16,
            record_sec: int = 5,
            output_path: str = "resources/output.wav"
    ):
        """コンストラクタ

        Args:
            channels (int, optional): チャンネル数. Defaults to 1.
            fs (int, optional): サンプリングレート. Defaults to 44100.
            chunk (int, optional): チャンクサイズ(一度に読み込むフレームの長さ). Defaults to 1024.
            format (int, optional): データのフォーマット. Defaults to pa.paInt16.
            record_sec (int, optional): 録音時間. Defaults to 5.
            output_path (str, optional): 録音データを保存するパス. Defaults to "resources/output.wav".
        """
        
        self.channels = channels
        self.fs = fs
        self.chunk = chunk
        self.format = format
        self.record_sec = record_sec
        self.output_path = output_path

    def record(self):
        """録音を行うメソッド
        
        PyAudioオブジェクトを生成し、streamを開いて録音を行う
        録音したデータをwavファイルとして保存する
        
        """

        frames = []
        p = pa.PyAudio()
        stream = p.open(
            format=self.format,
            channels=self.channels,
            rate=self.fs,
            frames_per_buffer=self.chunk,
            input=True
        )

        print("Recording...")
        for i in range(int(self.fs / self.chunk * self.record_sec)):
            data = stream.read(self.chunk)
            frames.append(data)
        print("Finished recording.")

        stream.stop_stream()
        stream.close()
        self.__save(p, frames)
        p.terminate()


    def __save(self, p: pa.PyAudio, frames: list):
        """録音したデータをwavファイルとして保存するメソッド

        Note:
            外部参照不可

        Args:
            p (pa.PyAudio): PyAudioオブジェクト
            frames (list): 録音したデータ
        """

        try:
            with wave.open(self.output_path, "wb") as wf:
                wf.setnchannels(self.channels)
                wf.setsampwidth(p.get_sample_size(self.format))
                wf.setframerate(self.fs)
                wf.writeframes(b"".join(frames))
                print(f"Saved as {self.output_path}")

        except FileNotFoundError as e:
            print(f"Error: {e}")
            print("Failed to save the file.")


if __name__ == "__main__":
    recorder = Recorder()
    recorder.record()