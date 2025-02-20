import pygame  
from pygame.locals import *  

# 游戏配置  
GRID_SIZE = 50  
CELL_SIZE = 10  
WIDTH = HEIGHT = GRID_SIZE * CELL_SIZE  

# 颜色配置  
COLORS = {  
    'background': (255, 255, 255),  
    'grid': (200, 200, 200),  
    'start': (0, 255, 0),  
    'close1': (255, 165, 0),  
    'close2': (0, 128, 0),  
    'far1': (255, 192, 203),  
    'far2': (128, 0, 128),  
    'obstacle': (100, 100, 100)  
}  

# 关键点坐标  
POINTS = {  
    'start': (7, 42),  
    'close1': (20, 18),  
    'close2': (31, 29),  
    'far1': (5, 1),  
    'far2': (48, 44)  
}  

# 障碍物定义  
ORIGINAL_OBSTACLES = [  
    (9, 9, 8, 1),    
    (8, 8, 12, 1),    
    (10, 10, 6, 1),  
    (11, 7, 4, 1),  

    (14, 25, 6, 1), 
    (13, 24, 5, 1),  
    (15, 26, 3, 1),  
    (10, 23, 7, 1),   

    (24, 15, 5, 1), 
    (27, 14, 2, 1),  
    (23, 16, 6, 1),  

    (3, 31, 6, 1),
    (4, 32, 4, 1),
    (5, 30, 3, 1),

    (44, 9, 5, 1),
    (43, 10, 3, 1),
    (45, 8, 4, 1),

]  

# 手动计算的对称障碍物  
MIRRORED_OBSTACLES = [  

    (39, 32, 1, 8),    
    (40, 29, 1, 12),    
    (38, 33, 1, 6),    
    (41, 34, 1, 4),

    (23, 29, 1, 6),   
    (24, 31, 1, 5),  
    (22, 31, 1, 3),  
    (25, 32, 1, 7),
    
    (33, 20, 1, 5),   
    (34, 20, 1, 2),  
    (32, 20, 1, 6),
    
    (17, 40, 1, 6),  
    (16, 41, 1, 4),  
    (18, 41, 1, 3),
    
    (39, 0, 1, 5),    
    (38, 3, 1, 3),    
    (40, 0, 1, 4),
]  

# 合并所有障碍物  
ALL_OBSTACLES = ORIGINAL_OBSTACLES + MIRRORED_OBSTACLES  

class PathGame:  
    def __init__(self):  
        pygame.init()  
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))  
        pygame.display.set_caption("对称障碍物路径游戏")  
        self.clock = pygame.time.Clock()  
        self.running = True  

    def convert_coords(self, x, y):  
        """将逻辑坐标转换为屏幕坐标（左下原点转左上原点）"""  
        return (x * CELL_SIZE, (GRID_SIZE - y - 1) * CELL_SIZE)  

    def draw_grid(self):  
        """绘制网格系统"""  
        for i in range(GRID_SIZE + 1):  
            pygame.draw.line(self.screen, COLORS['grid'],  
                           (i*CELL_SIZE, 0), (i*CELL_SIZE, HEIGHT))  
            pygame.draw.line(self.screen, COLORS['grid'],  
                           (0, i*CELL_SIZE), (WIDTH, i*CELL_SIZE))  

    def draw_obstacles(self):  
        """绘制所有障碍物"""  
        for x, y, w, h in ALL_OBSTACLES:  
            pygame.draw.rect(self.screen, COLORS['obstacle'],  
                           (x*CELL_SIZE, (GRID_SIZE - y - h)*CELL_SIZE,  
                            w*CELL_SIZE, h*CELL_SIZE))  

    def draw_points(self):  
        """绘制所有关键点"""  
        for name, (x, y) in POINTS.items():  
            pos = self.convert_coords(x, y)  
            pygame.draw.circle(self.screen, COLORS.get(name, (0,0,0)), pos, 6)  

    def run(self):  
        """主游戏循环"""  
        while self.running:  
            for event in pygame.event.get():  
                if event.type == QUIT:  
                    self.running = False  

            self.screen.fill(COLORS['background'])  
            self.draw_grid()  
            self.draw_obstacles()  
            self.draw_points()  
            
            pygame.display.flip()  
            self.clock.tick(30)  
        
        pygame.quit()  

if __name__ == "__main__":  
    game = PathGame()  
    game.run()  