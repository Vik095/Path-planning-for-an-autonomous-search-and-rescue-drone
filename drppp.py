import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial.distance import euclidean

class DARP:
    def __init__(self, rows, cols, robots, obstacles,multiplier):
        self.rows = rows
        self.cols = cols
        self.robots = robots
        self.obstacles = obstacles
        self.assignment_matrix = None
        self.multiplier=multiplier

    def calculate_distance(self, point1, point2):
        return euclidean(point1, point2)

    def custom_cost(self, i, j, robot_id):
        # Add a penalty for cells already assigned to the robot
        
        return  self.multiplier * np.sum(self.assignment_matrix == robot_id + 1)
        

    def assign_cells(self):
        self.assignment_matrix = np.zeros((self.rows, self.cols), dtype=int)

        for i in range(self.rows):
            for j in range(self.cols):
                if (i, j) not in self.obstacles:
                    min_cost = float('inf')
                    assigned_robot = -1

                    for robot_id, robot in enumerate(self.robots):
                        distance = self.calculate_distance(robot, (i, j))
                        cost = distance +  self.custom_cost(i, j, robot_id)
                        
                        
                        if cost < min_cost:
                            min_cost = cost
                            assigned_robot = robot_id

                    self.assignment_matrix[i, j] = assigned_robot + 1  # Adding 1 to label robots starting from 1

    def visualize_assignment(self):
        if self.assignment_matrix is not None:
            plt.imshow(self.assignment_matrix.astype(float), cmap='viridis', interpolation='nearest')  # Convert to float
            plt.title('Assignment Matrix')
            plt.colorbar()
           

            for i in range(self.rows):
                for j in range(self.cols):
                    plt.text(j, i, str(self.assignment_matrix[i, j]), color='white', ha='center', va='center')

            # plt.show()
            #print(self.assignment_matrix)
            rval=[]
            for i in range(1,5):
                count_of_threes = np.count_nonzero(self.assignment_matrix == i)
                rval.append(count_of_threes)
            
            
        else:
            print("Assignment matrix is not available. Run the assignment first.")
        return self.assignment_matrix

# Example usage
# rows = 10
# cols = 10
# robots = [(9, 0), (0, 9)]
# obstacles = [(2, 2), (1, 2), (3, 2),(4,4)]



# darp_solver = DARP(rows, cols, robots, obstacles,0)
# darp_solver.assign_cells()
# result = darp_solver.visualize_assignment()
# print(result)
