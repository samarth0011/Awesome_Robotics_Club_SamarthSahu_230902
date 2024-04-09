import cv2
import numpy as np
from collections import deque

# Function to check if a box is valid and within the grid bounds
def is_valid_cell(row, col, rows, cols):
    return 0 <= row < rows and 0 <= col < cols

# Function to perform BFS to find the shortest path
def shortest_path(grid):
    rows, cols = len(grid), len(grid[0])
    visited = set()
    queue = deque([(0, 0, 0)])  # (row, col, distance)
    
    while queue:
        row, col, distance = queue.popleft()
        # Check if we reached the destination
        if (row, col) == (rows - 1, cols - 1):
            return distance
        # Mark the cell as visited
        visited.add((row, col))
        # Explore neighbors
        for dr, dc in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            new_row, new_col = row + dr, col + dc
            if is_valid_cell(new_row, new_col, rows, cols) and (new_row, new_col) not in visited and grid[new_row][new_col] == 'Y':
                queue.append((new_row, new_col, distance + 1))
    
    return -1  # No valid path found

# Read the image and convert it to the grid format
def image_to_grid(image_path):
    image = cv2.imread(image_path)
    # Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # Threshold to get binary image
    _, binary = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY)
    # Invert binary image
    binary = cv2.bitwise_not(binary)
    # Reshape binary image to match grid dimensions
    grid = np.where(binary == 255, 'Y', 'B')
    return grid.tolist(), image

# Sample image path
image_path = 'img.png'

# Convert image to grid
grid, original_image = image_to_grid(image_path)

# Find the shortest path
shortest_distance = shortest_path(grid)

# Mark the shortest path on the grid
if shortest_distance != -1:
    rows, cols = len(grid), len(grid[0])
    current_row, current_col = 0, 0
    path_grid = [[' ' for _ in range(cols)] for _ in range(rows)]
    for _ in range(shortest_distance):
        path_grid[current_row][current_col] = '-'
        for dr, dc in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            new_row, new_col = current_row + dr, current_col + dc
            if is_valid_cell(new_row, new_col, rows, cols) and grid[new_row][new_col] == 'Y':
                current_row, current_col = new_row, new_col
                break

    # Print the grid with the shortest path represented by dashes
    for row in path_grid:
        print(' '.join(row))

    # Display the original image
    cv2.imshow('Original Image', original_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
else:
    print("No valid path exists.")
