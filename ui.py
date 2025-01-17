"""
 + ui.py - Handles all graphics for gameboard
"""
import pygame, random
import numpy as np

# Constants
WINDOW_SIZE = 600
GRID_SIZE = 5
CELL_SIZE = WINDOW_SIZE // GRID_SIZE
FPS = 30

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
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)  # Default font with size 36

    def draw_board(self, board): 
        '''
        Function: Draws out the board on new window
        Input: + board: Matrix of current state of board
        Return: None 
        '''
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
        '''
        Function: Gets mouse selections of candies and swaps them
        Input: + mouse_pos - Current position on board
               + game - object for game to reference board
        Return: None 
        '''

        row, col = mouse_pos[1] // CELL_SIZE, mouse_pos[0] // CELL_SIZE
        if self.selected:
            pos1 = self.selected
            pos2 = (row, col)
            self.selected = None # To handle clicking of two points
            
            dist = abs(np.subtract(pos1, pos2)) # Distance between both candies
            
            if np.sum(dist) == 1: #only cardinal direction no diagonal
                pygame.draw.circle(
                            self.screen,
                            (200,200,100),
                            (col * CELL_SIZE + CELL_SIZE // 2, row * CELL_SIZE + CELL_SIZE // 2),
                            CELL_SIZE // 3,
                            width = 5
                        )
                # Swap candies on board, if no matches found revert this swap
                swapped = game.swap_candies(pos1, pos2)
                
                if swapped: # Animate swap if match made
                    # Update variables to be in graphics metric system
                    candycolors = (CANDY_COLORS[game.board[pos2[0]][pos2[1]]], CANDY_COLORS[game.board[pos1[0]][pos1[1]]]) # Position of color swapped as actual swap already happened
                    pos1 = np.array((pos1[0] * CELL_SIZE + CELL_SIZE // 2, pos1[1] * CELL_SIZE + CELL_SIZE // 2))
                    pos2 = np.array((pos2[0] * CELL_SIZE + CELL_SIZE // 2, pos2[1] * CELL_SIZE + CELL_SIZE // 2))
                    dist = abs(np.subtract(pos1, pos2)) # Distance between both candies

                    self.animate_swap(pos1= pos1, pos2= pos2, candycolors = candycolors, dist = dist)

        else:
            self.selected = (row, col)
            pygame.draw.circle(
                        self.screen,
                        (250,250,250),
                        (col * CELL_SIZE + CELL_SIZE // 2, row * CELL_SIZE + CELL_SIZE // 2),
                        CELL_SIZE // 3,
                        width = 5
                    )
    
    def animate_swap(self, pos1, pos2, candycolors, dist):
        '''
        Function: Interpolate between two candies and animate swap
        Input: + board - Matrix of current state of board
               + pos1, pos2 - Positions of candies to swap
        Return: None 
        '''
        
        candy1_pos, candy1_color = pos1, candycolors[0] 
        candy2_pos, candy2_color = pos2, candycolors[1]

        if pos1[0] > pos2[0]: dist[0] = -dist[0] # Candy 1 is lower than 2 so dist to move is negative
        if pos1[1] > pos2[1]: dist[1] = -dist[1] # Candy 1 is right of 2 so dist to move is negative
        
        steps = 5 # Number of interpolation steps
        dx, dy = dist[0] / steps, dist[1] / steps #distance to increment
        
        for _ in range(steps): 
            # Remove previos iteration of candy
            pygame.draw.circle(
                        self.screen,
                        (0,0,0),
                        (candy1_pos[1], candy1_pos[0]),
                        CELL_SIZE // 3
                    )
            
            pygame.draw.circle(
                        self.screen,
                        (0,0,0),
                        (candy2_pos[1], candy2_pos[0]),
                        CELL_SIZE // 3
                    )
            
            # Iterate candy position
            candy1_pos[0] += dx
            candy1_pos[1] += dy

            candy2_pos[0] -= dx
            candy2_pos[1] -= dy

            # Draw new iteration of candy
            pygame.draw.circle(
                        self.screen,
                        candy1_color,
                        (candy1_pos[1], candy1_pos[0]),
                        CELL_SIZE // 3
                    )
            
            pygame.draw.circle(
                        self.screen,
                        candy2_color,
                        (candy2_pos[1], candy2_pos[0]),
                        CELL_SIZE // 3
                    )
            
            pygame.display.flip()
            self.clock.tick(FPS)

    def animate_removal(self, matches_to_remove, board):
        '''
        Function: Fade out matched candies
        Input: + board - Matrix of current state of board
               + matches_to_remove - List of matches to remove
        Return: None
        '''
        for _ in range(5):  # Number of fade steps
            for match in matches_to_remove:
                for row, col in match:
                    candy = board[row][col]
                    curr_color = CANDY_COLORS[candy] 
                    curr_color = tuple(c // 2 for c in curr_color)
                    pygame.draw.circle(
                        self.screen,
                        curr_color,
                        (col * CELL_SIZE + CELL_SIZE // 2, row * CELL_SIZE + CELL_SIZE // 2),
                        CELL_SIZE // 3
                    )
            pygame.display.flip()
            self.clock.tick(FPS)

    def draw_score(self, score):
        '''
        Function: Display score on screen
        Input: + score - Score
        Return: None
        '''
        score_text = f"Score: {score}"
        text_surface = self.font.render(score_text, True, (255, 255, 255)) 
        self.screen.blit(text_surface, (10, 10))  # Draw at top-left corner
        
