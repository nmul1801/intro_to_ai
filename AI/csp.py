class spot:
    def __init__(self, num, i, j):
        self.i = i
        self.j = j        
        self.num = num
        self.domain = list(range(1, 10))

class mutable_int:
    def __init__(self):
        self.num_assignments = 0
    
    def increment_count(self):
        self.num_assignments += 1

def draw_board(board):
    print("—————————————————————————————————————")
    for i in range(len(board)):
        print("|  ", end = "")
        for j in  range(len(board[i])):
            print(board[i][j].num, end = "  ")
            if (j + 1) % 3 == 0:
                print("|  ", end = "")
        if (i + 1) % 3 == 0:
            print('\n' + "—————————————————————————————————————")
        else:
            print('\n' + "|           |           |           |")

def remove_domains(curr_num, i, j, board):

    for curr_row in range(9):
            curr_space = board[curr_row][j]
            if curr_num in curr_space.domain:
                curr_space.domain.remove(curr_num)
    
    for curr_col in range(9):
        curr_space = board[i][curr_col]
        if curr_num in curr_space.domain:
            curr_space.domain.remove(curr_num)

    start_row = i // 3 * 3
    start_col = j // 3 * 3

    for add_row in range(3):
        for add_col in range(3):
            curr_space = board[start_row + add_row][start_col + add_col]
            if curr_num in curr_space.domain:
                curr_space.domain.remove(curr_num)

def set_all_domains(board):
    for i in range(len(board)): # set all domains to default
        for j in range(len(board[i])):
            board[i][j].domain = list(range(1, 10))

    for i in range(len(board)): # set all domains
        for j in range(len(board[i])):
            curr_num = board[i][j].num
            if curr_num != 0:
                remove_domains(curr_num, i, j, board)

def convert_board(board):
    struct_board = list()
    for i in range(len(board)):
        curr_row = list()
        for j in range(len(board[i])):
            new_space = spot(board[i][j], i, j)
            curr_row.append(new_space)
        struct_board.append(curr_row)

    set_all_domains(struct_board)

    return struct_board
    
def find_empty_space(board):
    for i in range(len(board)):
        for j in range(len(board)):
            if board[i][j].num == 0:
                return i, j
    return None, None

def find_lowest_domain(board): # finds the space with the smallest domain
    smallest_domain_size = 10
    best_i = 0
    best_j = 0

    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j].num == 0:
                curr_len = len(board[i][j].domain)
                if curr_len < smallest_domain_size:
                    best_i = i
                    best_j = j
                    smallest_domain_size = curr_len

    if smallest_domain_size == 10:
        return None, None

    return best_i, best_j

def satisfies(i, j, num, board):
    for col_num in range(9): # test col
        if board[i][col_num].num == num:
            return False
    for row_num in range(len(board)): # test row
        if board[row_num][j].num == num:
            return False

    start_row = i // 3 * 3
    start_col = j // 3 * 3

    for add_row in range(3): # test for the square
        for add_col in range(3):
            if board[start_row + add_row][start_col + add_col].num == num:
                return False

    return True

def copy_board(board):
    new_board = list()
    for i in range(len(board)):
        curr_row = list()
        for j in range(len(board[i])):
            new_space = spot(board[i][j].num, i, j)
            curr_row.append(new_space)
        new_board.append(curr_row)

    set_all_domains(new_board)

    return new_board

def backtrack_solve(board, num_assignments, stack=None):
    i, j, = find_empty_space(board)

    if i == None and j == None:
        draw_board(board)
        return True, num_assignments

    for pos_assignment in range(1, 10):
        if satisfies(i, j, pos_assignment, board):
            board[i][j].num = pos_assignment
            num_assignments.increment_count()
            solved, num = backtrack_solve(board, num_assignments)
            if solved:
                return True, num

    board[i][j].num = 0
    return False, num_assignments

def min_remaining_vals(board, num_assignments, stack=None):
    i, j, = find_lowest_domain(board)

    if i == None and j == None:
        draw_board(board)
        return True, num_assignments

    curr_spot = board[i][j]

    for pos_assignment in curr_spot.domain: # only check vals in the domain
        if satisfies(i, j, pos_assignment, board):
            copy = copy_board(board)
            copy[i][j].num = pos_assignment
            remove_domains(pos_assignment, i, j, copy)
            num_assignments.increment_count()
            solved, num = min_remaining_vals(copy, num_assignments)
            if solved:
                return True, num

    return False, num_assignments

def check_possible_val(copy, row_num, col_num):
    for k in range(1, 10): # check that there valid assignment for given square
        if satisfies(row_num, col_num, k, copy):
            return True
    return False

def check_all_possiblities(board, pos_assignment, i, j):
    copy = copy_board(board)
    copy[i][j].num = pos_assignment

    for col_num in range(9): # check that all squares in row still have valid assignment
        if copy[i][col_num].num == 0 and col_num != j: # skip own square
            if not check_possible_val(copy, i, col_num):
                return False

    for row_num in range(len(board)): # check that all squares in col still have valid assignment
        if copy[row_num][j].num == 0 and row_num != i: # skip own square
            if not check_possible_val(copy, row_num, j):
                return False

    start_row = i // 3 * 3
    start_col = j // 3 * 3

    for add_row in range(3): # check that all squares in section still have valid assignment
        for add_col in range(3):
            curr_row = start_row + add_row
            curr_col = start_col + add_col
            if (curr_row != i or curr_col != j) and board[curr_row][curr_col].num == 0: # skip over own square
                if not check_possible_val(copy, curr_row, curr_col):
                    return False

    return True

def forward_checking(board, num_assignments, stack=None):
    i, j, = find_empty_space(board)

    if i == None and j == None: # if no more empty squares, puzzle is completed
        draw_board(board)
        return True, num_assignments

    for pos_assignment in range(1, 10):
        if satisfies(i, j, pos_assignment, board):
            if check_all_possiblities(board, pos_assignment, i, j): # check if effected squares will have valid assignment
                board[i][j].num = pos_assignment
                num_assignments.increment_count()
                solved, num = forward_checking(board, num_assignments)
                if solved:
                    return True, num

    board[i][j].num = 0 # reset variable
    return False, num_assignments

def remove_domains_cdb(curr_num, i, j, board): # removes curr_num from all appropriate domains

    conflict = False # returns whether there is a conflict

    for curr_row in range(9):
            curr_space = board[curr_row][j]
            if curr_num in curr_space.domain:

                conflict = True
                curr_space.domain.remove(curr_num)
    
    for curr_col in range(9):
        curr_space = board[i][curr_col]
        if curr_num in curr_space.domain:
            conflict = True
            curr_space.domain.remove(curr_num)

    start_row = i // 3 * 3
    start_col = j // 3 * 3

    for add_row in range(3):
        for add_col in range(3):
            curr_space = board[start_row + add_row][start_col + add_col]
            if curr_num in curr_space.domain:
                conflict = True
                curr_space.domain.remove(curr_num)
    return conflict

def cd_backjumping(board, num_assignments, stack=None):
    i, j, = find_empty_space(board)

    if i == None and j == None:
        draw_board(board)
        return True, num_assignments

    for pos_assignment in range(1, 10): # only check vals in the domain
        if satisfies(i, j, pos_assignment, board):
            copy = copy_board(board)
            copy[i][j].num = pos_assignment
            conflict = remove_domains_cdb(pos_assignment, i, j, copy)
            if conflict:
                stack.append(copy)
            num_assignments.increment_count()
            solved, num = cd_backjumping(copy, num_assignments, stack=stack)
            if solved:
                return True, num

    board = stack.pop()
    return False, num_assignments


easy_board = [[6, 0, 8, 7, 0, 2, 1, 0, 0],
              [4, 0, 0, 0, 1, 0, 0, 0, 2],
              [0, 2, 5, 4, 0, 0, 0, 0, 0],
              [7, 0, 1, 0, 8, 0, 4, 0, 5],
              [0, 8, 0, 0, 0, 0, 0, 7, 0],
              [5, 0, 9, 0, 6, 0, 3, 0, 1],
              [0, 0, 0, 0, 0, 6, 7, 5, 0],
              [2, 0, 0, 0, 9, 0, 0, 0, 8],
              [0, 0, 6, 8, 0, 5, 2, 0, 3]]

hard_board = [[0, 7, 0, 0, 4, 2, 0, 0, 0],
              [0, 0, 0, 0, 0, 8, 6, 1, 0],
              [3, 9, 0, 0, 0, 0, 0, 0, 7],
              [0, 0, 0, 0, 0, 4, 0, 0, 9],
              [0, 0, 3, 0, 0, 0, 7, 0, 0],
              [5, 0, 0, 1, 0, 0, 0, 0, 0],
              [8, 0, 0, 0, 0, 0, 0, 7, 6],
              [0, 5, 4, 8, 0, 0, 0, 0, 0],
              [0, 0, 0, 6, 1, 0, 0, 5, 0],
              ]

evil_board = [[2, 0, 0, 0, 0, 0, 0, 0, 0],
              [6, 5, 0, 0, 9, 0, 0, 0, 8],
              [0, 0, 0, 0, 0, 3, 9, 0, 0],
              [0, 0, 7, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 4, 0, 0, 0, 1, 0],
              [9, 8, 0, 0, 3, 0, 0, 0, 6],
              [0, 0, 2, 0, 5, 0, 0, 0, 0],
              [5, 7, 0, 0, 0, 1, 0, 6, 0],
              [0, 0, 3, 0, 0, 0, 0, 0, 7]]


query = int(input('\n' + "Welcome! Would you like to solve the easy puzzle or the hard puzzle: (1: Easy, 2: Difficult, 3: Evil): "))

if query == 1:
    board = easy_board
elif query == 2:
    board = hard_board
else:
    board = evil_board
    
converted = convert_board(board)

methods = [backtrack_solve, forward_checking, min_remaining_vals, cd_backjumping]


query = int(input('\n' + "Which pruning method would you prefer? (1: No pruning, 2: Forward Checking, 3: Minimum Values Remaining, 4: Conflict Directed Backjumping): "))
method = methods[query - 1]

print('\n' + "      ——— BEFORE SOLVING ————")
draw_board(converted)

print("      ——— AFTER SOLVING ————")

assigment_counter = mutable_int()
stack = list()
    
solved = method(converted, assigment_counter, stack=stack)
if solved:
    print("TOTAL NUMBER OF ASSIGNMENTS: " + str(assigment_counter.num_assignments))
else: 
    print("UNABLE TO SOLVE")