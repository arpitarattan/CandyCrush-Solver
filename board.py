import random
from collections import Counter

candy = ['r', 'b', 'g']
color_map = {
    'r': '\033[38;5;196m●\033[0m',  # Bright Red
    'b': '\033[38;5;21m●\033[0m',   # Bright Blue
    'g': '\033[38;5;46m●\033[0m',   # Bright Green
    'w': '\033[38;5;15m●\033[0m'    # White
}
directions = [(0,1),(1,0)] #check down and right while traversing

random.seed(1)

class CandyCrush:
    def __init__(self, size):
        self.size = size
        self.board = [[random.choice(candy) for _ in range(size)] for _ in range(size)]
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
                self.board[candy[0]][candy[1]] ='w'

def print_board(board):
    for row in board:
        print(" ".join(color_map[candy] for candy in row))

if __name__ == "__main__":
    game = CandyCrush(5)
    
    print_board(game.board)
    print('--------------')
    #lines = [f'{key} {value}' for key, value in game.adj_list.items()]
    #print('\n'.join(lines))
    
    matches = game.find_matches()
    game.update_board(matches)
    print_board(game.board)

    
