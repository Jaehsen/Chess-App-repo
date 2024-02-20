import time
import math
import pygame

pygame.init()

main_surface:pygame.Surface=pygame.display.set_mode((1280,720)) # ,pygame.FULLSCREEN
pygame.display.set_caption("Chess GUI")

class GUIBoard:
    """
    A class which manages the checkerboard and all of the peices on the screen. It also handles all mouse clicks with this area.
    """

    xpos:int=0
    ypos:int=0
    width:int=0
    height:int=0
    selected:int=-1
    mouseClicked:float=0
    mouseClickX:int=0 #stores the initial position of the mouse click. used for clicking and dragging.
    mouseClickY:int=0 #stores the initial position of the mouse click. used for clicking and dragging.
    clickTime:float=0.25 #If the player holds the mouse down for a greater amount of time than clickTime, then it will be considered a click-and-drag. Else, it will be considered a normal click.

    def __init__(self,xpos:int,ypos:int,width:int,height:int):
        """
        Initiate the GUIBoard class, which manges the checkerboard, peices, and all mouse clicks in the board area.
        xpos: x position of the board on the screen in pixels.
        ypos: y position of the board on the screen in pixels.
        width: width of the board on the screen in pixels.
        height: height of the board on the screen in pixels.
        """

        if not(width>0 and height>0 and xpos>=0 and ypos>=0):
            print("failed to initiate board, incorrect parameters")
            return
        self.xpos=xpos
        self.ypos=ypos
        self.width=width
        self.height=height

    def render(self,surface:pygame.Surface) -> None:
        """
        Renders the chess board and its peices onto the given surface. This also handles all mouse events for the board.
        """

        lmb,mmb,rmb=pygame.mouse.get_pressed()
        mousex,mousey=pygame.mouse.get_pos()
        if self.mouseClicked==0 and lmb:
            self.mouseClicked=time.time()
            self.mouseClickX=mousex
            self.mouseClickY=mousey
            if mousex>self.xpos and mousex<self.xpos+self.width:
                if mousey>self.ypos and mousey<self.ypos+self.height:
                    self.selected=math.floor((mousex-self.xpos)/(self.width/8))+math.floor((mousey-self.ypos)/(self.height/8))*8
        elif time.time()-self.mouseClicked<self.clickTime and not(lmb): # user has clicked
            self.mouseClicked=0
        elif time.time()-self.mouseClicked>=self.clickTime and lmb: # user is clicking and dragging
            pass
        elif time.time()-self.mouseClicked>=self.clickTime and not(lmb): # user has stopped clicking and dragging
            self.mouseClicked=0
        for x in range(0,8):
            for y in range(0,8):
                if (x+y*8)==self.selected:
                    surface.fill((240,180,50),(math.floor(self.xpos+x*self.width/8),math.floor(self.ypos+y*self.height/8),math.ceil(self.width/8),math.ceil(self.height/8)))
                else:
                    surface.fill((50,50,50) if (x+y*8+y+1)%2==0 else (255,255,255),(math.floor(self.xpos+x*self.width/8),math.floor(self.ypos+y*self.height/8),math.ceil(self.width/8),math.ceil(self.height/8)))
        
    def resize(self,width:int,height:int) -> None:
        """
        Resize the chess board. Generally, the width and height should be the same values.
        width: the width in pixels that the chess board will be.
        height: the height in pixels that the chess board will be.
        """

        if not(width>0 and height>0):
            print("failed to resize board, incorrect parameters")
            return
        self.width=width
        self.height=height

#gameIcon=pygame.image.load("Assets/GameIcon2.ico")
#pygame.display.set_icon(gameIcon)

main_surface.fill((0,0,0))
pygame.display.flip()

board:GUIBoard=GUIBoard(10,20,500,500)
window_open:bool=True

while window_open:
    time.sleep(0.016)
    main_surface.fill((0,0,0))
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            window_open=False
    
    k=pygame.key.get_pressed()
    lmb,mmb,rmb=pygame.mouse.get_pressed()
    (x,y)=pygame.mouse.get_pos()

    board.render(main_surface)
    pygame.display.flip()

pygame.quit()
