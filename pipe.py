# pipe.py: Template para implementação do projeto de Inteligência Artificial 2023/2024.

# Grupo 09:
# 106658 António Pinheiro Rodrigues Ortigão Delgado
# 106194 Sofia Dinis Pinto Piteira

import sys
import copy
import time
from sys import stdin
from search import (
    Problem,
    Node,
    astar_search,
    breadth_first_tree_search,
    depth_first_tree_search,
    greedy_search,
    recursive_best_first_search,
    depth_first_graph_search,
)

class Board:
    def __init__(self, matrix=None, possible_matrix=None, correct_blocks=None):
        if matrix is None:
            matrix = []
        if possible_matrix is None:
            possible_matrix = []
        if correct_blocks is None:
            correct_blocks = 0
        self.matrix = matrix
        self.possible_matrix = possible_matrix
        self.correct_blocks = correct_blocks
        self.rows = len(matrix)
        self.cols = len(matrix[0])

        
    def no_clusters(self):
        start = (0,0)
        visited = set()
        visited.add((0, 0))
        queue = [start]
        while queue:
            (r, c) = queue.pop(0)
            if r > 0 and self.matrix[r][c][1] == 1 and self.matrix[r-1][c][3] == 1 and (r-1, c) not in visited:
                queue.append((r-1, c))
                visited.add((r-1, c))
            if r < self.rows - 1 and self.matrix[r][c][3] == 1 and self.matrix[r+1][c][1] == 1 and (r+1, c) not in visited:
                queue.append((r+1, c))
                visited.add((r+1, c))
            if c > 0 and self.matrix[r][c][0] == 1 and self.matrix[r][c-1][2] == 1 and (r, c-1) not in visited:
                queue.append((r, c-1))
                visited.add((r, c-1))
            if c < self.cols - 1 and self.matrix[r][c][2] == 1 and self.matrix[r][c+1][0] == 1 and (r, c+1) not in visited:
                queue.append((r, c+1))
                visited.add((r, c+1))
        return (len(visited) == (self.rows * self.rows))

    def final_matrix(self):
        final_string = ""
        dict = {(0, 1, 0, 0): 'FC', (0, 0, 0, 1): 'FB', (1, 0, 0, 0): 'FE', (0, 0, 1, 0): 'FD',
                (1, 1, 1, 0): 'BC', (1, 0, 1, 1): 'BB', (1, 1, 0, 1): 'BE', (0, 1, 1, 1): 'BD',
                (1, 1, 0, 0): 'VC', (0, 0, 1, 1): 'VB', (1, 0, 0, 1): 'VE', (0, 1, 1, 0): 'VD',
                (1, 0, 1, 0): 'LH', (0, 1, 0, 1): 'LV'}
        for x in range(self.rows):
            for y in range(self.cols):
                if y != self.cols - 1:
                    final_string += dict.get(tuple(self.matrix[x][y])) + "\t"
                elif y == self.cols - 1 and x != self.rows - 1:
                    final_string += dict.get(tuple(self.matrix[x][y])) + "\n"
                else:
                    final_string += dict.get(tuple(self.matrix[x][y]))
        return final_string

    @staticmethod
    def parse_instance():
        matrix = []
        possible_matrix = []
        dict = {'FC': [0, 1, 0, 0], 'FB': [0, 0, 0, 1], 'FE': [1, 0, 0, 0], 'FD': [0, 0, 1, 0],
                'BC': [1, 1, 1, 0], 'BB': [1, 0, 1, 1], 'BE': [1, 1, 0, 1], 'BD': [0, 1, 1, 1],
                'VC': [1, 1, 0, 0], 'VB': [0, 0, 1, 1], 'VE': [1, 0, 0, 1], 'VD': [0, 1, 1, 0],
                'LH': [1, 0, 1, 0], 'LV': [0, 1, 0, 1]}
        rows = stdin.read().strip().split('\n')
        for row in rows:
            matrix.append(row.split())
        num_rows = len(matrix)
        for x in range(num_rows):
            possible_matrix_row = []
            for y in range(num_rows):
                possible_matrix_row.append([])
                matrix[x][y] = dict.get(matrix[x][y])
            possible_matrix.append(possible_matrix_row)

        only_way_actions = []
        correct_blocks = 0
        bad_connections = 0
        for row in range(num_rows):
            for col in range(num_rows):
                block_actions = []
                positions = [1, 1, 1, 1]
                block = matrix[row][col]
                if row-1 < 0 and row+1 > num_rows:
                    vertical_values = [[0, 0, 0, 0], [0, 0, 0, 0]]
                elif row-1 < 0:
                    vertical_values = [[0, 0, 0, 0], matrix[row+1][col]]
                elif row+1 >= num_rows:
                    vertical_values = [matrix[row-1][col], [0, 0, 0, 0]]
                else:
                    vertical_values = [matrix[row-1][col], matrix[row+1][col]]

                if col-1 < 0 and col+1 > num_rows:
                    horizontal_values = [[0, 0, 0, 0], [0, 0, 0, 0]]
                elif col-1 < 0:
                    horizontal_values = [[0, 0, 0, 0], matrix[row][col+1]]
                elif col+1 >= num_rows:
                    horizontal_values = [matrix[row][col-1], [0, 0, 0, 0]]
                else:
                    horizontal_values = [matrix[row][col-1], matrix[row][col+1]]

                if vertical_values[0] == [0, 0, 0, 0]:
                    positions[1] = 0
                if vertical_values[1] == [0, 0, 0, 0]:
                    positions[3] = 0
                if horizontal_values[0] == [0, 0, 0, 0]:
                    positions[0] = 0
                if horizontal_values[1] == [0, 0, 0, 0]:
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
                        block_actions.append(block)

                length = len(block_actions)
                new_block_actions = []
                if(length == 1):
                    only_way_actions.append([row, col])
                    matrix[row][col] = block_actions[0]
                    correct_blocks += 1
                    new_block_actions = [[], 0]
                else:
                    new_block_actions.append(block_actions)
                    new_block_actions.append(length)
                possible_matrix[row][col] = new_block_actions


                block = matrix[row][col]
                if col != 0:
                    if block[0] == 1 and block[0] != matrix[row][col-1][2]:
                        bad_connections += 1
                if row != 0:
                    if block[1] == 1 and block[1] != matrix[row-1][col][3]:
                        bad_connections += 1
                if col != num_rows - 1:
                    if block[2] == 1 and block[2] != matrix[row][col+1][0]:
                        bad_connections += 1
                if row != num_rows - 1:
                    if block[3] == 1 and block[3] != matrix[row+1][col][1]:
                        bad_connections += 1

        num_row_minus = (len(possible_matrix) - 1)
        index = 0
        while index < len(only_way_actions):
            x = only_way_actions[index][0]
            y = only_way_actions[index][1]
            if y > 0:
                if possible_matrix[x][y-1][1] != 0 and possible_matrix[x][y-1][1] != 1:
                    not_removed = []
                    not_removed = copy.deepcopy(possible_matrix[x][y-1][0])
                    for item in possible_matrix[x][y-1][0]:
                        if matrix[x][y][0] == 1:
                            if item[2] == 0:
                                not_removed.remove(item)
                                continue
                        else:
                            if item[2] == 1:
                                not_removed.remove(item)
                                continue
                    l = len(not_removed) 
                    if l == 1:
                        only_way_actions.append([x,y-1])
                        matrix[x][y-1] = not_removed[0]
                        correct_blocks += 1
                        possible_matrix[x][y-1][1] = 0
                        possible_matrix[x][y-1][0] = []
                    else:
                        possible_matrix[x][y-1][1] = l
                        possible_matrix[x][y-1][0] = not_removed
            if x > 0:
                if possible_matrix[x-1][y][1] != 0 and possible_matrix[x-1][y][1] != 1:
                    not_removed = []
                    not_removed = copy.deepcopy(possible_matrix[x-1][y][0])
                    for item in possible_matrix[x-1][y][0]:
                        if matrix[x][y][1] == 1:
                            if item[3] == 0:
                                not_removed.remove(item)
                                continue
                        else:
                            if item[3] == 1:
                                not_removed.remove(item)
                                continue
                    l = len(not_removed)
                    if l == 1:
                        only_way_actions.append([x-1,y])
                        matrix[x-1][y] = not_removed[0]
                        correct_blocks += 1
                        possible_matrix[x-1][y][1] = 0
                        possible_matrix[x-1][y][0] = []
                    else:
                        possible_matrix[x-1][y][1] = l
                        possible_matrix[x-1][y][0] = not_removed
            if y < (num_row_minus):
                if possible_matrix[x][y+1][1] != 0 and possible_matrix[x][y+1][1] != 1:
                    not_removed = []
                    not_removed = copy.deepcopy(possible_matrix[x][y+1][0])
                    for item in possible_matrix[x][y+1][0]:
                        if matrix[x][y][2] == 1:
                            if item[0] == 0:
                                not_removed.remove(item)
                                continue
                        else:
                            if item[0] == 1:
                                not_removed.remove(item)
                                continue
                    l = len(not_removed)
                    if l == 1:
                        only_way_actions.append([x,y+1])
                        matrix[x][y+1] = not_removed[0]
                        correct_blocks += 1
                        possible_matrix[x][y+1][1] = 0
                        possible_matrix[x][y+1][0] = []
                    else:
                        possible_matrix[x][y+1][1] = l
                        possible_matrix[x][y+1][0] = not_removed
            if x < (num_row_minus):
                if possible_matrix[x+1][y][1] != 0 and possible_matrix[x+1][y][1] != 1:
                    not_removed = []
                    not_removed = copy.deepcopy(possible_matrix[x+1][y][0])
                    for item in possible_matrix[x+1][y][0]:
                        if matrix[x][y][3] == 1:
                            if item[1] == 0:
                                not_removed.remove(item)
                                continue
                        else:
                            if item[1] == 1:
                                not_removed.remove(item)
                                continue
                    l = len(not_removed)
                    if l == 1:
                        only_way_actions.append([x+1,y])
                        matrix[x+1][y] = not_removed[0]
                        correct_blocks += 1
                        possible_matrix[x+1][y][1] = 0
                        possible_matrix[x+1][y][0] = []
                    else:
                        possible_matrix[x+1][y][1] = l
                        possible_matrix[x+1][y][0] = not_removed
            index += 1

            if bad_connections == 0:
                correct_blocks = num_rows * num_rows

        return Board(matrix, possible_matrix, correct_blocks)


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

class PipeMania(Problem):
    def __init__(self, initial_state: Board):
        # O construtor especifica o estado inicial.
        self.initial_state = initial_state
        self.initial = PipeManiaState(initial_state)
        # TODO
        pass
    
    def actions(self, state: PipeManiaState):
        # Retorna uma lista de ações que podem ser executadas a
        # partir do estado passado como argumento.
        # TODO
        action_list = []
        branch = 0
        #print(state.id)
        for row in range(state.board.rows):        
            col = 0
            for item in state.board.possible_matrix[row]:
                if item[1] == -1:
                    return []
                if item[1] != 0:
                    for possible_action_block in item[0]:
                        branch += 1
                        new_item = [row, col, possible_action_block, item[1]]
                        action_list.append(new_item)
                        if branch == 6:
                            return action_list
                col += 1
        return action_list


    def result(self, state: PipeManiaState, action: list):
        # Retorna o estado resultante de executar a 'action' sobre
        # 'state' passado como argumento. A ação a executar deve ser uma
        # das presentes na lista obtida pela execução de
        # self.actions(state).
        # TODO
        n_correct_blocks = state.board.correct_blocks
        n_matrix = copy.deepcopy(state.board.matrix)
        n_possible_matrix = copy.deepcopy(state.board.possible_matrix)
        n_only_way_actions = []
        n_matrix[action[0]][action[1]] = action[2]
        n_correct_blocks += 1
        n_only_way_actions.append([action[0], action[1]])
        n_possible_matrix[action[0]][action[1]] = [[], 0]

        num_row_minus = (len(state.board.possible_matrix) - 1)
        index = 0
        while index < len(n_only_way_actions):
            x = n_only_way_actions[index][0]
            y = n_only_way_actions[index][1]
            if y > 0:
                if n_possible_matrix[x][y-1][1] != 0 and n_possible_matrix[x][y-1][1] != 1:
                    not_removed = []
                    not_removed = copy.deepcopy(n_possible_matrix[x][y-1][0])
                    for item in n_possible_matrix[x][y-1][0]:
                        if n_matrix[x][y][0] == 1:
                            if item[2] == 0:
                                not_removed.remove(item)
                                continue
                        else:
                            if item[2] == 1:
                                not_removed.remove(item)
                                continue
                    l = len(not_removed) 
                    if l == 1:
                        n_only_way_actions.append([x,y-1])
                        n_matrix[x][y-1] = not_removed[0]
                        n_correct_blocks += 1
                        n_possible_matrix[x][y-1] = [[], 0]
                    elif l == 0:
                        n_possible_matrix[x][y-1] = [[], -1]
                        break
                    else:
                        n_possible_matrix[x][y-1] = [not_removed, l]
            if x > 0:
                if n_possible_matrix[x-1][y][1] != 0 and n_possible_matrix[x-1][y][1] != 1:
                    not_removed = []
                    not_removed = copy.deepcopy(n_possible_matrix[x-1][y][0])
                    for item in n_possible_matrix[x-1][y][0]:
                        if n_matrix[x][y][1] == 1:
                            if item[3] == 0:
                                not_removed.remove(item)
                                continue
                        else:
                            if item[3] == 1:
                                not_removed.remove(item)
                                continue
                    l = len(not_removed)
                    if l == 1:
                        n_only_way_actions.append([x-1,y])
                        n_matrix[x-1][y] = not_removed[0]
                        n_correct_blocks += 1
                        n_possible_matrix[x-1][y] = [[], 0]
                    elif l == 0:
                        n_possible_matrix[x-1][y] = [[], -1]
                        break
                    else:
                        n_possible_matrix[x-1][y] = [not_removed, l]
            if y < (num_row_minus):
                if n_possible_matrix[x][y+1][1] != 0 and n_possible_matrix[x][y+1][1] != 1:
                    not_removed = []
                    not_removed = copy.deepcopy(n_possible_matrix[x][y+1][0])
                    for item in n_possible_matrix[x][y+1][0]:
                        if n_matrix[x][y][2] == 1:
                            if item[0] == 0:
                                not_removed.remove(item)
                                continue
                        else:
                            if item[0] == 1:
                                not_removed.remove(item)
                                continue
                    l = len(not_removed)
                    if l == 1:
                        n_only_way_actions.append([x,y+1])
                        n_matrix[x][y+1] = not_removed[0]
                        n_correct_blocks += 1
                        n_possible_matrix[x][y+1] = [[], 0]
                    elif l == 0:
                        n_possible_matrix[x][y+1] = [[], -1]
                        break
                    else:
                        n_possible_matrix[x][y+1] = [not_removed, l]
            if x < (num_row_minus):
                if n_possible_matrix[x+1][y][1] != 0 and n_possible_matrix[x+1][y][1] != 1:
                    not_removed = []
                    not_removed = copy.deepcopy(n_possible_matrix[x+1][y][0])
                    for item in n_possible_matrix[x+1][y][0]:
                        if n_matrix[x][y][3] == 1:
                            if item[1] == 0:
                                not_removed.remove(item)
                                continue
                        else:
                            if item[1] == 1:
                                not_removed.remove(item)
                                continue
                    l = len(not_removed)
                    if l == 1:
                        n_only_way_actions.append([x+1,y])
                        n_matrix[x+1][y] = not_removed[0]
                        n_correct_blocks += 1
                        n_possible_matrix[x+1][y] = [[], 0]
                    elif l == 0:
                        n_possible_matrix[x+1][y] = [[], -1]
                        break
                    else:
                        n_possible_matrix[x+1][y] = [not_removed, l]
            index += 1

        new_board = Board(matrix=n_matrix, possible_matrix=n_possible_matrix, correct_blocks=n_correct_blocks)
        new_state = PipeManiaState(new_board)
        return new_state

    def goal_test(self, state):
        if (state.board.correct_blocks == (state.board.rows * state.board.rows)):
            return state.board.no_clusters()
        return False
    
    def h(self, node: Node):
        # Função heuristica utilizada para a procura A*.
        return (node.state.board.rows * node.state.board.rows) - node.state.board.correct_blocks

def main():
        #start_time = time.time()
        board = Board.parse_instance()
        problem = PipeMania(board)
        result = depth_first_tree_search(problem)
        print(result.state.board.final_matrix())
        #print(time.time() - start_time)

if __name__ == "__main__":
    main()
