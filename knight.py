import numpy as np
from numpy.core.fromnumeric import size

def knight_move(i, j):
    return [(x,y) for (x,y) in [(i+2, j-1), (i+2, j+1), (i-2, j-1), (i-2, j+1), (i+1, j+2), (i+1, j-2), (i-1, j+2), (i-1, j-2)] if (x >=0 and y>=0)]

def find_next_spot(
    visited:list,
    location:tuple,
    traversing_array:np.ndarray,
):
    best = None
    new_location = (0, 0)

    for x, y in knight_move(location[0], location[1]):
        best = traversing_array.size+1
        if traversing_array[x, y] < best and (x, y) not in visited:
            new_location = x, y
        
    visited.append(new_location)
    return visited, new_location


if __name__ == '__main__':
    trav = np.arange((50*50)).reshape((50,50))
    location = (0, 0)

    visited = []
    for j in range(30):
        visited, location = find_next_spot(visited, location, trav)
        print(location, trav[location])
