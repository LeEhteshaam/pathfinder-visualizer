import heapq
import random
from collections import deque
from grid import grid_instance
from config import NODE_COLORS

def reconstruct_path(came_from, current):
    path = []
    total_cost = 0
    while current in came_from:
        path.append(current)
        prev = came_from[current]
        total_cost += current.weight
        current = prev
    path.reverse()
    
    for node in path:
        if node != grid_instance.start_node and node != grid_instance.end_node:
            node.color = NODE_COLORS["PATH"]
        yield
    
    yield total_cost

def h(p1, p2):
    return abs(p1.row - p2.row) + abs(p1.col - p2.col)

def a_star_search():
    start = grid_instance.start_node
    end = grid_instance.end_node
    if not start or not end:
        yield
        return

    count = 0
    open_set = [(0, count, start)]
    came_from = {}
    
    start.g_score = 0
    start.f_score = h(start, end)
    
    open_set_hash = {start}

    while open_set:
        current = heapq.heappop(open_set)[2]
        open_set_hash.remove(current)
        
        if current == end:
            yield from reconstruct_path(came_from, end)
            return

        for neighbor in current.neighbors:
            if neighbor.is_wall:
                continue
            
            temp_g_score = current.g_score + neighbor.weight

            if temp_g_score < neighbor.g_score:
                came_from[neighbor] = current
                neighbor.g_score = temp_g_score
                neighbor.f_score = temp_g_score + h(neighbor, end)
                if neighbor not in open_set_hash:
                    count += 1
                    heapq.heappush(open_set, (neighbor.f_score, count, neighbor))
                    open_set_hash.add(neighbor)
                    if neighbor != end:
                        neighbor.color = NODE_COLORS["OPEN"]
        yield
        if current != start:
            current.color = NODE_COLORS["CLOSED"]

def dijkstra_search():
    start = grid_instance.start_node
    end = grid_instance.end_node
    if not start or not end:
        yield
        return

    count = 0
    open_set = [(0, count, start)]
    came_from = {}
    
    start.g_score = 0
    
    open_set_hash = {start}

    while open_set:
        current = heapq.heappop(open_set)[2]
        open_set_hash.remove(current)

        if current == end:
            yield from reconstruct_path(came_from, end)
            return

        for neighbor in current.neighbors:
            if neighbor.is_wall:
                continue
            
            distance = current.g_score + neighbor.weight

            if distance < neighbor.g_score:
                came_from[neighbor] = current
                neighbor.g_score = distance
                if neighbor not in open_set_hash:
                    count += 1
                    heapq.heappush(open_set, (neighbor.g_score, count, neighbor))
                    open_set_hash.add(neighbor)
                    if neighbor != end:
                        neighbor.color = NODE_COLORS["OPEN"]
        yield
        if current != start:
            current.color = NODE_COLORS["CLOSED"]

def bfs_search():
    start = grid_instance.start_node
    end = grid_instance.end_node
    if not start or not end:
        yield
        return

    queue = deque([start])
    came_from = {start: None}
    visited = {start}

    while queue:
        current = queue.popleft()

        if current == end:
            yield from reconstruct_path(came_from, end)
            return

        for neighbor in current.neighbors:
            if neighbor not in visited and not neighbor.is_wall:
                visited.add(neighbor)
                came_from[neighbor] = current
                queue.append(neighbor)
                if neighbor != end:
                    neighbor.color = NODE_COLORS["OPEN"]
        yield
        if current != start:
            current.color = NODE_COLORS["CLOSED"]

def dfs_search():
    start = grid_instance.start_node
    end = grid_instance.end_node
    if not start or not end:
        yield
        return

    stack = [start]
    came_from = {start: None}
    visited = {start}

    while stack:
        current = stack.pop()

        if current == end:
            yield from reconstruct_path(came_from, end)
            return

        for neighbor in reversed(current.neighbors):
            if neighbor not in visited and not neighbor.is_wall:
                visited.add(neighbor)
                came_from[neighbor] = current
                stack.append(neighbor)
                if neighbor != end:
                    neighbor.color = NODE_COLORS["OPEN"]
        yield
        if current != start:
            current.color = NODE_COLORS["CLOSED"]

def generate_maze_recursive_backtracking():
    grid = grid_instance.grid
    
    for row in grid:
        for node in row:
            node.set_type("WALL")
    yield

    start_node = grid[random.randrange(1, len(grid), 2)][random.randrange(1, len(grid[0]), 2)]
    start_node.set_type("AIR")
    stack = [start_node]
    
    while stack:
        current = stack[-1]
        current.color = NODE_COLORS["OPEN"]
        yield
        
        neighbors = []
        r, c = current.row, current.col
        if r > 1 and grid[r-2][c].is_wall: neighbors.append(grid[r-2][c])
        if r < len(grid) - 2 and grid[r+2][c].is_wall: neighbors.append(grid[r+2][c])
        if c > 1 and grid[r][c-2].is_wall: neighbors.append(grid[r][c-2])
        if c < len(grid[0]) - 2 and grid[r][c+2].is_wall: neighbors.append(grid[r][c+2])

        if neighbors:
            next_node = random.choice(neighbors)
            
            wall_between_row = (current.row + next_node.row) // 2
            wall_between_col = (current.col + next_node.col) // 2
            grid[wall_between_row][wall_between_col].set_type("AIR")
            next_node.set_type("AIR")
            
            stack.append(next_node)
        else:
            stack.pop()
        
        current.color = NODE_COLORS["AIR"]

    for row in grid:
        for node in row:
            if not node.is_wall:
                node.color = NODE_COLORS["AIR"]
    yield