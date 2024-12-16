import scipy.io.wavfile as wav
import numpy as np
import pyworld as pw
import librosa as lr
from typing import Tuple

class WaveAnalyzer:
    """録音した音声データを解析するクラス

    録音した音声データを解析し、ピッチやBPMを取得する

    Attributes:
        wave_path (str): 解析する音声データのパス
    """

    def __init__(self, wave_path: str):
        """コンストラクタ

        Args:
            wave_path (str): 解析する音声データのパス
        """
        
        self.wave_path = wave_path

    def get_pitch(self) -> Tuple[np.ndarray, float]:
        """ピッチを取得するメソッド

        pyworldで、dioとstonemaskを使ってピッチを取得する

        Returns:
            Tuple[np.ndarray, float]: ピッチのリストと時間軸
        """
        
        fs, data = wav.read(self.wave_path)

        data = data.astype(np.float64)
        if data.ndim >= 2:
            data = np.mean(data, axis=1)
        
        _f0_list, timeaxis = pw.dio(data, fs)
        f0_list = pw.stonemask(data, _f0_list, timeaxis, fs)
        BIAS = 10
        f0_list += BIAS
        time = timeaxis[1] - timeaxis[0]

        return f0_list, time
    
    def get_bpm(self) -> float:
        """BPMを取得するメソッド

        librosaでビートトラッキングを行い、BPMを取得する

        Returns:
            float: BPM
        """
        
        data, fs = lr.load(self.wave_path)
        bpm, _ = lr.beat.beat_track(y=data, sr=fs)

        if type(bpm) == np.ndarray:
            return bpm[0]
        else:
            return bpm

if __name__ == "__main__":
    wa = WaveAnalyzer("resources/output.wav")
    print(wa.get_pitch())
    print(wa.get_bpm())