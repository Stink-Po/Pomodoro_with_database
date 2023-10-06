import pygame


class Sounds:
    def __init__(self):
        pygame.mixer.init()

    @staticmethod
    def study():
        pygame.mixer.music.load("sounds/study.mp3")
        pygame.mixer.music.play(loops=0,)

    @staticmethod
    def short_break():
        pygame.mixer.music.load("sounds/short.mp3")
        pygame.mixer.music.play(loops=0, )

    @staticmethod
    def long_break():
        pygame.mixer.music.load("sounds/long.mp3.mp3")
        pygame.mixer.music.play(loops=0, )
