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

random.seed(11)

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
            match = self.filter_paths(sorted(path))
            print(sorted(path), match)
            if len(match) > 2:
                matches.append(match)
        
    
    def filter_paths(self, path):
        # Count occurrences of each row and column
        row_counts = Counter(x for x, y in path)
        col_counts = Counter(y for x, y in path)

        # Determine the most common row and column
        majority_row = row_counts.most_common(1)[0][0]
        majority_col = col_counts.most_common(1)[0][0]

        # Filter coordinates by majority row and column
        filtered_by_row = [coord for coord in path if coord[0] == majority_row]
        filtered_by_col = [coord for coord in path if coord[1] == majority_col]

        # Choose the larger group (in case of ties, row group is chosen)
        if len(filtered_by_row) >= len(filtered_by_col):
            return filtered_by_row
        else:
            return filtered_by_col

def print_board(board):
    for row in board:
        print(" ".join(color_map[candy] for candy in row))

if __name__ == "__main__":
    game = CandyCrush(5)
    
    print_board(game.board)
    print('--------------')
    #lines = [f'{key} {value}' for key, value in game.adj_list.items()]
    #print('\n'.join(lines))
    
    game.find_matches()

    
