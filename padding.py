import matplotlib.pyplot as plt
import math

class PointMinimizer:
    def __init__(self, points, obstacles):
        self.points = points
        self.obstacles = obstacles

    def euclidean_distance(self, point1, point2):
        x1, y1 = point1
        x2, y2 = point2
        return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)

    def is_valid_move(self, point1, point2):
        # Check if there is an obstacle between two points
        for obstacle in self.obstacles:
            if self.euclidean_distance(point1, obstacle) + self.euclidean_distance(obstacle, point2) == self.euclidean_distance(point1, point2):
                return True
        return False

    def minimize_distance(self):
        sorted_points = [self.points[0]]  # Start with the first point
        remaining_points = set(self.points[1:])

        while remaining_points:
            current_point = sorted_points[-1]
            valid_moves = [p for p in remaining_points if self.is_valid_move(current_point, p)]
            if not valid_moves:
                break  # No valid moves left, exit the loop
            closest_point = min(valid_moves, key=lambda p: self.euclidean_distance(current_point, p))
            sorted_points.append(closest_point)
            remaining_points.remove(closest_point)

        return sorted_points

    def plot_configuration(self):
        sorted_points = self.minimize_distance()

        x_values, y_values = zip(*sorted_points)
        plt.scatter(x_values, y_values, color='blue', label='Points')

        for i in range(len(sorted_points) - 1):
            (x1, y1), (x2, y2) = sorted_points[i], sorted_points[i + 1]
            plt.plot([y1, y2], [x1, x2], color='red', linewidth=2)  # Swapped X and Y

        plt.xlabel('Y-axis')  # Swapped X and Y
        plt.ylabel('X-axis')  # Swapped X and Y
        plt.title('Minimized Distance Configuration')
        plt.legend()

# Example usage
points = [(0, 0), (1, 1), (2, 2), (3, 3)]
obstacles = [(0.5, 0.5), (1.5, 1.5), (2.5, 2.5)]
point_minimizer = PointMinimizer(points, obstacles)
point_minimizer.plot_configuration()
# plt.show()
