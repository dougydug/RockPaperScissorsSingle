import pygame


class card:
    def __init__(self, x, y, value, image, size):
        self.value = value
        self.card_size = size
        self.rect = pygame.Rect(x, y, size[0], size[1])
        self.image = pygame.transform.scale(image, size)
        self.back = pygame.transform.scale(pygame.image.load("Images/CARD_BACK.png"), size)
        self.is_shown = False

    def draw(self, screen):
        if self.is_shown:
            screen.blit(self.image, self.rect)
        else:
            screen.blit(self.back, self.rect)

    def move_to(self, location):
        self.rect = pygame.Rect(location[0], location[1], self.card_size[0], self.card_size[1])