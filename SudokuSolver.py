def cross(a,b): # Helper function
    '''
    When given two strings, 'a', 'b', 
    it will return the list formed by all 
    the possible concatenations of 
    a letter 's' in string 'a' with a letter 't' in string 'b'
    '''
    return [s+t for s in a for t in b]

def display(values): # Udacity's 
    """
    Display the values as a 2-D grid.
    Input: The sudoku in dictionary form
    Output: None
    """
    width = 1+max(len(values[s]) for s in boxes)
    line = '+'.join(['-'*(width*3)]*3)
    for r in rows:
        print(''.join(values[r+c].center(width)+('|' if c in '36' else '')
                      for c in columns))
        if r in 'CF': print(line)
    return

# the . represent empty grids
grid = '..3.2.6..9..3.5..1..18.64....81.29..7.......8..67.82....26.95..8..2.3..9..5.1.3..'

# Creating the boxes
rows = 'ABCDEFGHI'
columns = '123456789'
boxes = cross(rows,columns)

# Creating the units
row_units = [cross(r, columns) for r in rows] # therefore row_units[0] will return ['A1','A2',....'A9']
column_units = [cross(rows, c) for c in columns] # therefore column_units[0] will return ['A1','B1',.....'I1']
square_units = [cross(rs, cs) for rs in ('ABC', 'DEF', 'GHI') for cs in ('123', '456', '789')] # therefore square_units[0] will return A1 to 3, B1 to 3, C1 to 3

# Creating a dictionary
unitlist = row_units + column_units + square_units
units = dict((s,[u for u in unitlist if s in u]) for s in boxes) # needed to create the peers dictionary
peers = dict((s, set(sum(units[s],[])) - set([s])) for s in boxes)

def grid_values(grid):
    """Convert grid string into {<box>: <value>} dict with '123456789' value for empties.

    Args:
        grid: Sudoku grid in string form, 81 characters long
    Returns:
        Sudoku grid in dictionary form:
        - keys: Box labels, e.g. 'A1'
        - values: Value in corresponding box, e.g. '8', or '123456789' if it is empty.
    """
    values = []
    digits = '123456789'
    
    for box in grid:
        if box == '.':
            values.append(digits)
        elif box in digits:
            values.append(box)
    
    # assert len(grid) == 81, "Grid must contain 81 characters, realtive to boxes" # ensure the grid has 81 boxes (second statement shows durint the assertion error)
    assert len(values) == 81, "Something went wrong, the len of values doesn't equal 81" # ensures that the values are 81, so it can be zipped with the boxes
    # return dict(zip(boxes, grid)) # boxes as the dictionary key and grid details as the values
    return dict(zip(boxes,values)) # matches boxes with values containing guesses

def eliminate(values):
    """Eliminate values from peers of each box with a single value.

    Go through all the boxes, and whenever there is a box with a single value,
    eliminate this value from the set of values of all its peers.

    Args:
        values: Sudoku in dictionary form.
    Returns:
        Resulting Sudoku in dictionary form after eliminating values.
    
    """
    solvedvals = [box for box in values.keys() if len(values[box]) == 1] # if the value is 1 digit, then it counts as a sovled value
    
    for box in solvedvals:
        for pbox in peers[box]:
            values[pbox] = values[pbox].replace(values[box],'')
                
    
    return values

def only_choice(values):
    """Finalize all values that are the only choice for a unit.

    Go through all the units, and whenever there is a unit with a value
    that only fits in one box, assign the value to this box.

    Input: Sudoku in dictionary form.
    Output: Resulting Sudoku in dictionary form after filling in only choices.
    
    """
    # TODO: Implement only choice strategy here
    
    for unit in unitlist:
        for number in '123456789':
            choice = [box for box in unit if number in values[box]]
            if len(choice) == 1: # meaning that if only 1 choice is availble
                values[choice[0]] = number
    return values


#display(grid_values(grid)) # Viewing the grid
print(unitlist)

def reduce_puzzle(values): #Udacity and Me
    stalled = False
    while not stalled:
        # Check how many boxes have a determined value
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])

        # Your code here: Use the Eliminate Strategy
        solvedvalues = [box for box in values.keys() if len(values[box]) == 1]
        
        for box in solvedvalues:
            for pbox in peers[box]:
                values[pbox] = values[pbox].replace(values[box],'')
        
        # Your code here: Use the Only Choice Strategy
        for unit in unitlist:
            for number in '123456789':
                chosen = [box for box in unit if number in values[box]]
                if len(chosen) == 1:
                    values[chosen[0]] = number

        # Check how many boxes have a determined value, to compare
        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
        # If no new values were added, stop the loop.
        stalled = solved_values_before == solved_values_after
        # Sanity check, return False if there is a box with zero available values:
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False
    return values

def search(values): # Using basic 'Depth First Serch'
    "Using depth-first search and propagation, create a search tree and solve the sudoku."
    # First, reduce the puzzle using the previous function
    values = reduce_puzzle(values)
    if values is False:
        return False # meaning that it failed to solve the puzzle
    
    if all(len(values[box]) == 1 for box in boxes): # all() returns true if all the iterables within it are true
        return values # meaning it got solved
        
    # Choose one of the unfilled squares with the fewest possibilities
    choices, box = min((len(values[box]), box) for box in boxes if len(values[box]) > 1)    
    # Now use recursion to solve each one of the resulting sudokus, and if one returns a value (not False), return that answer!
    for vals in values[box]:
        new_puzzle = values.copy() # this way we don't overwrite the main dictionary
        new_puzzle[box] = vals
        trying = search(new_puzzle)
        if trying: # if it returns True, by returning an non-False value
            return trying
    # If you're stuck, see the solution.py tab!
    
    