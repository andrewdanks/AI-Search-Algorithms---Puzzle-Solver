#Look for <<<...>>> tags in this file. These tags indicate changes in the 
#file to implement the required routines. Some mods have been made some others
#you have to make. Don't miss addressing each <<<...>>> tag in the file!


'''
Missionaries and Cannibals STATESPACE 

States: the number of missionaries and cannibals on each side, and which
side the boat is on.

Actions: move up to 2 people to the other side, along with the boat.

Initial State: all people and the boat are on the left side.

Goal: have everyone on the right side without ever having cannibals
outnumber missionaries on either side.
'''
#from search import *
#from search_pc import *
from id_astar import *

class mc(StateSpace):

    StateSpace.n = 0
    
    def __init__(self, action, gval, Boat, ML, CL, parent = None):
        """Given the number of missionaries on the left (ML) and the
        number of cannibals on the left (CL) and the location of the
        boat (Boat). Generate a state.  Boat is a value 'L' or 'R'
        indicating left or right bank, ML and CL are any of the values
        0, 1, 2, or 3. 

        Note you can represent the state in any way you want, but the
        init routine must take these arguments (from which you can
        compute your own state representation)."""

        StateSpace.__init__(self, action, gval, parent)

        if self._illegal_params(ML, CL, Boat):
            print "Error in mc init state. Illegal parameters passed"
        else:
            self.CL = CL
            self.ML = ML
            self.B = Boat
            self.gval = gval
            self.parent = parent

    def _illegal_params(self, ML, CL, Boat):
        return ML < 0 or ML > 3 or CL < 0 or CL > 3 or (Boat != 'L' and Boat != 'R')

    def successors(self) :
        """Implement the five actions of the mc search space. Ensure
        that an illegal state is not generated (i.e., the missionaries
        must never be outnumbered by the cannibals on either side"""

        # A list of all possible successor states
        ret = []

        next_B = 'R' if self.B is 'L' else 'R'
        next_gval = self.gval + 1

        # Each [C,M] in moves represents the number of cannibals
        # and missionaries that move to next_B, respectively.
        moves = [[0,1], [1,0], [2,0], [0,2], [1,1]]

        for n in moves:

            # The name of the action
            name = str(n[0]) + 'C' + str(n[1]) + 'M->' + next_B

            # If the boat is moving to the right, we're subtracting
            # people from the left side.
            if next_B is 'R':
                n[0] *= -1
                n[1] *= -1

            next_CL = self.CL + n[0]
            next_ML = self.ML + n[1]

            # Check if this was a legal move and make sure missionaries are not outnumbered
            if self._illegal_params(next_ML, next_CL, next_B) or missionaries_outnumbered(next_ML, next_CL):
                continue

            new_state = mc(name, next_gval, next_B, next_ML, next_CL, self)
            ret.append(new_state)

        return ret


    def hashable_state(self) :
        return (self.B, self.ML, self.CL)

    def print_state(self):
        print str(self.CL) + "C left, " + str(3-self.CL) + "C right",
        print str(self.ML) + "M left, " + str(3-self.ML) + "M right,",
        print "B" + self.B
        

def missionaries_outnumbered(ML, CL):
    """Returns True if cannibals ever outnumber missionaries"""
    MR = 3 - ML
    CR = 3 - CL
    return ((CL > ML) and ML > 0) or ((CR > MR) and MR > 0)

#Some auxillary heuristic functions and goal test functions.

def h0(state):
    #a null heuristic is fine (always returns zero)
    return 0

def mc_set_goal(boat, ML, CL):
    '''set the current goal. boat = 'L' or 'R', ML and CL are the
    numbers of missionaries and cannibals on the left hand side, 
    ML-3, CL-3 are the numbers on the right hand side'''
    mc.goal_state = (boat, ML, CL)

def mc_goal_fn(state):
    return mc.goal_state == (state.B, state.ML, state.CL)




if __name__ == '__main__':

    se = SearchEngine('depth_first')
    mc_set_goal('R', 0, 0)

    # DFS w/ cycle checing
    s0 = mc("START", 0, 'L', 3, 3)
    se.search(s0, mc_goal_fn, h0)

    # BFS w/ cycle checing
    se.set_strategy('breadth_first')
    s1 = mc("START", 0, 'L', 3, 3)
    se.search(s1, mc_goal_fn, h0)

    se.cycle_check_off()

    # BFS w/o cycle checing
    s1 = mc("START", 0, 'L', 3, 3)
    se.search(s1, mc_goal_fn, h0)

    # DFS w/o cycle checing
    se.set_strategy('depth_first')
    s1 = mc("START", 0, 'L', 3, 3)
    se.search(s1, mc_goal_fn, h0)
    

#<<<MC: Make sure the sample code below works when it is uncommented
# se = SearchEngine('breadth_first')
# s0 = mc("START", 0, 'L', 3, 3)
# mc_set_goal('R', 0, 0)
# se.search(s0, mc_goal_fn, h0)
# s1 = mc("START", 0, 'R', 3, 3)
# se.search(s1, mc_goal_fn, h0)
# s2 = mc("START", 0, 'R', 0, 0)
# mc_set_goal('L', 3, 3)
# se.search(s2, mc_goal_fn, h0)
#>>>MC: Make sure the sample code above works when it is uncommented
