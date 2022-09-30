import random as random

### NODE CLASSES ###

# Result class: whenever a node returns anything, it will be in the form of a Result (.outcome)
class Result:
    def __init__(self, code):
        if code == 0:
            self.outcome = "FAILURE"
        elif code == 1:
            self.outcome = "SUCCESS"
        elif code == 2:
            self.outcome = "RUNNING"
        else:
            self.outcome = "ERROR, NO RESULT SPECIFIED"
            exit(1)

# Most basic representation — each node can have a priority, children, and a name
class Node:
    def __init__(self, priority = 0, name = ""):
        self.children = []
        self.priority = priority
        self.name = name
    def run(self, blackboard):
        return Result(0)
    
# used only for priority nodes
def keyFunc(Node):
    return Node.priority

# Priority node — sorts children by priority, evaluates them left to right
class Priority(Node):
    def __init__(self, priority = 0, name = ""):
        Node.__init__(self, priority, name)

    def run(self, blackboard):
        self.children.sort(key = keyFunc)
        for child in self.children:
            result = child.run(blackboard)
            if result == Result(1).outcome:
                return result # success
            if result == Result(2).outcome:
                return result # running
        return Result(0).outcome # failure

# Selector node — evaluates children left to right until one succeeds or is running
class Selector(Node):
    def __init__(self, priority = 0, name = ""):
        Node.__init__(self, priority, name)

    def run(self, blackboard):
        for child in self.children:
            result = child.run(blackboard)
            if result == Result(1).outcome:
                return result # success
            if result == Result(2).outcome:
                return result # running
        return Result(0) # failure

# Sequence node — evaluates children until one fails or is running
class Sequence(Node):
    def __init__(self, priority = 0, name = ""):
        Node.__init__(self, priority, name)

    def run(self, blackboard):
        for child in self.children:
            result = child.run(blackboard)
            if result == Result(0).outcome:
                return result # failure
            if result == Result(2).outcome:
                return result # running
        return Result(1).outcome # success

# Task node — most basic version of task
class Task(Node):
    def __init__(self, priority = 0, name = ""):
        Node.__init__(self, priority, name)

    def run(self, blackboard):
        print(self.name + " SUCCESS")
        return Result(1).outcome # success

# Timed Task — Accesses the blackboard timer associated with it. If the timer is
# still running, then the task hasn't been completed. If the timers is at zero, 
# the task has been executed successfully. Used for clean floor and recharging
# battery
class Timed(Task):
    def __init__(self, priority=0, name="", timer="", time=0):
        Task.__init__(self, priority, name)
        self.timer = timer
        self.time = time

    def run(self, blackboard):
        blackboard[self.timer] -= 1
        if blackboard[self.timer] != 0:
            print(self.name + " IS RUNNING WITH " + str(blackboard[self.timer]) + " SECONDS LEFT")
            return Result(2).outcome # RUNNING

        blackboard[self.timer] = self.time # reset timer
        if self.name == "DOCK":
            print("BATTERY RECHARGED") # end of timer for dock, battery gets recharged
            blackboard["BATTERY_LEVEL"] = 100
        return Result(1).outcome # SUCCESS

# Read node — reads data from the blackboard and stores it
class Read(Task):
    def __init__(self, priority=0, name="", time=0, readObj=""):
        Task.__init__(self, priority, name)
        self.readObj = readObj

    def run(self, blackboard):
        store = blackboard[self.readObj] # 'store' the data
        print("RETRIEVED (" + store + ") FROM " + self.readObj, end = ", ")
        return Result(1).outcome # success
    
# Write node — writes data to the blackboard
class Write(Task):
    def __init__(self, priority=0, name="", writeObj="", store=""):
        Task.__init__(self, priority, name)
        self.writeObj = writeObj
        self.store = store

    def run(self, blackboard):
        if self.store == Result(0).outcome: # pass in boolean value (failure) to store
            blackboard[self.writeObj] = False
        elif self.store == Result(1).outcome: # pass in boolean value (success) to store
            blackboard[self.writeObj] = True
        else:                                 # pass in any other string value
            print("STORING (" + self.store + ") IN " + self.writeObj, end = ", ")
            blackboard[self.writeObj] = self.store
        if self.name != "FIND_HOME":
            print(self.name + " SUCCESS") 
        return Result(1).outcome
        
# Condition node — evaluates a boolean operation by accessing the blackboard
class Condition(Node):
    def __init__(self, priority=0, name="", code=""):
        Node.__init__(self, priority, name)
        self.code = code
    
    def run(self, blackboard):
        if self.code == "DUSTY_SPOT" and blackboard["DUSTY_SPOT_TIME"] == 35: # if timer hasn't begun
            dusty = input("Spot encountered, is it dusty? (y/n) ") 
            checkChoice(dusty)
            if dusty == "y":    # evaluate dusty spot with user decision
                blackboard["DUSTY_SPOT"] = True
            else:
                blackboard["DUSTY_SPOT"] = False
            print() # newline for better UI
        if self.code == "BATTERY_LEVEL": # special case for battery level
            if blackboard[self.code] < 30:
                print(self.code + " SUCCESS", end = ", ")
                return Result(1).outcome
            print(self.code + " FAILURE", end = ", ")
            return Result(0).outcome
        if blackboard[self.code]: # return speficied bool value in for of Result
            print(self.code + " SUCCESS", end = ", ")
            return Result(1).outcome
        print(self.code + " FAILURE", end = ", ")
        return Result(0).outcome

# Clean floor node — only used for the clean floor task. There is a one in ten 
# chance that,
# when reached, the floor is clean. 
class Clean_Floor(Node):
    def __init__(self, priority=0, name=""):
        Node.__init__(self, priority, name)
    
    def run(self, blackboard):
        prob_fail = random.randint(1, 20) # 5 percent chance of a clean floor
        if prob_fail == 1:
            print("CLEAN FLOOR SUCCESS, FLOOR IS CLEAN!")
            return Result(1).outcome # SUCCESS
        print("CLEAN FLOOR FAILURE (RETURNING RUNNING), FLOOR IS DIRTY!")
        return Result(2).outcome # RUNNING

### TREE CREATION ###

#root node
root = Priority(name = "ROOT_NODE")

#children of root node
doNothing = Task(priority=3, name="DO_NOTHING")
evalBattery = Sequence(priority=1, name="EVAL_BATTERY_SUBTREE")
cleaning = Selector(priority=2, name="CLEANING")

root.children = [cleaning, evalBattery, doNothing]

# battery subtree (LST)
checkBattery = Condition(name="BATTERY_<_30", code="BATTERY_LEVEL")
findHome = Write(name = "FIND_HOME", writeObj="HOME_PATH", store="0, 0")
goHome = Read(name = "GO_HOME", readObj="HOME_PATH")
dock = Timed(name="DOCK", timer = "DOCKING_TIME", time = 10)

# battery children
evalBattery.children = [checkBattery, findHome, goHome, dock]

# spot cleaning subtree (MST)
spotCleaningSequence = Sequence(name="SPOT_CLEANING_SEQUENCE")
generalSequence = Sequence(name="GENERAL_SEQUENCE")

# spot cleaning children
cleaning.children = [spotCleaningSequence, generalSequence]

# spotCleaningSequence subtree (Middle left subtree)
spot = Condition(name="SPOT", code="SPOT_CLEANING")
cleanSpot20s = Timed(name="CLEAN_SPOT", timer="SPOT_CLEAN_TIME", time=20)
doneSpot = Write(name="DONE_SPOT", writeObj="SPOT_CLEANING", store=Result(0).outcome)

# spotCleaningSequence children
spotCleaningSequence.children = [spot, cleanSpot20s, doneSpot]

# general cleaning children (Middle right subtree)
general = Condition(name="GENERAL", code="GENERAL_CLEANING")
generalTrueSequence = Sequence(name="NO_GENERAL_SEQUENCE") # only accessed if general evaluates to true

# general sequence's children
generalSequence.children = [general, generalTrueSequence]

#generalTrue's children
dustyCleanPriority = Priority(name="DUSTY_CLEAN_PRIORITY")
doneGeneral = Write(name="DONE_GENERAL", writeObj="GENERAL_CLEANING", store=Result(0).outcome)

generalTrueSequence.children = [dustyCleanPriority, doneGeneral]

# dustyCleanPriority's children
cleanDustySpotSequence = Sequence(name="DUSTY_SPOT_SEQUENCE", priority=1)
cleanFloor = Clean_Floor(name="CLEAN_FLOOR", priority=2)

dustyCleanPriority.children = [cleanDustySpotSequence, cleanFloor]

# cleanDustySpotSequence's children
dustySpot = Condition(name="DUSTY_SPOT", code="DUSTY_SPOT")
cleanSpot35s = Timed(name="CLEAN_SPOT", timer="DUSTY_SPOT_TIME", time=35)

cleanDustySpotSequence.children = [dustySpot, cleanSpot35s]

### INTERFACE ###

# setBool — used in (re)initializing the blackboard if the user decides to do so
def setBool(code, blackboard):
    print(code + " (T/F): ", end = "")
    var = str(input())
    if var != "T" and var != "F":
        print("ERROR: INVALID VALUE FOR " + code + " (T/F)")
        exit(1)
    if var == "T":
        blackboard[code] = True
    else:
        blackboard[code] = False

# init_vacuum — used in (re)initializing vacuum if user decides to do so
def init_vaccuum(vacuum):
    var = int(input("Batterylevel (0 - 100): "))
    vacuum["BATTERY_LEVEL"] = var
    if var < 0 or var > 100:
        print("ERROR: INVALID BATTERY LEVEL (0 - 100)")
        exit(1)

    setBool("SPOT_CLEANING", vacuum)
    setBool("GENERAL_CLEANING", vacuum)

# checkChoice — ensures that a yes or no option has the correct format (y/n)
def checkChoice(choice):
    if choice != "y" and choice != "n":
        print("ERROR: INVALID CHOICE (y/n)")
        exit(1)

# checkChoice — ensures that battery level has the correct format (y/n)
def checkNum(num):
    if num < 1:
        print("ERROR: INVALID NUMBER OF EVALUATIONS (must be more than 0)")
        exit(1)

# runProg UI for program
def runProg(root):
    #default vacuum initialization
    vacuum = {"BATTERY_LEVEL": 100, "SPOT_CLEANING": False, 
        "GENERAL_CLEANING": False, "DUSTY_SPOT": False, 
        "HOME_PATH": "", "SPOT_CLEAN_TIME": 20, 
        "DUSTY_SPOT_TIME": 35, "DOCKING_TIME": 10}
    
    # welcome user, intialize vacuum
    print('\n' "Welcome! Set up the blackboard, then input the amount of evaluations." + '\n')
    print("—— After each set of evaluations, you will have the choice to continue or stop the program")
    print("—— If you choose to continue the program, you will also have the choice change to edit the blackboard before continuing" + '\n')
    init_vaccuum(vacuum)

    num = int(input("Number of evaluations: "))
    checkNum(num)
    i = 0

    while i != num:
        print("BATTERY LEVEL AT " + str(vacuum["BATTERY_LEVEL"]), end = ", ")
        root.run(vacuum)
        print()
        if vacuum["DOCKING_TIME"] == 10:
            vacuum["BATTERY_LEVEL"] -= 1
        if i == num - 1:
            choice = input("Would you like to continue? (y/n) ")
            checkChoice(choice)
            if choice == "y":
                num = int(input("Number of evaluations: "))
                checkNum(num)
                i = 0
                choice = input("Would you like to edit the vacuum? (y/n) ")
                checkChoice(choice)
                if choice == "y":
                    init_vaccuum(vacuum)
                continue
            else:
                exit(0)
        i += 1

# run the program
runProg(root)