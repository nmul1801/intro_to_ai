Nicholas Mulligan

OBSERVATIONS:

Total number of assignments for chronological backtracking:
Easy: 607
Difficult: 8751
Evil: 175701

Total number of assignments for forward checking:
Easy: 175
Difficult: 2376
Evil: 22285

Total number of assignments for min remaining :
Easy: 47
Difficult: 257
Evil: 192

Total number of assignments for conflict directed chronological backtracking:
Easy: 607
Difficult: 8751
Evil: Didn't run, took more than 5 minutes, but I predict 175701


ASSUMPTIONS

I'm assuming that the user will enter a valid integer according to the prompts. So for the first prompt,
I'm assuming that the user will enter either a one, two, or three (for easy, hard, or evil), and for the second input,
I'm assuming the user will enter either a one, two, three, or four (for no pruning method, forward checking, min values 
remaining, or conflict directed backjumping). I also have assumed that the value '0' represents an empty spot when 
printing the board prior to solving.

DISCUSSION

The forward checking and min remaining values pruning methods were both more efficient than normal chronological backtracking, 
with the min remaining values performing better than the forward checking method. While these algorithms are more efficient 
in terms of total number of assignments, my method for implementing forward checking and min remaining values have issues 
with time and space complexity. For the forward checking method, after every hypothetical assignment, I checked that every 
square that may have been impacted (every square in the row, every square in the column, and every square in the sub-square) 
was still satisfiable. In other words, for every hypothetical assignment, the algorithm confirmed that the affected 24 squares
had a valid assignment, having to check a maximum of 9 possibilities per square. So for every valid assignment, the algorithm 
had to check 24 * 9 = 216 possibilities before confirming that an assignment was valid. Although this is an improvement 
compared to the normal chronological backtracking, I believe that towards the end, when each square has only one or two 
possibilities, this method is actually less efficient than the normal chronological backtracking. In other words, the forward 
checking is too thorough towards the end of solving the puzzle. 

For my implementation of minimum remaining value, the board is copied with every assignment. This is because changing the 
domains for each space after every assignment led to problems with pointers, and resetting domains after a failed assignment. 
So while the time complexity for this algorithm was much better than that of normal, chronological backtracking, the space 
complexity is much larger. Not to mention the time complexity addition in copying all numbers and domains between boards. 
Nevertheless, the min remaining value assignment was far more efficient in terms of number of assignments. For the easy 
board, the method does not encounter a failed assignment. 

NO IMPLEMENTATION OF CONFLICT-DIRECTED BACKJUMPING

For some of the pruning methods, I believed that they were either minimally applicable, or completely 
useless in the example of Sudoku. For example, the implementation of a conflict directed backjumping
algorithm would be useless, and would ultimately result, approximately, in the same number of assignments as
normal, chronological backtracking. This is due to the structure of the game, and how every square influences other squares.
Unless the square being assigned is the last square in its row, column, and sub-square, an assignment in
that square will cause a conflict. This is an extremely rare case, and is not worth the addition to
space and time complexity, as well as keeping track of all previous boards. Therefore, I have chosen to not implement
the conflict directed backjumping algorithm.

UPDATE
I implemented a Conflict Directed Backjumping algorithm to prove my point. The number of assignments was
EXACTLY the same for both the easy and the hard boards. I didn't run the program on the evil board, as it
would take too long to copy the contents and domains of the boards for every assignment. I predicted that 
the number of assignments would be slightly less, but not exactly the same. My method for finding a conflict
was to remove domains for the appropriate squares on every assignment, and if any domain was changed during
this, then this means that there was a conflict. If there was a conflict, then I loaded the current board 
into the stack, and upon encountering an invalid assignment, I then changed the board to the one on the top of the 
conflict stack. Now considering what I previously wrote, I suppose that, given a square (let's say with a true 
value of A) with a filled column, row, and sub-square, those spaces will still have A in their domain. Only after 
the assignment of A to the given square will A be removed from the others' domain. Therefore, even in this situation, the
assignment still causes a conflict.

This is due to the satisfaction requirement for an assignment. The proof would look something like:

Let x be assigned to square A. For the sake of contradiction, suppose that this assignment causes no conflicts
The it follows that there must be a value x for some square in the square A's column, row, and sub-square.
Therefore, x does not satisfy A, and would never be assigned to it.


