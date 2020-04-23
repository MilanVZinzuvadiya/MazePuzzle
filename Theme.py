import pygame
class Theme:
    WallGraphics = {
        'Rock'              : pygame.image.load('Images/Theme/Rock.png'),
        'TreeShort'         : pygame.image.load('Images/Theme/Tree_Short.png'),
        'TreeTall'          : pygame.image.load('Images/Theme/Tree_Tall.png'),
        'TreeUgly'          : pygame.image.load('Images/Theme/Tree_Ugly.png'),
        'WallBlockTall'     : pygame.image.load('Images/Theme/Wall_Block_Tall.png'),
        'WoodBlockTall'     : pygame.image.load('Images/Theme/Wood_Block_Tall.png')
    }

    PathGraphics = {
        'GrassBlock'    : pygame.image.load('Images/Theme/Grass_Block.png'),
        'PlainBlock'    : pygame.image.load('Images/Theme/Plain_Block.png')
    }

    Themes = [
        { '#':[WallGraphics['TreeShort'],WallGraphics['TreeTall'],WallGraphics['TreeUgly']] ,    ' ':[PathGraphics['GrassBlock']] },
        { '#':[WallGraphics['WallBlockTall']] , ' ':[PathGraphics['PlainBlock']] },
        { '#':[WallGraphics['WoodBlockTall']] , ' ':[PathGraphics['GrassBlock']] },
        { '#':[WallGraphics['WoodBlockTall'],WallGraphics['WallBlockTall']] , ' ':[PathGraphics['GrassBlock']] }
    ]