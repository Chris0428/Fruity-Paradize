import pygame, sys

#Pygame setup
pygame.init()


#Button Code
class Button():
    def __init__(self, x, y, image, hvr_img):
        self.image = pygame.image.load(image).convert_alpha()
        self.hvr_img = pygame.image.load(hvr_img).convert_alpha()
        self.x = x
        self.y = y
        self.rect = self.image.get_rect(center=(self.x, self.y))

    def update(self, screen):
        screen.blit(self.image, self.rect)

    def checkForInput(self, position):
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
            return True
        return False
    
    def hover_button(self, position):
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
            self.image = self.hvr_img

        else:
            self.image = self.image

