from cv2 import sort, sqrt
import matplotlib.pyplot as plt
import numpy as np
from AreaDivision import DARP

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
        graphi=self.darp_solver.visualize_assignment()
        plt.imshow(graphi, cmap='viridis', interpolation='nearest', origin='lower')  # Convert to float
        plt.title('Assignment Matrix')
        plt.colorbar()
        

        for i in range(self.rows):
            for j in range(self.cols):
                plt.text(j, i, str(graphi[i, j]), color='white', ha='center', va='center')

        plt.show()
        return graphi

    def create_indices_dict(self, assignment_matrix):
        indices_dict = {}
        num_rows = len(assignment_matrix)
        num_columns = len(assignment_matrix[0])

        for i in range(num_rows):
            for j in range(num_columns):
                element = assignment_matrix[j][i]  # Corrected the index order
                if element != 0:
                    if element in indices_dict:
                        indices_dict[element].append((i, j))
                    else:
                        indices_dict[element] = [(i, j)]

        return indices_dict

    # def euclidean_distance(self, point1, point2):
    #     x1, y1 = point1
    #     x2, y2 = point2
    #     if math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2) == 1:
    #         return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
    #     else:
    #         return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

    def count_turns(self, spanning_tree):
        num_turns = sum(
            1 for edge in spanning_tree if edge[0][0] != edge[1][0] and edge[0][1] != edge[1][1])
        return num_turns

    def generate_spanning_tree(self, points):
        
        # Filter out obstacle points
        points = [point for point in points if point not in self.obstacles]

        shuffled_points = sorted(points, key=lambda point: point[0])
        edges = []

        for i in range(len(shuffled_points)):
            for j in range(i + 1, len(shuffled_points)):
                
                x1, y1 = shuffled_points[i]
                x2, y2 = shuffled_points[j]
                if (((abs(x2 - x1) == 1 and abs(y2 - y1) == 0)) ^ ((abs(x2 - x1) == 0 and abs(y2 - y1) == 1))):
                    print(shuffled_points[i-1] if i>0 else print("ok"))
                    edges.append((shuffled_points[i], shuffled_points[j], 0.61))
                    edges.sort(key=lambda edge: edge[2], reverse=False)

                # Check if the points are diagonally adjacent
                if abs(x2 - x1) == 1 and abs(y2 - y1) == 1:
                    edges.append((shuffled_points[i], shuffled_points[j], 0.61))

        edges.sort(key=lambda edge: edge[2], reverse=False)
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


    def plot_configuration(self, points, spanning_tree):
        
        x_values, y_values = zip(*points)
        plt.scatter(x_values, y_values, color='blue')
        print(spanning_tree)
        color = np.random.rand(3,)
        for edge in spanning_tree:
            
            (x1, y1), (x2, y2), weight = edge


            # plt.plot([x1, x2], [y1, y2], color='red', linewidth=2)
       

        plt.xlabel('X-axis')
        plt.ylabel('Y-axis')
        plt.title('Generated Energy Aware MST')
        plt.legend()

    def get_points_for_robot(self, i):
        assignment_matrix = self.visualize_assignment()
        indices_dict = self.create_indices_dict(assignment_matrix)
        rarr=[]

        if i in indices_dict:
            points = indices_dict[i]

            formatted_points = [[x, y, 5.5] for x, y in points]

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
            if i in indices_dict:
                points = indices_dict[i]
                
                spanning_tree = self.generate_spanning_tree(points)

                self.plot_configuration(points, spanning_tree)
                for i in range(1, 3):
                    if i in indices_dict:
                        points = indices_dict[i]

                        self.generate_and_visualize_dfs(points, spanning_tree)
                        


        # plt.show()
    def dfs_traversal(self, start_point, visited, dfs_points):
        visited.add(start_point)
        dfs_points.append(start_point)

        for neighbor in self.get_neighbors(start_point):
            if neighbor not in visited:
                self.dfs_traversal(neighbor, visited, dfs_points)

    def get_neighbors(self, point):
        x, y = point
        neighbors = [
            (x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1),
            (x + 1, y + 1), (x - 1, y - 1), (x + 1, y - 1), (x - 1, y + 1)
        ]
        return [(neighbor_x, neighbor_y) for neighbor_x, neighbor_y in neighbors if 0 <= neighbor_x<self.rows  and 0 <= neighbor_y <self.cols]


    def generate_and_visualize_dfs(self, points, spanning_tree):
        
        start_point = points[0]  # Assuming starting from the first point in the list
        visited = set()
        dfs_points = []

        self.dfs_traversal(start_point, visited, dfs_points)

        # self.plot_configuration(points, spanning_tree)  # Change this to plot MST or other elements
        for i in range(len(dfs_points) - 1):
            current_point = dfs_points[i]
            next_point = self.get_neighbors(current_point)

            # Check if the edge exists in the spanning tree before plotting
            for point in next_point:
                if any(((current_point, point) == (edge[0], edge[1]) or ((current_point, point) == (edge[1], edge[0])) for edge in spanning_tree)):
                    plt.plot([current_point[0], point[0]], [current_point[1], point[1]], color='green', linewidth=2)
                    print("curremt point", current_point, "point", point)
    
        



rows = 9
cols = 9
robots = [(0, 0)]
obstacles = [(2, 2), (1, 2), (3, 2), (0, 9)]
obstacles = [(2, 4), (2, 2), (2, 1), (3, 0), (1, 1), (0, 0), (2, 4), (2, 2), (2, 1), (3, 0), (1, 1), (0, 0), (2, 4), (2, 2), (2, 1), (3, 0), (1, 1), (0, 0)]
m = 0.1
obstacles=[(2,2),(3,2)]



darp_visualizer = DARPVisualizer(rows, cols, robots, obstacles, m)

robot_index = 1  # Replace with the desired robot index
robot_points = darp_visualizer.get_points_for_robot(robot_index)
darp_visualizer.visualize_darp()


plt.show()
grid=np.zeros((5,5), dtype=int)
for point in obstacles:
        y, x = point
        grid[x][y] = 1
plt.imshow(1 - grid, cmap='gray', origin='lower', extent=[0, 5, 0, 5], vmin=0, vmax=1)

# Add grid lines
plt.grid(color='black', linestyle='-', linewidth=1)

# Set axis ticks to go up by 1s
plt.xticks(np.arange(0, 5 + 1, step=1))
plt.yticks(np.arange(0, 5 + 1, step=1))

plt.title('Occupancy Grid Map')
plt.xlabel('X')
plt.ylabel('Y')
plt.show()