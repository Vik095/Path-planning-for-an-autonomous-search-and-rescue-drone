import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial.distance import euclidean
import math
import random

class DARP:
    def __init__(self, rows, cols, robots, obstacles, multiplier=0.1):
        self.rows = rows
        self.cols = cols
        self.robots = robots
        self.obstacles = obstacles
        self.assignment_matrix = None
        self.multiplier = multiplier
    def visualize_assignment(self):
        if self.assignment_matrix is not None:
            plt.imshow(self.assignment_matrix.astype(float), cmap='viridis', interpolation='nearest')  # Convert to float
            plt.title('Assignment Matrix')
            plt.colorbar()

            for i in range(self.rows):
                for j in range(self.cols):
                    plt.text(j, i, str(self.assignment_matrix[i, j]), color='white', ha='center', va='center')

            plt.show()
            print(self.assignment_matrix)
            rval=[]
            for i in range(1,5):
                count_of_threes = np.count_nonzero(self.assignment_matrix == i)
                rval.append(count_of_threes)
            
        else:
            print("Assignment matrix is not available. Run the assignment first.")
        return rval

    def calculate_distance(self, point1, point2):
        return euclidean(point1, point2)

    def custom_cost(self, i, j, robot_id):
        return 1 + self.multiplier * np.sum(self.assignment_matrix == robot_id + 1)

    def assign_cells(self):
        self.assignment_matrix = np.zeros((self.rows, self.cols), dtype=int)

        # Partition the grid into separate areas (for simplicity, using a single partition for the entire grid)
        partitioned_areas = [(0, self.rows, 0, self.cols)]

        for area in partitioned_areas:
            area_rows_start, area_rows_end, area_cols_start, area_cols_end = area

            area_robots = [robot for robot in self.robots if
                           area_rows_start <= robot[0] < area_rows_end and area_cols_start <= robot[1] < area_cols_end]

            area_obstacles = [(obstacle[0], obstacle[1]) for obstacle in self.obstacles if
                              area_rows_start <= obstacle[0] < area_rows_end and area_cols_start <= obstacle[1] < area_cols_end]

            area_assignment_matrix = np.zeros((area_rows_end - area_rows_start, area_cols_end - area_cols_start),
                                              dtype=int)

            for i in range(area_rows_start, area_rows_end):
                for j in range(area_cols_start, area_cols_end):
                    if (i, j) not in area_obstacles:
                        min_cost = float('inf')
                        assigned_robot = -1

                        for robot_id, robot in enumerate(area_robots):
                            distance = self.calculate_distance(robot, (i, j))
                            cost = distance + self.custom_cost(i, j, robot_id)

                            if cost < min_cost:
                                min_cost = cost
                                assigned_robot = robot_id

                        area_assignment_matrix[i - area_rows_start, j - area_cols_start] = assigned_robot + 1

            # Apply MST to the current partitioned area
            mst_spanning_tree = self.apply_mst(area_robots)

            # Visualize the MST for the current partitioned area (you may want to adapt this visualization)
            self.visualize_mst(area_robots, mst_spanning_tree, area_rows_start, area_cols_start)

            # Merge the area_assignment_matrix into the overall assignment_matrix
            self.assignment_matrix[area_rows_start:area_rows_end, area_cols_start:area_cols_end] = area_assignment_matrix

    def apply_mst(self, points):
        shuffled_points = points.copy()
        random.shuffle(shuffled_points)
        return self.generate_spanning_tree(shuffled_points)

    def generate_spanning_tree(self, points):
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
                    edges.append((shuffled_points[i], shuffled_points[j], euclidean(shuffled_points[i], shuffled_points[j])))

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

    def visualize_mst(self, points, spanning_tree, offset_rows, offset_cols):
        adjusted_spanning_tree = [(tuple((x1 + offset_rows, y1 + offset_cols)),
                                   tuple((x2 + offset_rows, y2 + offset_cols)), weight)
                                  for (x1, y1), (x2, y2), weight in spanning_tree]
        self.plot_configuration(points, adjusted_spanning_tree)

    def plot_configuration(self, points, spanning_tree):
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
        plt.show()

# Example usage
rows = 20
cols = 20
robots = [(1, 1), (24, 1), (1, 24), (24, 24)]
obstacles = [(2, 2), (1, 2), (3, 2)]

darp_solver = DARP(rows, cols, robots, obstacles)
darp_solver.assign_cells()
result = darp_solver.visualize_assignment()
print(result)
