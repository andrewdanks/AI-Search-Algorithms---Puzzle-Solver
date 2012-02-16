#Look for <<<...>>> tags in this file. These tags indicate changes in the 
#file to implement the required routines. Some mods have been made some others
#you have to make. Don't miss addressing each <<<...>>> tag in the file!

'''Search routines.
   A) Class StateSpace

      An abstract base class for representing the states in a search
      space.  Each state has a pointer to the parent that was used to
      generate it, and the cost of g-value of the sequence of actions
      that was used to generate it.

      Equivalent states can be reached via different paths, so to
      avoid exploring the same state multiple times the search
      routines employ cycle checking using hashing techniques. Hence,
      each StateSpace state (or object) must be able to return an
      immutable representation that uniquely represents the state and
      can be used to index into a dictionary.

      The StateSpace class must be specialized for the particular problem. Each
      particular problem will define a subclass of StateSpace that will also
      include information specific to that problem. See WaterJugs.py for an
      example, and the Class implementation for more details.


    B) class SearchEngine

      objects of this class define the search routines. They utilize
      two auxiliary classes (1) Class sNode---the objects of this class
      are used to represent nodes in the search space (these nodes
      contain problem states, i.e., StateSpace objects but they are
      search nodes not states of the state space.  (2) Class
      Open---these objects are used to store the set of unexpanded
      nodes. These objects are search strategy specific. For example,
      Open is implemented as a stack when doing depth-first search, as
      a priority queue when doing astar search etc.

      The main routines that the user will employ are in the SearchEngine class.
      These include the ability to set the search strategy, and to invoke
      search (using the search method). See the implementation for details. 

    '''
import heapq
from collections import deque
import os


class StateSpace:
    '''Abstract class for defining State spaces for search routines'''
    n = 0
    path = dict()
    
    def __init__(self, action, gval, parent):
        '''Problem specific state space objects must always include the data items
           a) self.action === the name of the action used to generate
              this state from parent. If it is the initial state a good
              convention is to supply the action name "START"
           b) self.gval === a number (integer or real) that is the cost
              of getting to this state.
           c) parent the state from which this state was generated (by
              applying "action"
           d)... other problem specific data used to specify the state in
                 this specific state space.
        '''
        self.action = action
        self.gval = gval
        self.parent = parent
        self.index = StateSpace.n
        StateSpace.n = StateSpace.n + 1

    def successors(self):
        '''This method when invoked on a state space object must return a
           list of successor states, each with the data items "action"
           the action used to generate this successor state, "gval" the
           gval of self plus the cost of the action, and parent set to self.
           Also any problem specific data must be specified property.'''
        
        print "Must be over ridden."

    def hashable_state(self):
        '''This method must return an immutable and unique representation
           of the state represented by self. The return value, e.g., a
           string or tuple, will be used by hashing routines. So if obj1 and
           obj2, both StateSpace objects then obj1.hashable_state() == obj2.hashable_state()
           if and only if obj1 and obj2 represent the same problem state.'''

        print "Must be over ridden."

    def print_state(self):
        '''Print a representation of the state'''
        print "Must be over ridden."

    def print_path(self):
        '''print the sequence of actions used to reach self'''
        #can be over ridden to print problem specific information
        s = self
        states = []
        while s:
            states.append(s)
            s = s.parent
        states.pop().print_state()
        while states:
            print " ==> ",
            states.pop().print_state()
        print ""
 
    def has_path_cycle(self):
        '''Returns true if self is equal to a prior state on its path'''
#<<<PATH CHECK: Implement has_path_cycle below
        p = self.parent
        while p:
          if p.hashable_state() == self.hashable_state():
            return True
          p = p.parent
        return False
#>>>PATH CHECK: Implement has_path_cycle above


#Constants to denote the search strategy. 
DEPTH_FIRST = 0
BREADTH_FIRST = 1
BEST_FIRST = 2
ASTAR = 3
#<<<IDASTAR: Modification below
IDASTAR = 4
#>>>IDASTAR: Modification above

#For best first and astar we use a priority queue. This requires
#a comparison function for nodes. These constants indicate if we use
#the gval, the hval or the sum of gval and hval in the comparison.
SUM_HG = 0
H = 1
G = 2

class sNode:
    '''Object of this class form the nodes of the search space.  Each
    node consists of a search space object (determined by the problem
    definition) along with the h and g values (the g values is
    redundant as it is stored in the state, but we make a copy in the
    node object for convenience), and a the number of the node'''
    
    n = 0
    lt_type = SUM_HG
    
    def __init__(self, state, hval):
        self.state = state
        self.hval = hval
        self.gval = state.gval
        self.index = sNode.n
        sNode.n = sNode.n + 1

    def __lt__(self, other):
        '''For astar and best first we muse a priority queue for the
           OPEN set. This queue stores search nodes waiting to be
           expanded. Thus we need to define a node1 < node2 function
           by defining the __lt__ function. Dependent on the type of
           search this comparison function compares the h-value, the
           g-value or the f-value of the nodes. Note for the f-value
           we wish to break ties by letting node1 < node2 if they both
           have identical f-values but if node1 has a GREATER g
           value. This means that we expand nodes along deeper paths
           first causing the search to proceed directly to the goal'''
        
        if sNode.lt_type == SUM_HG:
            if (self.gval+self.hval) == (other.gval+other.hval):
                #break ties by greatest gval. 
                return self.gval > other.gval
            else: return ((self.gval+self.hval) < (other.gval+other.hval))
        if sNode.lt_type == G:
            return self.gval < other.gval
        if sNode.lt_type == H:
            return self.hval < other.hval
        print 'sNode class has invalid comparator setting!'
        #return default of lowest gval (generating breadth first behavior)
        return self.gval < other.gval

class Open:
    '''Open objects hold the search frontier---the set of unexpanded
       nodes. Depending on the search strategy used we want to extract
       nodes from this set in different orders, so set up the object's
       functions to operate as needed by the particular search
       strategy'''
    
    def __init__(self, search_strategy):
        if search_strategy == DEPTH_FIRST:
            #use stack for OPEN set (last in---most recent successor
            #added---is first out)
            self.open = []
            self.insert = self.open.append
            self.extract = self.open.pop
        elif search_strategy == BREADTH_FIRST:
            #use queue for OPEN (first in---earliest node not yet
            #expanded---is first out)
            self.open = deque()
            self.insert = self.open.append
            self.extract = self.open.popleft
        elif search_strategy == BEST_FIRST:
            #use priority queue for OPEN (first out is node with
            #lowest hval)
            self.open = []
            #set node less than function to compare hvals only
            sNode.lt_type = H
            self.insert = lambda node: heapq.heappush(self.open, node)
            self.extract = lambda: heapq.heappop(self.open)
        elif search_strategy == ASTAR:
            #use priority queue for OPEN (first out is node with
            #lowest fval = gval+hval)
            self.open = []
            #set node less than function to compare sums of hval and gval
            sNode.lt_type = SUM_HG
            self.insert = lambda node: heapq.heappush(self.open, node)
            self.extract = lambda: heapq.heappop(self.open)
#<<<IDASTAR: Implement the right open data structure for IDASTAR below
        elif search_strategy == IDASTAR:
            self.open = []
            self.insert = self.open.append
            self.extract = self.open.pop
#>>>IDASTAR: Implement the right open data structure for IDASTAR above

    def empty(self): return not self.open

    def print_open(self):
        print "{",
        if len(self.open) == 1: 
            print "   <S{}:{}, g={}, h={}, f=g+h={}>".format(self.open[0].state.index, self.open[0].state.hashable_state(), self.open[0].gval, self.open[0].hval, self.open[0].gval+self.open[0].hval),
        else:
            for nd in self.open:
                print "   <S{}:{}, g={}, h={}, f=g+h={}>".format(nd.state.index, nd.state.hashable_state(), nd.gval, nd.hval, nd.gval+nd.hval),
        print "}"

class SearchEngine:
    def __init__(self, strategy = 'depth_first'):
        self.set_strategy(strategy)
        self.trace = 0
        self.cycle_check = True  #Default do cycle check.
#<<<PATH CHECK:Initialize path_check
        self.path_check = False #Default not path checking
#>>>PATH CHECK: Initialize path_check

    def initStats(self):
        sNode.n = 0
        StateSpace.n = 1    #initial state already generated on call so search
        self.cycle_check_pruned = 0
        #<<<PATH CHECK: Keep track of number of nodes pruned
        self.path_check_pruned = 0
        #>>>PATH CHECK: Keep track of number of nodes pruned
        self.total_search_time = os.times()[0]        

    def trace_on(self, level = 1):
        '''For debugging, set tracking level 1 or 2'''
        self.trace = level

    def trace_off(self):
        '''Turn off tracing'''
        self.trace = 0

#<<<IDASTAR: Modification below
    def set_strategy(self, s):
        if not s in ['depth_first', 'breadth_first', 'best_first', 'astar', 'id_astar']:
            print 'Unknown search strategy specified:', s
            print "Must be one of 'depth_first', 'breadth_first', 'best_first', 'astar', or 'id_astar'"
        else:
            if   s == 'depth_first'  : self._strategy = DEPTH_FIRST
            elif s == 'breadth_first': self._strategy = BREADTH_FIRST
            elif s == 'best_first'   : self._strategy = BEST_FIRST
            elif s == 'astar'        : self._strategy = ASTAR
            elif s == 'id_astar'     : self._strategy = IDASTAR


    def get_strategy(self):
        if   self._strategy == DEPTH_FIRST    : return 'depth_first'
        elif self._strategy == BREADTH_FIRST  : return 'breadth_first'
        elif self._strategy == BEST_FIRST     : return 'best_first' 
        elif self._strategy == ASTAR          : return 'astar'
        elif self._strategy == IDASTAR        : return 'id_astar' 

#>>>IDASTAR: Modification above

    def cycle_check_on(self):
        self.cycle_check = True

    def cycle_check_off(self):
        self.cycle_check = False

#<<<PATH CHECK: Turn path checking on and off below (already impemented)

    def path_check_on(self):
        self.path_check = True


    def path_check_off(self):
        self.path_check = False

#>>>PATH CHECK: Turn path checking on and off above


    def search(self, initState, goal_fn, heur_fn):
#<<<IDASTAR: Implement changes to search to allow for for IDA* search
#MARK ALL OF YOUR CHANGES BETWEEN COMMENT LINES STARTING WITH '#<<<IDASTAR:'
#AND ENDING WITH '#>>>IDASTAR: '
#>>>IDASTAR: 
#Also include your implementation of path checking so that IDASTAR also allows
#for path checking.

        #Perform cycle checking as follows
        #a. check state before inserting into OPEN. If we had already reached
        #   the same state via a cheaper path, don't insert into OPEN.
        #b. Sometimes we find a new cheaper path to a state (after the older
        #   more expensive path to the state has already been inserted.
        #   We deal with this lazily. We check states extracted from OPEN
        #   and if we have already expanded that state via a cheaper path
        #   we don't expand it. If we had expanded the state via a more
        #   expensive path, we re-expand it.
     
    ###INIT the Search
        self.initStats()

        #BEGIN TRACING
        if self.trace:
            print "   TRACE: Search Strategy: ", self.get_strategy()
            print "   TRACE: Initial State:",
            initState.print_state()
        #END TRACING
        
        if self.cycle_check: self.cc_dictionary = dict() 

        OPEN = Open(self._strategy)
        
        node = sNode(initState, heur_fn(initState))
        #the cycle check dictionary stores the cheapest path (g-val) found
        #so far to a state. 
        if self.cycle_check: self.cc_dictionary[initState.hashable_state()] = initState.gval
        OPEN.insert(node)

        #<<<IDASTAR: Set the initial bound for f-cost
        if self._strategy == IDASTAR:
          self.initState = initState
          self.root = node
          OPEN.cur_bound = initState.gval + heur_fn(initState)
        #>>>IDASTAR: Set the initial bound for f-cost

    ###NOW do the search and return the result
        goal_node = self.searchOpen(OPEN, goal_fn, heur_fn)
        if goal_node:
            print "============================"
            print "Search Successful! Solution cost = {}, Goal state:".format(goal_node.gval)
            print "    ",
            goal_node.state.print_state()
            print "----------------------------"
            print "Solution Path:"
            goal_node.state.print_path()
            self.total_search_time = os.times()[0] - self.total_search_time
            print "----------------------------"
            print "Search time = {}, nodes expanded = {}, states generated = {}, states cycle/path check pruned = {}".format(self.total_search_time,sNode.n, StateSpace.n, self.cycle_check_pruned)
            return goal_node.state
        else:
        #exited the while without finding goal---search failed
            print "============================"
            print "Search Failed! No solution found"
            self.total_search_time = os.times()[0] - self.total_search_time
            print "----------------------------"
            print "Search time = {}, nodes expanded = {}, states generated = {}, states cycle/path check pruned = {}".format(self.total_search_time,sNode.n, StateSpace.n, self.cycle_check_pruned)
            return False

    def searchOpen(self, OPEN, goal_fn, heur_fn):
        '''Open has some nodes on it, now search from that state of OPEN'''

        #BEGIN TRACING
        if self.trace:
            print "   TRACE: Initial OPEN: ", OPEN.print_open()
            if self.cycle_check: print "   TRACE: Initial CC_Dict:", self.cc_dictionary
        #END TRACING

        #<<<IDASTAR:
        if self._strategy == IDASTAR:
          smallest_discarded_f_cost = None
        #>>>IDASTAR:

        while not OPEN.empty():
            node = OPEN.extract()

            #BEGIN TRACING
            if self.trace:
                print "   TRACE: Next State to expand: <S{}:{}, g={}, h={}, f=g+h={}>".format(node.state.index, node.state.hashable_state(), node.gval, node.hval, node.gval+node.hval)
                if node.state.gval != node.gval:
                    print "ERROR: Node gval not equal to state gval!"
            #END TRACING
                        
            if goal_fn(node.state):
                #node at front of OPEN is a goal...search is completed.
                return node

            #All states reached by a search node on OPEN have already
            #been hashed into the self.cc_dictionary. However,
            #before expanding a node we might have already expanded
            #an equivalent state with lower g-value. So only expand
            #the node if the hashed g-value is no greater than the
            #node's current g-value. 

            #BEGIN TRACING
            if self.trace:
                if self.cycle_check: print "   TRACE: CC_dict gval={}, node.gval={}".format(self.cc_dictionary[node.state.hashable_state()], node.gval)
            #END TRACING

            if (not self.cycle_check or self.cc_dictionary[node.state.hashable_state()] >= node.gval): 
                #note cycle checking is done lazily---when we remove node from OPEN
                successors = node.state.successors()

                #BEGIN TRACING
                if self.trace:
                    print "   TRACE: Expanding Node. Successors = {",
                    for ss in successors:
                        print "<S{}:{}, g={}, h={}, f=g+h={}>, ".format(ss.index, ss.hashable_state(), ss.gval, heur_fn(ss), ss.gval+heur_fn(ss)),
                    print "}"
                #END TRACING

                for succ in successors:
                    hash_state = succ.hashable_state()

                    #BEGIN TRACING
                    if self.trace > 1:
                        print "   TRACE: Successor State:",
                        print "<S{}:{}, g={}, h={}, f=g+h={}>, ".format(succ.index, succ.hashable_state(), succ.gval, heur_fn(succ), succ.gval+heur_fn(succ)),
                        if self.cycle_check and hash_state in self.cc_dictionary:
                            print "   TRACE: Already in CC_dict, CC_dict gval={}, successor state gval={}".format(self.cc_dictionary[hash_state], succ.gval)
                    #END TRACING

                    #<<<IDASTAR: Compare f-cost with current bound
                    if self._strategy == IDASTAR:
                      f_cost = node.gval + node.hval
                      if f_cost > OPEN.cur_bound:
                        if f_cost < smallest_discarded_f_cost or smallest_discarded_f_cost is None:
                          smallest_discarded_f_cost = f_cost
                        continue
                    #>>>IDASTAR: Compare f-cost with current bound

                    if (not self.path_check or not succ.has_path_cycle()) and (not self.cycle_check or not (hash_state in self.cc_dictionary) or (succ.gval < self.cc_dictionary[hash_state])):
                        
                        #this is the first path to succ's state or it is a cheaper path than found before
                        #so add it to open (stored in a new search node)                   
                        OPEN.insert(sNode(succ, heur_fn(succ)))
                            #record cost of this path in dictionary.
                        if self.cycle_check: self.cc_dictionary[hash_state] = succ.gval

                       #BEGIN TRACING
                        if self.trace > 1:
                            print " TRACE: Successor State added to OPEN"
                       #END TRACING

                    else:
                      self.cycle_check_pruned = self.cycle_check_pruned + 1
                     #BEGIN TRACING
                      if self.trace > 1:
                          print "   TRACE: Successor State rejected by cycle/path checking"
                     #END TRACING

                #BEGIN TRACING
                if self.trace > 1:
                     print "   TRACE: Updated OPEN: ", OPEN.print_open()
                     if self.cycle_check: print "   TRACE: Updated CC_Dict:", self.cc_dictionary
                     if self._strategy == IDASTAR: print "Updated cur_bound and smallest_not_explored: ", OPEN.cur_bound, OPEN.smallest_not_explored
                #END TRACING

            else:
                self.cycle_check_pruned = self.cycle_check_pruned + 1

                #BEGIN TRACING
                if self.trace:
                    print "   TRACE: Rejected Node---expanded cheaper path already"
                #END TRACING
            
            #<<<IDASTAR: Start a new search round with the new bound
            if self._strategy == IDASTAR and OPEN.empty():
              OPEN.insert(self.root)
              OPEN.cur_bound = smallest_discarded_f_cost
              smallest_discarded_f_cost = None
              # in case someone strangely has cycle check on:
              if self.cycle_check:
                self.cc_dictionary = dict()
                self.cc_dictionary[self.initState.hashable_state()] = self.initState.gval
            #>>>IDASTAR: Start a new search round with the new bound

              
        return False
            
