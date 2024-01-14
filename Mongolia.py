import math
import numpy as np

def distance(bot, cell):
    dx = bot[0] - cell[0]
    dy = bot[1] - cell[1]
    return math.sqrt(dx**2 + dy**2)

 
def dJdki(currentnumberOfCells):
    return -2*(4-currentnumberOfCells)

def normalize_distances(points):
    maxi = np.max(points)
    return points / maxi

k = [0, 0, 0, 0]
def min_index_1d(arr):
    """
    Returns the index of the minimum value in the given 1D array.

    Parameters:
    - arr (numpy.ndarray): 1D input array.

    Returns:
    - int: Index of the minimum value.
    """
    return np.argmin(arr)

intermediateCost = [0, 0, 0, 0]
finalpoints = []
points=np.zeros([4, 4])
bot1=[]
bot2=[]
bot3=[]
bot4=[]
botdist1=[]
bot1 = []
bot2 = []
bot3 = []
bot4 = []
k
    0: bot1,
    1: bot2,
    2: bot3,
    3: bot4
}

botdist1 = [[0, 0], [0, 4], [4, 4], [4, 0]]

for botnumber in range(4):
    distances = np.zeros([4, 4])

    for i in range(distances.shape[0]):
        for j in range(distances.shape[1]):
            distances[i, j] = distance(botdist1[botnumber], [i, j])

    normalized_distances = normalize_distances(distances)

    botDist[botnumber] = normalized_distances  # Assign the normalized_distances directly

# Now you can access the elements of bot1, bot2, bot3, and bot4


for i in range(distances.shape[0]):
    for j in range(distances.shape[1]):
        needScore = []
        needScoreStandard = [0, 0, 0, 0]
        for l in range(4):
            needScore.append(dJdki(k[l]  ))
        for l in range(4):
            needScoreStandard[l] = (needScore[l] - np.min(needScore)) / (np.max(needScore))
             # Accessing the elements of bot1, bot2, bot3, and bot4

        finalScore=[0,0,0,0]
        for l in range(4):
            finalScore[l]=needScoreStandard[l]+botDist[l][i][j]
        
        k[np.abs(min_index_1d(finalScore))]+=1
        points[i][j]=min_index_1d(finalScore)
        finalScore = [0, 0, 0, 0]
print(points)
