import pygame
from Level import Level
from Player import Player
from Theme import Theme
from pygame.locals import *
import sys

#FONT and color collection 
class Screen:
    
    def __init__(self,displaySurf,winWidth,winHeight):
        self.DISPLAYSURF = displaySurf
        self.WINWIDTH = winWidth
        self.WINHEIGHT = winHeight
        self.goalStar = pygame.image.load('Images/Theme/Star.png')
         

    def starts(self):
        #first display logo for 2 sec(2000 miliseconds)
        self.fullScreenImageDisplay('Images/credit/logo.png',halt=2000)
    
    def runLevels(self):
        theme_no,playerSprite_no = self.Selection()
        theme_no,playerSprite_no = self.Selection(theme_no,playerSprite_no,False)

        self.level = Level("level/MazePuzzle.txt")
        no_levels = self.level.levelInfo()[1]
        for i in range(no_levels):
            self.runLevel(self.level.getCurLevelObj(),theme_no,playerSprite_no)
            self.level.gotoNextLevel()
        self.fullScreenImageDisplay('Images/credit/logo.png',halt=2000)

    def fullScreenImageDisplay(self,imagePath,halt=1500,BGCOLOR=(255,255,255)):
        self.DISPLAYSURF.fill(BGCOLOR)
        xImg1 = pygame.image.load(imagePath)
        xImg = xImg1.get_rect()
        xImg.centerx = int(self.WINWIDTH/2)
        xImg.centery = int(self.WINHEIGHT/2)
        self.DISPLAYSURF.blit(xImg1,xImg)
        pygame.display.update()
        pygame.time.wait(halt)

    def Selection(self,theme_no=0,playerSprite_no=0,themeSelect = True):
        themelevel = Level("level/themeLevel.txt")
        BGCOLOR = (0,170,255)
        self.DISPLAYSURF.fill(BGCOLOR)
        mapSurf = self.drawMap(themelevel.getCurLevelObj(),Theme.Themes[theme_no],list(Player.CharacterSprites.values())[playerSprite_no])

        Font = Theme.getTitleFont()

        if themeSelect:
            themeText = Font.render('Select Theme',1,(255,255,255))
        else:
            themeText = Font.render('Select Character',1,(255,255,255))
        themeTextRect = themeText.get_rect()
        themeTextRect.center = (self.WINWIDTH/2,90)
        self.DISPLAYSURF.blit(themeText,themeTextRect)

        mapSurfRect = mapSurf.get_rect()
        mapSurfRect.center = (self.WINWIDTH/2,self.WINHEIGHT/2)
        self.DISPLAYSURF.blit(mapSurf,mapSurfRect)

        pygame.display.update()
        
        while True:
            Move = None
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == KEYDOWN:
                    KeyPressed = True
                    if event.key == K_LEFT or event.key == K_DOWN:
                        if themeSelect:
                            theme_no = (theme_no + 1)%len(Theme.Themes)
                        playerSprite_no = (playerSprite_no + 1) % len(Player.CharacterSprites)
                    elif event.key == K_RIGHT or event.key == K_UP:
                        if themeSelect:
                            theme_no = (theme_no + 1)%len(Theme.Themes)
                        playerSprite_no = (playerSprite_no + 1) % len(Player.CharacterSprites)
                    elif event.key == K_ESCAPE:
                        pygame.quit()
                        sys.exit()
                    elif event.key == K_RETURN:
                        return theme_no,playerSprite_no
                    mapSurf = self.drawMap(themelevel.getCurLevelObj(),Theme.Themes[theme_no],list(Player.CharacterSprites.values())[playerSprite_no])
                    mapSurfRect = mapSurf.get_rect()
                    mapSurfRect.center = (self.WINWIDTH/2,self.WINHEIGHT/2)
                    self.DISPLAYSURF.blit(mapSurf,mapSurfRect)
                    pygame.display.update()




    def runLevel(self,levelObj,theme_no=0,playerSprite_no=0):
        levelDisplayFont = Theme.getInfoFont()
        selectedTheme,selectedPlayer = Theme.Themes[theme_no],list(Player.CharacterSprites.values())[playerSprite_no]
        
        level_no = self.level.levelInfo()
        MapRefresh = True
        LevelCompleted = False

        self.DISPLAYSURF.fill(Theme.Colors['LIGHTBLUE'])
        
        
        levelSurf = levelDisplayFont.render('Level %s of %s' % level_no, 1, Theme.Colors['BLACK'])
        levelRect = levelSurf.get_rect()
        levelRect.bottomleft = (20, self.WINHEIGHT - 35)
        self.DISPLAYSURF.blit(levelSurf,levelRect)

        mapSurf = self.drawMap(levelObj,selectedTheme,selectedPlayer)
        mapSurfRect = mapSurf.get_rect()
        mapSurfRect.center = (self.WINWIDTH/2,self.WINHEIGHT/2)
        self.DISPLAYSURF.blit(mapSurf,mapSurfRect)
        pygame.display.update()
        
        #main game loop for level
        while not LevelCompleted:
            Move = None
            KeyPressed = False
            
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == KEYDOWN:
                    KeyPressed = True
                    if event.key == K_LEFT:
                        Move = 'left'
                    elif event.key == K_RIGHT:
                        Move = 'right'
                    elif event.key == K_UP:
                        Move = 'up'
                    elif event.key == K_DOWN:
                        Move = 'down'
                    elif event.key == K_ESCAPE:
                        pygame.quit()
                        sys.exit()
            self.DISPLAYSURF.fill(Theme.Colors['LIGHTBLUE'])
            if Move != None and not LevelCompleted:
                moved,levelObj,LevelCompleted = self.level.makeMove(Move)
                if moved:
                    MapRefresh = True
                
            if MapRefresh:
                mapSurf = self.drawMap(levelObj,selectedTheme,selectedPlayer)
                MapRefresh = False
            
            levelSurf = levelDisplayFont.render('Level %s of %s' % level_no, 1, Theme.Colors['BLACK'])
            levelRect = levelSurf.get_rect()
            levelRect.bottomleft = (20, self.WINHEIGHT - 35)
            self.DISPLAYSURF.blit(levelSurf,levelRect)
            
            mapSurfRect = mapSurf.get_rect()
            mapSurfRect.center = (self.WINWIDTH/2,self.WINHEIGHT/2)
            self.DISPLAYSURF.blit(mapSurf,mapSurfRect)
            pygame.display.update()
            #FPSLOCK.tick()
    


    def drawMap(self,levelObj,theme,playerSprite):
        TILEWIDTH = 50
        TILEHEIGHT = 85
        TILEFLOORHEIGHT = 40
        BGCOLOR = (  0, 170, 255)

        mapSurfHeight = (len(levelObj['map'])-1) * TILEFLOORHEIGHT + TILEHEIGHT
        mapSurfWidth = len(levelObj['map'][0])*TILEWIDTH
        mapSurf = pygame.Surface((mapSurfWidth,mapSurfHeight))
        mapSurf.fill(BGCOLOR)

        k,l = 0,0

        # iterate through map and create graphics on mapSurf(MapSurface) 
        for i in range(len(levelObj['map'])):
            for j in range(len(levelObj['map'][0])):
                spriteRect = pygame.Rect((j*TILEWIDTH,i*TILEFLOORHEIGHT,TILEWIDTH,TILEHEIGHT))
                if levelObj['map'][i][j] == '#' :
                    baseTile = theme['#'][k]
                    k = (k+1)%len(theme['#'])
                else:
                    baseTile = theme[' '][l]
                    l = (l+1)%len(theme[' '])
                
                mapSurf.blit(baseTile,spriteRect)

                if (i,j) == levelObj['Start']:
                    mapSurf.blit(playerSprite, spriteRect)
                elif (i,j) == levelObj['Goal']:
                    mapSurf.blit(self.goalStar,spriteRect)
        return mapSurf