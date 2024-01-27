from cv2 import sort, sqrt
import matplotlib.pyplot as plt
import numpy as np
from drppp import DARP
from extre import nearest_neighbor
from padding import PointMinimizer
import optuna
from sympy import true
import random
import math


class DARPVisualizer:
    def __init__(self, rows, cols, robots, obstacles, m):
        self.rows = rows
        self.cols = cols
        self.robots = robots
        self.obstacles = obstacles
        self.m = m
        self.darp_solver = DARP(rows, cols, robots, obstacles, m)

    def visualize_assignment(self):
        self.darp_solver.assign_cells()
        return self.darp_solver.visualize_assignment()

    def create_indices_dict(self, assignment_matrix):
        indices_dict = {}
        for i in range(assignment_matrix.shape[0]):
            for j in range(assignment_matrix.shape[1]):
                element = assignment_matrix[i, j]
                if element in indices_dict:
                    indices_dict[element].append((i, j))
                else:
                    indices_dict[element] = [(i, j)]
        return indices_dict

    def euclidean_distance(self, point1, point2):
        x1, y1 = point1
        x2, y2 = point2
        if math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2) == 1:
            return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
        else:
            return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2) - sqrt(2) + 1

    def count_turns(self, spanning_tree):
        num_turns = sum(
            1 for edge in spanning_tree if edge[0][0] != edge[1][0] and edge[0][1] != edge[1][1])
        return num_turns

    def generate_spanning_tree(self, points):
        shuffled_points = sorted(points, key=lambda point: point[0])
        edges = []

        for i in range(len(shuffled_points)):
            for j in range(i + 1, len(shuffled_points)):
                x1, y1 = shuffled_points[i]
                x2, y2 = shuffled_points[j]
                if (((abs(x2 - x1) == 1 and abs(y2 - y1) == 0)) or ((abs(x2 - x1) == 0 and abs(y2 - y1) == 1))):
                    edges.append((shuffled_points[i], shuffled_points[j],1))

                # Check if the points are diagonally adjacent
                if abs(x2 - x1) == 1 and abs(y2 - y1) == 1:
                    edges.append((shuffled_points[i], shuffled_points[j], 2))

        edges.sort(key=lambda edge: edge[2],reverse=False)
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


    def calculate_distance(self, point1, point2):
        return math.sqrt((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2)

    def remove_points_within_radius(self, points, radius=1):
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
                distance = self.calculate_distance(current_point, other_point)

                if distance <= radius:
                    remaining_points.remove(j)

        return result

    def plot_configuration(self, points, spanning_tree):
        
        x_values, y_values = zip(*points)
        plt.scatter(x_values, y_values, color='blue', label='Points')

        for edge in spanning_tree:
            (x1, y1), (x2, y2), weight = edge
            plt.plot([y1, y2], [x1, x2], color='red', linewidth=2)

        plt.xlabel('X-axis')
        plt.ylabel('Y-axis')
        plt.title('Spanning Tree with Adjusted Diagonal Cost')
        plt.legend()

    def get_points_for_robot(self, i):
        assignment_matrix = self.visualize_assignment()
        indices_dict = self.create_indices_dict(assignment_matrix)

        if i in indices_dict:
            points = indices_dict[i]

            formatted_points = [[y, x, 5.5] for x, y in points]

            # Convert the formatted points to a numpy array for easy manipulation
            np_points = np.array(formatted_points)

            # Calculate distances between adjacent points
            distances = np.linalg.norm(
                np_points[:, :2] - np.roll(np_points[:, :2], shift=-1, axis=0), axis=1)

            # Sort the formatted points based on distances
            sorted_points = np_points[np.argsort(distances)]
            return formatted_points
        else:
            return []

    def visualize_darp(self):
        assignment_matrix = self.visualize_assignment()
        indices_dict = self.create_indices_dict(assignment_matrix)

        for i in range(1, 3):
            points = indices_dict[i]
            
            spanning_tree = self.generate_spanning_tree(points)

            self.plot_configuration(points, spanning_tree)

        # plt.show()

rows = 10
cols = 10
robots = [(0, 9), (9, 0)]
obstacles = [(2, 2), (1, 2), (3, 2), (0, 9)]
obstacles = [(2, 4), (2, 2), (2, 1), (3, 0), (1, 1), (0, 0), (2, 4), (2, 2), (2, 1), (3, 0), (1, 1), (0, 0), (2, 4), (2, 2), (2, 1), (3, 0), (1, 1), (0, 0)]
m = 0.1

darp_visualizer = DARPVisualizer(rows, cols, robots, obstacles, m)

robot_index = 1  # Replace with the desired robot index
robot_points = darp_visualizer.get_points_for_robot(robot_index)
darp_visualizer.visualize_darp()

print(f"Points for Robot {robot_index}: {robot_points}")
optimamth= nearest_neighbor(robot_points)
print(robot_points)
for val in optimamth:
    print(robot_points[val])
