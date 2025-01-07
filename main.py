"""
 + main.py - Main Runner file, Sets up game board and game loop, outputs game mechanics
"""

from board import GameBoard
from ui import BoardGraphics
import pygame, random, time

pygame.init()

FPS = 30
random.seed(0)
if __name__ == "__main__":
    game = GameBoard(5)
    graphics = BoardGraphics(5)
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                graphics.handle_click(pygame.mouse.get_pos(), game)
        
        matches = game.find_matches()
        graphics.animate_removal(matches, board= game.board)
        game.update_board(matches)
        graphics.draw_board(game.board)
        pygame.display.flip()
        graphics.clock.tick(FPS)

    pygame.quit()
