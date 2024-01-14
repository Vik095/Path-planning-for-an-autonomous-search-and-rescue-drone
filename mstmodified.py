import numpy as np
from drppp import DARP

# Example assignment matrix
rows = 6
cols = 6
robots = [(0, 6), (6, 0), (6, 6), (0, 0)]
obstacles = []#[(2, 2), (1, 2), (3, 2)]
obstacles = []

m = 0.1

darp_solver = DARP(rows, cols, robots, obstacles,0.1)
darp_solver.assign_cells()
assignment_matrix = darp_solver.visualize_assignment()
non_zero_indices = np.argwhere(assignment_matrix != 0)
indices_dict = {}
# Create an assignment_matrix of assignment_matrix locations
for i in range(assignment_matrix.shape[0]):
    for j in range(assignment_matrix.shape[1]):
        element = assignment_matrix[i, j]
        if element in indices_dict:
            indices_dict[element].append((i, j))
        else:
            indices_dict[element] = [(i, j)]
for key, value in indices_dict.items():
    print(f"Element {key}: {value}")

# import matplotlib.pyplot as plt
# import math

# def euclidean_distance(point1, point2):
#     x1, y1 = point1
#     x2, y2 = point2
#     if math.sqrt((x2 - x1)**2 + (y2 - y1)**2)//1 != math.sqrt((x2 - x1)**2 + (y2 - y1)**2):
#         return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
#     else:
#         return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)

# def kruskals_algorithm(points):
#     edges = []
    
#     # Generate edges for horizontal, vertical, and adjacent diagonal connections
#     for i in range(len(points)):
#         for j in range(i + 1, len(points)):
#             x1, y1 = points[i]
#             x2, y2 = points[j]

#             if x1 == x2 or y1 == y2 or abs(x2 - x1) == abs(y2 - y1):
#                 edges.append((points[i], points[j], euclidean_distance(points[i], points[j])))

#     edges.sort(key=lambda edge: edge[2])

#     parent = {point: point for point in points}

#     def find_set(point):
#         if parent[point] != point:
#             parent[point] = find_set(parent[point])
#         return parent[point]

#     def union(set1, set2):
#         root1 = find_set(set1)
#         root2 = find_set(set2)
#         parent[root1] = root2

#     minimum_spanning_tree = []
#     for edge in edges:
#         point1, point2, weight = edge
#         if find_set(point1) != find_set(point2):
#             minimum_spanning_tree.append((point1, point2, weight))
#             union(point1, point2)

#     return minimum_spanning_tree

# # Given points in the grid
# #points = [(x, y) for x in range(5) for y in range(5)]
# points=[(1,4),(1,5),(1,6),(1,7),(2,4),(2,6),(3,6),(3,4),(6,5),(6,7)]

# # Applying Kruskal's algorithm
# minimum_spanning_tree = kruskals_algorithm(points)

# # Plotting the points
# x_values, y_values = zip(*points)
# plt.scatter(x_values, y_values, color='blue', label='Points')

# # Plotting the minimum spanning tree in red
# for edge in minimum_spanning_tree:
#     (x1, y1), (x2, y2), weight = edge
#     plt.plot([x1, x2], [y1, y2], color='red', linewidth=2)

# # Adding labels and legend
# plt.xlabel('X-axis')
# plt.ylabel('Y-axis')
# plt.title('Minimum Spanning Tree')
# plt.legend()

# # Show the plot
# plt.show()
# print(minimum_spanning_tree)
# import matplotlib.pyplot as plt
# import math
# import optuna

# def euclidean_distance(point1, point2):
#     x1, y1 = point1
#     x2, y2 = point2
#     return math.sqrt((x2 - x1)**2 + (y2 - y1)**2) + 0.5

# def kruskals_algorithm(points):
#     edges = []
    
#     # Generate edges for horizontal, vertical, and adjacent diagonal connections
#     for i in range(len(points)):
#         for j in range(i + 1, len(points)):
#             x1, y1 = points[i]
#             x2, y2 = points[j]

#             if x1 == x2 or y1 == y2 or abs(x2 - x1) == abs(y2 - y1):
#                 edges.append((points[i], points[j], euclidean_distance(points[i], points[j])))

#     edges.sort(key=lambda edge: edge[2])

#     parent = {point: point for point in points}

#     def find_set(point):
#         if parent[point] != point:
#             parent[point] = find_set(parent[point])
#         return parent[point]

#     def union(set1, set2):
#         root1 = find_set(set1)
#         root2 = find_set(set2)
#         parent[root1] = root2

#     minimum_spanning_tree = []
#     for edge in edges:
#         point1, point2, weight = edge
#         if find_set(point1) != find_set(point2):
#             minimum_spanning_tree.append((point1, point2, weight))
#             union(point1, point2)

#     return minimum_spanning_tree

# def objective(trial):
#     # Given points in the grid
#     points = [(x, 2*y + 0.5) for x in range(25) for y in range(25)]

#     # Applying Kruskal's algorithm
#     minimum_spanning_tree = kruskals_algorithm(points)

#     # Count the number of turns in the minimum spanning tree
#     num_turns = sum(1 for edge in minimum_spanning_tree if edge[0][0] != edge[1][0] and edge[0][1] != edge[1][1])

#     return num_turns

# if __name__ == '__main__':
#     study = optuna.create_study(
#         study_name="study",
#         direction="minimize",
#         sampler=optuna.samplers.TPESampler(),
#         pruner=optuna.pruners.MedianPruner()
#     )

#     study.optimize(objective, n_trials=100)

#     # Get the best trial
#     best_trial = study.best_trial
#     print("Number of turns:", best_trial.value)
#     print("Best parameters:", best_trial.params)
import matplotlib.pyplot as plt
import math

import random

import optuna
from sympy import true

def euclidean_distance(point1, point2):
    x1, y1 = point1
    x2, y2 = point2
    if math.sqrt((x2 - x1)**2 + (y2 - y1)**2)==1:
        return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
    else: 
        return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)+1005

def count_turns(spanning_tree):
    # Count the number of turns in the spanning tree
    num_turns = sum(1 for edge in spanning_tree if edge[0][0] != edge[1][0] and edge[0][1] != edge[1][1])
    return num_turns

import random

import random

import random

def generate_spanning_tree(points):
    # Randomly shuffle the points
    shuffled_points = points.copy()
    random.shuffle(shuffled_points)

    edges = []
    
    # Generate edges for adjacent or diagonal connections
    for i in range(len(shuffled_points)):
        for j in range(i + 1, len(shuffled_points)):
            x1, y1 = shuffled_points[i]
            x2, y2 = shuffled_points[j]

            # Check if points are adjacent or diagonally adjacent
            if (abs(x2 - x1) <= 1 and abs(y2 - y1) ==0)  or (abs(x2 - x1) == 0 and abs(y2 - y1) <=1):
                edges.append((shuffled_points[i], shuffled_points[j], euclidean_distance(shuffled_points[i], shuffled_points[j])))

    edges.sort(key=lambda edge: edge[2],reverse=False)

    # Convert lists to tuples for hashability
    parent = {tuple(point): tuple(point) for point in shuffled_points}

    def find_set(point):
        point_tuple = tuple(point)
        if parent[point_tuple] != point_tuple:
            parent[point_tuple] = find_set(parent[point_tuple])
        return parent[point_tuple]


    def union(set1, set2):
        root1 = find_set(tuple(set1))
        root2 = find_set(tuple(set2))

        parent[root1] = root2

    spanning_tree = []
    for edge in edges:
        point1, point2, weight = edge
        if find_set(point1) != find_set(point2):
            spanning_tree.append((point1, point2, weight))
            union(point1, point2)

    return spanning_tree
import math

def calculate_distance(point1, point2):
    return math.sqrt((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2)

def remove_points_within_radius(points, radius=1):
    result = []
    remaining_points = set(range(len(points)))

    for i in range(len(points)):
        if i not in remaining_points:
            continue

        current_point = points[i]
        result.append(current_point)
        remaining_points.remove(i)

        for j in remaining_points.copy():
            other_point = points[j]
            distance = calculate_distance(current_point, other_point)

            if distance <= radius:
                remaining_points.remove(j)

    return result






def plot_configuration(points, spanning_tree):
    # Plotting the points
    x_values, y_values = zip(*points)
    plt.scatter(x_values, y_values, color='blue', label='Points')

    # Plotting the spanning tree in red
    for edge in spanning_tree:
        (x1, y1), (x2, y2), weight = edge
        plt.plot([x1, x2], [y1, y2], color='red', linewidth=2)

    # Adding labels and legend
    plt.xlabel('X-axis')
    plt.ylabel('Y-axis')
    plt.title('Spanning Tree with Adjusted Diagonal Cost')
    plt.legend()

    # Show the plot
    


# Given points in the grid
for i in range(1,5):
    points = indices_dict[i]
    print(points)


    # Generate a random spanning tree
    spanning_tree = generate_spanning_tree(points)

    # # Count the number of turns in the spanning tree


    # # Plot the configuration for the best trial
    plot_configuration(points, spanning_tree)

plt.show()

# import matplotlib.pyplot as plt
# import math

# def euclidean_distance(point1, point2):
#     x1, y1 = point1
#     x2, y2 = point2
#     return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)

# def kruskals_algorithm(points):
#     edges = []

#     # Generate edges for horizontal, vertical, and adjacent diagonal connections
#     for i in range(len(points)):
#         for j in range(i + 1, len(points)):
#             x1, y1 = points[i]
#             x2, y2 = points[j]

#             if x1 == x2 or y1 == y2 or abs(x2 - x1) == abs(y2 - y1):
#                 edges.append((points[i], points[j], euclidean_distance(points[i], points[j])))

#     edges.sort(key=lambda edge: edge[2])

#     parent = {point: point for point in points}

#     def find_set(point):
#         if parent[point] != point:
#             parent[point] = find_set(parent[point])
#         return parent[point]

#     def union(set1, set2):
#         root1 = find_set(set1)
#         root2 = find_set(set2)
#         parent[root1] = root2

#     minimum_spanning_tree = []
#     for edge in edges:
#         point1, point2, weight = edge
#         if find_set(point1) != find_set(point2):
#             minimum_spanning_tree.append((point1, point2, weight))
#             union(point1, point2)

#     return minimum_spanning_tree

# # Given points in the grid
# points = [(1, 4), (1, 5), (1, 6), (1, 7), (2, 4), (2, 6), (3, 6), (3, 4), (6, 5), (6, 7)]

# # Applying Kruskal's algorithm
# minimum_spanning_tree = kruskals_algorithm(points)

# # Plotting the points
# x_values, y_values = zip(*points)
# plt.scatter(x_values, y_values, color='blue', label='Points')

# # Plotting the minimum spanning tree in red
# for edge in minimum_spanning_tree:
#     (x1, y1), (x2, y2), weight = edge
#     plt.plot([x1, x2], [y1, y2], color='red', linewidth=2)

# # Adding labels and legend
# plt.xlabel('X-axis')
# plt.ylabel('Y-axis')
# plt.title('Minimum Spanning Tree')

# # Creating a closed path with 1-unit padding around every point of the minimum spanning tree
# padding = 1
# padded_path = []
# for point in minimum_spanning_tree:
#     (x, y), (u,v), _ = point
#     padded_point = (x + padding, y + padding)
    
#     padded_path.append(padded_point)
    

# # Plotting the padded path in green
# padded_path_x, padded_path_y = zip(*padded_path)
# plt.plot(padded_path_x, padded_path_y, color='green', linewidth=2, linestyle='dashed', label='Padded Path')

# # Show the plot
# plt.legend()
# plt.show()
