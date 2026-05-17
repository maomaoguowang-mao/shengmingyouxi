import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# ===================== 1. 解决中文乱码问题 =====================
plt.rcParams['toolbar'] = 'None'
plt.rcParams['font.sans-serif'] = ['SimHei']   # 设置黑体
plt.rcParams['axes.unicode_minus'] = False     # 解决负号显示问题

# ===================== 可调整参数 =====================
GRID_SIZE = 40       # 网格大小（40x40）
UPDATE_SPEED = 1000   # 演化速度（毫秒，越小越快）
CELL_EDGE_COLOR = 'black'  # 细胞边框颜色（和网格线配合）
# ======================================================

# 全局变量
grid = np.zeros((GRID_SIZE, GRID_SIZE), dtype=int)
is_running = False
ani = None

# --------------------- 鼠标点击：绘制/删除细胞 ---------------------
def on_click(event):
    if event.inaxes is None or is_running:
        return
    # 获取点击的细胞坐标
    j = int(np.round(event.xdata))
    i = int(np.round(event.ydata))
    if 0 <= i < GRID_SIZE and 0 <= j < GRID_SIZE:
        grid[i, j] = 1 - grid[i, j]  # 切换细胞状态
        img.set_data(grid)
        fig.canvas.draw_idle()  # 重绘图像（含网格）

# --------------------- 键盘控制：空格开始/暂停，R重置 ---------------------
def on_key(event):
    global is_running, grid
    if event.key == ' ':
        is_running = not is_running
    elif event.key == 'r':
        grid = np.zeros((GRID_SIZE, GRID_SIZE), dtype=int)
        is_running = False
        img.set_data(grid)
        fig.canvas.draw_idle()

# --------------------- 生命游戏核心演化规则 ---------------------
def update(frame):
    global grid
    if not is_running:
        return img,
    
    new_grid = grid.copy()
    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            # ✅ 修复：固定边界，超出地图的邻居按死细胞算，不循环
            neighbors = 0
            for di in (-1, 0, 1):
                for dj in (-1, 0, 1):
                    if di == 0 and dj == 0:
                        continue
                    ni = i + di
                    nj = j + dj
                    # 只统计地图内的邻居，超出范围的不算
                    if 0 <= ni < GRID_SIZE and 0 <= nj < GRID_SIZE:
                        neighbors += grid[ni, nj]
            
            # 生命游戏规则
            if grid[i, j] == 1:
                if neighbors < 2 or neighbors > 3:
                    new_grid[i, j] = 0
            else:
                if neighbors == 3:
                    new_grid[i, j] = 1

    grid = new_grid
    img.set_data(grid)
    return img,

# ===================== 初始化界面（网格永久显示） =====================
fig, ax = plt.subplots(figsize=(8, 8))
fig.canvas.toolbar_visible = False
# 1. 显示细胞，关闭插值，让每个细胞是清晰方块
img = ax.imshow(
    grid, 
    cmap="binary", 
    vmin=0, vmax=1,
    interpolation='nearest',  # 关键：关闭模糊插值，细胞是方块
    zorder=1  # 细胞层级低于网格线
)

# 2. 设置坐标轴范围，让网格线正好框住每个细胞
ax.set_xlim(-0.5, GRID_SIZE - 0.5)
ax.set_ylim(-0.5, GRID_SIZE - 0.5)

# 3. 设置网格线（关键：层级高于细胞，永久显示）
ax.set_xticks(np.arange(-0.5, GRID_SIZE, 1))
ax.set_yticks(np.arange(-0.5, GRID_SIZE, 1))
ax.grid(
    True, 
    color='black', 
    linewidth=1.0, 
    zorder=2,  # 网格线在细胞上方，不会被覆盖
    linestyle='-'
)

# 4. 隐藏刻度标签
ax.set_xticklabels([])
ax.set_yticklabels([])
ax.tick_params(length=0)  # 隐藏刻度线

# 绑定鼠标/键盘事件
fig.canvas.mpl_connect("button_press_event", on_click)
fig.canvas.mpl_connect("key_press_event", on_key)

# 设置中文标题
ax.set_title(
    "生命游戏 | 鼠标点击绘制 | 空格开始/暂停 | R键重置", 
    fontsize=12, 
    pad=15
)

# --------------------- 启动动画（关闭blit，让网格永久显示） ---------------------
ani = animation.FuncAnimation(
    fig, 
    update, 
    interval=UPDATE_SPEED, 
    blit=False  # 关键：关闭blit，每次重绘整个画面（含网格线）
)

plt.tight_layout()
plt.show()
