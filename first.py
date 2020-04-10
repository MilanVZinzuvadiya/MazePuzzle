# -*- coding: utf-8 -*-
"""
Created on Thu Mar 26 02:03:49 2020

@author: mvzin
"""


import pygame,os,sys
from pygame.locals import *

WINWIDTH = 800
WINHEIGHT = 600
HALF_WINWIDTH = int(WINWIDTH / 2)
HALF_WINHEIGHT = int(WINHEIGHT / 2)

TILEWIDTH = 50
TILEHEIGHT = 85
TILEFLOORHEIGHT = 40

BRIGHTBLUE = (  0, 170, 255)
WHITE      = (255, 255, 255)
BGCOLOR = BRIGHTBLUE
TEXTCOLOR = WHITE

UP = 'up'
DOWN = 'down'
LEFT = 'left'
RIGHT = 'right'

def readlevels(filename):
    assert os.path.exists(filename), 'Cannot find the level file: %s' % (filename)
    mapFile = open(filename,'r')
    content = mapFile.readlines() + ['\r\n']
    mapFile.close()
    
    # dictionary of levels
    levels = {}
    #current processing Level in loop
    curLevel = 0
    #current level Map in list
    clevelMap = []
    
    for lineNum in range(len(content)):
        line = content[lineNum].rstrip('\r\n')
        if 'i' in line:
            pass
        elif len(line) > 0 :
            clevelMap.append(line)
        elif line == '' and len(clevelMap) > 0:
            levels[curLevel] = {}
            for i in range(len(clevelMap)):
                if 'S' in clevelMap[i]:
                    levels[curLevel]['Start'] = (i,clevelMap[i].index('S'))
                if 'G' in clevelMap[i]:
                    levels[curLevel]['Goal'] = (i,clevelMap[i].index('G'))
            
            # make all line with same length by adding space at end
            maxLen = len(max(clevelMap,key= lambda i: len(i)))
            print(maxLen)
            for i in range(len(clevelMap)):
                if len(clevelMap[i]) < maxLen :
                    clevelMap[i] += (maxLen-len(clevelMap[i])) *" "
            
            
            levels[curLevel]['map'] = clevelMap
            try:
                assert 'Start' in levels[curLevel].keys(), 'Cannot Find Start State for player in level %d' % (curLevel)
                assert 'Goal' in levels[curLevel].keys(), 'Cannot Find Goal State for player in level %d' % (curLevel)
            except AssertionError as error:
                print(error)
                levels[curLevel] = {}
            clevelMap = []
            curLevel += 1
    return levels

def GameExit():
    pygame.quit()
    sys.exit()


def runLevel(levelObj):
    global CurrentPLYRCharacter,PLAYERIMGS,DISPLAYSURF,FPSLOCK
    
    
    MapRefresh = True
    LevelCompleted = False
    
    DISPLAYSURF.fill(BGCOLOR)
    mapSurf = drawMap(levelObj)
    levelSurf = BASICFONT.render('Level %s of %s' % (0 + 1, 3), 1, TEXTCOLOR)
    levelRect = levelSurf.get_rect()
    levelRect.bottomleft = (20, WINHEIGHT - 35)
    mapSurfRect = mapSurf.get_rect()
    mapSurfRect.center = (HALF_WINWIDTH,HALF_WINHEIGHT)
    DISPLAYSURF.blit(mapSurf,mapSurfRect)
    pygame.display.update()
    
    #main game loop for level
    while True:
        Move = None
        KeyPressed = False
        
        for event in pygame.event.get():
            if event.type == QUIT:
                GameExit()
            elif event.type == KEYDOWN:
                KeyPressed = True
                if event.key == K_LEFT:
                    Move = LEFT
                elif event.key == K_RIGHT:
                    Move = RIGHT
                elif event.key == K_UP:
                    Move = UP
                elif event.key == K_DOWN:
                    Move = DOWN
                    
                elif event.key == K_ESCAPE:
                    GameExit()
                elif event.key == K_p:
                    CurrentPLYRCharacter = (CurrentPLYRCharacter+1)%len(PLAYERIMGS)
                    MapRefresh = True
        DISPLAYSURF.fill(BGCOLOR)
        if Move != None and not LevelCompleted:
            moved,levelObj = makemove(levelObj,Move)
            if moved:
                MapRefresh = True
            
        if MapRefresh:
            mapSurf = drawMap(levelObj)
            MapRefresh = False
        
        levelSurf = BASICFONT.render('Level %s of %s' % (0 + 1, 3), 1, TEXTCOLOR)
        levelRect = levelSurf.get_rect()
        levelRect.bottomleft = (20, WINHEIGHT - 35)
        
        mapSurfRect = mapSurf.get_rect()
        mapSurfRect.center = (HALF_WINWIDTH,HALF_WINHEIGHT)

        DISPLAYSURF.blit(mapSurf,mapSurfRect)
        pygame.display.update()
        FPSLOCK.tick()

def makemove(level,Move):
    #return True,level
    x,y = level['Start']
    if Move == LEFT:
        y -= 1
    elif Move == RIGHT:
        y += 1
    elif Move == UP:
        x -= 1
    else:
        x += 1
    
    if x < 0 or y < 0 or x >= len(level['map']) or y >= len(level['map'][0]):
        return False,level
    
    if level['map'][x][y] == 'G':
        level['map'][x][y] = ' '
    
    if level['map'][x][y] == ' ':
        level['Start'] = (x,y)
        return True,level
    
    return True,level


def drawMap(levelObj):
    mapSurfHeight = (len(levelObj['map'])-1) * TILEFLOORHEIGHT + TILEHEIGHT
    mapSurfWidth = len(levelObj['map'][0])*TILEWIDTH
    mapSurf = pygame.Surface((mapSurfWidth,mapSurfHeight))
    mapSurf.fill(BGCOLOR)

    # iterate through map and create graphics on mapSurf(MapSurface) 
    for i in range(len(levelObj['map'])):
        for j in range(len(levelObj['map'][0])):
            spriteRect = pygame.Rect((j*TILEWIDTH,i*TILEFLOORHEIGHT,TILEWIDTH,TILEHEIGHT))
            if levelObj['map'][i][j] in PATHMAPPING:
                baseTile = PATHMAPPING[levelObj['map'][i][j]]
            else:
                baseTile = PATHMAPPING[' ']
            
            mapSurf.blit(baseTile,spriteRect)

            if (i,j) == levelObj['Start']:
                mapSurf.blit(PLAYERIMGS[CurrentPLYRCharacter], spriteRect)
            elif (i,j) == levelObj['Goal']:
                mapSurf.blit(IMAGEDICT['goal'],spriteRect)
    return mapSurf

def main():
    global FPSLOCK, DISPLAYSURF, IMAGEDICT, BASICFONT,PATHMAPPING,PLAYERIMGS,CurrentPLYRCharacter
    
    pygame.init()
    FPSLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINWIDTH,WINHEIGHT))
    DISPLAYSURF.fill(BGCOLOR)
    BASICFONT =  pygame.font.Font('freesansbold.ttf',20)
    
    #loading images into imageArray
    IMAGEDICT = {'goal':pygame.image.load('Star.png'),
                 'floor':pygame.image.load('Plain_Block.png'),
                 'grass':pygame.image.load('Grass_Block.png'),
                 #characters
                 'princess': pygame.image.load('princess.png'),
                  'boy': pygame.image.load('boy.png'),
                  'catgirl': pygame.image.load('catgirl.png'),
                  'horngirl': pygame.image.load('horngirl.png'),
                  'pinkgirl': pygame.image.load('pinkgirl.png'),
                  #blocker
                  'rock': pygame.image.load('Rock.png'),
                  'short tree': pygame.image.load('Tree_Short.png'),
                  'tall tree': pygame.image.load('Tree_Tall.png'),
                  'ugly tree': pygame.image.load('Tree_Ugly.png'),
                  'wallBlock': pygame.image.load('Wall_Block_Tall.png'),
                  'woodBlock': pygame.image.load('Wood_Block_Tall.png'),
                 }
    
    PATHMAPPING = { ' ':IMAGEDICT['floor'],
                   '#':IMAGEDICT['wallBlock']
                }
    CurrentPLYRCharacter = 1
    PLAYERIMGS = [IMAGEDICT['princess'],
                    IMAGEDICT['boy'],
                    IMAGEDICT['catgirl'],
                    IMAGEDICT['horngirl'],
                    IMAGEDICT['pinkgirl']]
    
    #startScreen
    
    # extract levels from the level file
    levels = readlevels('mazepuzzle.txt')
    
    
    # run level 
    currentLevel = 0
    while True:
        result = runLevel(levels[currentLevel])
        
        if result == 'passed':
            currentLevel = (currentLevel + 1) % len(levels)
    
main()