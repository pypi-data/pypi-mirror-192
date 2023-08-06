import contextlib
with contextlib.redirect_stdout(None):
    import pygame

class Sound:
    def __init__(self, file: str, play_count: int=1, volume: float=1):
        pygame.init()
        pygame.mixer.set_num_channels(499)

        self.file = file
        self.volume = volume
        self.play_count = play_count
    
    def play(self):
        self.channel = pygame.mixer.find_channel()
        self.channel.set_volume(self.volume)
        self.channel.play(pygame.mixer.Sound(self.file), self.play_count)
    
    def stop(self):
        self.channel.pause()