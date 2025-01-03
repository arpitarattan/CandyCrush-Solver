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

random.seed(1)

class CandyCrush:
    def __init__(self, size):
        self.size = size
        self.board = [[random.choice(candy_types) for _ in range(size)] for _ in range(size)]
        self.adj_list = self.build_graph()

    def build_graph(self):
        adj_list = {}

        for row in range(self.size):
            for col in range(self.size):
                if (row, col) not in adj_list: #add vertex
                    adj_list[(row, col)] = []
                for dy, dx in directions:
                    ny, nx = row + dy, col + dx 
                    if ny < self.size and nx < self.size:
                        if self.board[row][col] == self.board[ny][nx]:
                            adj_list[(row, col)].append((ny, nx))
                            if (ny, nx) not in adj_list:
                                adj_list[(ny, nx)] = []
                            adj_list[(ny, nx)].append((row, col))

        return adj_list

    def bfs(self, start, adj_list):
        queue = [start]
        visited = set()
        component = []

        while queue:
            node = queue.pop(0)
            if node not in visited:
                visited.add(node)
                component.append(node)
                for neighbor in adj_list[node]:
                    if neighbor not in visited:
                        queue.append(neighbor)
        return component

    def find_matches(self):
        visited = set()
        paths = []
        matches = []

        for node in self.adj_list:
            if node not in visited:
                component = self.bfs(node, self.adj_list)
                for n in component:
                    visited.add(n)
                if len(component) >= 3:
                    paths.append(component)
        
        for path in paths:
            sorted_by_x = sorted(path, key=lambda coord: coord[0])
            sorted_by_y = sorted(path, key=lambda coord: coord[1])
            
            matches_x = self.filter_paths(sorted_by_x, 0)
            matches_y = self.filter_paths(sorted_by_y, 1)

            if(len(matches_x)> 0):
                matches.append(matches_x)
            if(len(matches_y)> 0):
                matches.append(matches_y)
        
        return matches
    
    def filter_paths(self, path, coord = 0):
        matches = []
        current_match = [path[0]]
        for i in range(1, len(path)):
            if path[i][coord] == path[i-1][coord] and abs(path[i][~coord] - path[i-1][~coord]) == 1:
                current_match.append(path[i])
            else:
                if len(current_match) >= 3:
                    matches.append(current_match)
                current_match = [path[i]]
        if len(current_match) >= 3:
            matches.append(current_match)
        return matches

    def update_board(self, matches):
        for match in matches:
            for candy in match[0]:
                self.board[candy[0]][candy[1]] = None
        
        for col in range(self.size):
            column_candies = [self.board[row][col] for row in range(self.size) if self.board[row][col] is not None]
            num_new_candies = self.size - len(column_candies)
            new_candies = [random.choice(candy_types) for _ in range(num_new_candies)]
            for row in range(self.size):
                if row < num_new_candies:
                    self.board[row][col] = new_candies[row]
                else:
                    self.board[row][col] = column_candies[row - num_new_candies]
    
    def swap_candies(self, pos1, pos2):
        spots = []
        for i in range(-2, 3):
            for j in range(-2, 3):
                if i == 0 and j == 0:
                    continue  # Skip the center spot
                new_x, new_y = pos2[0] + i, pos2[1] + j
                if 0 <= new_x < self.size and 0 <= new_y < self.size:
                    spots.append((new_x, new_y))

        matches = []
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        board = self.board
        temp = self.board[pos2[0]][pos2[1]]
        board[pos2[0]][pos2[1]] = board[pos1[0]][pos1[1]]
        board[pos1[0]][pos1[1]] = temp

        for direction in directions:
            match = self.check_match_in_direction(board, pos2, direction)
            if match:
                matches.extend(match)

        # Remove duplicates and sort
        matches = list(set(matches))
        matches.sort()
        return matches


    def check_match_in_direction(self, board, start, direction, length=3):
        x, y = start
        dx, dy = direction
        match = [(x, y)]
        candy_type = board[x][y]
        
        for i in range(1, length):
            new_x, new_y = x + i*dx, y + i*dy
            if 0 <= new_x < len(board) and 0 <= new_y < len(board[0]):
                if board[new_x][new_y] == candy_type:
                    match.append((new_x, new_y))
                else:
                    break
            else:
                break

        if len(match) >= length:
            return match
        return []
    
def print_board(board):
    for row in board:
        print(" ".join(color_map[candy] for candy in row))

if __name__ == "__main__":
    game = CandyCrush(5)
    
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
    
