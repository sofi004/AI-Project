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

    def __init__(self, matrix=None, transformed=None, completed=None):
        self.matrix = matrix
        self.transformed = transformed
        self.completed = completed
        self.rows = len(matrix)
        self.cols = len(matrix[0])
    
    def adjacent_vertical_values(self, row: int, col: int):
        if row-1 < 0 and row+1 > self.rows:
            return ("None", "None")
        if row-1 < 0:
            return ("None", self.transformed[row+1][col])
        if row+1 >= self.rows:
            return (self.transformed[row-1][col], "None")
        else:
            return (self.transformed[row-1][col], self.transformed[row+1][col])
    
    def adjacent_horizontal_values(self, row: int, col: int):
        if col-1 < 0 and col+1 > self.cols:
            return ("None", "None")
        if col-1 < 0:
            return ("None", self.transformed[row][col+1])
        if col+1 >= self.cols:
            return (self.transformed[row][col-1], "None")
        else:
            return (self.transformed[row][col-1], self.transformed[row][col+1])
    
    def get_value(self, row, col):
        return self.transformed[row][col]
    
    @staticmethod
    def parse_instance():
        matrix = []
        transformed = []
        completed = []
        dict = {'FC': [0, 1, 0, 0], 'FB': [0, 0, 0, 1], 'FE': [1, 0, 0, 0], 'FD': [0, 0, 1, 0],
                'BC': [1, 1, 1, 0], 'BB': [1, 0, 1, 1], 'BE': [1, 1, 0, 1], 'BD': [0, 1, 1, 1],
                'VC': [1, 1, 0, 0], 'VB': [0, 0, 1, 1], 'VE': [1, 0, 0, 1], 'VD': [0, 1, 1, 0],
                'LH': [1, 0, 1, 0], 'LV': [0, 1, 0, 1]}
        rows = stdin.read().strip().split('\n')
        for row in rows:
            matrix.append(row.split())
        for x in range(len(matrix)):
            transformed_row = []
            completed_row = []
            for y in range(len(matrix[0])):
                transformed_row.append(dict.get(matrix[x][y]))
                completed_row.append([0])
            transformed.append(transformed_row)
            completed.append(completed_row)
        return Board(matrix, transformed, completed)

def main():
        board = Board.parse_instance()
        print("\nmatrix:")
        print(board.matrix[0][0], board.matrix[0][1], board.matrix[0][2])
        print(board.matrix[1][0], board.matrix[1][1], board.matrix[1][2])
        print(board.matrix[2][0], board.matrix[2][1], board.matrix[2][2])
        print("\nadjacent values:")
        print(board.adjacent_vertical_values(0, 0))
        print(board.adjacent_horizontal_values(0, 0))
        print(board.adjacent_vertical_values(1, 1))
        print(board.adjacent_horizontal_values(1, 1))
        problem = PipeMania(board)
        initial_state = PipeManiaState(board)
        print(initial_state.board.get_value(2,2))
        result_state = problem.result(initial_state, (2, 2, [0, 1, 0, 0]))
        print(result_state.board.get_value(2, 2))

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
        # > from sys import stdin1
        # > line = stdin.readline().split()
        # TODO
        pass

class PipeMania(Problem):
    def __init__(self, initial_state: Board): #goal_state: Board
        # O construtor especifica o estado inicial.
        self.initial = initial_state
        #self.goal = goal_state
        # TODO
        pass

    def actions(self, state: PipeManiaState):
        # Retorna uma lista de ações que podem ser executadas a
        # partir do estado passado como argumento.
        # TODO
        actions = []
        for row in range(state.board.rows):
            for col in range(state.board.cols):
                positions = [1, 1, 1, 1]
                vertical_values = state.board.adjacent_vertical_values(row, col)
                horizontal_values = state.board.adjacent_horizontal_values(row, col)
                if vertical_values[0] == "None":
                    positions[1] = 0
                if vertical_values[1] == "None":
                    positions[3] = 0
                if horizontal_values[0] == "None":
                    positions[0] = 0
                if horizontal_values[1] == "None":
                    positions[2] = 0
                
                block = state.board.transformed[row][col]
                if block == [0, 1, 0, 1] or block == [1, 0, 1, 0]:
                    x = 1
                else:
                    x = 3

                flag = 1
                for _ in range(x):
                    flag1 = 1
                    block = block[-1:] + block[:-1]
                    for i in range(4):
                        if block[i] == 1 and positions[i] == 0:
                            flag1 = 0
                            break
                    if flag1:
                        actions.append((row, col, block))
                        flag = 0
                if flag:
                    state.board.completed[row][col] = 1
                    print("completo", row, col)
        print(actions)
        return actions

    def result(self, state: PipeManiaState, action: list):
        # Retorna o estado resultante de executar a 'action' sobre
        # 'state' passado como argumento. A ação a executar deve ser uma
        # das presentes na lista obtida pela execução de
        # self.actions(state).
        # TODO
        if (action in self.actions(state)):
            new_state = PipeManiaState(state.board)
            new_state.board.transformed[action[0]][action[1]] = action[2]
            return new_state
        else:
            return state
    """
    def goal_test(self, state: PipeManiaState):
        if state.board.completed
        pass
    """
    def h(self, node: Node):
        # Função heuristica utilizada para a procura A*.
        # TODO
        pass

if __name__ == "__main__":
    main()