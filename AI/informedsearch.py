
import sys
import random as rand


class Node:
    def __init__(self, stack):
        self.children = []
        self.prev = None
        self.stack = stack.copy()
        self.h_cost = 0
        self.t_cost = 0
        self.total_cost = 0
        self.index_of_flip = 0

def generate_random_stack(size):
    stack = list(range(1, size + 1))
    rand.shuffle(stack)
    return stack

def get_total_cost(node):
    print("")
    return node.total_cost

def flip(stack, index):
    new_list = stack.copy()
    temp = stack[index:]
    temp.reverse()
    new_list[index:] = temp
    return new_list

def gap_heuristic(stack):
    h_val = 0
    for i in range(len(stack) - 1):
        if abs(stack[i] - stack[i + 1]) > 1:
            h_val += 1
    return h_val

def dummy_heuristic(stack): 
    return 0
    
def single_flip_cost_function(stack, index):
    return 1

def flip_least_pancakes_cost(stack, index): 
    return len(stack) - index

def goal_test(node):
    for i in range(len(node.stack) - 1):
        if node.stack[i] < node.stack[i + 1]:
            return False
    return True

def gen_children(node, h_func, cost_func, total_generated):

    if goal_test(node):
            return None, True, node

    new_children = list()
    for i in range(len(node.stack) - 1): # flipping on last index has no effect on array
        temp = node.stack.copy()
        new_child_stack = flip(temp, i)

        new_child = Node(new_child_stack)
        new_child.h_cost = h_func(new_child_stack)
        new_child.t_cost = cost_func(new_child_stack, i) + node.t_cost

        new_child.total_cost = new_child.h_cost + new_child.t_cost
        new_child.prev = node
        new_child.index_of_flip = i

        new_children.append(new_child)

        total_generated += 1

        if goal_test(new_child):
            return new_children, True, new_child, total_generated

    return new_children, False, None, total_generated

def print_stack(stack, index = 0):
    for x in range(len(stack)):
        out = str(stack[x])
        print(out.ljust(4), end = "")
    print()
    for x in range(len(stack) - 1):

        if x != index - 1:
            print("    ", end = "")
        else:
            print("  | ", end = "")
    print()

def check_stack(stack):
    for i in range(len(stack)):
        for j in range(len(stack)):
            if i != j and stack[i] == stack[j]:
                print("ERROR: REPEAT VALUES IN STACK")
                exit(1)

def gen_user_stack(size):
    stack = list()
    for i in range(size):
        next = int(input("In position " + str(abs(i - size)) + ": "))
        if next > size or next < 1:
            print("ERROR: INVALID ENTRY RANGE, MUST BE MORE THAN (1) AND LESS THAN (LENGTH)")
            exit(1)
        stack.append(next)
    check_stack(stack)
    return stack

def check_input(query):
    if query != 1 and query != 2:
        print("ERROR: INVALID QUERY")

def insertion_sort(queue, next_children):

    for child in next_children:
        inserted = False
        for i in range(len(queue)):
            if queue[i].total_cost > child.total_cost:
                queue.insert(i, child)
                inserted = True
                break
        if inserted == False:
            queue.append(child)

size = int(input("Welcome! How many pancakes are in your stack? "))

print("Would you like to generate a random stack, or create your own (1/2)")
print("(1) Create a random stack")
print("(2) Create your own stack")
stack = None
query = int(input())
check_input(query)

if query == 1:
    stack = generate_random_stack(size)
else:
    stack = gen_user_stack(size)

print("Choose a cost function")
print("(1) The cost of every flip is equal")
print("(2) The cost of each flip is the number of pancakes flipped  (WARNING: STACK SIZE SHOULD NOT BE LARGER THAN 6)")

query = int(input())
check_input(query)

if query == 1:
    c_func = single_flip_cost_function
else:
    c_func = flip_least_pancakes_cost

print("Choose a heuristic function")
print("(1) Gap heuristic")
print("(2) None, Uniform Cost Search (WARNING: STACK SIZE SHOULD NOT BE LARGER THAN 6)")

query = int(input())
check_input(query)

if query == 1:
    h_func = gap_heuristic 
else: 
    h_func = dummy_heuristic

print("The flip location in shown by the '|' in the previous stack.")
print("If there is no '|' in the previous stack, the entire stack was flipped.")

root = Node(stack)
root.h_cost = h_func(stack)
root.t_cost = c_func(stack, len(stack))
root.total_cost = root.h_cost + root.t_cost

curr = root
queue = [root]
next_children = list()
success = goal_test(root)
solution = None
if success:
    solution = root
else:
    solution = None

total_generated = 1

while not success:

    insertion_sort(queue, next_children)

    curr = queue.pop(0)

    next_children, success, solution, total_generated = gen_children(curr, h_func, c_func, total_generated)

path = [solution]
curr = solution

while curr != None:
    path.append(curr)
    curr = curr.prev

path.reverse()

print("Path to solution: ")

for i in range(len(path) - 2):
    print_stack(path[i].stack, path[i + 1].index_of_flip)

goal = list(range(1, len(path[0].stack) + 1))
goal.reverse()

for curr in goal:
    print((str(curr)).ljust(4), end = "")


print('\n' + "Number of nodes generated: " + str(total_generated))