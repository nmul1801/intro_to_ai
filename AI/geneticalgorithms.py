
import random

# questions for office hours
# fitness function ok?

LENGTH = 40

def rand_bool():
    if random.getrandbits(1):
        return True
    return False

def fitness_func(phen):
    weight = 0
    val = 0
    for curr in phen:
        if curr.in_backpack:
            weight += curr.weight
            val += curr.value
    if weight > 250:
        return 0
    return val

class Object:
    def __init__(self, w, v):
        self.weight = w
        self.value = v
        self.in_backpack = rand_bool()

def get_random_phen():
    return [Object(20, 6), Object(30, 5), Object(60, 8), Object(90, 7), Object(50, 6), Object(70, 9),
             Object(30, 4), Object(30, 5), Object(70, 4), Object(20, 9), Object(20, 2), Object(60, 1)]

def get_fitness(list):
    return fitness_func(list)

def get_next_parents(list, generation):
    list.sort(key=get_fitness, reverse=True)
    print("For gen " + str(generation) + ", best fit is " + str(fitness_func(list[0])))
    next_gen_parents = (start_phenos[:int(LENGTH / 2)]).copy()
    return next_gen_parents

def get_start_phenos():
    start_phenos = list()

    for i in range(LENGTH):
        start_phenos.append(get_random_phen())
    return start_phenos

# starting off as single point mutation, will change to mp later
def crossover(fatha, motha, spcr, mutate, mp_mut):
    offspring_1, offspring_2 = None, None

    if spcr: # single point crossover
        pt = random.randint(1, 11) # size of the chromasome - 1
        offspring_1 = fatha[:pt].copy() + motha[pt:].copy()
        offspring_2 = motha[:pt].copy() + fatha[pt:].copy()
    else:
        indices = [random.randint(1, 4), random.randint(6, 10)] # cut out a middle section of the pheno
        offspring_1 = fatha[:indices[0]].copy() + motha[indices[0]:indices[1]].copy() + fatha[indices[1]:].copy()
        offspring_2 = motha[:indices[0]].copy() + fatha[indices[0]:indices[1]].copy() + motha[indices[1]:].copy()

    if mutate:
        if not mp_mut: # single point mutation
            pt = random.randint(1, 11)
            offspring_1[pt].in_backpack = not offspring_1[pt].in_backpack
            offspring_2[pt].in_backpack = not offspring_2[pt].in_backpack
        else: # multi point mutation
            num_mutations = random.randint(1, 4) # don't go too crazy
            indices = random.sample(range(1, 12), num_mutations)
            for curr in indices:
                offspring_1[curr].in_backpack = not offspring_1[curr].in_backpack
                offspring_2[curr].in_backpack = not offspring_2[curr].in_backpack

    return offspring_1, offspring_2

def set_bool(query):
    if query != 1 and query != 2:
        print("ERROR: INVALID BOOL INPUT (1 OR 2)")
        exit(1)
    if query == 1:
        return True
    return False

def print_pheno(pheno):
    print("Phenotype with a fitness level of " + str(fitness_func(pheno)) + ": ")
    for i in range(len(pheno)):
        print(str(i + 1) + ": " + str(pheno[i].in_backpack))

print("Welcome, which halting condition would you prefer?")
print("1) Number of generations")
print("2) Fitness level")
stop_pt = int(input())
if stop_pt != 1 and stop_pt != 2:
    print("ERROR: INVALID BOOLEAN INPUT")
    exit(1)

print("Which crossover method would you prefer?")
print("1) Single point crossover")
print("2) Multi point crossover")
query = int(input())

spcr = set_bool(query)

print("Would you like to turn on mutation?")
print("1) Yes")
print("2) No")
query = int(input())

mutate = set_bool(query)

mp_mut = False

if mutate:
    print("Would you prefer multi point mutation or single point?")
    print("1) Multi-point mutation")
    print("2) Single-point mutation")
    query = int(input())
    mp_mut = set_bool(query)

start_phenos = get_start_phenos()
curr_rents = get_next_parents(start_phenos, 0)
best_fit = 0
best_pheno = None

if stop_pt == 1:
    num_gens = int(input("How many generations would you like to create? "))
    for i in range(1, num_gens):
        new_gen = list()
        for j in range(int(LENGTH / 2)):
            fatha = random.choice(curr_rents)
            motha = random.choice(curr_rents)
            child_one, child_two = crossover(fatha.copy(), motha.copy(), spcr, mutate, mp_mut)
            new_gen.append(child_one)
            new_gen.append(child_two)
        curr_rents = get_next_parents(new_gen, i)

        if i == num_gens - 1:
            for curr in new_gen:
                if fitness_func(curr) > best_fit:
                    best_pheno = curr
                    best_fit = fitness_func(curr)
else:
    threshold = int(input("What level fitness would you like to find? "))
    gen_num = 0
    while best_pheno == None:
        new_gen = list()
        for j in range(int(LENGTH / 2)):
            fatha = random.choice(curr_rents)
            motha = random.choice(curr_rents)

            child_one, child_two = crossover(fatha.copy(), motha.copy(), spcr, mutate, mp_mut)
            new_gen.append(child_one)
            new_gen.append(child_two)

        curr_rents = get_next_parents(new_gen, gen_num)
        for curr in new_gen:
            if fitness_func(curr) >= threshold:
                best_pheno = curr
                break
        gen_num += 1

print_pheno(best_pheno)
