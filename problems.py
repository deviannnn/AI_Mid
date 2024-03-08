import os
import time

class PacmanProblem:

    PACMAN_SYMBOL = 'P'
    FOOD_SYMBOL = '.'
    WALL_SYMBOL = '%'

    def __init__(self):
        self.map = []
        self.pacman_pos = None
        self.target_pos = set()

    def __str__(self):
        return '\n'.join([''.join(row) for row in self.map])

    def load_map(self, filename):
        with open(filename, 'r') as file:
            self.map = [list(line.strip()) for line in file]

        self.get_pacman_position()
        self.get_corners()
        self.get_food_positions()

    def get_pacman_position(self):
        try:
            self.pacman_pos = next((i, j) for i, row in enumerate(self.map) for j, cell in enumerate(row) if cell == self.PACMAN_SYMBOL)
        except StopIteration:
            raise ValueError("Pacman position not found in the map.")

    def get_corners(self):
        corners = [(1, 1), (1, len(self.map[0]) - 2), (len(self.map) - 2, 1), (len(self.map) - 2, len(self.map[0]) - 2)]
        self.target_pos.update(corners)

    def get_food_positions(self):
        food_positions = [(i, j) for i, row in enumerate(self.map) for j, cell in enumerate(row) if cell == self.FOOD_SYMBOL]
        self.target_pos.update(food_positions)

    def get_successors(self, state):
        row, col = state
        successors = []

        def add_successor(action, next_row, next_col):
            if 0 <= next_row < len(self.map) and 0 <= next_col < len(self.map[0]) and self.map[next_row][next_col] != self.WALL_SYMBOL:
                successors.append((action, (next_row, next_col)))

        add_successor('N', row-1, col)
        add_successor('S', row+1, col)
        add_successor('W', row, col-1)
        add_successor('E', row, col+1)

        return successors

    '''def path_cost(self, cost):
        return cost+1'''

    def goal_test(self, state):
        return state in self.target_pos

    def let_go_pacman(self, actions: list) -> None:
        current_state = self.pacman_pos

        for action in actions:
            if action == 'Stop':
                break

            # Find next position based on action
            if action == 'N':
                new_state = (current_state[0] - 1, current_state[1])
            elif action == 'S':
                new_state = (current_state[0] + 1, current_state[1])
            elif action == 'W':
                new_state = (current_state[0], current_state[1] - 1)
            elif action == 'E':
                new_state = (current_state[0], current_state[1] + 1)
            else:
                raise ValueError(f"Invalid action: {action}")

            # Update current PACMAN's position
            self.map[current_state[0]][current_state[1]] = ' '
            self.map[new_state[0]][new_state[1]] = self.PACMAN_SYMBOL

            # Remove PACMAN's food
            if self.map[new_state[0]][new_state[1]] == self.FOOD_SYMBOL:
                self.map[new_state[0]][new_state[1]] = ' '

            # Update current state
            current_state = new_state

            # Show map
            os.system('cls' if os.name == 'nt' else 'clear')
            print(self)
            time.sleep(0.05)