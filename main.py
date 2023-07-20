import random
import pygame
import sys
from pygame.locals import *
from Card import card
pygame.font.init()

pygame.init()

clock = pygame.time.Clock()

WINDOW_SIZE = (500, 500)
screen = pygame.display.set_mode(WINDOW_SIZE, 0, 32)

paused = False

default_card_size = [100, 100]
default_play_area_size = [300, 100]
default_button_size = [100, 50]

player_hand_box = pygame.image.load("Images/hand_space.png")
player_hand_box = pygame.transform.scale(player_hand_box, default_play_area_size)
player_hand_location = [((screen.get_width() - player_hand_box.get_width()) / 2),
                        ((screen.get_height() - player_hand_box.get_height()) - 50)]
player_hand = pygame.Rect(player_hand_location[0], player_hand_location[1], 32, 32)

enemy_hand_box = pygame.image.load("Images/hand_space.png")
enemy_hand_box = pygame.transform.scale(enemy_hand_box, default_play_area_size)
enemy_hand_location = [((screen.get_width() - player_hand_box.get_width()) / 2), 20]
enemy_hand = pygame.Rect(enemy_hand_location[0], enemy_hand_location[1], 32, 32)

player_center = ((screen.get_width() - 100)/2 - 100, (screen.get_height() - default_card_size[1])/2)
comp_center = ((screen.get_width() + 100)/2, (screen.get_height() - default_card_size[1])/2)

card_list = ["paper", "rock", "scissors"]

images = [pygame.transform.scale(pygame.image.load("Images/paper.png"), default_card_size),
          pygame.transform.scale(pygame.image.load("Images/rock.png"), default_card_size),
          pygame.transform.scale(pygame.image.load("Images/scissors.png"), default_card_size)]


class Game:
    def __init__(self):
        self.deck = []
        self.numSci = 0
        self.numRock = 0
        self.numPap = 0
        self.textColor = [0, 0, 0]
        self.is_turn = False
        self.font = pygame.font.SysFont("comicsans", 16)
        self.button = pygame.Rect(screen.get_width()/2-50, screen.get_height()/2, default_button_size[0],
                                  default_button_size[1])
        self.button_images = [pygame.transform.scale(pygame.image.load('Images/LOST_BUTTON.png'), default_button_size),
                              pygame.transform.scale(pygame.image.load('Images/WIN_BUTTON.png'), default_button_size),
                              pygame.transform.scale(pygame.image.load('Images/TIE_BUTTON.png'), default_button_size)]
        self.cur_img = self.button_images[0]

    def make_deck(self):
        self.deck.clear()
        self.numPap = 0
        self.numRock = 0
        self.numSci = 0

        for x in range(50):
            self.deck.append(random.choice(card_list))
            self.change_card_nums(self.deck[x], 1)

    def draw(self):
        if len(self.deck):
            return self.deck.pop()

    def get_num_sci(self):
        return self.numSci

    def get_num_pap(self):
        return self.numPap

    def get_num_rock(self):
        return self.numRock

    def get_deck_size(self):
        return len(self.deck)

    def change_card_nums(self, cur_card, value):
        if cur_card == "paper":
            self.numPap += value
            return 0
        elif cur_card == "scissors":
            self.numSci += value
            return 0
        else:
            self.numRock += value
            return 0

    def play(self, controller, comp):
        if self.numRock == 0 or self.numPap == 0 or self.numSci == 0 or self.get_deck_size() <= 6:
            self.make_deck()

        if not self.is_turn:
            controller.turn(system, True)
            comp.turn(system, False)
            self.is_turn = True

    def compare(self, player_card, comp_card):
        if player_card == 'scissors':
            if comp_card == 'rock':
                self.human_lose()
            elif comp_card == 'paper':
                self.human_win()
            else:
                self.tie()

        if player_card == 'rock':
            if comp_card == 'paper':
                self.human_lose()
            elif comp_card == 'scissors':
                self.human_win()
            else:
                self.tie()

        if player_card == 'paper':
            if comp_card == 'scissors':
                self.human_lose()
            elif comp_card == 'rock':
                self.human_win()
            else:
                self.tie()

    def draw_side(self):
        screen.blit(pygame.font.Font.render(self.font, "Rock = " + str(self.numRock), False, self.textColor, None),
                    (screen.get_width() - 100, screen.get_height()/2 - 100))
        screen.blit(pygame.font.Font.render(self.font, "Scissors = " + str(self.numSci), False, self.textColor, None),
                    (screen.get_width() - 100, screen.get_height()/2))
        screen.blit(pygame.font.Font.render(self.font, "Paper = " + str(self.numPap), False, self.textColor, None),
                    (screen.get_width() - 100, screen.get_height()/2 + 100))

    def human_lose(self):
        self.cur_img = self.button_images[0]
        print('you lose')

    def human_win(self):
        self.cur_img = self.button_images[1]
        print('you win')

    def tie(self):
        self.cur_img = self.button_images[2]
        print('tie')

    def draw_button(self):
        if paused:
            screen.blit(self.cur_img, self.button)

    def resolve_click(self, position):
        if self.button.collidepoint(position):
            return True


class Player:
    def __init__(self, hand_location):
        self.hand = []
        self.hand_loc = hand_location

    def turn(self, game, shown):
        self.hand.clear()
        for x in range(3):
            value = game.draw()
            self.hand.append(card(self.hand_loc[0] + (default_card_size[0] * x), self.hand_loc[1],
                                  value, images[card_list.index(value)], default_card_size))
            self.hand[x].is_shown = shown

    def get_hand(self):
        return self.hand

    def display_hand(self):
        for x in self.hand:
            x.draw(screen)

    def resolve_click(self, position):
        for card_obj in self.hand:
            if card_obj.is_shown:
                if card_obj.rect.collidepoint(position):
                    card_obj.move_to(player_center)
                    return card_obj

    def make_selection(self):
        choice = random.choice(self.hand)
        choice.is_shown = True
        choice.move_to(comp_center)
        return choice

    def delete_hand(self, game):
        for x in range(3):
            game.change_card_nums(self.hand[x].value, -1)
        self.hand.clear()


system = Game()
system.make_deck()

player = Player(player_hand_location)
computer = Player(enemy_hand_location)

system.play(player, computer)


while True:
    screen.fill((250, 250, 250))
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()

            if not paused:
                selection = player.resolve_click(pos)
                if selection:
                    comp_selection = computer.make_selection()
                    system.compare(selection.value, comp_selection.value)
                    paused = True

            if paused:
                selection = system.resolve_click(pos)
                if selection:
                    player.delete_hand(system)
                    computer.delete_hand(system)
                    player.turn(system, True)
                    computer.turn(system, False)
                    paused = False

    system.play(player, computer)

    player.display_hand()
    computer.display_hand()
    system.draw_button()
    system.draw_side()

    pygame.display.flip()
    clock.tick(30)
