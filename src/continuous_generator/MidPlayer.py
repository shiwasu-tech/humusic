import pygame
from pathlib import Path

#pygameによる再生

file_path = Path("generated_test10.mid")


def play_midi(file_path)->None:
    # Initialize pygame
    pygame.init()

    # Set up the mixer
    pygame.mixer.init()

    # Load the MIDI file
    pygame.mixer.music.load(file_path)

    # Play the MIDI file
    pygame.mixer.music.set_volume(0.25)
    pygame.mixer.music.play()


    # Keep the program running until the music stops
    while pygame.mixer.music.get_busy():
        if input("Press 'q' to quit: ") == 'q':
            break
        pygame.time.Clock().tick(10)

    # Quit pygame
    pygame.quit()
    
    return None

if __name__ == "__main__":
    play_midi(file_path)