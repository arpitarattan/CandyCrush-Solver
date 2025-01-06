import random
from collections import Counter

candy_types = ['r', 'b', 'g', 'p', 'o']
color_map = {
    'r': '\033[38;5;196m●\033[0m',  # Bright Red
    'b': '\033[38;5;33m●\033[0m',   # Bright Blue
    'g': '\033[38;5;46m●\033[0m',   # Bright Green
    'w': '\033[38;5;15m●\033[0m',   # White
    'p': '\033[38;5;93m●\033[0m',   # Pink
    'o': '\033[38;5;214m●\033[0m'   # Orange

}
directions = [(0,1),(1,0)] #check down and right while traversing

random.seed(3)

class CandyCrush:
    def __init__(self, size):
        self.size = size # User defined size
        self.board = [[random.choice(candy_types) for _ in range(size)] for _ in range(size)]
        self.adj_list = self.build_graph() # Build adjacency list for candy matches

    def build_graph(self):
        '''
        Function: Creates a graph of board where connected candies of the same type form edges
        Input: self 
        Return: Adjacency list representing graph of Game Board
        '''
        adj_list = {}

        for row in range(self.size):
            for col in range(self.size):
                if (row, col) not in adj_list: # Add vertex if previously unseen
                    adj_list[(row, col)] = []

                # Check neighbors in down and right directions
                for dy, dx in directions:
                    ny, nx = row + dy, col + dx 
                    if ny < self.size and nx < self.size: 
                        if self.board[row][col] == self.board[ny][nx]: # If same type of candy -> create edge
                            adj_list[(row, col)].append((ny, nx))
                            if (ny, nx) not in adj_list: # Add vertex to list
                                adj_list[(ny, nx)] = []
                            adj_list[(ny, nx)].append((row, col)) #Bi-directional edge
        return adj_list

    def bfs(self, start):
        '''
        Function: Performs BFS to find all connected components starting from a node
        Input: Starting node
        Return: Path of connected components
        '''
        queue = [start] 
        visited = set()
        path = []

        while queue:
            node = queue.pop(0) # Dequeue
            if node not in visited:
                visited.add(node)
                path.append(node)
                # Add unvisited neighbors to the queue
                for neighbor in self.adj_list[node]:
                    if neighbor not in visited:
                        queue.append(neighbor)
        return path

    def find_matches(self):
        '''
        Function: Finds all valid matches (paths of 3+ candies)
        Input: self
        Return: All found matches as a large list, each sublist being a match consisting of coords of candies, e.g.:
                matches = [[(0,0), (0,1), (0,2)]]
        '''

        visited = set()
        paths = [] # Holds connected components
        matches = [] # Valid matches 

        # BFS on all unvisited nodes to find connected components
        for node in self.adj_list:
            if node not in visited:
                path = self.bfs(node, self.adj_list)
                for n in path:
                    visited.add(n) #Mark each node as visited

                if len(path) >= 3: #If valid path length
                    paths.append(path)
        
        # Filter matches into horizontal and vertical groups
        for path in paths: 
            sorted_by_x = sorted(path, key=lambda coord: coord[0])
            sorted_by_y = sorted(path, key=lambda coord: coord[1])
            
            #Check paths in x & y directions
            matches_x = self.filter_paths(sorted_by_x, 0) 
            matches_y = self.filter_paths(sorted_by_y, 1)

            if(len(matches_x)> 0):
                matches.append(matches_x)
            if(len(matches_y)> 0):
                matches.append(matches_y)
        
        return matches
    
    def filter_paths(self, path, coord = 0):
        '''
        Function: Filters connected paths into valid matches of 3+ candies.
        Input: - A sorted list of (x, y) coordinates representing a potential matching path.
               - The coordinate to compare for continuity: 0 -> x 1 -> y

        Return: A list of matched groups, where each group is a list of (x, y) coordinates forming a valid match.
        '''

        matches = []
        current_match = [path[0]] # Initialize by setting first candy in path

        # Iterate through the path to find sequences of consecutive candies, starting from second candy
        for i in range(1, len(path)):
            # Check if the current candy is aligned with the previous one along the specified axis and is adjacent on the other axis.
            if (path[i][coord] == path[i-1][coord]) and abs(path[i][~coord] - path[i-1][~coord]) == 1:
                current_match.append(path[i])

            # If the current match group ends and is valid, save it.
            else:
                if len(current_match) >= 3:
                    matches.append(current_match)
                current_match = [path[i]] # Start a new match group with the current candy.

        # Check if the last match group is valid and add it to the list of matches.
        if len(current_match) >= 3: 
            matches.append(current_match)
            
        return matches

    def update_board(self, matches):
        '''
        Function: Updates the game board in place by removing matched candies and generating new candies to fill the gaps.
        Input: matches - A list of matched groups, where each group is a list of (x, y) coordinates.
        Return: None
        '''

        # Step 1: Mark matched positions as empty by setting them to None
        for match in matches:
            for candy in match[0]:
                self.board[candy[0]][candy[1]] = None
        
        # Step 2: Fill the board column by column.
        for col in range(self.size):
            # Collect current column candies, find how many needed to fill, and generate those
            column_candies = [self.board[row][col] for row in range(self.size) if self.board[row][col] is not None]
            num_new_candies = self.size - len(column_candies)
            new_candies = [random.choice(candy_types) for _ in range(num_new_candies)]

            # Rebuild the column with new candies at the top and existing candies shifted down
            for row in range(self.size):
                if row < num_new_candies:
                    self.board[row][col] = new_candies[row]
                else:
                    self.board[row][col] = column_candies[row - num_new_candies]
    
    def swap_candies(self, pos1, pos2):
        '''
        Function: Swaps two candies on the board and checks for matches formed as a result.
        Input: + pos1: The coordinates (x1, y1) of the first candy to be swapped.
               + pos2: The coordinates (x1, y1) of the second candy to be swapped.
        Return: A list of (x, y) coordinates representing all matched candies formed due to the swap.
        '''
        
        # Step 1: Swap the two candies on the board. (Generate a new temporary board)
        board = self.board
        temp = self.board[pos2[0]][pos2[1]]
        board[pos2[0]][pos2[1]] = board[pos1[0]][pos1[1]]
        board[pos1[0]][pos1[1]] = temp

        # Step 2: Check for matches in all four cardinal directions around the new position of pos2.
        matches = []
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)] #left, right, down ,up
        
        for direction in directions:
            #Find match in current each direction
            match = self.check_match_in_direction(board, pos2, direction)
            if match:
                matches.extend(match)

        # Remove duplicates and sort
        matches = list(set(matches))
        matches.sort()

        return matches

    def check_match_in_direction(self, board, start, direction, length=3):
        '''
        Function: Checks for a sequence of candies of the same type in a specific direction from a given starting position.
        Input: + board - State of board at swap time
               + start - Starting position (x,y)
               + direction - Direction vector (dx, dy)
               + length - Length of desired match 
               
        Return: + match - Match found in specified direction
        '''

        x, y = start
        dx, dy = direction
        match = [(x, y)] # Initialize the match list with the starting position.
        candy_type = board[x][y]
        
        # Traverse in the specified direction to find matching candies.
        for i in range(1, length):
            new_x, new_y = x + (i * dx), y + (i * dy)

            # Check if the next position is within bounds and matches the candy type.
            if 0 <= new_x < len(board) and 0 <= new_y < len(board[0]):
                if board[new_x][new_y] == candy_type: # Nested as bound check first
                    match.append((new_x, new_y))
                else:
                    break
            else:
                break
        
        # Return only if match meets required length else return no match
        if len(match) >= length:
            return match
        return []

def print_board(board):
    for row in board:
        print(" ".join(color_map[candy] for candy in row))

if __name__ == "__main__":
    game = CandyCrush(8)
    
    while True:
        matches = game.find_matches()
        for i in range(5):
            print_board(game.board)
            print(matches)
            game.update_board(matches)
            matches = game.find_matches()

        print_board(game.board)
        pos1 = input('Position 1:')
        pos2 = input('Position 2:')
        #(3,2), (2,2)
        match = game.swap_candies(pos1, pos2)
        matches = game.find_matches()

        #while len(matches) != 0:
        #    game.update_board(matches)
        #    matches = game.find_matches()
        print('--------------')
        print_board(game.board)
        #print('--------------')
        #game.update_board([[match]])
        #print_board(game.board)
    
