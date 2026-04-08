# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.
    DFS (Depth-First Search) is an algorithm that explores as deeply as possible 
    along each branch before backtracking to explore alternative paths.
    """
    
    # ===================================================================
    # 1. STATE REPRESENTATION
    # ===================================================================
    # Each search node is represented as a (state, path) tuple:
    # - state: the current position (e.g., (x, y) coordinates)
    # - path: the sequence of actions from the start to the current state
    
    start_state = problem.getStartState()
    start_node = (start_state, [])  # (state, path)
    
    # ===================================================================
    # 2. EXPLORATION
    # ===================================================================
    # DFS uses a LIFO (Last In, First Out) strategy.
    # It explores the most recently added nodes first by using a stack.
    
    from util import Stack
    stack = Stack()  # Stack to store nodes to be explored
    stack.push(start_node)
    
    # Set to record visited states (to avoid revisiting nodes in graph search)
    explored = set()
    
    print(f"Starting DFS: Start state = {start_state}")
    
    # ===================================================================
    # 3. SEARCH ALGORITHM
    # ===================================================================
    
    while not stack.isEmpty():
        # Pop the node from the stack (deepest node = most recently added)
        current_state, path = stack.pop()
        
        # Check if the current state is the goal
        if problem.isGoalState(current_state):
            print(f"DFS Complete: Goal found! Path length = {len(path)}")
            return path
        
        # Skip if this state has already been explored (graph search)
        if current_state in explored:
            continue
            
        # Mark the current state as explored
        explored.add(current_state)
        
        # Generate all successor nodes from the current state
        # Example: if current_state = (5, 5),
        # successors = [((5, 6), 'North', 1), ((6, 5), 'East', 1), ...]
        successors = problem.getSuccessors(current_state)
        
        # Push successors to the stack (in reverse order to preserve correct traversal order)
        for next_state, action, step_cost in reversed(successors):
            # Only add states that haven't been explored yet
            if next_state not in explored:
                # New path = current path + new action
                new_path = path + [action]
                new_node = (next_state, new_path)
                stack.push(new_node)
    
    # If no solution is found
    print("DFS failed: Goal is unreachable.")
    return []
    

def breadthFirstSearch(problem):
    """
    Search the shallowest nodes in the search tree first.

    BFS (Breadth-First Search) is an algorithm that explores nodes 
    in order of their distance from the start state. It guarantees the shortest path.
    """
    
    # ===================================================================
    # 1. STATE REPRESENTATION
    # ===================================================================
    # Each search node is represented as a (state, path) tuple:
    # - state: the current position (e.g., (x, y) coordinates)
    # - path: the sequence of actions from the start to the current state
    
    start_state = problem.getStartState()
    start_node = (start_state, []) # (state, path)
    
    # ===================================================================
    # 2. EXPLORATION
    # ===================================================================
    # BFS uses a FIFO (First In, First Out) strategy.
    # It uses a queue to explore nodes in the order they were added.
    # This ensures that nodes at shallower depths are explored first.
        
    from util import Queue
    queue = Queue()  # Queue to store nodes to be explored
    queue.push(start_node)
    
    explored = set()
    print(f"Starting BFS: Start state = {start_state}")
    
    # ===================================================================
    # 3. SEARCH ALGORITHM
    # ===================================================================
    
    while not queue.isEmpty():
        # Remove the node from the front of the queue (shallowest node)
        current_state, path = queue.pop()
        
        if problem.isGoalState(current_state):
            print(f"BFS Complete: Goal found! Path length = {len(path)}")
            return path
        
        if current_state in explored:
            continue
        explored.add(current_state)
        
        successors = problem.getSuccessors(current_state)
        
        # Add successors to the queue
        for next_state, action, step_cost in successors:
            if next_state not in explored:
                new_path = path + [action]
                new_node = (next_state, new_path)
                queue.push(new_node)
    
    print("BFS failed: Goal is unreachable.")
    return []


def uniformCostSearch(problem):
    """
    Search the node of least total cost first.
    
    UCS (Uniform Cost Search) is an algorithm that always expands
    the node with the lowest cumulative path cost. 
    It uses a priority queue ordered by total cost from the start state.
    """
    
    # ===================================================================
    # 1. STATE REPRESENTATION
    # ===================================================================
    # Each search node is represented as a (state, path, cost) tuple:
    # - state: the current position (e.g., (x, y) coordinates)
    # - path: the sequence of actions from the start to the current state
    # - cost: the cumulative cost from the start state to the current state
    
    start_state = problem.getStartState()
    start_node = (start_state, [], 0)  # (state, path, cost)
    
    # ===================================================================
    # 2. EXPLORATION
    # ===================================================================
    # UCS uses a priority queue ordered by cumulative path cost.
    # It always expands the node with the lowest total cost first.
    # This guarantees finding the optimal (least-cost) path.
    
    from util import PriorityQueue
    pq = PriorityQueue()  # Priority queue to store nodes to be explored
    pq.push(start_node, 0)  # push(item, priority) — priority = cumulative cost
    
    # Set to record visited states (to avoid revisiting nodes in graph search)
    explored = set()
    
    print(f"Starting UCS: Start state = {start_state}")
    
    # ===================================================================
    # 3. SEARCH ALGORITHM
    # ===================================================================
    
    while not pq.isEmpty():
        # Pop the node with the lowest cumulative cost
        current_state, path, current_cost = pq.pop()
        
        # Check if the current state is the goal
        if problem.isGoalState(current_state):
            print(f"UCS Complete: Goal found! Path length = {len(path)}, Total cost = {current_cost}")
            return path
        
        # Skip if this state has already been explored (graph search)
        if current_state in explored:
            continue
            
        # Mark the current state as explored
        explored.add(current_state)
        
        # Generate all successor nodes from the current state
        # Example: if current_state = (5, 5),
        # successors = [((5, 6), 'North', 1), ((6, 5), 'East', 1), ...]
        successors = problem.getSuccessors(current_state)
        
        # Push successors to the priority queue with their cumulative cost
        for next_state, action, step_cost in successors:
            # Only add states that haven't been explored yet
            if next_state not in explored:
                # New cumulative cost = current cost + step cost
                new_cost = current_cost + step_cost
                new_path = path + [action]
                new_node = (next_state, new_path, new_cost)
                pq.push(new_node, new_cost)  # priority = cumulative cost
    
    # If no solution is found
    print("UCS failed: Goal is unreachable.")
    return []

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0


def bestFirstSearch(problem, heuristic=nullHeuristic):
    """
    Search the node that has the lowest heuristic value first.

    Best-First Search (Greedy) is an algorithm that always expands
    the node which appears closest to the goal according to a heuristic
    function h(n). Unlike UCS, it ignores the cost already paid (g(n)),
    and unlike A*, it does not combine g(n) with h(n).
    It is generally fast but neither complete nor optimal.
    """

    # ===================================================================
    # 1. STATE REPRESENTATION
    # ===================================================================
    # Each search node is represented as a (state, path) tuple:
    # - state: the current position (e.g., (x, y) coordinates)
    # - path:  the sequence of actions from the start to the current state
    #
    # Note: cumulative cost is NOT stored, because Greedy Best-First
    # ranks nodes purely by the heuristic h(n).

    start_state = problem.getStartState()
    start_node = (start_state, [])  # (state, path)

    # ===================================================================
    # 2. EXPLORATION
    # ===================================================================
    # Greedy Best-First uses a priority queue ordered by h(n).
    # The node with the smallest heuristic value is expanded first.

    from util import PriorityQueue
    pq = PriorityQueue()
    pq.push(start_node, heuristic(start_state, problem))

    explored = set()
    print(f"Starting Best-First Search: Start state = {start_state}")

    # ===================================================================
    # 3. SEARCH ALGORITHM
    # ===================================================================

    while not pq.isEmpty():
        # Pop the node with the lowest heuristic value
        current_state, path = pq.pop()

        # Check if the current state is the goal
        if problem.isGoalState(current_state):
            print(f"Best-First Complete: Goal found! Path length = {len(path)}")
            return path

        # Skip if this state has already been explored (graph search)
        if current_state in explored:
            continue

        # Mark the current state as explored
        explored.add(current_state)

        # Generate all successors from the current state
        successors = problem.getSuccessors(current_state)

        # Push successors to the priority queue with priority = h(next_state)
        for next_state, action, step_cost in successors:
            if next_state not in explored:
                new_path = path + [action]
                new_node = (next_state, new_path)
                priority = heuristic(next_state, problem)
                pq.push(new_node, priority)

    # If no solution is found
    print("Best-First Search failed: Goal is unreachable.")
    return []


def aStarSearch(problem, heuristic=nullHeuristic):
    """
    Search the node that has the lowest combined cost and heuristic first.

    A* Search expands the node with the smallest f(n) = g(n) + h(n), where
    - g(n) is the cumulative cost from the start state to n
    - h(n) is the heuristic estimate of the cost from n to the goal
    With an admissible (and consistent) heuristic, A* is both complete
    and optimal, and typically expands fewer nodes than UCS.
    """

    # ===================================================================
    # 1. STATE REPRESENTATION
    # ===================================================================
    # Each search node is represented as a (state, path, cost) tuple:
    # - state: the current position (e.g., (x, y) coordinates)
    # - path:  the sequence of actions from the start to the current state
    # - cost:  g(n), the cumulative cost from the start state to this state

    start_state = problem.getStartState()
    start_node = (start_state, [], 0)  # (state, path, cost)

    # ===================================================================
    # 2. EXPLORATION
    # ===================================================================
    # A* uses a priority queue ordered by f(n) = g(n) + h(n).
    # The priority is the estimated total cost of the cheapest solution
    # passing through the current node.

    from util import PriorityQueue
    pq = PriorityQueue()
    pq.push(start_node, 0 + heuristic(start_state, problem))

    explored = set()
    print(f"Starting A* Search: Start state = {start_state}")

    # ===================================================================
    # 3. SEARCH ALGORITHM
    # ===================================================================

    while not pq.isEmpty():
        # Pop the node with the lowest f(n) = g(n) + h(n)
        current_state, path, current_cost = pq.pop()

        # Check if the current state is the goal
        if problem.isGoalState(current_state):
            print(f"A* Complete: Goal found! Path length = {len(path)}, "
                  f"Total cost = {current_cost}")
            return path

        # Skip if this state has already been explored (graph search)
        if current_state in explored:
            continue

        # Mark the current state as explored
        explored.add(current_state)

        # Generate all successors from the current state
        successors = problem.getSuccessors(current_state)

        # Push successors with priority = g(next_state) + h(next_state)
        for next_state, action, step_cost in successors:
            if next_state not in explored:
                new_cost = current_cost + step_cost          # g(n')
                new_path = path + [action]
                new_node = (next_state, new_path, new_cost)
                priority = new_cost + heuristic(next_state, problem)  # f(n')
                pq.push(new_node, priority)

    # If no solution is found
    print("A* Search failed: Goal is unreachable.")
    return []


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
bestfs = bestFirstSearch