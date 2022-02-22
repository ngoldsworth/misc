import numpy as np
import matplotlib.pyplot as plt


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

def spiral_cell(x, y):
    m = max(abs(x), abs(y))
    p = (2*m+1)**2

    """
    1 . For an element (x, y): determine which square of the spiral the point
    belongs to
    2. For that square, get the value at the right-bottom point. A simple
    observation will show you these are the consecutive squares of odd natural
    numbers (1,9,25,49,…).
    3. For x, y: determine if we are in the left, top, right, or bottom side of
    the square. From this, we can easily find how to retrace from the
    right-bottom point to get the value at (x, y).
    """
    if x == m:
        #right side
        return p - (m + y)
    if y == m:
        #top side
        return p - 2*m - (m-x)
    if x == -m:
        #left side
        return p - 4*m -(m-y)
    if y==-m:
        return p - 6*m - (m+x)

# using the above function to generate the spiral as an array is terribly
# inefficient, but it works
def spiral_grid(side_length:int):
    if side_length % 2 == 0:
        side_length += 1
    
    c = (side_length-1)//2
    spiral = np.zeros((side_length, side_length))
    for i in range(side_length):
        y = i - c
        for j in range(side_length):
            x = j - c
            spiral[j, i] = spiral_cell(x, y)
    
    return spiral

if __name__ == '__main__':
    s = 201
    m = (s-1)//2
    trav = spiral_grid(s)
    location = (m,m)

    visited = []
    for j in range(199):
        visited, location = find_next_spot(visited, location, trav)

    visx = [x for (x, y) in visited]
    visy = [y for (x, y) in visited]

    plt.plot(visx, visy)
    plt.show()