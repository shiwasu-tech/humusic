# pygameのmixerモジュールを使ってwavファイルを再生
import pygame

def play_audio(file_path: str):
    VOLUME = 1.0
    pygame.init()
    pygame.mixer.music.load(file_path)
    pygame.mixer.music.set_volume(VOLUME)
    pygame.mixer.music.play()

    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)

    pygame.quit()

if __name__ == "__main__":
    play_audio("resources/generated/generated_best.mid")