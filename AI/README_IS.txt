Nicholas Mulligan
Comp 131 - Intro to AI
Assignment 2 — Informed Search

COMPILATION: python3 informedsearch.py

1) Define the problem as a searching problem.
Initial State: Initial stack, either user generated or randomly generated

Description of Possible Actions: Priority queue of nodes with lowest total cost. Each node contains 
a stack that is generated depending on the parent stack

Transition Function: Function that generates all possible flips from a given node and inserts them 
in the priority queue accordingly

Goal Test: For each stack generated, test whether each pancake is larger than the one it is under

Cost function: Each flip has a cost of 1

2) Define a possible cost function (backward cost).

I have implemented two cost functions: one is defined as each flip costing an equal amount (1),
and another (2) is defined as each flip costing the amount of pancakes that are flipped. The 
second cost function is very risky. If there is a high-number pancake toward the top of the stack,
the function will try every other option before flipping the high-number pancake toward the bottom.
This results in extremely poor performance.

3) Define a possible heuristic function (forward cost)
I used the recommended heuristic function, the gap heuristic

4) Could the Uniform-Cost-Search algorithm be used?
Yes, it can be tested when prompted to choose a heuristic function. It would functionally be a BFS 
search if the user chooses the cost function where all flips are of equal value. Similar to the 
heuristic function that calculates a cost based on the number of pancakes flipped, I strongly recommend 
against running the program with the uniform cost function if the stack length is above 6.

ASSUMPTIONS / INTERFACE

The program starts off with prompting the user to decide how large they would like their stack to be.
This is to avoid complications which I will discuss later. After choosing a stack size, the user has
the option to decide whether the stack will be randomly generated, or if they would like to create
the stack themselves. Creating the stack themselves will result in entering one number at a time,
one for each position in the stack. I believe that I have covered all the error cases for this 
option, but I would still assume that the user is entering a valid stack size, and if they do choose
to customize it, entering a valid order. After a stack has been created, the user will choose a cost
function. As previously mentioned, the cost function for each pancake flipped costing (1) should not
be used if the stack size is > 6. I've tried this multiple times, and because of the branching factor
along with the queue size growth, these operations can take an inconvenient long amount of time. After
choosing a cost function, the user will then choose a heuristic function, one is the recommended
heuristic function, the gap heuristic, and the other is no heuristic, or the uniform cost search.
Similarly to the cost function, the uniform cost should only be used if the stack size is > 6. My CPU
almost overheated trying to run uniform cost search on a stack size of 10

Example on running uniform cost search on a stack size of 10:
Running a randomly-generated starting stack with the gap heuristic, the algorithm generated 7226 nodes,
and took about 2 seconds to compute
The resulting path: 
6   7   3   10  8   5   2   1   4   9   
              |                     
6   7   3   10  9   4   1   2   5   8   
      |                             
6   7   8   5   2   1   4   9   10  3   
                                    
3   10  9   4   1   2   5   8   7   6   
                          |         
3   10  9   4   1   2   5   6   7   8   
          |                         
3   10  9   8   7   6   5   2   1   4   
                          |         
3   10  9   8   7   6   5   4   1   2   
  |                                 
3   2   1   4   5   6   7   8   9   10  
                                    
10  9   8   7   6   5   4   1   2   3   
                          |         
10  9   8   7   6   5   4   3   2   1 

With a uniform cost implementation, the algorithm would generate between 10^8 and 10^9 nodes, as the depth
of the solution is 9, and the branching factor is 10. If the computation generated 7500 nodes in 2 seconds, 
then to generate 10^8 nodes, the computation would take 26666 seconds, or about 7 and a half hours. This 
doesn't even account for the increase in operations once the size of the queue grows to 10^4 nodes, 10^5
nodes, and beyond. For every node generated, it must be inserted into the queue appropriately, meaning the 
runtime would probably take even longer than the previously calculated 7 and a half hours