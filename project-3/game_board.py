import sys

import pygame as pg
from pygame.locals import *

from minimax_agent import Game

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
MAX_COLOR = (255, 136, 115, 88)
MIN_COLOR = (117, 190, 224, 88)
SELECTION_COLOR = (158, 255, 128, 88)

SCREEN_HEIGHT = 300
SCREEN_WIDTH = 300


def play_game(max_starts=True):
    pg.init()
    screen = pg.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
    pg.display.set_caption('Tic Tac Toe')

    char_font = pg.font.SysFont('msuigothic.ttf', 175)
    end_font = pg.font.SysFont('msuigothic.ttf', 50)

    boxes = {
        0: pg.Rect(2, 2, 96, 96),
        1: pg.Rect(102, 2, 96, 96),
        2: pg.Rect(202, 2, 96, 96),
        3: pg.Rect(2, 102, 96, 96),
        4: pg.Rect(102, 102, 96, 96),
        5: pg.Rect(202, 102, 96, 96),
        6: pg.Rect(2, 202, 96, 96),
        7: pg.Rect(102, 202, 96, 96),
        8: pg.Rect(202, 202, 96, 96),
    }

    move_list = {
        'X': [],
        'O': []
    }

    symbols = {
        'X': char_font.render('X', True, MAX_COLOR),
        'O': char_font.render('Y', True, MIN_COLOR)
    }

    print("\n####################")
    print("Use arrow keys to select a space.\nPress enter to commit your move.")
    print("####################")

    game = Game.new_game(max_starts=max_starts)
    location = 0

    while not game.has_ended:
        draw_board(screen, move_list, boxes, symbols, player_loc=location)
        max_turn(game, move_list)
        for event in pg.event.get():
            if event.type == KEYDOWN:
                key = event.key
                if key == K_UP:
                    if location > 2:
                        location -= 3
                elif key == K_DOWN:
                    if location < 6:
                        location += 3
                elif key == K_RIGHT:
                    if location not in [2, 5, 8]:
                        location += 1
                elif key == K_LEFT:
                    if location not in [0, 3, 6]:
                        location -= 1
                elif key == K_RETURN:
                    player_input(game, move_list, location)
            elif event.type == QUIT:
                pg.quit()
                sys.exit()
        pg.display.update()

    while True:
        draw_board(screen, move_list, boxes, symbols, player_loc=location)
        end_screen(screen, game, end_font)
        for event in pg.event.get():
            if event.type == QUIT or event.type == KEYDOWN:
                end_game_info(game)
                pg.quit()
                sys.exit()
        pg.display.update()


def draw_board(screen, move_list, boxes, symbols, player_loc):
    screen.fill(BLACK)
    draw_grid(screen)
    draw_moves(boxes, move_list, screen, symbols)
    draw_player(screen, player_loc, boxes)


def draw_grid(screen):
    for i in range(1, 3):
        pg.draw.line(screen, WHITE, (0, SCREEN_HEIGHT*i//3), (SCREEN_WIDTH, SCREEN_HEIGHT*i//3))
        pg.draw.line(screen, WHITE, (SCREEN_WIDTH*i//3, 0), (SCREEN_WIDTH*i//3, SCREEN_HEIGHT))


def draw_moves(boxes, move_list, screen, symbols):
    for sign, moves in move_list.items():
        for move in moves:
            screen.blit(symbols[sign], boxes[move])


def draw_player(screen, player_loc, boxes):
    pg.draw.rect(screen, SELECTION_COLOR, boxes[player_loc], width=2)


def max_turn(game, move_list):
    if game.max_turn:
        new_move = game.do_turn()
        move_list['X'].append(new_move)


def player_input(game, move_list, player_loc):
    if player_loc not in move_list['X'] and player_loc not in move_list['O']:
        game.turn_input(player_loc)
        move_list['O'].append(player_loc)


def end_screen(screen, game, font):
    message = "Draw!" if game.utility(game.state) == (False, 0) else f"{game.winner} wins!"
    message = font.render(message, True, BLACK, SELECTION_COLOR)
    message_center = message.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
    screen.blit(message, message_center)


def end_game_info(game):
    message = "Draw!" if game.utility(game.state) == (False, 0) else f"{game.winner} wins!"
    print("\n####################")
    print(message)
    print("####################")
