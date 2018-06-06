# both take an appropriate coordinate and it's relavant dimension of the canvas, and returns the same coordinate, wrapped around the canvas if necessary

def wrapped_x(i, Width):
    if Width > i >= 0:
        return i
    elif i < 0:
        return Width-1 + i
    else:
        return i - Width-1
    
def wrapped_y(j, Height):
    if Height > j >= 0:
        return j
    elif j < 0:
        return Height-1 + j
    else:
        return j - Height-1
