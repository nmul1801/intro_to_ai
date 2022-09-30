README - Nicholas Mulligan - Intro to AI - CS 131

COMPILATION: python3 behaviortree.py

ASSUMPTIONS

The following program is an implementation of a behavior tree. On each iteration (or 
second), the robot will lose one percent of its battery. When initializing the vacuum, 
users must enter an integer value <= 100 and >= 0. To set the boolean values of the 
blackboard, users must enter either "T" or "F". Any other value will result in the 
program immediately stopping (exit(1)). The user will also be presented with choices 
to continue evaluations, edit the blackboard (see INTERFACE), and decide whether or 
not the current spot is is dusty. Again, users must enter either a "y" or "n". Any 
other input will also stop the program with exit(1).

Another thing that I was unsure of, and I want to make clear is intentional, is the
timing mechanic. For each timed task, I made sure to subtract one second, then 
check that the timer was zero as opposed to checking that the timer was zero,
and if it wasn't, then subtracting one second. My method ensures that if a task
runs for 20 seconds, there are 19 outputs of the task "RUNNING", and one output
the task "SUCCESS", meaning after the 20th second, the task succeeded in executing
the task.

The last assumption is that the tree given is correct. I may be mistaken, but I believe 
there is a small bug in the tree, encountered when the robot senses a dusty spot. When 
it encounters a spot that needs 35 second cleaning, it will run the cleaning for 35 
iterations, but then not check whether the floor is completely clean (Clean Floor). 
Instead, it will report a successful clean to the priority node, turn off general 
cleaning, and on the next evaluation, do nothing. I think it would make more sense 
to execute the clean floor task after cleaning a dusty spot, but I didn't want to 
change the tree, as I'm assuming the given tree was what we were expected to create. 
I still thought I should mention this, though.

CREATIVE LIBERTIES

There were a couple features that I either implemented with reccomendations from the 
spec, or from ideas I thought came up with. When the robot enters the "docking" task, 
instead of simply returning success without changing the battery level, the robot 
recharges, setting the battery level to 100%. This made sense to me, as the tree enters the 
docking task only when the battery is < 30, meaning it should recharge. This also allows 
the robot to return to running tasks after recharging. 

From the spec, the clean_floor task is implemented almost as suggested. In the slides that go
over the "until success" decorator, it specifies that the decorator means "It executes the 
attached node, while it fails returning RUNNING. It returns SUCCEEDED at the first success.
However, in the spec, we are told that the clean floor task "will fail when there is nothing 
more to clean. The result of the task can be determined at random (with a low probability 
of failure). I assumed that this was a mistake, as making it this way would mean there is a low
probability that the floor is still  dirty. Instead, I created the node to have a low probability
of success, success meaning that the floor is clean. With my implementation, there is a 95% 
(random) chance that the floor is still dirty, which makes more sense to me. Talking with my
classmates, I think others would agree.

Another feature has to do with the DUSTY_SPOT condition. Every time General Cleaning 
is switched on, users must act as the robot's DUSTY_SPOT sensor, deciding 
whether the current spot needs deep cleaning. If the user decides that the current spot 
needs cleaning, vacuum[DUSTY_SPOT] is set to True, sending the robot into a 35 second 
deep cleaning process. After the cleaning process, the tree will evaluate to "done general". 
Of course, if the user decides that the current spot is not dusty, the tree will continue 
the evaluation and execute the clean_floor task. 

INTERFACE

The interface for the vacuum allows the user to customize the blackboard, specify a
number of evaluations, and then observe the outcome of each "second" the vacuum runs.
After all executions are evaluated, the user can decide to continue for another specified
number of evaluations, or stop the process completely. If the user decides to continue, they
also have the option to edit the blackbord again before continuing to evaluate the tree. The
interface will also prompt the user to "sense" whether or not the current spot is dusty as
needed. I was wary to create the interface in a way that the user is able to edit the blackboard
multiple times, as I thought this may lead to some complications, but I was told by the professor 
that this is okay. I still believe that there may be complications with the timers and artificially 
stopping tasks from running, but I trust that the Professor Santini was right that including this 
feature in the UI is acceptable.