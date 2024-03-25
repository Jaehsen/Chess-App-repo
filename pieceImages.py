import pygame
import os

# There is a better way to do this but for the sake of simplicity and time this current solution is sufficient enough

class PieceImages:
    def __init__(self,DEFAULT_IMAGE_SIZE:int,DEFAULT_SMALL_IMAGE_SIZE:int):
        self.BLACKPAWNIMAGE = pygame.transform.scale(pygame.image.load(os.path.join('images', 'black-bpawn.png')).convert_alpha(), DEFAULT_IMAGE_SIZE)
        self.BLACKROOKIMAGE = pygame.transform.scale(pygame.image.load(os.path.join('images', 'black-rook.png')).convert_alpha(), DEFAULT_IMAGE_SIZE)
        self.BLACKKNIGHTIMAGE = pygame.transform.scale(pygame.image.load(os.path.join('images', 'black-knight.png')).convert_alpha(), DEFAULT_IMAGE_SIZE)
        self.BLACKBISHOPIMAGE = pygame.transform.scale(pygame.image.load(os.path.join('images', 'black-bishop.png')).convert_alpha(), DEFAULT_IMAGE_SIZE)
        self.BLACKKINGIMAGE = pygame.transform.scale(pygame.image.load(os.path.join('images', 'black-king.png')).convert_alpha(), DEFAULT_IMAGE_SIZE)
        self.BLACKQUEENIMAGE = pygame.transform.scale(pygame.image.load(os.path.join('images', 'black-queen.png')).convert_alpha(), DEFAULT_IMAGE_SIZE)
        
        self.deadBLACKPAWNIMAGE = pygame.transform.scale(pygame.image.load(os.path.join('images', 'black-bpawn.png')).convert_alpha(), DEFAULT_SMALL_IMAGE_SIZE)
        self.deadBLACKROOKIMAGE = pygame.transform.scale(pygame.image.load(os.path.join('images', 'black-rook.png')).convert_alpha(), DEFAULT_SMALL_IMAGE_SIZE)
        self.deadBLACKKNIGHTIMAGE = pygame.transform.scale(pygame.image.load(os.path.join('images', 'black-knight.png')).convert_alpha(), DEFAULT_SMALL_IMAGE_SIZE)
        self.deadBLACKBISHOPIMAGE = pygame.transform.scale(pygame.image.load(os.path.join('images', 'black-bishop.png')).convert_alpha(), DEFAULT_SMALL_IMAGE_SIZE)
        self.deadBLACKQUEENIMAGE = pygame.transform.scale(pygame.image.load(os.path.join('images', 'black-queen.png')).convert_alpha(), DEFAULT_SMALL_IMAGE_SIZE)

        self.WHITEPAWNIMAGE = pygame.transform.scale(pygame.image.load(os.path.join('images', 'white-bpawn.png')).convert_alpha(), DEFAULT_IMAGE_SIZE)
        self.WHITEROOKIMAGE = pygame.transform.scale(pygame.image.load(os.path.join('images', 'white-rook.png')).convert_alpha(), DEFAULT_IMAGE_SIZE)
        self.WHITEKNIGHTIMAGE = pygame.transform.scale(pygame.image.load(os.path.join('images', 'white-knight.png')).convert_alpha(), DEFAULT_IMAGE_SIZE)
        self.WHITEBISHOPIMAGE = pygame.transform.scale(pygame.image.load(os.path.join('images', 'white-bishop.png')).convert_alpha(), DEFAULT_IMAGE_SIZE)
        self.WHITEKINGIMAGE = pygame.transform.scale(pygame.image.load(os.path.join('images', 'white-king.png')).convert_alpha(), DEFAULT_IMAGE_SIZE)
        self.WHITEQUEENIMAGE = pygame.transform.scale(pygame.image.load(os.path.join('images', 'white-queen.png')).convert_alpha(), DEFAULT_IMAGE_SIZE)
        
        self.deadWHITEPAWNIMAGE = pygame.transform.scale(pygame.image.load(os.path.join('images', 'white-bpawn.png')).convert_alpha(), DEFAULT_SMALL_IMAGE_SIZE)
        self.deadWHITEROOKIMAGE = pygame.transform.scale(pygame.image.load(os.path.join('images', 'white-rook.png')).convert_alpha(), DEFAULT_SMALL_IMAGE_SIZE)
        self.deadWHITEKNIGHTIMAGE = pygame.transform.scale(pygame.image.load(os.path.join('images', 'white-knight.png')).convert_alpha(), DEFAULT_SMALL_IMAGE_SIZE)
        self.deadWHITEBISHOPIMAGE = pygame.transform.scale(pygame.image.load(os.path.join('images', 'white-bishop.png')).convert_alpha(), DEFAULT_SMALL_IMAGE_SIZE)
        self.deadWHITEQUEENIMAGE = pygame.transform.scale(pygame.image.load(os.path.join('images', 'white-queen.png')).convert_alpha(), DEFAULT_SMALL_IMAGE_SIZE)

    def getImage(self, piece:str, small:bool=False) -> pygame.surface:
        """
        Get an image of a peice based off of it's respective string. 
        For example, 'q' will return a queen image. The small boolean will make the resulting image the small version.

        Args:
            piece (Str): a string for the chess piece.
            small (bool): determines if a piece is the small version.
        Returns:
            pygame.Surface: The image of a given chess piece. 

        """
        if small:
            if piece=="p":
                return self.deadBLACKPAWNIMAGE
            if piece=="n":
                return self.deadBLACKKNIGHTIMAGE
            if piece=="b":
                return self.deadBLACKBISHOPIMAGE
            if piece=="r":
                return self.deadBLACKROOKIMAGE
            if piece=="q":
                return self.deadBLACKQUEENIMAGE
            if piece=="P":
                return self.deadWHITEPAWNIMAGE
            if piece=="N":
                return self.deadWHITEKNIGHTIMAGE
            if piece=="B":
                return self.deadWHITEBISHOPIMAGE
            if piece=="R":
                return self.deadWHITEROOKIMAGE
            if piece=="Q":
                return self.deadWHITEQUEENIMAGE
            return pygame.surface.Surface((2,2))
        if piece=="p":
            return self.BLACKPAWNIMAGE
        if piece=="n":
            return self.BLACKKNIGHTIMAGE
        if piece=="b":
            return self.BLACKBISHOPIMAGE
        if piece=="r":
            return self.BLACKROOKIMAGE
        if piece=="q":
            return self.BLACKQUEENIMAGE
        if piece=="k":
            return self.BLACKKINGIMAGE
        if piece=="P":
            return self.WHITEPAWNIMAGE
        if piece=="N":
            return self.WHITEKNIGHTIMAGE
        if piece=="B":
            return self.WHITEBISHOPIMAGE
        if piece=="R":
            return self.WHITEROOKIMAGE
        if piece=="Q":
            return self.WHITEQUEENIMAGE
        if piece=="K":
            return self.WHITEKINGIMAGE
        return pygame.surface.Surface((4,4),flags=-1)
    