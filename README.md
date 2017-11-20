# sudoku-solver

A Python program that uses constraint satisfaction to solve Sudoku puzzles.

## Example

```console
$ ./example.py
EXAMPLE:
+---+---+---+
|13 |  6|   |
| 74|  2|58 |
|   | 5 |3  |
+---+---+---+
| 8 | 1 |   |
|   | 6 | 29|
|   |   |43 |
+---+---+---+
|   | 3 | 5 |
|9 3|   |7 4|
|   | 75|8  |
+---+---+---+
Solution:
+---+---+---+
|135|846|297|
|674|392|581|
|892|157|346|
+---+---+---+
|289|413|675|
|347|568|129|
|561|729|438|
+---+---+---+
|718|634|952|
|953|281|764|
|426|975|813|
+---+---+---+
...
```

## Installation

### From PyPi

```bash
pip install sudoku-solver
```

### From source

```bash
git clone https://github.com/dcmshi/sudoku-solver.git
cd sudoku-solver
make install
```

## Usage

Once installed, the Sudoku solver is available in the `sudoku` module:

```pycon
>>> from sudoku import Sudoku
>>>
>>> puzzle = Sudoku([
...   8,5,0, 0,0,2, 4,0,0,
...   7,2,0, 0,0,0, 0,0,9,
...   0,0,4, 0,0,0, 0,0,0,
...
...   0,0,0, 1,0,7, 0,0,2,
...   3,0,5, 0,0,0, 9,0,0,
...   0,4,0, 0,0,0, 0,0,0,
...
...   0,0,0, 0,8,0, 0,7,0,
...   0,1,7, 0,0,0, 0,0,0,
...   0,0,0, 0,3,6, 0,4,0,
... ])
>>>
>>> print "Sudoku puzzle:"
Sudoku puzzle:
>>> print puzzle.ascii
+---+---+---+
|85 |  2|4  |
|72 |   |  9|
|  4|   |   |
+---+---+---+
|   |1 7|  2|
|3 5|   |9  |
| 4 |   |   |
+---+---+---+
|   | 8 | 7 |
| 17|   |   |
|   | 36| 4 |
+---+---+---+
>>> solution = puzzle.solve()
>>> print "Solution:"
Solution:
>>> print solution.ascii
+---+---+---+
|859|612|437|
|723|854|169|
|164|379|528|
+---+---+---+
|986|147|352|
|375|268|914|
|241|593|786|
+---+---+---+
|432|981|675|
|617|425|893|
|598|736|241|
+---+---+---+
>>>
```

## Heuristics

3 Heuristics are used to minimize the search space

1. Most constrained variable, choosing the variable with the fewest "legal" moves. 
2. Most constraining variable, this acts as a tie breaker for the first heuristic, choose the variable which affects the most neighbours.
3. Least constraining values, choose the value for the variable that affects the least neighbours.

## Algorithm

The algorithm used is backtracking, with forward checking, and the 3 additional heuristics on top of that.  Backtracking is just a tree traversal of all possible board states as you try each value ([1,2,3,4,5,6,7,8,9]), for each possible variable (square).  By itself it is quite costly, so using the heuristics we can order the variables and values to try first in our tree traversal.  And then with forward checking we check that there are still valid options for the affected variables when assigning a value to a variable, which saves additional costly recursive calls.