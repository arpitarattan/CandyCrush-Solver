"""
 + ui.py - Handles all graphics for gameboard
"""
import pygame
import random

# Constants
WINDOW_SIZE = 600
GRID_SIZE = 8
CELL_SIZE = WINDOW_SIZE // GRID_SIZE
FPS = 10

# Colors (replace these with candy images if available)
CANDY_COLORS = {
    'r': (255, 0, 0),   # Red
    'b': (0, 0, 255),   # Blue
    'g': (0, 255, 0),   # Green
    'p': (255, 0, 255), # Pink
    'o': (255, 165, 0)  # Orange
}

CANDY_TYPES = list(CANDY_COLORS.keys())

class BoardGraphics:
    def __init__(self, size):
        # Initialize screen
        self.screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
        pygame.display.set_caption("Candy Crush")

        self.size = size
        self.board = [[random.choice(CANDY_TYPES) for _ in range(size)] for _ in range(size)]
        self.selected = None  # Track selected candy
        self.matches_to_remove = []  # Track candies to remove
        self.clock = pygame.time.Clock()

    def draw_board(self, board): 
        self.screen.fill((0, 0, 0))  # Black background

        for row in range(self.size):
            for col in range(self.size):
                candy_type = board[row][col]
                if candy_type is not None:
                    color = CANDY_COLORS[candy_type]
                    pygame.draw.circle(
                        self.screen,
                        color,
                        (col * CELL_SIZE + CELL_SIZE // 2, row * CELL_SIZE + CELL_SIZE // 2),
                        CELL_SIZE // 3
                    )

    def handle_click(self, mouse_pos, game):
        row, col = mouse_pos[1] // CELL_SIZE, mouse_pos[0] // CELL_SIZE
        if self.selected:
            pos1 = self.selected
            pos2 = (row, col)
            self.selected = None # To handle clicking of two points
            
            # Swap candies on board, if no matches found revert this swap
            matches = game.swap_candies(pos1, pos2)


        else:
            self.selected = (row, col)

    def animate_removal(self):
        """Fade out matched candies."""
        for _ in range(5):  # Number of fade steps
            for match in self.matches_to_remove:
                for row, col in match:
                    pygame.draw.circle(
                        screen,
                        (0, 0, 0),
                        (col * CELL_SIZE + CELL_SIZE // 2, row * CELL_SIZE + CELL_SIZE // 2),
                        CELL_SIZE // 3
                    )
            pygame.display.flip()
            clock.tick(FPS)

# Main loop
def main():
    game = CandyCrush(GRID_SIZE)
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                game.handle_click(pygame.mouse.get_pos())

        if game.matches_to_remove:
            game.animate_removal()
            game.update_board()

        game.draw_board()
        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()

if __name__ == "__main__":
    main()
