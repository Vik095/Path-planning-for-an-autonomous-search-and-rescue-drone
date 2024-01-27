import numpy as np
from scipy.spatial.distance import euclidean

def nearest_neighbor(points):
    unvisited = set(range(len(points)))
    current_point = 0
    path = [current_point]

    while unvisited:
        nearest_point = min(unvisited, key=lambda x: euclidean(points[current_point], points[x]))
        path.append(nearest_point)
        unvisited.remove(nearest_point)
        current_point = nearest_point

    return path

# Given points
start_point = np.array([0, 0, 5.5])
points=np.array([[1,0,5.5],[2,0,5.5],[3,0,5.5],[0,5,5.5]])
# Add start point to the list of points
points = np.vstack([points])

# Find the optimal path
optimal_path = nearest_neighbor(points)

# Print the optimal path
print("Optimal Path:", optimal_path)
for val in optimal_path:
    print(points[val])

