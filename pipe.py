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
    
    def adjacent_vertical_values(self, row: int, col: int):
        if row-1 < 0 and row+1 > self.rows:
            return ("None", "None")
        if row-1 < 0:
            return ("None", self.matrix[row+1][col])
        if row+1 > self.rows:
            return (self.matrix[row-1][col], "None")
        else:
            return (self.matrix[row-1][col], self.matrix[row+1][col])
    
    def adjacent_horizontal_values(self, row: int, col: int):
        if col-1 < 0 and col+1 > self.rows:
            return ("None", "None")
        if col-1 < 0:
            return ("None", self.matrix[row][col+1])
        if col+1 > self.rows:
            return (self.matrix[row][col-1], "None")
        else:
            return (self.matrix[row][col-1], self.matrix[row][col+1])
    
    def get_value(self, row, col):
        return self.matrix[row][col]
    
    @staticmethod
    def parse_instance():
        matrix = []
        rows = stdin.read().strip().split('\n')
        for row in rows:
            matrix.append(row.split())
        return Board(matrix)

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
        result_state = problem.result(initial_state, (2, 2, True))
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
        # > from sys import stdin
        # > line = stdin.readline().split()
        # TODO
        pass

class PipeMania(Problem):
    def __init__(self, initial_state: Board):
        # O construtor especifica o estado inicial.
        self.initial_state = initial_state

        # TODO
        pass

    def actions(self, state: PipeManiaState):
        # Retorna uma lista de ações que podem ser executadas a
        # partir do estado passado como argumento.
        # TODO

        pass

    def result(self, state: PipeManiaState, action: tuple):
        # Retorna o estado resultante de executar a 'action' sobre
        # 'state' passado como argumento. A ação a executar deve ser uma
        # das presentes na lista obtida pela execução de
        # self.actions(state).
        # TODO
        positions = "ECDB"
        block = state.board.get_value(action[0], action[1])
        index = positions.find(block[1])
        if(action[2]):
            if(index == 3):
                state.board.matrix[action[0]][action[1]] = block[0] + positions[0]
            else:
                state.board.matrix[action[0]][action[1]] = block[0] + positions[index + 1]
        else:
            if(index == 0):
                state.board.matrix[action[0]][action[1]] = block[0] + positions[3]
            else:
                state.board.matrix[action[0]][action[1]] = block[0] + positions[index - 1]
        return state
    
    def h(self, node: Node):
        # Função heuristica utilizada para a procura A*.
        # TODO
        pass

if __name__ == "__main__":
    main()