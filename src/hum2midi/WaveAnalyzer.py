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
        method (str): 解析手法の指定
        
    """

    def __init__(self, wave_path: str, method: str = "harvest"):
        """コンストラクタ

        Args:
            wave_path (str): 解析する音声データのパス
            method (str): 解析手法の指定. "harvest"か"dio"を指定. Defaults to "harvest".
        """
        
        self.wave_path = wave_path
        self.method = method

    def get_pitch(self) -> Tuple[np.ndarray, float]:
        """ピッチを取得するメソッド

        音声データからピッチを取得する
        pyworldの、harvestかdioのどちらかの手法を指定する

        Returns:
            Tuple[np.ndarray, float]: ピッチのリストと時間軸の間隔

        Note:
            ステレオ音源の場合は、平均値を振幅としたモノラル音源に変換される
        """
        
        fs, data = wav.read(self.wave_path)
        data = data.astype(np.float64)
        if data.ndim >= 2:
            data = np.mean(data, axis=1)
        
        if self.method == "dio":
            _f0_list, timeaxis = pw.dio(data, fs)
            f0_list = pw.stonemask(data, _f0_list, timeaxis, fs)
        elif self.method == "harvest":
            f0_list, timeaxis = pw.harvest(data, fs)
        else:
            raise ValueError("method must be 'dio' or 'harvest'")

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