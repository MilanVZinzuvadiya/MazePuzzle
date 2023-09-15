import pygame

# player class for creating player in game
class Player:
    CharacterSprites = {
            'princess': pygame.image.load('Images/characters/princess.png'),
            'boy': pygame.image.load('Images/characters/boy.png'),
            'pinkgirl': pygame.image.load('Images/characters/pinkgirl.png'),
            'catgirl': pygame.image.load('Images/characters/catgirl.png'),
            'horngirl': pygame.image.load('Images/characters/horngirl.png')
        }

    def __init__(self):
        print(Player.CharacterSprites.keys())
    