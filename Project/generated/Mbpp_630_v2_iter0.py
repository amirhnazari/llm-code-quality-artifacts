def get_coordinates(coord):
    # Extract the x and y coordinates from the input tuple
    x = coord[0]
    y = coord[1]
    
    # Generate all adjacent coordinates by iterating over a range of 3 values for both x and y
    return [[x + i, y + j] for i in range(-1, 2) for j in range(-1, 2)]
