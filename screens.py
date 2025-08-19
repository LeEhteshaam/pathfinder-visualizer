import pygame
from enum import Enum, auto
from config import *
from grid import grid_instance
from ui import Button, Panel, draw_text
from algorithms import a_star_search, dijkstra_search, bfs_search, dfs_search, generate_maze_recursive_backtracking

class Screen(Enum):
    HOME = auto()
    VISUALIZER = auto()
    QUIT = auto()

class AppState:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(AppState, cls).__new__(cls)
            cls._instance.init_state()
        return cls._instance

    def init_state(self):
        self.algorithm_iterator = None
        self.is_running_algo = False
        self.selected_brush = "WALL"
        self.path_cost = None
        self.ui_elements = {}
        self.fonts = {
            "title": pygame.font.SysFont("Arial", 72, bold=True),
            "button": pygame.font.SysFont("Arial", 20),
            "label": pygame.font.SysFont("Arial", 14)
        }
        self._create_ui_elements()

    def _create_ui_elements(self):
        self.ui_elements['bottom_panel'] = Panel(0, BOTTOM_PANEL_Y, WIDTH, BOTTOM_PANEL_HEIGHT, COLOR_GRAY_DARK)
        
        btn_x, btn_y, btn_w, btn_h, btn_gap = 20, BOTTOM_PANEL_Y + 15, 80, 40, 5
        self.ui_elements['btn_astar'] = Button(btn_x, btn_y, btn_w, btn_h, "A*", self.fonts['button'], lambda: self.start_algorithm(a_star_search))
        self.ui_elements['btn_dijkstra'] = Button(btn_x + (btn_w + btn_gap), btn_y, btn_w, btn_h, "Dijkstra", self.fonts['button'], lambda: self.start_algorithm(dijkstra_search))
        self.ui_elements['btn_bfs'] = Button(btn_x + 2*(btn_w + btn_gap), btn_y, btn_w, btn_h, "BFS", self.fonts['button'], lambda: self.start_algorithm(bfs_search))
        self.ui_elements['btn_dfs'] = Button(btn_x + 3*(btn_w + btn_gap), btn_y, btn_w, btn_h, "DFS", self.fonts['button'], lambda: self.start_algorithm(dfs_search))

        ctrl_btn_x = btn_x + 4*(btn_w + btn_gap) + 20
        self.ui_elements['btn_maze'] = Button(ctrl_btn_x, btn_y, 120, btn_h, "Generate Maze", self.fonts['button'], self.generate_maze)
        ctrl_btn_x += 120 + btn_gap
        self.ui_elements['btn_reset'] = Button(ctrl_btn_x, btn_y, 100, btn_h, "Reset Path", self.fonts['button'], self.reset_path)
        ctrl_btn_x += 100 + btn_gap
        self.ui_elements['btn_clear'] = Button(ctrl_btn_x, btn_y, 100, btn_h, "Clear All", self.fonts['button'], self.clear_all)
        ctrl_btn_x += 100 + btn_gap

        brush_x, brush_y, brush_w, brush_h, brush_gap = ctrl_btn_x + 20, BOTTOM_PANEL_Y + 15, 40, 40, 25
        self.ui_elements['brush_start'] = Button(brush_x, brush_y, brush_w, brush_h, "", self.fonts['button'], lambda: self.set_brush("START"))
        self.ui_elements['brush_end'] = Button(brush_x + (brush_w + brush_gap), brush_y, brush_w, brush_h, "", self.fonts['button'], lambda: self.set_brush("END"))
        self.ui_elements['brush_wall'] = Button(brush_x + 2*(brush_w + brush_gap), brush_y, brush_w, brush_h, "", self.fonts['button'], lambda: self.set_brush("WALL"))
        self.ui_elements['brush_air'] = Button(brush_x + 3*(brush_w + brush_gap), brush_y, brush_w, brush_h, "", self.fonts['button'], lambda: self.set_brush("AIR"))
        self.ui_elements['brush_dirt'] = Button(brush_x + 4*(brush_w + brush_gap), brush_y, brush_w, brush_h, "", self.fonts['button'], lambda: self.set_brush("DIRT"))
        self.ui_elements['brush_mud'] = Button(brush_x + 5*(brush_w + brush_gap), brush_y, brush_w, brush_h, "", self.fonts['button'], lambda: self.set_brush("MUD"))
        self.ui_elements['brush_tar'] = Button(brush_x + 6*(brush_w + brush_gap), brush_y, brush_w, brush_h, "", self.fonts['button'], lambda: self.set_brush("TAR"))
        
        self.ui_elements['brush_start'].color = NODE_COLORS["START"]
        self.ui_elements['brush_end'].color = NODE_COLORS["END"]
        self.ui_elements['brush_wall'].color = NODE_COLORS["WALL"]
        self.ui_elements['brush_air'].color = NODE_COLORS["AIR"]
        self.ui_elements['brush_dirt'].color = NODE_COLORS["DIRT"]
        self.ui_elements['brush_mud'].color = NODE_COLORS["MUD"]
        self.ui_elements['brush_tar'].color = NODE_COLORS["TAR"]

    def start_algorithm(self, algo_func):
        if not self.is_running_algo and grid_instance.start_node and grid_instance.end_node:
            self.reset_path()
            self.algorithm_iterator = algo_func()
            self.is_running_algo = True
            self.path_cost = None

    def generate_maze(self):
        if not self.is_running_algo:
            self.clear_all()
            self.algorithm_iterator = generate_maze_recursive_backtracking()
            self.is_running_algo = True
    
    def set_brush(self, brush_type):
        self.selected_brush = brush_type

    def reset_path(self):
        if not self.is_running_algo:
            grid_instance.reset_path()
            self.path_cost = None

    def clear_all(self):
        if not self.is_running_algo:
            grid_instance.full_reset()
            self.path_cost = None

app_state = AppState()

home_enter_button = Button(
    WIDTH // 2 - 100, 
    HEIGHT // 2, 
    200, 60, 
    "Enter", 
    app_state.fonts['button'], 
    lambda: None
)

def home_screen_loop(screen, events):
    for event in events:
        home_enter_button.handle_event(event)
        
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and home_enter_button.is_hovered:
            return Screen.VISUALIZER

    screen.fill(COLOR_GRAY_DARK)
    draw_text(screen, "Shaam's Pathfinding Visualizer", app_state.fonts['title'], COLOR_WHITE, (WIDTH // 2, HEIGHT // 3))
    home_enter_button.draw(screen)
    
    return Screen.HOME

def visualizer_loop(screen, events):
    handle_visualizer_input(events)
    update_visualizer_state()
    draw_visualizer(screen)
    return Screen.VISUALIZER

def handle_visualizer_input(events):
    for event in events:
        for key, element in app_state.ui_elements.items():
            if isinstance(element, Button):
                element.handle_event(event)

        if app_state.is_running_algo:
            continue

        if pygame.mouse.get_pressed()[0]: # Left click
            node = grid_instance.get_node_from_pos(pygame.mouse.get_pos())
            grid_instance.set_node_type(node, app_state.selected_brush)

        elif pygame.mouse.get_pressed()[2]: # Right click
            node = grid_instance.get_node_from_pos(pygame.mouse.get_pos())
            grid_instance.set_node_type(node, "AIR")

def update_visualizer_state():
    if app_state.is_running_algo and app_state.algorithm_iterator:
        try:
            result = next(app_state.algorithm_iterator)
            if isinstance(result, (int, float)):
                app_state.path_cost = result
                app_state.is_running_algo = False
                app_state.algorithm_iterator = None
        except StopIteration:
            app_state.is_running_algo = False
            app_state.algorithm_iterator = None

def draw_visualizer(screen):
    screen.fill(COLOR_GRAY_LIGHT)
    grid_instance.draw(screen)
    
    for key, element in app_state.ui_elements.items():
        element.draw(screen)

    font = app_state.fonts['label']
    labels = {
        'brush_start': 'Start',
        'brush_end': 'End',
        'brush_wall': 'Wall',
        'brush_air': 'Erase',
        'brush_dirt': f'Dirt ({NODE_WEIGHTS["DIRT"]})',
        'brush_mud': f'Mud ({NODE_WEIGHTS["MUD"]})',
        'brush_tar': f'Tar ({NODE_WEIGHTS["TAR"]})',
    }
    for key, text in labels.items():
        if key in app_state.ui_elements:
            btn = app_state.ui_elements[key]
            draw_text(screen, text, font, COLOR_WHITE, (btn.rect.centerx, btn.rect.bottom + 10))

    if app_state.path_cost is not None:
        stats_panel = Panel(0, 0, WIDTH, STATS_BAR_HEIGHT, COLOR_GRAY_DARK)
        stats_panel.draw(screen)
        cost_text = f"Path Cost: {app_state.path_cost:.2f}" if isinstance(app_state.path_cost, float) else f"Path Cost: {app_state.path_cost}"
        draw_text(screen, cost_text, app_state.fonts['button'], COLOR_WHITE, (WIDTH // 2, STATS_BAR_HEIGHT // 2))