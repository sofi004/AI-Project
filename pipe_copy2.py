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
    def __init__(self, transformed=None):
        self.transformed = transformed
        self.rows = len(transformed)
        self.cols = len(transformed[0])
        self.total_bad_connections = 0

        for row in range(self.rows):
            for col in range(self.cols):
                self.total_bad_connections += self.verify_connections(row, col)
    
    def adjacent_vertical_values(self, row: int, col: int):
        if row-1 < 0 and row+1 > self.rows:
            return ([[0, 0, 0, 0], 0], [[0, 0, 0, 0], 0])
        if row-1 < 0:
            return ([[0, 0, 0, 0], 0], self.transformed[row+1][col])
        if row+1 >= self.rows:
            return (self.transformed[row-1][col], [[0, 0, 0, 0], 0])
        else:
            return (self.transformed[row-1][col], self.transformed[row+1][col])
    
    def adjacent_horizontal_values(self, row: int, col: int):
        if col-1 < 0 and col+1 > self.cols:
            return ([[0, 0, 0, 0], 0], [[0, 0, 0, 0], 0])
        if col-1 < 0:
            return ([[0, 0, 0, 0], 0], self.transformed[row][col+1])
        if col+1 >= self.cols:
            return (self.transformed[row][col-1], [[0, 0, 0, 0], 0])
        else:
            return (self.transformed[row][col-1], self.transformed[row][col+1])
        
    def verify_connections(self, row: int, col: int):
        bad_connections = 0

        vertical_values = self.adjacent_vertical_values(row, col)
        horizontal_values = self.adjacent_horizontal_values(row, col)
        block = self.transformed[row][col][0]

        if block[0] == 1 and block[0] != horizontal_values[0][0][2]:
            bad_connections += 1
        if block[1] == 1 and block[1] != vertical_values[0][0][3]:
            bad_connections += 1
        if block[2] == 1 and block[2] != horizontal_values[1][0][0]:
            bad_connections += 1
        if block[3] == 1 and block[3] != vertical_values[1][0][1]:
            bad_connections += 1
        
        self.transformed[row][col][1] = bad_connections
        
        return bad_connections
    
    @staticmethod
    def parse_instance():
        matrix = []
        transformed = []
        dict = {'FC': [[0, 1, 0, 0], 0, 4], 'FB': [[0, 0, 0, 1], 0, 4], 'FE': [[1, 0, 0, 0], 0, 4], 'FD': [[0, 0, 1, 0], 0, 4],
                'BC': [[1, 1, 1, 0], 0, 4], 'BB': [[1, 0, 1, 1], 0, 4], 'BE': [[1, 1, 0, 1], 0, 4], 'BD': [[0, 1, 1, 1], 0, 4],
                'VC': [[1, 1, 0, 0], 0, 4], 'VB': [[0, 0, 1, 1], 0, 4], 'VE': [[1, 0, 0, 1], 0, 4], 'VD': [[0, 1, 1, 0], 0, 4],
                'LH': [[1, 0, 1, 0], 0, 2], 'LV': [[0, 1, 0, 1], 0, 2]}
        rows = stdin.read().strip().split('\n')
        for row in rows:
            matrix.append(row.split())
        for x in range(len(matrix)):
            transformed_row = []
            for y in range(len(matrix[0])):
                transformed_row.append(dict.get(matrix[x][y]))
            transformed.append(transformed_row)


        return Board(transformed)

def main():
        board = Board.parse_instance()
        print("\nadjacent values:")
        print(board.adjacent_vertical_values(0, 0))
        print(board.adjacent_horizontal_values(0, 0))
        print(board.adjacent_vertical_values(1, 1))
        print(board.adjacent_horizontal_values(1, 1))
        problem = PipeMania(board)
        initial_state = PipeManiaState(board)
        print(initial_state.board.transformed[0][0])
        result_state = problem.result(initial_state, (0, 0, [0, 0, 1, 0], 4))
        print(result_state.board.transformed[0][0])
        result = depth_first_tree_search(problem)
        print(result.state.board.transformed)

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
        self.initial_sate = initial_state
        self.initial = PipeManiaState(initial_state)
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
                row_actions = []
                total_actions = 0 
                block = state.board.transformed[row][col]
                positions = [1, 1, 1, 1]
                vertical_values = state.board.adjacent_vertical_values(row, col)
                horizontal_values = state.board.adjacent_horizontal_values(row, col)
                block = state.board.transformed[row][col][0]
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
                        total_actions += 1
                        row_actions.append([row, col, block])

                for item in row_actions:
                    new_item = item[:]  
                    new_item.append(total_actions)  
                    actions.append(new_item)

        actions_sorted = sorted(actions, key=lambda item: item[3])
        index = 0
        while index < len(actions_sorted) and actions_sorted[index][3] == 1:

            if actions_sorted[index][2][0]:
                count = 0
                for item_action in actions_sorted:
                    if (item_action[0] == actions_sorted[index][0] and
                        item_action[1] == actions_sorted[index][1] -1 and
                        item_action[2][2] == 0):
                        count += 1
                        actions_sorted.remove(item_action)
                for item_action in actions_sorted:
                    if (item_action[0] == actions_sorted[index][0] and
                        item_action[1] == actions_sorted[index][1] -1):
                        item_action[3] -= count
            else:
                count = 0
                for item_action in actions_sorted:
                    if (item_action[0] == actions_sorted[index][0] and
                        item_action[1] == actions_sorted[index][1] -1 and
                        item_action[2][2] == 1):
                        count += 1
                        actions_sorted.remove(item_action)
                for item_action in actions_sorted:
                    if (item_action[0] == actions_sorted[index][0] and
                        item_action[1] == actions_sorted[index][1] -1):
                        item_action[3] -= count

            if actions_sorted[index][2][1]:
                count = 0
                for item_action in actions_sorted:
                    if (item_action[0] == actions_sorted[index][0] -1 and
                        item_action[1] == actions_sorted[index][1] and
                        item_action[2][3] == 0):
                        count += 1
                        actions_sorted.remove(item_action)
                for item_action in actions_sorted:
                    if (item_action[0] == actions_sorted[index][0] -1 and
                        item_action[1] == actions_sorted[index][1]):
                        item_action[3] -= count
            else:
                count = 0
                for item_action in actions_sorted:
                    if (item_action[0] == actions_sorted[index][0] -1 and
                        item_action[1] == actions_sorted[index][1] and
                        item_action[2][3] == 1):
                        count += 1
                        actions_sorted.remove(item_action)
                for item_action in actions_sorted:
                    if (item_action[0] == actions_sorted[index][0] -1 and
                        item_action[1] == actions_sorted[index][1]):
                        item_action[3] -= count

            if actions_sorted[index][2][2]:
                count = 0
                for item_action in actions_sorted:
                    if (item_action[0] == actions_sorted[index][0] and
                        item_action[1] == actions_sorted[index][1] +1 and
                        item_action[2][0] == 0):
                        count += 1
                        actions_sorted.remove(item_action)
                for item_action in actions_sorted:
                    if (item_action[0] == actions_sorted[index][0] and
                        item_action[1] == actions_sorted[index][1] +1):
                        item_action[3] -= count
            else:
                count = 0
                for item_action in actions_sorted:
                    if (item_action[0] == actions_sorted[index][0] and
                        item_action[1] == actions_sorted[index][1] +1 and
                        item_action[2][0] == 1):
                        count += 1
                        actions_sorted.remove(item_action)
                for item_action in actions_sorted:
                    if (item_action[0] == actions_sorted[index][0] and
                        item_action[1] == actions_sorted[index][1] +1):
                        item_action[3] -= count

            if actions_sorted[index][2][3]:
                count = 0
                for item_action in actions_sorted:
                    if (item_action[0] == actions_sorted[index][0] +1 and
                        item_action[1] == actions_sorted[index][1] and
                        item_action[2][1] == 0):
                        count += 1
                        actions_sorted.remove(item_action)
                for item_action in actions_sorted:
                    if (item_action[0] == actions_sorted[index][0] +1 and
                        item_action[1] == actions_sorted[index][1]):
                        item_action[3] -= count
            else:
                count = 0
                for item_action in actions_sorted:
                    if (item_action[0] == actions_sorted[index][0] +1 and
                        item_action[1] == actions_sorted[index][1] and
                        item_action[2][1] == 1):
                        count += 1
                        actions_sorted.remove(item_action)
                for item_action in actions_sorted:
                    if (item_action[0] == actions_sorted[index][0] +1 and
                        item_action[1] == actions_sorted[index][1]):
                        item_action[3] -= count

            old_actions = actions_sorted[:index+1]
            new_actions = actions_sorted[index+1:]
            new_actions_sorted = sorted(new_actions, key=lambda item: item[3])
            actions_sorted = old_actions + new_actions_sorted
            if(len(actions_sorted) == (state.board.rows * state.board.cols)):
                index = state.board.rows * state.board.cols
                break
            index += 1
        
        #actions_sorted = actions_sorted[index:]
        print("\n actions_sorted_final:\n", actions_sorted)
        print(len(actions_sorted))

        for row1 in range(state.board.rows): 
            for col1 in range(state.board.cols):
                for itemx in actions_sorted:
                    print("Board:", state.board.transformed[row1][col1][2])
                    print("Itemx:", itemx[2])
                    if itemx[2] == state.board.transformed[row1][col1][0] and itemx[0] == row1 and itemx[1] == col1:
                        actions_sorted.remove(itemx)
        return actions_sorted  

    def result(self, state: PipeManiaState, action: list):
        # Retorna o estado resultante de executar a 'action' sobre
        # 'state' passado como argumento. A ação a executar deve ser uma
        # das presentes na lista obtida pela execução de
        # self.actions(state).
        # TODO
        if (action in self.actions(state)):
            new_transformed = []
            for row in state.board.transformed:
                new_row = []
                for item in row:
                    new_row.append(item.copy())
                new_transformed.append(new_row)
            new_transformed[action[0]][action[1]][0] = action[2]
            new_board = Board(new_transformed)
            new_state = PipeManiaState(new_board)
            return new_state
        else:
            return state
    
    def goal_test(self, state):
        print("BAD CONECTIONS: ", state.board.total_bad_connections)
        return state.board.total_bad_connections == 0
    
    def h(self, node: Node):
        # Função heuristica utilizada para a procura A*.
        return node.state.board.total_bad_connections

if __name__ == "__main__":
    main()