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
    def __init__(self, matrix=None, possible_matrix=None, only_way_actions=None):
        if matrix is None:
            matrix = []
        if possible_matrix is None:
            possible_matrix = []
        if only_way_actions is None:
            only_way_actions = []
        self.matrix = matrix
        self.rows = len(matrix)
        self.cols = len(matrix[0])
        self.only_way_actions = only_way_actions
        self.possible_matrix = possible_matrix

    def adjacent_vertical_values(self, row: int, col: int):
        if row-1 < 0 and row+1 > self.rows:
            return ([0, 0, 0, 0], [0, 0, 0, 0])
        if row-1 < 0:
            return ([0, 0, 0, 0], self.matrix[row+1][col])
        if row+1 >= self.rows:
            return (self.matrix[row-1][col], [0, 0, 0, 0])
        else:
            return (self.matrix[row-1][col], self.matrix[row+1][col])
    
    def adjacent_horizontal_values(self, row: int, col: int):
        if col-1 < 0 and col+1 > self.cols:
            return ([0, 0, 0, 0], [0, 0, 0, 0])
        if col-1 < 0:
            return ([0, 0, 0, 0], self.matrix[row][col+1])
        if col+1 >= self.cols:
            return (self.matrix[row][col-1], [0, 0, 0, 0])
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
                if(length == 1):
                    only_way_actions.append([row, col])
                    if(block_actions[0] == matrix[row][col]): 
                        length = 0
                new_block_actions = []
                new_block_actions.append(block_actions)
                new_block_actions.append(length)
                possible_matrix[row][col] = new_block_actions

        num_row_minus = (len(possible_matrix) - 1)
        index = 0
        while index < len(only_way_actions):
            x = only_way_actions[index][0]
            y = only_way_actions[index][1]
            if y > 0:
                if possible_matrix[x][y-1][1] != 0 and possible_matrix[x][y-1][1] != 1:
                    #print("entrou0")
                    not_removed = []
                    not_removed = copy.deepcopy(possible_matrix[x][y-1][0])
                    for item in possible_matrix[x][y-1][0]:
                        if possible_matrix[x][y][1] == 0:
                            perfect_block = matrix[x][y]
                        else:
                            perfect_block = possible_matrix[x][y][0][0]
                        if perfect_block[0] == 1:
                            if item[2] == 0:
                                #print("0:", item)
                                not_removed.remove(item)
                                continue
                        else:
                            if item[2] == 1:
                                #print("1:", item)
                                not_removed.remove(item)
                                continue
                    l = len(not_removed) 
                    if l == 1:
                        only_way_actions.append([x,y-1])
                        if(not_removed[0] == matrix[x][y-1]):
                            possible_matrix[x][y-1][1] = 0
                        else:
                            possible_matrix[x][y-1][1] = l
                    else:
                        possible_matrix[x][y-1][1] = l
                    possible_matrix[x][y-1][0] = not_removed
            if x > 0:
                if possible_matrix[x-1][y][1] != 0 and possible_matrix[x-1][y][1] != 1:
                    #print("entrou1")
                    not_removed = []
                    not_removed = copy.deepcopy(possible_matrix[x-1][y][0])
                    for item in possible_matrix[x-1][y][0]:
                        if possible_matrix[x][y][1] == 0:
                            perfect_block = matrix[x][y]
                        else:
                            perfect_block = possible_matrix[x][y][0][0]
                        if perfect_block[1] == 1:
                            if item[3] == 0:
                                #print("2:", item)
                                not_removed.remove(item)
                                continue
                        else:
                            if item[3] == 1:
                                #print("3:", item)
                                not_removed.remove(item)
                                continue
                    l = len(not_removed)
                    if l == 1:
                        only_way_actions.append([x-1,y])
                        if(not_removed[0] == matrix[x-1][y]):
                            possible_matrix[x-1][y][1] = 0
                        else:
                            possible_matrix[x-1][y][1] = l
                    else:
                        possible_matrix[x-1][y][1] = l
                    possible_matrix[x-1][y][0] = not_removed
            if y < (num_row_minus):
                if possible_matrix[x][y+1][1] != 0 and possible_matrix[x][y+1][1] != 1:
                    #print("entrou2")
                    not_removed = []
                    not_removed = copy.deepcopy(possible_matrix[x][y+1][0])
                    for item in possible_matrix[x][y+1][0]:
                        if possible_matrix[x][y][1] == 0:
                            perfect_block = matrix[x][y]
                        else:
                            perfect_block = possible_matrix[x][y][0][0]
                        if perfect_block[2] == 1:
                            if item[0] == 0:
                                #print("4:", item)
                                not_removed.remove(item)
                                continue
                        else:
                            if item[0] == 1:
                                #print("5:", item)
                                not_removed.remove(item)
                                continue
                    l = len(not_removed)
                    if l == 1:
                        only_way_actions.append([x,y+1])
                        if(not_removed[0] == matrix[x][y+1]):
                            possible_matrix[x][y+1][1] = 0
                        else:
                            possible_matrix[x][y+1][1] = l
                    else:
                        possible_matrix[x][y+1][1] = l
                    possible_matrix[x][y+1][0] = not_removed
            if x < (num_row_minus):
                if possible_matrix[x+1][y][1] != 0 and possible_matrix[x+1][y][1] != 1:
                    #print("entrou3")
                    not_removed = []
                    not_removed = copy.deepcopy(possible_matrix[x+1][y][0])
                    for item in possible_matrix[x+1][y][0]:
                        if possible_matrix[x][y][1] == 0:
                            perfect_block = matrix[x][y]
                        else:
                            perfect_block = possible_matrix[x][y][0][0]
                        if perfect_block[3] == 1:
                            if item[1] == 0:
                                #print("6:", item)
                                not_removed.remove(item)
                                #print("1", not_removed)
                                continue
                        else:
                            if item[1] == 1:
                                #print("7:", item)
                                not_removed.remove(item)
                                #print("2", not_removed)
                                continue
                    l = len(not_removed)
                    if l == 1:
                        only_way_actions.append([x+1,y])
                        if(not_removed[0] == matrix[x+1][y]):
                            possible_matrix[x+1][y][1] = 0
                        else:
                            possible_matrix[x+1][y][1] = l
                    else:
                        possible_matrix[x+1][y][1] = l
                    #print("p", possible_matrix[x+1][y][0])
                    #print("3", not_removed)
                    possible_matrix[x+1][y][0] = not_removed
            #print("only:", only_way_actions)
            index += 1
            #print("possible_matrix: ", possible_matrix)
        return Board(matrix, possible_matrix, only_way_actions)
    

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
        #print("actions id", state.id)
        num_row_minus = (len(state.board.possible_matrix) - 1)
        index = 0
        while index < len(state.board.only_way_actions):
            x = state.board.only_way_actions[index][0]
            y = state.board.only_way_actions[index][1]
            #print("only:", only_way_actions)
            if y > 0:
                if state.board.possible_matrix[x][y-1][1] != 0 and state.board.possible_matrix[x][y-1][1] != 1:
                    #print("entrou0")
                    not_removed = []
                    not_removed = copy.deepcopy(state.board.possible_matrix[x][y-1][0])
                    for item in state.board.possible_matrix[x][y-1][0]:
                        if state.board.possible_matrix[x][y][1] == 0:
                            perfect_block = state.board.matrix[x][y]
                        else:
                            perfect_block = state.board.possible_matrix[x][y][0][0]
                        if perfect_block[0] == 1:
                            if item[2] == 0:
                                #print("0:", item)
                                not_removed.remove(item)
                                continue
                        else:
                            if item[2] == 1:
                                #print("1:", item)
                                not_removed.remove(item)
                                continue
                    l = len(not_removed) 
                    if l == 1:
                        state.board.only_way_actions.append([x,y-1])
                        if(not_removed[0] == state.board.matrix[x][y-1]):
                            state.board.possible_matrix[x][y-1][1] = 0
                        else:
                            state.board.possible_matrix[x][y-1][1] = l
                    else:
                        state.board.possible_matrix[x][y-1][1] = l
                    state.board.possible_matrix[x][y-1][0] = not_removed
            if x > 0:
                if state.board.possible_matrix[x-1][y][1] != 0 and state.board.possible_matrix[x-1][y][1] != 1:
                    #print("entrou1")
                    not_removed = []
                    not_removed = copy.deepcopy(state.board.possible_matrix[x-1][y][0])
                    for item in state.board.possible_matrix[x-1][y][0]:
                        if state.board.possible_matrix[x][y][1] == 0:
                            perfect_block = state.board.matrix[x][y]
                        else:
                            perfect_block = state.board.possible_matrix[x][y][0][0]
                        if perfect_block[1] == 1:
                            if item[3] == 0:
                                #print("2:", item)
                                not_removed.remove(item)
                                continue
                        else:
                            if item[3] == 1:
                                #print("3:", item)
                                not_removed.remove(item)
                                continue
                    l = len(not_removed)
                    if l == 1:
                        state.board.only_way_actions.append([x-1,y])
                        if(not_removed[0] == state.board.matrix[x-1][y]):
                            state.board.possible_matrix[x-1][y][1] = 0
                        else:
                            state.board.possible_matrix[x-1][y][1] = l
                    else:
                        state.board.possible_matrix[x-1][y][1] = l
                    state.board.possible_matrix[x-1][y][0] = not_removed
            if y < (num_row_minus):
                if state.board.possible_matrix[x][y+1][1] != 0 and state.board.possible_matrix[x][y+1][1] != 1:
                    #print("entrou2")
                    not_removed = []
                    not_removed = copy.deepcopy(state.board.possible_matrix[x][y+1][0])
                    for item in state.board.possible_matrix[x][y+1][0]:
                        if state.board.possible_matrix[x][y][1] == 0:
                            perfect_block = state.board.matrix[x][y]
                        else:
                            perfect_block = state.board.possible_matrix[x][y][0][0]
                        if perfect_block[2] == 1:
                            if item[0] == 0:
                                #print("4:", item)
                                not_removed.remove(item)
                                continue
                        else:
                            if item[0] == 1:
                                #print("5:", item)
                                not_removed.remove(item)
                                continue
                    l = len(not_removed)
                    if l == 1:
                        state.board.only_way_actions.append([x,y+1])
                        if(not_removed[0] == state.board.matrix[x][y+1]):
                            state.board.possible_matrix[x][y+1][1] = 0
                        else:
                            state.board.possible_matrix[x][y+1][1] = l
                    else:
                        state.board.possible_matrix[x][y+1][1] = l
                    state.board.possible_matrix[x][y+1][0] = not_removed
            if x < (num_row_minus):
                if state.board.possible_matrix[x+1][y][1] != 0 and state.board.possible_matrix[x+1][y][1] != 1:
                    #print("entrou3")
                    not_removed = []
                    not_removed = copy.deepcopy(state.board.possible_matrix[x+1][y][0])
                    for item in state.board.possible_matrix[x+1][y][0]:
                        if state.board.possible_matrix[x][y][1] == 0:
                            perfect_block = state.board.matrix[x][y]
                        else:
                            perfect_block = state.board.possible_matrix[x][y][0][0]
                        if perfect_block[3] == 1:
                            if item[1] == 0:
                                #print("6:", item)
                                not_removed.remove(item)
                                #print("1", not_removed)
                                continue
                        else:
                            if item[1] == 1:
                                #print("7:", item)
                                not_removed.remove(item)
                                #print("2", not_removed)
                                continue
                    l = len(not_removed)
                    if l == 1:
                        state.board.only_way_actions.append([x+1,y])
                        if(not_removed[0] == state.board.matrix[x+1][y]):
                            state.board.possible_matrix[x+1][y][1] = 0
                        else:
                            state.board.possible_matrix[x+1][y][1] = l
                    else:
                        state.board.possible_matrix[x+1][y][1] = l
                    #print("p", possible_matrix[x+1][y][0])
                    #print("3", not_removed)
                    state.board.possible_matrix[x+1][y][0] = not_removed
            #print("only:", only_way_actions)
            index += 1
        action_list = []
        for row in range(state.board.rows):
            #print("row: ", row)
            col = 0
            for item in state.board.possible_matrix[row]:
                #print("col: ", col)
                #print("item: ", item)
                #print(item[0] != [])
                if (item[1] > 0):
                    for possible_action_block in item[0]:
                        #print(possible_action_block != state.board.matrix[row][col])
                        if (possible_action_block != state.board.matrix[row][col]):
                            #print("entrou")
                            new_item = [row, col, possible_action_block, item[1]]
                            action_list.append(new_item)
                col += 1
        action_list_sorted = sorted(action_list, key=lambda item: item[3])
        #print("possible_matrix actions ",state.board.possible_matrix)
        #print("action_list_sorted  ",action_list_sorted)
        return action_list_sorted

        

    def result(self, state: PipeManiaState, action: list):
        # Retorna o estado resultante de executar a 'action' sobre
        # 'state' passado como argumento. A ação a executar deve ser uma
        # das presentes na lista obtida pela execução de
        # self.actions(state).
        # TODO
        #print("result id", state.id)
        actions_list = self.actions(state)
        n_matrix = copy.deepcopy(state.board.matrix)
        n_possible_matrix = copy.deepcopy(state.board.possible_matrix)
        n_only_way_actions = copy.deepcopy(state.board.only_way_actions)
        n_only_way_actions = []
        n_matrix[action[0]][action[1]] = action[2]
        #print("action", action[0], action[1], action[2], action[3])
        n_possible_matrix[action[0]][action[1]][0].remove(action[2])
        n_possible_matrix[action[0]][action[1]][1] -= 1
        if n_possible_matrix[action[0]][action[1]][1] == 0:
            n_only_way_actions.append([action[0], action[1]])
        itr = 0
        while itr < len(actions_list) and actions_list[itr][3] == 1:
            if actions_list[itr][0] != action[0] and actions_list[itr][1] != action[1]:
                n_matrix[actions_list[itr][0]][actions_list[itr][1]] = actions_list[itr][2]
                n_possible_matrix[actions_list[itr][0]][actions_list[itr][1]] = [[], 0]
                n_only_way_actions.append([actions_list[itr][0], actions_list[itr][1]])
            itr += 1
        #print("remove", n_possible_matrix)
        new_board = Board(matrix=n_matrix, possible_matrix=n_possible_matrix, only_way_actions=n_only_way_actions)
        new_state = PipeManiaState(new_board)
        return new_state
    
    def goal_test(self, state):
        for row in range(state.board.rows):
            for col in range(state.board.rows):
                if state.board.possible_matrix[row][col][1] != 0:
                    return False
        return True
    
    def h(self, node: Node):
        # Função heuristica utilizada para a procura A*.
        count = 0
        for row in range(node.state.board.rows):
            for col in range(node.state.board.rows):
                count += node.state.board.possible_matrix[row][col][1]
        return count
    
def main():
        #start_time = time.time()
        board = Board.parse_instance()
        problem = PipeMania(board)
        result = greedy_search(problem)
        print(result.state.board.final_matrix())
        #print(time.time() - start_time)

if __name__ == "__main__":
    main()