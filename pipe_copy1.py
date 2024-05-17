# pipe.py: Template para implementação do projeto de Inteligência Artificial 2023/2024.

# Grupo 09:
# 106658 António Pinheiro Rodrigues Ortigão Delgado
# 106194 Sofia Dinis Pinto Piteira

import sys
import copy
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
    def __init__(self, matrix=None, possible_matrix=None, correct_blocks=None, only_way_actions=None):
        self.correct_blocks = correct_blocks
        self.only_way_actions = only_way_actions
        self.matrix = matrix
        self.rows = len(matrix)
        self.cols = len(matrix[0])
        self.total_bad_connections = 0
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

        ##################################################################
        correct_blocks = 0
        only_way_actions = []
        for row in range(num_rows):
            for col in range(num_rows):
                block_actions = []
                positions = [1, 1, 1, 1]
                block = matrix[row][col]
                if row-1 < 0 and row+1 > num_rows:
                    vertical_values = [[0, 0, 0, 0], [0, 0, 0, 0]]
                if row-1 < 0:
                    vertical_values = [[0, 0, 0, 0], matrix[row+1][col]]
                if row+1 >= num_rows:
                    vertical_values = [matrix[row-1][col], [0, 0, 0, 0]]
                else:
                    vertical_values = [matrix[row-1][col], matrix[row+1][col]]
                if col-1 < 0 and col+1 > num_rows:
                    horizontal_values = [[0, 0, 0, 0], [0, 0, 0, 0]]
                if col-1 < 0:
                    horizontal_values = [[0, 0, 0, 0], matrix[row][col+1]]
                if col+1 >= num_rows:
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

                lenght = len(block_actions)
                if(lenght == 1):
                    only_way_actions.append([row, col])
                    if(block_actions[0] == matrix[row][col]):
                        lenght = 0
                        correct_blocks += 1
                new_block_actions = []
                new_block_actions.append(block_actions)
                new_block_actions.append(lenght)
                possible_matrix[row][col] = []
                possible_matrix[row][col].append(new_block_actions)
        correct_blocks = correct_blocks

        # ATÉ AQUI ESTÁ TUDO CERTO SÓ NÃO PERCEBO PORQUE É QUE O ACTIONS É CORRIDO DUAS VEZES COM STATE.ID = 0 SECALHAR É SUPOSTO GUARDAR MOS A actions_list PARA APROVEITARMOS ESSA PRIMEIRA VEZ QUE CORRE O ACTIONS E DEPOIS SÓ CHAMAR O ACTIONS NO RESULT APÓS TROCAR O ESTADO ID?
        
        print("only_way_actions0: ", only_way_actions)
        print("possible_matrix0: ", possible_matrix)
        num_row_minus = (len(possible_matrix) - 1)
        index = 0
        while index < len(only_way_actions):
            x = only_way_actions[index][0]
            y = only_way_actions[index][1]
            if y > 0:
                if possible_matrix[x][y-1][0][1] != 0 or possible_matrix[x][y-1][0][1] != 1:
                    not_removed = []
                    for item in possible_matrix[x][y-1][0][0]:
                        not_removed = copy.deepcopy(possible_matrix[x][y-1][0][0])
                        if matrix[x][y][0] == 1:
                            if item[2] == 0:
                                not_removed.remove(item)
                                continue
                        else:
                            if item[2] == 1:
                                not_removed.remove(item)
                                continue
                    l = len(not_removed) 
                    if l == 1 and len(possible_matrix[x][y-1][0][0]) != 1:
                        only_way_actions.append([x,y-1])
                    possible_matrix[x][y-1][0][0] = not_removed
                    possible_matrix[x][y-1][0][1] = l
            if x > 0:
                if possible_matrix[x-1][y][0][1] != 0 or possible_matrix[x-1][y][0][1] != 1:
                    not_removed = []
                    for item in possible_matrix[x-1][y][0][0]:
                        not_removed = copy.deepcopy(possible_matrix[x-1][y][0][0])
                        if matrix[x][y][1] == 1:
                            if item[3] == 0:
                                not_removed.remove(item)
                                continue
                        else: 
                            if item[3] == 1:
                                not_removed.remove(item)
                                continue
                    l = len(not_removed)
                    if l == 1 and len(possible_matrix[x-1][y][0][0]) != 1:
                        only_way_actions.append([x-1,y])
                    possible_matrix[x][y-1][0][0] = not_removed
                    possible_matrix[x][y-1][0][1] = l
            if y < (num_row_minus):
                if possible_matrix[x][y+1][0][1] != 0 or possible_matrix[x][y+1][0][1] != 1:
                    not_removed = []
                    for item in possible_matrix[x][y+1][0][0]:
                        not_removed = copy.deepcopy(possible_matrix[x][y+1][0][0])
                        if matrix[x][y][2] == 1:
                            if item[0] == 0:
                                not_removed.remove(item)
                                continue
                        else:
                            if item[0] == 1:
                                not_removed.remove(item)
                                continue
                    l = len(not_removed)
                    if l == 1 and len(possible_matrix[x][y+1][0][0]) != 1:
                        only_way_actions.append([x,y+1])
                    possible_matrix[x][y-1][0][0] = not_removed
                    possible_matrix[x][y-1][0][1] = l
            if x < (num_row_minus):
                if possible_matrix[x+1][y][0][1] != 0 or possible_matrix[x+1][y][0][1] != 1:
                    not_removed = []
                    for item in possible_matrix[x+1][y][0][0]:
                        not_removed = copy.deepcopy(possible_matrix[x+1][y][0][0])
                        if matrix[x][y][3] == 1:
                            if item[1] == 0:
                                not_removed.remove(item)
                                continue
                        else:
                            if item[1] == 1:
                                not_removed.remove(item)
                                continue
                    l = len(not_removed)
                    if l == 1 and len(possible_matrix[x+1][y][0][0]) != 1:
                        only_way_actions.append([x+1,y])
                    possible_matrix[x][y-1][0][0] = not_removed
                    possible_matrix[x][y-1][0][1] = l
            index += 1
        return Board(matrix, possible_matrix, correct_blocks, only_way_actions)
    

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
    def __init__(self, initial_state: Board): #goal_state: Board
        # O construtor especifica o estado inicial.
        self.initial_state = initial_state
        self.initial = PipeManiaState(initial_state)
        #self.goal = goal_state
        # TODO
        pass
    
    def actions(self, state: PipeManiaState):
        # Retorna uma lista de ações que podem ser executadas a
        # partir do estado passado como argumento.
        # TODO
        print("state id actions: ", state.id)
        # O CÓDIGO ENTRE ESTE COMENTÁRIO E O ANTERIOR DEVE ESTAR BEM, CONTUDO AINDA NÃO ESTIVE A VER COM TOTAL ATENÇÃO SE O OBTIDO REALMENTE É O SUPOSTO, MAS PARECE-ME QUE SIM
        # FLATA RESTRINGIR PELA PEÇA QUE ANTERIORMENTE FOI TROCADA E VER OS SEUS VIZINHOS QUE CONSISTE EM CORRER O CÓDIGO A CIMA COM ONLY_WAY_ACTIONS SÓ COM A LINHA E COLUNA DA PÇA TROCADA ANTERIORMENTE, INICIALMENTE
        # NAO SEI SE É NECESSÁRIO MAS VER O CASO EM QUE MESMO QUE HAJA MAIS QUE UMA AÇÃO POSSIVEL PARA UM BLOCO, SE AS AÇÕES TIVEREM DIREÇÕES COMUNS EM TODAS AS AÇÕES POSSIVEIS PODEMOS RESTRINGIR AS SUAS VIZINHAS COM BASE NO SITIO PARA ONDE ESSA PEÇA APONTA OU NÃO APONTA
        # A PARTIR DAQUI E DENTRO DO ACTIONS ESTÁ TUDO BEM
        print("only_way_actions: ", state.board.only_way_actions)
        print("correct_blocks", state.board.correct_blocks)
        print("possible_matrix: ", state.board.possible_matrix)
        action_list = []
        for row in range(state.board.rows):
                for col in range(state.board.cols):
                    for item in state.board.possible_matrix[row][col]:
                        if item[0][-1] != state.board.matrix[row][col]:
                            for possible_action_block in item[0]:
                                new_item = [row, col, possible_action_block, item[1]]
                                action_list.append(new_item)
        print ("action_list: ", action_list)
        action_list_sorted = sorted(action_list, key=lambda item: item[3])
        print ("action_list_sorted: ", action_list_sorted)
        return action_list_sorted

        

    def result(self, state: PipeManiaState, action: list):
        # Retorna o estado resultante de executar a 'action' sobre
        # 'state' passado como argumento. A ação a executar deve ser uma
        # das presentes na lista obtida pela execução de
        # self.actions(state).
        # TODO
        print("result id: ", state.id)
        actions_list = self.actions(state)
        if (action in actions_list):
            matrix = copy.deepcopy(state.board.matrix)
            possible_matrix = copy.deepcopy(state.board.possible_matrix)
            matrix[action[0]][action[1]][0] = action[2]
            possible_matrix[action[0]][action[1]][0][0].remove(action[2])
            possible_matrix[action[0]][action[1]][0][1] -= 1
            correct_blocks = copy.deepcopy(state.correct_blocks)
            only_way_actions = copy.deepcopy(state.only_way_actions)
            if (action[3] == 1):
                correct_blocks += 1 
                only_way_actions.append([action[0], action[1]])
            new_board = Board(matrix, possible_matrix)
            new_state = PipeManiaState(new_board)
            print("new_state.id: ", new_state.id)
            new_state.correct_blocks = correct_blocks
            new_state.only_way_actions = only_way_actions
            return new_state
        else:
            return state
        
            # importantissimo implementar bem o while que está no código abaixo e ao mesmo tempo que fazemos o while ir atualizando o correct_blocks, para a heuristica e o test_goal funcionarem, enquanto isto não estiver feito é normal dar ciclo infinito
            # OLHAR PARA O CÓDIGO A BAIXO E VER OQUE FALTA NO A CIMA E IMPLEMENTAR COMO DEVE DE SER
            """
            new_matrix = []
            new_possible_matrix = []
            for row in range(state.board.rows):
                new_row = []
                new_possible_row = []
                for col in range(state.board.cols):
                    new_row.append(matrix[row][col].copy())
                    for item in possible_matrix[row][col]:
                        if row == action[0] and col == action[1]:
                            if item[0] != action[2]:
                                new_possible_item = []
                                new_possible_item.append(item[0].copy())
                                item1 = item[1].copy()
                                if item1 == 2:
                                    only_one_action = 1
                                new_possible_item.append(item1 -1)
                        else:
                            new_possible_item = []
                            new_possible_item.append(item[0].copy())
                            new_possible_item.append(item[1].copy())
                        new_possible_row.append(new_possible_item)
                new_matrix.append(new_row)
                new_possible_matrix.append(new_row)
            new_matrix[action[0]][action[1]] = action[2]
            itr = 0
            correct_blocks = state.correct_blocks
            while itr < len(actions_list) and actions_list[itr][3] == 1:
                new_matrix[actions_list[itr][0]][actions_list[itr][1]] = actions_list[itr][2]
                new_possible_matrix[actions_list[itr][0]][actions_list[itr][1]] = []
                correct_blocks += 1
                itr += 1
            print("new_possible_matrix: ", new_possible_matrix)
            new_board = Board(new_matrix, new_possible_matrix)
            new_state = PipeManiaState(new_board)
            new_state.only_one_action = only_one_action
            new_state.correct_blocks = correct_blocks
            return new_state
        else:
            return state
        """
    
    def goal_test(self, state):
        if state.board.correct_blocks == (state.board.rows * state.board.cols): # OU VER QUANDO O NÚMERO DE AÇÕES POSSIVEIS FOR 0
            return True
        else:
            return False
    
    def h(self, node: Node):
        # Função heuristica utilizada para a procura A*.
        return node.state.board.correct_blocks # OU UTILIZAR O NÚMERO DE AÇÕES POSSIVEIS, MAS ACHO QUE FAZ MAIS SENTIDO VER O NÚMERO DE PEÇAS QUE JÁ FORAM TROCADAS E QUE EFETIVAMENTE JÁ ESTÃO BEM NO BOARD
    
def main():
        board = Board.parse_instance()
        problem = PipeMania(board)
        result = greedy_search(problem)
        print(result.state.board.final_matrix())

if __name__ == "__main__":
    main()