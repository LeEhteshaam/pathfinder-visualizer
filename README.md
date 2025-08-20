# Pathfinding Algorithm Visualizer

This project is a Python-based interactive tool for visualizing various pathfinding algorithms and maze generation. Built with Pygame, it provides a hands-on way to understand how different algorithms explore a grid to find the shortest path between two points.

 
## **[➡️ Play the Live Demo on Itch.io!](https://ehteshaam.itch.io/pathfinding-algorithms)**

## Features

*   **Multiple Algorithms**: Visualize the execution of A*, Dijkstra's, Breadth-First Search (BFS), and Depth-First Search (DFS).
*   **Maze Generation**: Automatically generate complex mazes using the Recursive Backtracking algorithm.
*   **Interactive Grid**:
    *   Place and move the Start and End nodes.
    *   Draw Walls to create obstacles.
    *   Right-click to erase any node.
*   **Weighted Nodes**: Add "terrain" with different movement costs (Dirt, Mud, Tar) to see how weighted algorithms like A* and Dijkstra adapt.
*   **Step-by-Step Visualization**: Watch the algorithms explore the grid in real-time, showing open and closed sets.
*   **Path Cost Display**: After a search is complete, the total cost of the found path is displayed.
*   **Intuitive UI**: Simple controls to select algorithms, generate mazes, reset the path, or clear the entire grid.

## Technologies Used

*   **Python 3**
*   **Pygame**

## Getting Started

Follow these instructions to get a copy of the project up and running on your local machine.

### Prerequisites

You need to have Python 3 installed on your system.

### Installation

1.  **Clone the repository:**
    ```sh
    git clone https://github.com/your-username/your-repository-name.git
    cd your-repository-name
    ```

2.  **Install the required packages:**
    The only dependency is Pygame.
    ```sh
    pip install pygame
    ```

3.  **Run the application:**
    ```sh
    python main.py
    ```

## How to Use

1.  Launch the application to see the home screen.
2.  Click **"Enter"** to navigate to the visualizer.
3.  **Drawing on the Grid**:
    *   Use the brush panel at the bottom right to select what you want to draw (`Start`, `End`, `Wall`, `Dirt`, etc.).
    *   **Left-click** on the grid to place the selected node type.
    *   **Right-click** on any node to erase it (turn it into an "Air" node).
4.  **Running an Algorithm**:
    *   Once you have placed a Start and an End node, click on one of the algorithm buttons (`A*`, `Dijkstra`, `BFS`, `DFS`) to start the visualization.
5.  **Controls**:
    *   **Generate Maze**: Clears the grid and generates a new random maze.
    *   **Reset Path**: Clears the algorithm's path and search visualization but keeps your walls and weights.
    *   **Clear All**: Resets the entire grid to its initial empty state.

## Project Structure

```
pathfinder/
├── main.py           # Main application entry point, handles the game loop.
├── config.py         # Stores all constants (colors, sizes, weights).
├── grid.py           # Defines the Node and Grid classes.
├── algorithms.py     # Contains all pathfinding and maze generation logic.
├── screens.py        # Manages application state and screen loops (Home, Visualizer).
└── ui.py             # Contains UI component classes (Button, Panel).
```
