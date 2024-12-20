# pygameのmixerモジュールを使ってwavファイルを再生
import pygame
import sys
sys.path.append("src/application")
from src.application.Getch import Getch

def play_audio(file_path: str):
    VOLUME = 1.0
    pygame.init()
    pygame.mixer.music.load(file_path)
    pygame.mixer.music.set_volume(VOLUME)
    pygame.mixer.music.play()

    getch = Getch()
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)

        if getch.getch_or_pass() == 'q':
            pygame.mixer.music.stop()
            break
    pygame.quit()

if __name__ == "__main__":
    play_audio("resources/generated/generated_best.mid")