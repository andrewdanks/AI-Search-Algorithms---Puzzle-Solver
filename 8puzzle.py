#Look for <<<...>>> tags in this file. These tags indicate changes in the 
#file to implement the required routines. Some mods have been made some others
#you have to make. Don't miss addressing each <<<...>>> tag in the file!


'''
8-Puzzle STATESPACE 

State Space Representation: 
<<<8-Puzzle: 

Initial state: Any state can be the initial one.
Actions: It depends where the blank square is, 

>>>8-Puzzle:

'''

#<<<8-Puzzle: Definitions for row/col number
FIRST = 1
MIDDLE = 2
LAST = 3
#>>>8-Puzzle: Definitions for row/col number

#from search import *
#from search_pc import *
from id_astar import *

class eightPuzzle(StateSpace):

    StateSpace.n = 0
    
    def __init__(self, action, gval, state, parent = None):
        """Given a list of 9 numbers in the range [0-8] generate an eightPuzzle state
           The 9 numbers specify the position of the tiles in the puzzle from the
           top left corner, row by row, to the bottom right corner. E.g.:

           [2, 4, 5, 0, 6, 7, 8, 1, 3] represents the puzzle configuration

           |-----------|
           | 2 | 4 | 5 |
           |-----------|
           |   | 6 | 7 |
           |-----------|
           | 8 | 1 | 3 |
           |-----------|
           
           """

        StateSpace.__init__(self, action, gval, parent)

#<<<8-Puzzle: build your state representation from the passed data below

        self.state = state
        self.gval = gval
        self.parent = parent


#>>>8-Puzzle: build your state representation from the passed data above

    def successors(self) :
        """Implement the actions of the 8-puzzle search space."""

#<<<8-Puzzle: Your successor state function code below
#   IMPORTANT. The list of successor states returned must be in the ORDER
#   Move blank down move, move blank up, move blank right, move blank left
#   (with some successors perhaps missing, but the remaining ones in this
#   order!

        # Index of the blank square
        i = self.state.index(0)

        next_gval = self.gval + 1

        blank_row = row(i)
        blank_col = col(i)

        succ = []

        # Can blank move down?
        if blank_row != LAST:
          new_state = self._swap_index(i, i + 3)
          succ.append(eightPuzzle("D", next_gval, new_state, self))
          
        # Can blank move up?
        if blank_row != FIRST:
          new_state = self._swap_index(i, i - 3)
          succ.append(eightPuzzle("U", next_gval, new_state, self))

        # Can blank move right?
        if blank_col != LAST:
          new_state = self._swap_index(i, i + 1)
          succ.append(eightPuzzle("R", next_gval, new_state, self))

        # Can blank move left?
        if blank_col != FIRST:
          new_state = self._swap_index(i, i - 1)
          succ.append(eightPuzzle("L", next_gval, new_state, self))

        return succ

    def _swap_index(self, i, j):
      """Return the list with the values with locations i and j swapped"""

      new_state = []
      new_state.extend(self.state)
      new_state[i], new_state[j] = new_state[j], new_state[i]
      return new_state

#>>>8-Puzzle: Your successor state function code above


    def hashable_state(self):
#<<<8-Puzzle: your hashable_state implementation below
      return tuple(x for x in self.state)
#>>>8-Puzzle: your hashable_state implementation above

    def print_state(self):
        if self.parent:
            print "Action= \"{}\", S{}, g-value = {}, (From S{})".format(self.action, self.index, self.gval, self.parent.index)
        else:
            print "Action= \"{}\", S{}, g-value = {}, (Initial State)".format(self.action, self.index, self.gval)

#<<<8-Puzzle: print the state in an informative way below
        print self.state[0:3]
        print self.state[3:6]
        print self.state[6:9]

        return 0
#>>>8-Puzzle: print the state in an informative way above


def row(i):
  """Return the row of index i."""
  if i <= 2:
    return FIRST
  elif i <= 5:
    return MIDDLE
  else:
    return LAST

def col(i):
  """Return the column of index i."""  
  if i % 3 == 0:
    return FIRST
  elif i % 3 == 1:
    return MIDDLE
  else:
    return LAST


#<<<8-Puzzle: below you will place your implementation of the misplaced 
#tiles heuristic and the manhattan distance heuristic
#You can alter any of the routines below to aid in your implementation. 
#However, mark all changes between 
#<<<8-Puzzle ... and >>>8-Puzzle tags.
#>>>8-Puzzle

eightPuzzle.goal_state = False

def eightPuzzle_set_goal(state):
    '''set the goal state to be state. Here state is a list of 9
       numbers in the same format as eightPuzzle.___init___'''
    eightPuzzle.goal_state = state
#<<<8-Puzzle: store additional information if wanted below

#>>>8-Puzzle: store additional information if wanted above

def eightPuzzle_goal_fn(puzzle_state):
#Assume that the goal is a fully specified state.
#<<<8-Puzzle: your implementation of the goal test function below
    return puzzle_state.state == eightPuzzle.goal_state
#>>>8-Puzzle: your implementation of the goal test function above

def h0(state):
    #a null heuristic (always returns zero)
    return 0

def h_misplacedTiles(puzzle_state):
    #return a heurstic function that given as state returns the number of
    #tiles (NOT INCLUDING THE BLANK!) in that state that are
    #not in their goal position 

#<<<8-Puzzle: your implementation of this function below

    state = puzzle_state.state
      
    misplaced = 0

    for i in range(len(state)):
      if state[i] != 0 and state[i] != eightPuzzle.goal_state[i]:
        misplaced += 1
    
    return misplaced

#>>>8-Puzzle: your implementation of this function above
    
def h_MHDist(puzzle_state):
    #return a heurstic function that given as state returns 
    #the sum of the manhattan distances each tile (NOT INCLUDING
    #THE BLANK) is from its goal configuration. 
    #The manhattan distance of a tile that is currently in row i column j
    #and that has to be in row i" j" in the goal is defined to be
    #  abs(i - i") + abs(j - j")
#<<<8-Puzzle: your implementation of this function below

    state = puzzle_state.state
    #state = puzzle_state

    sum_mh_distances = 0

    for t in range(len(state)):

      tile = state[t]

      if tile == 0:
        continue
      
      goal_index = eightPuzzle.goal_state.index(tile)

      goal_row = row(goal_index)
      goal_col = col(goal_index)

      curr_row = row(t)
      curr_col = col(t)

      #print tile, "|", goal_row, goal_col, "|", curr_row, curr_col

      sum_mh_distances += abs(curr_row - goal_row) + abs(curr_col - goal_col)
 

    return sum_mh_distances

#>>>8-Puzzle: your implementation of this function above


#<<<8-Puzzle: Make sure the sample code below works when it is uncommented

if __name__ == '__main__':

  
  se = SearchEngine('astar')
  #se.cycle_check_off()
  #se.path_check_on()
  #s0 = eightPuzzle("START", 0, [1, 0, 2, 3, 4, 5, 6, 7, 8])
  eightPuzzle_set_goal([0, 1, 2, 3, 4, 5, 6, 7, 8])
  #se.search(s0, eightPuzzle_goal_fn, h0)
  #se.search(s0, eightPuzzle_goal_fn, h_misplacedTiles)
  s1 = eightPuzzle("START", 0, [8, 7, 6, 0, 4, 1, 2, 5, 3])
  se.search(s1, eightPuzzle_goal_fn, h_MHDist)
  se.set_strategy('astar')
  se.cycle_check_on()
  se.path_check_off()
  se.search(s1, eightPuzzle_goal_fn, h_MHDist)

  se.search(s1, eightPuzzle_goal_fn, h_misplacedTiles)
  #se.set_strategy('astar')
  #se.search(s1, eightPuzzle_goal_fn, h_misplacedTiles)
  



#>>>8-Puzzle: Make sure the sample code above works when it is uncommented

#<<<8-Puzzle: IMPORTANT. CHECK the website. Some additional problems and
#   questions will be posted for you to run your 8-puzzle code on.
#>>>8-Puzzle:
