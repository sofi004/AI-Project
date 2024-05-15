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
    def __init__(self, matrix=None):
        self.matrix = matrix
        self.rows = len(matrix)
        self.cols = len(matrix[0])
        self.total_bad_connections = 0

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
        self.possible_actions = []
        #self.goal = goal_state
        # TODO
        pass
    
    def actions(self, state: PipeManiaState):
        # Retorna uma lista de ações que podem ser executadas a
        # partir do estado passado como argumento.
        # TODO
        pass
        

    def result(self, state: PipeManiaState, action: list):
        # Retorna o estado resultante de executar a 'action' sobre
        # 'state' passado como argumento. A ação a executar deve ser uma
        # das presentes na lista obtida pela execução de
        # self.actions(state).
        # TODO
        self.actions(state)
        if (action in self.possible_actions):
            new_matrix = []
            for row in state.board.matrix:
                new_row = []
                for item in row:
                    new_row.append(item.copy())
                new_matrix.append(new_row)
            new_matrix[action[0]][action[1]][0] = action[2]
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