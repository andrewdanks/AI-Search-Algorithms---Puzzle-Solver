'''
EXAMPLE STATESPACE WATERJUGS

States in the waterjugs problem can be represented by two integers, (gal3,gal4), where gal3 is the amount of water
in the 3 gallon jug, and gal4 is the amount of water in the 4 gallon jug.

'''
#from search import *
from search_pc import *
#from id_astar import *

class WaterJugs(StateSpace):

    StateSpace.n = 0
    
    def __init__(self, action, gval, gal3, gal4, parent = None):
        StateSpace.__init__(self, action, gval, parent)
        self.gal3 = gal3
        self.gal4 = gal4
        
    def successors(self):
        """We have x actions, (1) empty the gal3, (2) fill the gal3,
        (3) empty the gal4, (4) fill the gal4 (5) pour the
        gal3-->gal4, (6) pour the gal4-->gal3.  all actions have cost
        1.  in computing the list of successor states, however, make
        sure we don't return a state equal to self as this is a null
        transtion."""

        States = list()
        if self.gal3 > 0 :
            States.append( WaterJugs('Empty 3 Gallon', self.gval+1, 0, self.gal4, self) )
        if self.gal3 < 3 :
            States.append( WaterJugs('Fill 3 Gallon', self.gval+1, 3, self.gal4, self) )
        if self.gal4 > 0 :
            States.append( WaterJugs('Empty 4 Gallon', self.gval+1, self.gal3, 0, self) )
        if self.gal4 < 4 :
            States.append( WaterJugs('Fill 4 Gallon', self.gval+1, self.gal3, 4, self) )
        if self.gal4 < 4 and self.gal3 > 0:
            maxpour = min( 4 - self.gal4, self.gal3 ) #at most can only fill up 4 gallon
            States.append( WaterJugs('Pour 3 into 4', self.gval+1, self.gal3-maxpour, self.gal4+maxpour, self) )
        if self.gal3 < 3 and self.gal4 > 0:
            maxpour = min( 3 - self.gal3, self.gal4 ) #at most can only fill up 3 gallon
            States.append( WaterJugs('Pour 4 into 3', self.gval+1, self.gal3+maxpour, self.gal4-maxpour, self) )
        return States
    
    def hashable_state(self) :
        return (self.gal3, self.gal4)

    def print_state(self):
        if self.parent:
            print "Action= \"{}\", S{}, g-value = {}, (3gal, 4gal) = ({},{}), (From S{})".format(self.action, self.index, self.gval, self.gal3, self.gal4, self.parent.index)
        else:
            print "Action=\"{}\", S{}, g-value = {}, (3gal, 4gal) = ({},{}), (Initial state)".format(self.action, self.index, self.gval, self.gal3, self.gal4)

 
#Some auxillary heuristic functions and goal test functions.

#We use this to store the current goal
#So that the heuristics functions can get access to it
WaterJugs.goal_state = False


def waterjugs_set_goal(gal3, gal4):
    '''set the current goal'''
    WaterJugs.goal_state = (gal3, gal4)


def waterjugs_goal_fn(state):
    '''test if the state is equal to the current goal,
    allow wild cards '*' in the goal state'''
    return ((WaterJugs.goal_state[0] == '*' or 
             state.gal3 == WaterJugs.goal_state[0]) and
            (WaterJugs.goal_state[1] == '*' or 
             state.gal4 == WaterJugs.goal_state[1]))

def waterjugs_h_sum_function(state):
    hval = 0
    if WaterJugs.goal_state[0] != '*':
        hval = hval + abs(WaterJugs.goal_state[0] - state.gal3)
    if WaterJugs.goal_state[1] != '*':
        hval = hval + abs(WaterJugs.goal_state[1] - state.gal4)
    return hval

def waterjugs_h_max_function(state):
    hval = 0
    if WaterJugs.goal_state[0] != '*':
        hval = abs(WaterJugs.goal_state[0] - state.gal3)
    if WaterJugs.goal_state[1] != '*':
        hval = max(hval,abs(WaterJugs.goal_state[1] - state.gal4))
    return hval

def waterjugs_h_total_diff_function(state):
    hval = 0
    if WaterJugs.goal_state[0] != '*':
        wsum = WaterJugs.goal_state[0]
    if WaterJugs.goal_state[1] != '*':
        wsum = wsum + WaterJugs.goal_state[1]
    return abs(state.gal3+state.gal4 - wsum)



if __name__ == '__main__':


    se = SearchEngine('depth_first')

    se.cycle_check_off()
    se.path_check_on()

    waterjugs_set_goal(3, 2)

    # DFS with path checking
    s0 = WaterJugs("START", 0, 0, 0)
    se.search(s0, waterjugs_goal_fn, waterjugs_h_sum_function)

    se.cycle_check_on()
    se.path_check_off()

    # DFS with cycle checking
    s1 = WaterJugs("START", 0, 0, 0)
    se.search(s0, waterjugs_goal_fn, waterjugs_h_sum_function)

    se.set_strategy('breadth_first')

    se.cycle_check_off()
    se.path_check_on()

    # BFS with path checking
    s2 = WaterJugs("START", 0, 0, 0)
    se.search(s2, waterjugs_goal_fn, waterjugs_h_sum_function)

    se.cycle_check_on()
    se.path_check_off()

    # BFS with cycle checking
    s3 = WaterJugs("START", 0, 0, 0)
    se.search(s3, waterjugs_goal_fn, waterjugs_h_sum_function)


