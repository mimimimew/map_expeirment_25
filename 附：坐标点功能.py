import pygame  
import time  
from pygame.locals import *  


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
    'obstacle': (128, 128, 128)  
}  

# 坐标点配置 
POINTS = {  
    'start': (7, 42),  
    'close 1': (20, 18),  
    'close 2': (31, 29),  
    'far 1': (5, 1),  
    'far 2': (48, 44)  
}  

pygame.init()

# 窗口  
screen = pygame.display.set_mode((WIDTH, HEIGHT))  
pygame.display.set_caption("地图点击显示坐标")

# 绘制网格和坐标点
def draw_grid():
    screen.fill(COLORS['background'])
    
    # 网格
    for x in range(0, WIDTH, CELL_SIZE):
        for y in range(0, HEIGHT, CELL_SIZE):
            pygame.draw.rect(screen, COLORS['grid'], (x, y, CELL_SIZE, CELL_SIZE), 1)
    
    # 坐标点
    for point_name, (x, y) in POINTS.items():

        pygame.draw.circle(screen, COLORS[point_name], (x * CELL_SIZE + CELL_SIZE // 2, (GRID_SIZE - y) * CELL_SIZE + CELL_SIZE // 2), 5)

    pygame.display.flip()

# 获取鼠标当前位置的格子坐标
def get_grid_from_mouse(mouse_pos):
    x, y = mouse_pos
    grid_x = x // CELL_SIZE
    # y 坐标转换：将 y 坐标反转
    grid_y = GRID_SIZE - (y // CELL_SIZE)
    return grid_x, grid_y

# 显示坐标点
def display_coordinates(coords):
    font = pygame.font.Font(None, 30)
    text = font.render(f"Coordinates: {coords}", True, (0, 0, 0))
    screen.blit(text, (10, 10))  # 固定

# 主循环
running = True
while running:
    draw_grid()
    
    # 获取鼠标当前位置
    mouse_x, mouse_y = pygame.mouse.get_pos()
    grid_x, grid_y = get_grid_from_mouse((mouse_x, mouse_y))
    display_coordinates((grid_x, grid_y))
    
    pygame.display.flip()  # 更新显示

    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
    
    time.sleep(0.05)

pygame.quit()
