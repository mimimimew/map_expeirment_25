import pygame  
import time  
from pygame.locals import *  

# 游戏配置  
GRID_SIZE = 49  
CELL_SIZE = 15  
WIDTH, HEIGHT = GRID_SIZE * CELL_SIZE, GRID_SIZE * CELL_SIZE  

# 颜色配置
COLORS = {  
    'background': (255, 255, 255),  
    'grid': (211, 211, 211),  
    'start': (0, 0, 255),  
    'current': (255, 0, 0),  
    'close 1': (255, 165, 0),  
    'close 2': (0, 128, 0),  
    'far 1': (255, 192, 203),  
    'far 2': (128, 0, 128),
    'obstacle': (169, 169, 169)  
}  

# 坐标点配置
POINTS = {  
    'start': (7, 42),  
    'close 1': (20, 18),  
    'close 2': (31, 29),  
    'far 1': (5, 1),  
    'far 2': (48, 44)  
}  

# 障碍物定义（后期可修改）
ORIGINAL_OBSTACLES = [  
    (9, 9, 8, 1), (8, 8, 12, 1), (10, 10, 6, 1), (11, 7, 4, 1),
    (14, 25, 6, 1), (13, 24, 5, 1), (15, 26, 3, 1), (10, 23, 7, 1),
    (24, 15, 5, 1), (27, 14, 2, 1), (23, 16, 6, 1),
    (3, 31, 6, 1), (4, 32, 4, 1), (5, 30, 3, 1),
    (44, 9, 5, 1), (43, 10, 3, 1), (45, 8, 4, 1)
]  

MIRRORED_OBSTACLES = [  
    (39, 32, 1, 8), (40, 29, 1, 12), (38, 33, 1, 6), (41, 34, 1, 4),
    (23, 29, 1, 6), (24, 31, 1, 5), (22, 31, 1, 3), (25, 32, 1, 7),
    (33, 20, 1, 5), (34, 20, 1, 2), (32, 20, 1, 6),
    (17, 40, 1, 6), (16, 41, 1, 4), (18, 41, 1, 3),
    (39, 0, 1, 5), (38, 3, 1, 3), (40, 0, 1, 4)
]  

ALL_OBSTACLES = ORIGINAL_OBSTACLES + MIRRORED_OBSTACLES  

class PathGame:  
    def __init__(self):  
        pygame.init()  
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))  
        pygame.display.set_caption("对称障碍物路径游戏")  
        self.clock = pygame.time.Clock()  
        self.font = pygame.font.SysFont('Arial', 20)  
        
        # 游戏状态初始化  
        self.current_pos = list(POINTS['start'])  
        self.path = [tuple(self.current_pos)]  
        self.start_time = time.time()  
        self.running = True  
        self.finished = False  

    def convert_coords(self, x, y):  
        return (x * CELL_SIZE, (GRID_SIZE - y) * CELL_SIZE)  

    def draw_grid(self):  
        for i in range(GRID_SIZE + 1):  
            pygame.draw.line(self.screen, COLORS['grid'],
                            (i * CELL_SIZE, 0), (i * CELL_SIZE, HEIGHT))  
            pygame.draw.line(self.screen, COLORS['grid'],
                            (0, i * CELL_SIZE), (WIDTH, i * CELL_SIZE))  

    def draw_obstacles(self):  
        for x, y, w, h in ALL_OBSTACLES:  
            # pygame坐标系默认左上角为原点，需要转换
            rect_x = x * CELL_SIZE
            rect_y = (GRID_SIZE - y - h) * CELL_SIZE  
            pygame.draw.rect(self.screen, COLORS['obstacle'],
                            (rect_x, rect_y, w*CELL_SIZE, h*CELL_SIZE))

    def draw_points(self):  
        for name, (x, y) in POINTS.items():  
            pos = self.convert_coords(x, y)  
            color = COLORS.get(name, (0,0,0))  
            pygame.draw.circle(self.screen, color, pos, 6)  
        pygame.draw.circle(self.screen, COLORS['current'],
                          self.convert_coords(*self.current_pos), 6)  

    def draw_path(self):  
        if len(self.path) > 1:  
            points = [self.convert_coords(x, y) for x, y in self.path]  
            pygame.draw.lines(self.screen, (0,0,0), False, points, 2)  

    def is_obstructed(self, x, y):  
        """检查坐标是否在障碍物区域内"""
        for ox, oy, w, h in ALL_OBSTACLES:
            if ox <= x <= ox + w and oy <= y <= oy + h:
                return True
        return False

    def handle_input(self):  
        for event in pygame.event.get():  
            if event.type == QUIT:  
                self.running = False  
                
            if event.type == KEYDOWN and not self.finished:  
                if event.key == K_BACKSPACE:  
                    if len(self.path) > 1:  
                        self.path.pop()  
                        self.current_pos = list(self.path[-1])  
                    return  
                
                dx, dy = 0, 0  
                if event.key == K_UP: dy = 1  
                elif event.key == K_DOWN: dy = -1  
                elif event.key == K_LEFT: dx = -1  
                elif event.key == K_RIGHT: dx = 1  
                else: return  
                
                new_x = self.current_pos[0] + dx  
                new_y = self.current_pos[1] + dy  
                
                # 碰撞检测
                if self.is_obstructed(new_x, new_y):
                    return
                
                if not (0 <= new_x <= GRID_SIZE and 0 <= new_y <= GRID_SIZE):  
                    return  
                if (new_x, new_y) in self.path:  
                    return  
                if abs(new_x - self.current_pos[0]) + abs(new_y - self.current_pos[1]) != 1:  
                    return  
                
                self.current_pos = [new_x, new_y]  
                self.path.append(tuple(self.current_pos))  

    def check_finish(self):  
        current = tuple(self.current_pos)  
        for name, pos in POINTS.items():  
            if name != 'start' and current == pos:  
                self.finished = True  
                return name  
        return None  

    def run(self):  
        while self.running:  
            self.screen.fill(COLORS['background'])  
            self.handle_input()  
            
            # 绘制
            self.draw_grid()  
            self.draw_obstacles()  
            self.draw_path()  
            self.draw_points()  
            
            # 状态信息显示
            time_text = self.font.render(
                f"时间: {time.time()-self.start_time:.1f}秒", True, (0,0,0))  
            steps_text = self.font.render(
                f"步数: {len(self.path)-1}", True, (0,0,0))  
            self.screen.blit(time_text, (10, 10))  
            self.screen.blit(steps_text, (10, 35))  
            
            if result := self.check_finish():  
                finish_text = self.font.render(
                    f"到达 {result}！总步数: {len(self.path)-1}", 
                    True, (0,0,255))  
                self.screen.blit(finish_text, (WIDTH//2-150, HEIGHT//2))  
            
            pygame.display.flip()  
            self.clock.tick(30)  
            
        pygame.quit()  

if __name__ == "__main__":  
    game = PathGame()  
    game.run()