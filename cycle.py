import itertools
import math
import matplotlib.pyplot as plt

from mstmodified import DARPVisualizer

def calculate_distance(point1, point2):
    # Assuming points are represented as [x, y, z]
    return math.sqrt((point1[0] - point2[0])**2 + (point1[1] - point2[1])**2)

def total_distance(path, points):
    distance = 0
    for i in range(len(path) - 1):
        distance += calculate_distance(points[path[i]], points[path[i+1]])
    # Closing the loop
    distance += calculate_distance(points[path[-1]], points[path[0]])
    return distance

def shortest_cyclic_graph(points):
    # Generate all possible permutations of points
    permutations = itertools.permutations(range(len(points)))

    # Initialize with a large distance
    min_distance = float('inf')
    shortest_path = None

    # Iterate through all permutations
    for perm in permutations:
        distance = total_distance(perm, points)
        if distance < min_distance:
            min_distance = distance
            shortest_path = perm

    return shortest_path, min_distance

def plot_cyclic_graph(points, path):
    # Extract x and y coordinates from points
    x = [point[0] for point in points]
    y = [point[1] for point in points]

    # Plot points
    plt.scatter(x, y, color='red', marker='o', label='Points')

    # Plot lines connecting the points in the shortest path
    for i in range(len(path) - 1):
        plt.plot([x[path[i]], x[path[i + 1]]], [y[path[i]], y[path[i + 1]]], color='blue')

    # Connect the last and first points to complete the cycle
    plt.plot([x[path[-1]], x[path[0]]], [y[path[-1]], y[path[0]]], color='blue')

    plt.title('Shortest Cyclic Graph')
    plt.xlabel('X-coordinate')
    plt.ylabel('Y-coordinate')
    plt.legend()
    plt.show()

# Example usage
rows = 4
cols = 4
robots = [(0, 0), (9/3, 9/3)]
obstacles = [(2, 4), (2, 2), (2, 1), (3, 0), (1, 1), (0, 0)]
m = 0.1

# Use the desired robot index
robot_index = 1  # Replace with the desired robot index

darp_visualizer = DARPVisualizer(rows, cols, robots, obstacles, m)
robot_points = darp_visualizer.get_points_for_robot(robot_index)
shortest_path, min_distance = shortest_cyclic_graph(robot_points)
plot_cyclic_graph(robot_points, shortest_path)
