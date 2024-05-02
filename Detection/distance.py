SMALL = 15
BIG = 30

W_FOCAL = 654
D_FOCAL = 669

f = D_FOCAL

def measure(pos, label):
    if label == 0:
        w = SMALL
    else:
        w = BIG
    p = pos[2]
    #print("width", p)
    distance = (f * w) / p
    #print('Distance', distance)
    return distance

def setSource(source):
    if source == 0:
        f = W_FOCAL
    else:
        f = D_FOCAL
    return f
