import pygame  
import time  
from pygame.locals import *  


# 游戏配置  
GRID_SIZE = 49  # 0-49共50个坐标点  
CELL_SIZE = 15   # 像素尺寸  
WIDTH, HEIGHT = GRID_SIZE * CELL_SIZE, GRID_SIZE * CELL_SIZE  

# 颜色  
COLORS = {  
    'background': (255, 255, 255),  
    'grid': (211, 211, 211),  
    'start': (0, 0, 255),  
    'current': (255, 0, 0),  
    'close 1': (255, 165, 0),  
    'close 2': (0, 128, 0),  
    'far 1': (255, 192, 203),  
    'far 2': (128, 0, 128)  
}  

# 坐标点
POINTS = {  
    'start': (7, 42),  
    'close 1': (20, 18),  
    'close 2': (31, 29),  
    'far 1': (5, 1),  
    'far 2': (48, 44)  
}  

class PathGame:  
    def __init__(self):  
        pygame.init()  
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))  
        pygame.display.set_caption("Grid Path Game")  
        self.clock = pygame.time.Clock()  
        self.font = pygame.font.SysFont('Arial', 20)  
        
        # 游戏状态初始化  
        self.current_pos = list(POINTS['start'])  
        self.path = [tuple(self.current_pos)]  # 路径记录  
        self.start_time = time.time()  
        self.running = True  
        self.finished = False  

    def convert_coords(self, x, y):  
        """将逻辑坐标转换为屏幕坐标（左下角原点转左上角）"""  
        return (x * CELL_SIZE, (GRID_SIZE - y) * CELL_SIZE)  

    def draw_grid(self):  
        """绘制网格系统"""  
        for i in range(GRID_SIZE + 1):  
            pygame.draw.line(self.screen, COLORS['grid'],  
                            (i * CELL_SIZE, 0), (i * CELL_SIZE, HEIGHT))  
            pygame.draw.line(self.screen, COLORS['grid'],  
                            (0, i * CELL_SIZE), (WIDTH, i * CELL_SIZE))  

    def draw_points(self):  
        """绘制所有关键点"""  
        for name, (x, y) in POINTS.items():  
            pos = self.convert_coords(x, y)  
            color = COLORS.get(name, (0,0,0))  
            pygame.draw.circle(self.screen, color, pos, 6)  
        
        # 绘制当前位置（红色点）  
        pygame.draw.circle(self.screen, COLORS['current'],  
                          self.convert_coords(*self.current_pos), 6)  

    def draw_path(self):  
        """绘制玩家路径"""  
        if len(self.path) > 1:  
            points = [self.convert_coords(x, y) for x, y in self.path]  
            pygame.draw.lines(self.screen, (0,0,0), False, points, 2)  

    def handle_input(self):  
        """处理键盘输入"""  
        for event in pygame.event.get():  
            if event.type == QUIT:  
                self.running = False  
                
            if event.type == KEYDOWN and not self.finished:  
                # 撤回逻辑  
                if event.key == K_BACKSPACE:  
                    if len(self.path) > 1:  
                        self.path.pop()  
                        self.current_pos = list(self.path[-1])  
                    return  
                
                # 方向控制  
                dx, dy = 0, 0  
                if event.key == K_UP: dy = 1  
                elif event.key == K_DOWN: dy = -1  
                elif event.key == K_LEFT: dx = -1  
                elif event.key == K_RIGHT: dx = 1  
                else: return  # 忽略其他按键  
                
                # 计算新坐标  
                new_x = self.current_pos[0] + dx  
                new_y = self.current_pos[1] + dy  
                
                # 移动验证  
                if not (0 <= new_x <= GRID_SIZE and 0 <= new_y <= GRID_SIZE):  
                    return  # 超出边界  
                if (new_x, new_y) in self.path:  
                    return  # 路径重复  
                if abs(new_x - self.current_pos[0]) + abs(new_y - self.current_pos[1]) != 1:  
                    return  # 非相邻移动  
                
                # 更新状态  
                self.current_pos = [new_x, new_y]  
                self.path.append(tuple(self.current_pos))  

    def check_finish(self):  
        """检测是否到达终点"""  
        current = tuple(self.current_pos)  
        for name, pos in POINTS.items():  
            if name != 'start' and current == pos:  
                self.finished = True  
                return name  
        return None  

    def run(self):  
        """主游戏循环"""  
        while self.running:  
            self.screen.fill(COLORS['background'])  
            self.handle_input()  
            
            # 绘制 
            self.draw_grid()  
            self.draw_points()  
            self.draw_path()  
            
            # 显示统计信息（后期可以去掉显示页面）  
            time_text = self.font.render(  
                f"时间: {time.time()-self.start_time:.1f}秒", True, (0,0,0))  
            steps_text = self.font.render(  
                f"步数: {len(self.path)-1}", True, (0,0,0))  
            self.screen.blit(time_text, (10, 10))  
            self.screen.blit(steps_text, (10, 35))  
            
            # 完成检测  
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