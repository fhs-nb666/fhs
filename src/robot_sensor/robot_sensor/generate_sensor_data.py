import numpy as np
import os

def generate_straight_line_motion():
    """生成直线运动数据"""
    print("生成直线运动数据...")
    t = np.arange(0, 10, 0.01)  # 10秒，100Hz
    x = 1.0 + 0.5 * t  # x方向匀速运动
    y = 2.0 + 0.3 * t  # y方向匀速运动
    
    # 添加白噪声
    noise_x = np.random.normal(0, 0.05, len(t))
    noise_y = np.random.normal(0, 0.05, len(t))
    
    x += noise_x
    y += noise_y
    
    with open('data/sensor_data_straight.txt', 'w') as f:
        f.write("# 直线运动数据 (x y)\n")
        for i in range(len(t)):
            f.write(f"{x[i]:.3f} {y[i]:.3f}\n")
    print("生成完成: data/sensor_data_straight.txt")

def generate_circular_motion():
    """生成圆周运动数据"""
    print("生成圆周运动数据...")
    t = np.arange(0, 10, 0.01)
    radius = 2.0
    omega = 1.0  # 角速度
    
    x = radius * np.cos(omega * t)
    y = radius * np.sin(omega * t)
    
    # 添加白噪声
    noise_x = np.random.normal(0, 0.05, len(t))
    noise_y = np.random.normal(0, 0.05, len(t))
    
    x += noise_x
    y += noise_y
    
    with open('data/sensor_data_circle.txt', 'w') as f:
        f.write("# 圆周运动数据 (x y)\n")
        for i in range(len(t)):
            f.write(f"{x[i]:.3f} {y[i]:.3f}\n")
    print("生成完成: data/sensor_data_circle.txt")

def generate_random_motion():
    """生成随机运动数据"""
    print("生成随机运动数据...")
    num_points = 1000
    x = np.cumsum(np.random.normal(0, 0.1, num_points))
    y = np.cumsum(np.random.normal(0, 0.1, num_points))
    
    with open('data/sensor_data_random.txt', 'w') as f:
        f.write("# 随机运动数据 (x y)\n")
        for i in range(num_points):
            f.write(f"{x[i]:.3f} {y[i]:.3f}\n")
    print("生成完成: data/sensor_data_random.txt")

if __name__ == "__main__":
    # 创建数据目录
    data_dir = "data"
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)
    
    generate_straight_line_motion()
    generate_circular_motion()
    generate_random_motion()
    
    print("\n所有数据文件已生成在 'data' 目录中")