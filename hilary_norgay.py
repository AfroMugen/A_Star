import sys
import math
from queue import PriorityQueue


def main():
    # Check for proper arg amount and heur value 
    if len(sys.argv) < 3:
        print("Warning: Must have 2 args.\nFormat: 'python hilary_norgay.py [filename.txt] [0-2]'\nEx: 'python hilary_norgay.py water_world.txt 0'")
        return
    elif sys.argv[2] not in ['0', '1', '2']:
        print("Warning: Second arg must be integer between 0-2.\nFormat: 'python hilary_norgay.py [filename.txt] [0-2]'\nEx: 'python hilary_norgay.py water_world.txt 0'")
        return

    # Error check opening map file
    try:
        file =  open(sys.argv[1], 'r')
    except IOError:
        print("Error: File does not appear to exist.")
        return

    # Clean map of newline characters
    waterMap = clean(file.readlines())
    # Check if map has valid characters
    if not isValid(waterMap):
        print("Warning: Map found in" + sys.argv[1] + " contains invalid characters.\nCharacters allowed include ['~', '.', ':', 'M', 'S', '0', '1', '2', '3', '4']")
        return
    # List of heuristic functions
    heuristic = [h0, h1, h2]

    # Perform AStar algorithm
    aStar(waterMap, heuristic[int(sys.argv[2])])


def aStar(map, heur):
    """
    Performs A* algorithm on map using heuristic function heur

    Parameter map: map of heights
    Precondition: map is a list of strings

    Parameter heur: heuristic function
    Precondition: heur is a function taking in x, y, z, x1, y1, z1 integers representing coordinates
    """
    # Dictionaries allowing for conversion of symbols to heights and vice versa
    eleHeight = {'~': '0', '.': '1', ':': '2', 'M': '3', 'S': '4'}
    eleSymbol = {'0': '~', '1': '.', '2': ':', '3': 'M', '4': 'S'}
    # List of possible moves
    moves = ((-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1))

    # Set of visited coordinates
    visited = set()
    # Find start and goal coordinates
    start = findStart(map)
    goal = findGoal(map)
    # Dictionary containing states of each coordinate. Input values in format (f(n), previousNode). Used to reconstruct shortest path.
    states = {}
    # Coordinates being considered for the next move, aka "frontier". Input values in format (f(n), c, node)
    frontier = PriorityQueue()
    # Insert starting coordinate into frontier and states
    f = heur(start[1], start[0], int(map[start[0]][start[1]]), goal[1], goal[0], int(eleHeight[map[goal[0]][goal[1]]]), start[0])
    frontier.put((f, 0, start))
    states[start] = (f, None)
    # Replace starting coordinate with corresponding symbol for printing consistency later
    replaceChar(map, start, eleSymbol[map[start[0]][start[1]]])

    # A* algorithm begins
    while not frontier.empty():
        f, c, node = frontier.get()
        # Ignore visited nodes in the case that there are multiple entries of the same coordinate in frontier from intersecting coordinate paths
        if node in visited:
            continue

        # Mark node as visited
        visited.add(node)
        # Goal check. If passed, then print shortest path
        if node == goal:
            printPath(states, map, goal, eleHeight, eleSymbol, 0)
            return

        # Add possible valid moves from current node to frontier
        for coord in moves:
            y1 = node[0] + coord[0]
            x1 = node[1] + coord[1]
            # Check if move is valid
            if (0 <= y1 < len(map)) and (0 <= x1 < len(map[y1])) and (abs(int(eleHeight[map[node[0]][node[1]]]) - int(eleHeight[map[y1][x1]])) <= 1) and ((y1, x1) not in visited):
                c1 = c + 1
                f = c1 + heur(x1, y1, int(eleHeight[map[y1][x1]]), goal[1], goal[0], int(eleHeight[map[goal[0]][goal[1]]]), int(eleHeight[map[node[0]][node[1]]]))
                # Add/Update coord in states with smallest f(n) and corresponding previousNode, i.e. node in current step
                if (y1, x1) in states:
                    if states[(y1, x1)][0] > f:
                        states[(y1, x1)] = (f, node)
                else:
                    states[(y1, x1)] = (f, node)
                frontier.put((f, c1, (y1, x1)))

    print("Goal State is not possible.")


def clean(map):
    """
    Strips map of newline characters

    Parameter map: map of heights
    Precondition: map is a list of strings
    """
    for i in range(len(map)):
        if map[i][-1] == '\n':
            map[i] = map[i][:-1]

    return map


def isValid(map):
    """
    Checks if map contains only valid characters

    Parameter map: map of heights
    Precondition: map is a list of strings
    """
    allowed = set(['~', '.', ':', 'M', 'S', '0', '1', '2', '3', '4'])
    if not map:
        return False
    for row in map:
        for char in row:
            if char not in allowed:
                return False
    
    return True


def findStart(map):
    """
    Finds starting coordinate in map

    Parameter map: map of heights
    Precondition: map is a list of strings
    """
    start = set(['0', '1', '2', '3', '4'])
    for y in range(len(map)):
        for x in range(len(map[y])):
            if map[y][x] in start:
                return (y, x)

def findGoal(map):
    """
    Finds goal coordinate in map (goal state)

    Parameter map: map of heights
    Precondition: map is a list of strings
    """
    for y in range(len(map)):
        for x in range(len(map[y])):
            if map[y][x] == 'S':
                return (y, x)


def replaceChar(map, node, char):
    """
    Replaces character in map with another character

    Parameter map: map of heights
    Precondition: map is a list of strings

    Parameter node: coordinates of character to be changed
    Precondition: node is a tuple of ints. (coordinates such as (1, 3))

    Parameter char: replacement character
    Precondition: char is a string, preferrably of only len 1
    """
    map[node[0]] = map[node[0]][:node[1]] + char + map[node[0]][node[1] + 1:]


def printMap(map, move):
    """
    Prints map

    Parameter map: map of heights
    Precondition: map is a list of strings

    Parameter move: number of moves from initial state of map
    Precondition: move is an int
    """
    print("\nM_" + str(move))
    for row in map:
        print(row)


def printPath(states, map, node, heights, symbols, count):
    """
    Prints map state of each step in shortest path

    Parameter states: dictionary containing states of coordinates that were traversed in A*
    Precondition: states is a dictionary of with values in the form of (int, tuple(int, int))

    Parameter map: map of heights
    Precondition: map is a list of strings

    Parameter node: the goal state or goal coordinate
    Precondition: node is a tuple of form (int, int)

    Parameter heights: contains symbols mapped to heights
    Precondition: heights is a dictionary

    Parameter symbols: contains heights mapped to symbols
    Precondition: symbols is a dictionary

    Parameter count: tracks current step in shortest path
    Precondition: count is an int. It should always be 0.
    """
    curState = states[node]
    # Base case. Should be starting coordinate/node
    if not curState[1]:
        replaceChar(map, node, heights[map[node[0]][node[1]]])
        printMap(map, count)
        replaceChar(map, node, symbols[map[node[0]][node[1]]])
        return count + 1

    # Recurse down shortest path
    count1 = printPath(states, map, curState[1], heights, symbols, count)
    replaceChar(map, node, heights[map[node[0]][node[1]]])
    printMap(map, count1)
    replaceChar(map, node, symbols[map[node[0]][node[1]]])
    return count1 + 1


def h0(x, y, z, x1, y1, z1, parentHeight=None):
    """
    Heuristic function 0. Euclidian distance.

    Parameters: coordinates
    Precondition: all parameters should be ints
    """
    return math.sqrt(abs(x - x1)**2 + abs(y -y1)**2 + abs(z - z1)**2)


def h1(x, y, z, x1, y1, z1, parentHeight=None):
    """
    Heuristic function 1. Manhattan distance.

    Parameters: coordinates
    Precondition: all parameters should be ints
    """
    return abs(x - x1) + abs(y - y1) + abs(z - z1)


def h2(x, y, z, x1, y1, z1, parentHeight):
    """
    Heuristic function 3.

    Parameters: coordinates
    Precondition: all parameters should be ints
    """
    euc_dist = math.sqrt(abs(x - x1) ** 2 + abs(y - y1) ** 2 + abs(z - z1) ** 2)
    step = 0
    if (z - parentHeight) == 1:
        step = parentHeight - z
    else:
        step = abs(z - parentHeight)

    return euc_dist + step


if __name__ == "__main__":
    main()