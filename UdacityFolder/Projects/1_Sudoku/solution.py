
from utils import *


row_units = [cross(r, cols) for r in rows]
column_units = [cross(rows, c) for c in cols]
square_units = [cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')]
unitlist = row_units + column_units + square_units

# print(list(zip(rows,cols))) 
# To create diagonal units, concatenate the zip of the rows and columns into a list, and do the same in reverse 
# - therefore A+1 = A1, B+2 = B2 and so forth as rows = 'ABCDEFGHI' and cols = '123456789'
# - to do the opposite side, we need to put the columns in reverse so that it shos as A+9 = A9 , B+8 = B8....I+1 = I9 as rows = 'ABCDEFGHI' and cols = '987654321'
# - both need to be in a list, if not python will compile it as a tuple
diagonal_units = [[r + c for r, c in zip(rows, cols)], [r + c for r, c in zip(rows, cols[::-1])]]

# TODO: Update the unit list to add the new diagonal units
unitlist = unitlist + diagonal_units


# Must be called after all units (including diagonals) are added to the unitlist
units = extract_units(unitlist, boxes)
peers = extract_peers(units, boxes)


def naked_twins(values):
    """Eliminate values using the naked twins strategy.

    The naked twins strategy says that if you have two or more unallocated boxes
    in a unit and there are only two digits that can go in those two boxes, then
    those two digits can be eliminated from the possible assignments of all other
    boxes in the same unit.

    Parameters
    ----------
    values(dict)
        a dictionary of the form {'box_name': '123456789', ...}

    Returns
    -------
    dict
        The values dictionary with the naked twins eliminated from peers

    Notes
    -----
    Your solution can either process all pairs of naked twins from the input once,
    or it can continue processing pairs of naked twins until there are no such
    pairs remaining -- the project assistant test suite will accept either
    convention. However, it will not accept code that does not process all pairs
    of naked twins from the original input. (For example, if you start processing
    pairs of twins and eliminate another pair of twins before the second pair
    is processed then your code will fail the PA test suite.)

    The first convention is preferred for consistency with the other strategies,
    and because it is simpler (since the reduce_puzzle function already calls this
    strategy repeatedly).

    See Also
    --------
    Pseudocode for this algorithm on github:
    https://github.com/udacity/artificial-intelligence/blob/master/Projects/1_Sudoku/pseudocode.md
    """
    # TODO: Implement this function!
    
    twins = [box for box in values.keys() if len(values[box]) == 2] # all the values with two choices
    
    for box in twins:        
        twin1 = values[box]
        if len(twin1) == 2: # since there is a chance it will overwrite a twin within the twin list
            for pbox in peers[box]:          
                twin2 = values[pbox]
                if twin1 == twin2: # confirm the values match
                    # print(peers[pbox]) # debugging
                    peertwins = set(peers[box]).intersection(peers[pbox]) # needs to be a set to ensure the values are unique | intersection or a similar method is required as it only returns the boxes of the same name within both twin 1 and twin 2
                    # print(peertwins) # debugging
                    for peer in peertwins:
                        if peer != pbox: # to avoid ameding the second twin
                            for i in range(2):
                                values[peer] = values[peer].replace(twin1[i], '') # clear the first and second digits from its peers

    return values


def eliminate(values):
    """Apply the eliminate strategy to a Sudoku puzzle

    The eliminate strategy says that if a box has a value assigned, then none
    of the peers of that box can have the same value.

    Parameters
    ----------
    values(dict)
        a dictionary of the form {'box_name': '123456789', ...}

    Returns
    -------
    dict
        The values dictionary with the assigned values eliminated from peers
    """
    # TODO: Copy your code from the classroom to complete this function
    solvedvals = [box for box in values.keys() if len(values[box]) == 1]

    for box in solvedvals:
        for pbox in peers[box]:
            values[pbox] = values[pbox].replace(values[box], '')

    return values


def only_choice(values):
    """Apply the only choice strategy to a Sudoku puzzle

    The only choice strategy says that if only one box in a unit allows a certain
    digit, then that box must be assigned that digit.

    Parameters
    ----------
    values(dict)
        a dictionary of the form {'box_name': '123456789', ...}

    Returns
    -------
    dict
        The values dictionary with all single-valued boxes assigned

    Notes
    -----
    You should be able to complete this function by copying your code from the classroom
    """
    # TODO: Copy your code from the classroom to complete this function
    for unit in unitlist:
        for number in '123456789':
            choice = [box for box in unit if number in values[box]]
            if len(choice) == 1:
                values[choice[0]] = number
    return values


def reduce_puzzle(values):
    """Reduce a Sudoku puzzle by repeatedly applying all constraint strategies

    Parameters
    ----------
    values(dict)
        a dictionary of the form {'box_name': '123456789', ...}

    Returns
    -------
    dict or False
        The values dictionary after continued application of the constraint strategies
        no longer produces any changes, or False if the puzzle is unsolvable 
    """
    # TODO: Copy your code from the classroom and modify it to complete this function
    stalled = False
    while not stalled:
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])

        values = eliminate(values)
        # print('Elimination\n\n') # debugging
        # display(values) # debugging
    
        values = only_choice(values)
        # print('Only Choice\n\n') # debugging
        # display(values) # debugging
        
        values = naked_twins(values)
        # print('Naked Twins\n\n') # debugging
        # display(values) # debugging
    
        

        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])

        stalled = solved_values_before == solved_values_after
 
        if len([box for box in values.keys() if len(values[box]) == 0]):
            # print([box for box in values.keys() if len(values[box]) == 0]) # debugging
            # display(values) # debugging
            return False

    return values


def search(values):
    """Apply depth first search to solve Sudoku puzzles in order to solve puzzles
    that cannot be solved by repeated reduction alone.

    Parameters
    ----------
    values(dict)
        a dictionary of the form {'box_name': '123456789', ...}

    Returns
    -------
    dict or False
        The values dictionary with all boxes assigned or False

    Notes
    -----
    You should be able to complete this function by copying your code from the classroom
    and extending it to call the naked twins strategy.
    """
    # TODO: Copy your code from the classroom to complete this function
    values = reduce_puzzle(values)
    if values is False:
        return False
    
    if all(len(values[box]) == 1 for box in boxes):
        return values
    
    choices, box = min((len(values[box]), box) for box in boxes if len(values[box]) > 1)    

    for vals in values[box]:
        new_puzzle = values.copy()
        new_puzzle[box] = vals
        trying = search(new_puzzle)
        if trying:
            return trying


def solve(grid):
    """Find the solution to a Sudoku puzzle using search and constraint propagation

    Parameters
    ----------
    grid(string)
        a string representing a sudoku grid.
        
        Ex. '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'

    Returns
    -------
    dict or False
        The dictionary representation of the final sudoku grid or False if no solution exists.
    """
    values = grid2values(grid)
    values = search(values)
    return values


if __name__ == "__main__":
    diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    display(grid2values(diag_sudoku_grid))
    result = solve(diag_sudoku_grid)
    display(result)

    try:
        import PySudoku
        PySudoku.play(grid2values(diag_sudoku_grid), result, history)

    except SystemExit:
        pass
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')
    