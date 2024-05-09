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

    def __init__(self, matrix=None, transformed=None, actions=None):
        self.matrix = matrix
        self.transformed = transformed
        self.actions = actions
        self.rows = len(matrix)
        self.cols = len(matrix[0])
    
    def adjacent_vertical_values(self, row: int, col: int):
        if row-1 < 0 and row+1 > self.rows:
            return ("None", "None")
        if row-1 < 0:
            return ("None", self.matrix[row+1][col])
        if row+1 >= self.rows:
            return (self.matrix[row-1][col], "None")
        else:
            return (self.matrix[row-1][col], self.matrix[row+1][col])
    
    def adjacent_horizontal_values(self, row: int, col: int):
        if col-1 < 0 and col+1 > self.cols:
            return ("None", "None")
        if col-1 < 0:
            return ("None", self.matrix[row][col+1])
        if col+1 >= self.cols:
            return (self.matrix[row][col-1], "None")
        else:
            return (self.matrix[row][col-1], self.matrix[row][col+1])
    
    def get_value(self, row, col):
        return self.matrix[row][col]
    
    def get_tuple(self, row, col):
        return self.transformed[row][col]
    
    def parse_instance():
        matrix = []
        transformed = []
        actions = []
        dict = {'FC': (0, 1, 0, 0), 'FB': (0, 0, 0, 1), 'FE': (1, 0, 0, 0), 'FD': (0, 0, 1, 0),
                'BC': (1, 1, 1, 0), 'BB': (1, 0, 1, 1), 'BE': (1, 1, 0, 1), 'BD': (0, 1, 1, 1),
                'VC': (1, 1, 0, 0), 'VB': (0, 0, 1, 1), 'VE': (1, 0, 0, 1), 'VD': (0, 1, 1, 0),
                'LH': (1, 0, 1, 0), 'LV': (0, 1, 0, 1)}
        form_dict = {'F':[[0, 1, 0, 0], [0, 0, 0, 1], [1, 0, 0, 0], [0, 0, 1, 0]],
                     'B':[[1, 1, 1, 0], [1, 0, 1, 1], [1, 1, 0, 1], [0, 1, 1, 1]],
                     'V':[[1, 1, 0, 0], [0, 0, 1, 1], [1, 0, 0, 1], [0, 1, 1, 0]],
                     'L':[[1, 0, 1, 0], [0, 1, 0, 1]]
                    }

        rows = stdin.read().strip().split('\n')
        for row in rows:
            matrix.append(row.split())
        for x in range(len(matrix)):
            transformed_row = []
            actions_row = []
            for y in range(len(matrix[0])):
                if matrix[x][y] in dict:
                    transformed_row.append(dict.get(matrix[x][y]))
                else:
                    transformed_row.append(matrix[x][y])
                if matrix[x][y][0] in form_dict:
                    actions_row.append(form_dict.get(matrix[x][y][0]))
                else:
                    transformed_row.append(matrix[x][y][0])
            transformed.append(transformed_row)
            actions.append(actions_row)
        return Board(matrix, transformed, actions)

class PipeManiaState:
    state_id = 0
    
    def __init__(self, board):
        self.board = board
        self.id = PipeManiaState.state_id
        PipeManiaState.state_id += 1

    def __lt__(self, other):
        # Este método é utilizado em caso de empate na gestão da lista
        # de abertos nas procuras informadas.
        return self.id < other.id

    @staticmethod
    def parse_instance():
        # Lê a instância do problema do standard input (stdin)
        # e retorna uma instância da classe Board.
        # Por exemplo:
        # $ python3 pipe_mania.py < input_T01
        # > from sys import stdin
        # > line = stdin.readline().split()
        # TODO
        pass

class PipeMania(Problem):
    def __init__(self, initial_state: Board):
        # O construtor especifica o estado inicial.
        self.initial = initial_state

        # TODO
        pass

    def actions(self, state: PipeManiaState):
        # Retorna uma lista de ações que podem ser executadas a
        # partir do estado passado como argumento.
        # TODO
        for row in range(state.board.rows):
            for col in range(state.board.cols):
                block = state.board.get_tuple(row, col)
                if state.board.horizontal_values[0] == "None":
                    for sublista in state.board.actions[row][col]:
                        if sublista[0] == 1:
                            state.board.actions[row][col].remove(sublista)
                if state.board.vertical_values[0] == "None":
                    for sublista in state.board.actions[row][col]:
                        if sublista[1] == 1:
                            state.board.actions[row][col].remove(sublista)
                if state.board.horizontal_values[1] == "None":
                    for sublista in state.board.actions[row][col]:
                        if sublista[2] == 1:
                            state.board.actions[row][col].remove(sublista)
                if state.board.vertical_values[1] == "None":
                    for sublista in state.board.actions[row][col]:
                        if sublista[3] == 1:
                            state.board.actions[row][col].remove(sublista)
        return state.board.actions

    def result(self, state: PipeManiaState, action: tuple):
        # Retorna o estado resultante de executar a 'action' sobre
        # 'state' passado como argumento. A ação a executar deve ser uma
        # das presentes na lista obtida pela execução de
        # self.actions(state).
        # TODO
        tuple_to_value = {(0, 1, 0, 0): 'FC', (0, 0, 0, 1): 'FB', (1, 0, 0, 0): 'FE', (0, 0, 1, 0): 'FD',
                          (1, 1, 1, 0): 'BC', (1, 0, 1, 1): 'BB', (1, 1, 0, 1): 'BE', (0, 1, 1, 1): 'BD',
                          (1, 1, 0, 0): 'VC', (0, 0, 1, 1): 'VB', (1, 0, 0, 1): 'VE', (0, 1, 1, 0): 'VD',
                          (1, 0, 1, 0): 'LH', (0, 1, 0, 1): 'LV'}
        if (action in self.actions(state)):
            new_state = PipeManiaState(state.board)
            new_state.board.matrix[action[0]][action[1]] = new_state.board.matrix[action[0]][action[1]][0] + action[2]
            return new_state
        else:
            return state
    
    def h(self, node: Node):
        # Função heuristica utilizada para a procura A*.
        # TODO
        pass

def main():
    board = Board.parse_instance()
    print("\nmatrix:")
    print(board.matrix[0][0], board.matrix[0][1], board.matrix[0][2])
    print(board.matrix[1][0], board.matrix[1][1], board.matrix[1][2])
    print(board.matrix[2][0], board.matrix[2][1], board.matrix[2][2])
    print("\ntransformed_matrix:\n")
    print(board.transformed[0][0], board.transformed[0][1], board.transformed[0][2])
    print(board.transformed[1][0], board.transformed[1][1], board.transformed[1][2])
    print(board.transformed[2][0], board.transformed[2][1], board.transformed[2][2])
    print("\nactions_matrix:\n")
    print(board.actions[0][0], board.actions[0][1], board.actions[0][2])
    print(board.actions[1][0], board.actions[1][1], board.actions[1][2])
    print(board.actions[2][0], board.actions[2][1], board.actions[2][2])
    print("\nadjacent values:")
    print(board.adjacent_vertical_values(0, 0))
    print(board.adjacent_horizontal_values(0, 0))
    print(board.adjacent_vertical_values(1, 1))
    print(board.adjacent_horizontal_values(1, 1))
    problem = PipeMania(board)
    initial_state = PipeManiaState(board)
    print(initial_state.board.get_value(2,2))
    result_state = problem.result(initial_state, (2, 2, "C"))
    print(result_state.board.get_value(2, 2))

    result = depth_first_tree_search(problem)
    print(result)

if __name__ == "__main__":
    main()