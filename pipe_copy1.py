# pipe.py: Template para implementação do projeto de Inteligência Artificial 2023/2024.

# Grupo 09:
# 106658 António Pinheiro Rodrigues Ortigão Delgado
# 106194 Sofia Dinis Pinto Piteira

import sys
from sys import stdin
from search import (
    Problem,
    Node,
    astar_search,
    breadth_first_tree_search,
    depth_first_tree_search,
    greedy_search,
    recursive_best_first_search,
)

class Board:
    def __init__(self, matrix=None, possible_matrix=None):
        self.matrix = matrix
        self.rows = len(matrix)
        self.cols = len(matrix[0])
        self.total_bad_connections = 0
        self.possible_matrix = possible_matrix

    def adjacent_vertical_values(self, row: int, col: int):
        if row-1 < 0 and row+1 > self.rows:
            return ([[0, 0, 0, 0], 0], [[0, 0, 0, 0], 0])
        if row-1 < 0:
            return ([[0, 0, 0, 0], 0], self.matrix[row+1][col])
        if row+1 >= self.rows:
            return (self.matrix[row-1][col], [[0, 0, 0, 0], 0])
        else:
            return (self.matrix[row-1][col], self.matrix[row+1][col])
    
    def adjacent_horizontal_values(self, row: int, col: int):
        if col-1 < 0 and col+1 > self.cols:
            return ([[0, 0, 0, 0], 0], [[0, 0, 0, 0], 0])
        if col-1 < 0:
            return ([[0, 0, 0, 0], 0], self.matrix[row][col+1])
        if col+1 >= self.cols:
            return (self.matrix[row][col-1], [[0, 0, 0, 0], 0])
        else:
            return (self.matrix[row][col-1], self.matrix[row][col+1])
    
    def final_matrix(self):
        final_string = ""
        dict = {(0, 1, 0, 0): 'FC', (0, 0, 0, 1): 'FB', (1, 0, 0, 0): 'FE', (0, 0, 1, 0): 'FD',
                (1, 1, 1, 0): 'BC', (1, 0, 1, 1): 'BB', (1, 1, 0, 1): 'BE', (0, 1, 1, 1): 'BD',
                (1, 1, 0, 0): 'VC', (0, 0, 1, 1): 'VB', (1, 0, 0, 1): 'VE', (0, 1, 1, 0): 'VD',
                (1, 0, 1, 0): 'LH', (0, 1, 0, 1): 'LV'}
        for x in range(self.rows):
            for y in range(self.cols):
                if y != self.cols - 1:
                    final_string += dict.get(tuple(self.matrix[x][y][0])) + "\t"
                elif y == self.cols - 1 and x != self.rows - 1:
                    final_string += dict.get(tuple(self.matrix[x][y][0])) + "\n"
                else:
                    final_string += dict.get(tuple(self.matrix[x][y][0]))
        return final_string
    
    @staticmethod
    def parse_instance():
        matrix = []
        dict = {'FC': [[0, 1, 0, 0], 4], 'FB': [[0, 0, 0, 1], 4], 'FE': [[1, 0, 0, 0], 4], 'FD': [[0, 0, 1, 0], 4],
                'BC': [[1, 1, 1, 0], 4], 'BB': [[1, 0, 1, 1], 4], 'BE': [[1, 1, 0, 1], 4], 'BD': [[0, 1, 1, 1], 4],
                'VC': [[1, 1, 0, 0], 4], 'VB': [[0, 0, 1, 1], 4], 'VE': [[1, 0, 0, 1], 4], 'VD': [[0, 1, 1, 0], 4],
                'LH': [[1, 0, 1, 0], 2], 'LV': [[0, 1, 0, 1], 2]}
        rows = stdin.read().strip().split('\n')
        for row in rows:
            matrix.append(row.split())
        for x in range(len(matrix)):
            for y in range(len(matrix[0])):
                matrix[x][y] = dict.get(matrix[x][y])
        return Board(matrix)
    

class PipeManiaState:
    state_id = 0
    def __init__(self, board):
        self.is_goal = 0
        self.board = board
        self.id = PipeManiaState.state_id
        PipeManiaState.state_id += 1

    def __lt__(self, other):
        # Este método é utilizado em caso de empate na gestão da lista
        # de abertos nas procuras informadas.
        return self.id < other.id


class PipeMania(Problem):
    def __init__(self, initial_state: Board): #goal_state: Board
        # O construtor especifica o estado inicial.
        self.initial_sate = initial_state
        self.initial = PipeManiaState(initial_state)
        #self.goal = goal_state
        # TODO
        pass
    
    def actions(self, state: PipeManiaState):
        # Retorna uma lista de ações que podem ser executadas a
        # partir do estado passado como argumento.
        # TODO
        if state.id == 1:
            for row in range(state.board.rows):
                for col in range(state.board.cols):
                    block_actions = []
                    positions = [1, 1, 1, 1]
                    vertical_values = state.board.adjacent_vertical_values(row, col)
                    horizontal_values = state.board.adjacent_horizontal_values(row, col)
                    block = state.board.matrix[row][col][0]
                    if vertical_values[0][0] == [0, 0, 0, 0]:
                        positions[1] = 0
                    if vertical_values[1][0] == [0, 0, 0, 0]:
                        positions[3] = 0
                    if horizontal_values[0][0] == [0, 0, 0, 0]:
                        positions[0] = 0
                    if horizontal_values[1][0] == [0, 0, 0, 0]:
                        positions[2] = 0
                    
                    if block == [0, 1, 0, 1] or block == [1, 0, 1, 0]:
                        x = 2
                    else:
                        x = 4

                    for _ in range(x):
                        possible_action = 1
                        block = block[-1:] + block[:-1]
                        for i in range(4):
                            if block[i] == 1 and positions[i] == 0:
                                possible_action = 0
                                break
                        if possible_action:
                            block_actions.append([row, col, block]) 

                    for item in block_actions:
                        item.append(len(block_actions))

                    state.board.possible_matrix[row][col] = block_actions
        else:

        

    def result(self, state: PipeManiaState, action: list):
        # Retorna o estado resultante de executar a 'action' sobre
        # 'state' passado como argumento. A ação a executar deve ser uma
        # das presentes na lista obtida pela execução de
        # self.actions(state).
        # TODO
        actions_list = self.actions(state)
        matrix = self.state.board.matrix
        possible_matrix = self.state.board.possible_matrix
        if (action in actions_list):
            new_matrix = []
            new_possible_matrix = []
            for row in range(state.board.rows):
                new_row = []
                new_possible_row = []
                for col in range(state.board.cols):
                    for item in possible_matrix[row][col]:
                        if item[0] != action[2]:
                            new_possible_item = []
                            new_possible_item.append(item[0].copy())
                            new_possible_item.append(item[1].copy())
                        new_possible_row.append(new_possible_item)
                    new_item = []
                    new_item.append(matrix[row][col][0].copy())
                    new_item.append(matrix[row][col][1].copy())
                    new_row.append(new_item)
                new_matrix.append(new_row)
                new_possible_matrix.append(new_row)
            new_matrix[action[0]][action[1]][0] = action[2]
            item = actions_list[0]
            itr = 0
            while item[3] != 0:
                new_matrix[actions_list[itr][0]][actions_list[itr][1]] = actions_list[itr][2]
                new_possible_matrix[actions_list[itr][0]][actions_list[itr][1]]
                itr += 1
            self.possible_actions = self.possible_actions[itr:]
            new_board = Board(new_matrix)
            new_state = PipeManiaState(new_board)
            return new_state
        else:
            return state
    
    def goal_test(self, state):
        if len(state.possible_actions):
            return True
        else:
            return False
    
    def h(self, node: Node):
        # Função heuristica utilizada para a procura A*.
        return len(node.state.possible_actions)
    
def main():
        board = Board.parse_instance()
        problem = PipeMania(board)
        result = astar_search(problem)
        print(result.state.board.final_matrix())

if __name__ == "__main__":
    main()