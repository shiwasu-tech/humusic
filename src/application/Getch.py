import sys
import os

_windows = os.name == 'nt'
if _windows:
    import msvcrt
else:
    import termios
    import select
    import tty


class Getch:
    """キーボード入力を取得するクラス

    入力がないときは空文字列を返す

    Note:
        WindowsとLinuxで挙動が多少異なる
        使用後は必ずdelを呼び出して設定を元に戻すこと
    """
    def __init__(self):
        """コンストラクタ"""
        self.__set_canonical_mode(False)

    def __del__(self):
        """デストラクタ"""
        self.__set_canonical_mode(True)


    def getch_or_pass(self) -> str:
        """キーボード入力を取得する

        入力がなくても即座に返す
        また、ノンブロッキングで入力を取得するため、入力がないときは空文字列を返す

        Returns:
            str: 入力された文字 (入力がないときは空文字列)
        """
        key = b''
        if _windows:
            if msvcrt.kbhit():
                key = msvcrt.getch()
            else:
                key = b''
            return key.decode('utf-8')
        else:
            rlist, _, _ = select.select([sys.stdin], [], [], 0.01)
            if rlist:
                key = sys.stdin.buffer.read(1)
            else:
                key = b''
            return key.decode()


    @staticmethod
    def __set_canonical_mode(enable: bool):
        """キャノニカルモードを設定する

        Windowsでは何もしない
        Unix系OSでは、キャノニカルモード (rawモード) を設定する
        rawモードでは、入力があるまで待たずに即座に入力を取得できる

        Args:
            enable (bool): キャノニカルモードを有効にするかどうか

        Raises:
            e: キャノニカルモードの設定に失敗したときの例外
        """
        if _windows:
            return
        else:
            fd = sys.stdin.fileno()
            old_settings = termios.tcgetattr(fd)
            try:
                if enable:
                    termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
                else:
                    tty.setraw(fd)
            except Exception as e:
                termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
                raise e
