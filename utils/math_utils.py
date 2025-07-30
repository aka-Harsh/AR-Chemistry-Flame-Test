"""
Mathematical utility functions for AR Chemistry Flame Test Simulator
"""

import math
import numpy as np

def distance_2d(point1, point2):
    """Calculate 2D distance between two points"""
    return math.sqrt((point1[0] - point2[0])**2 + (point1[1] - point2[1])**2)

def normalize_vector(vector):
    """Normalize a 2D vector"""
    length = math.sqrt(vector[0]**2 + vector[1]**2)
    if length == 0:
        return (0, 0)
    return (vector[0] / length, vector[1] / length)

def lerp(start, end, factor):
    """Linear interpolation between two values"""
    return start + (end - start) * factor

def clamp(value, min_val, max_val):
    """Clamp value between min and max"""
    return max(min_val, min(max_val, value))

def smooth_step(edge0, edge1, x):
    """Smooth step function for smooth transitions"""
    t = clamp((x - edge0) / (edge1 - edge0), 0.0, 1.0)
    return t * t * (3.0 - 2.0 * t)

def simple_noise_2d(x, y, scale=1.0, octaves=1):
    """Simple 2D noise implementation to replace Perlin noise"""
    x *= scale
    y *= scale
    
    noise_value = 0
    amplitude = 1
    frequency = 1
    
    for _ in range(octaves):
        noise_value += amplitude * ((math.sin(x * frequency * 12.9898 + y * frequency * 78.233) * 43758.5453) % 1.0 - 0.5)
        amplitude *= 0.5
        frequency *= 2
    
    return noise_value

def rotate_point(point, center, angle):
    """Rotate point around center by angle (in radians)"""
    cos_angle = math.cos(angle)
    sin_angle = math.sin(angle)
    
    # Translate to origin
    x = point[0] - center[0]
    y = point[1] - center[1]
    
    # Rotate
    rotated_x = x * cos_angle - y * sin_angle
    rotated_y = x * sin_angle + y * cos_angle
    
    # Translate back
    return (rotated_x + center[0], rotated_y + center[1])

def point_in_circle(point, center, radius):
    """Check if point is inside circle"""
    return distance_2d(point, center) <= radius

def point_in_rectangle(point, rect_top_left, rect_bottom_right):
    """Check if point is inside rectangle"""
    x, y = point
    x1, y1 = rect_top_left
    x2, y2 = rect_bottom_right
    return x1 <= x <= x2 and y1 <= y <= y2

def generate_circle_points(center, radius, num_points):
    """Generate points on a circle"""
    points = []
    for i in range(num_points):
        angle = (i / num_points) * 2 * math.pi
        x = center[0] + radius * math.cos(angle)
        y = center[1] + radius * math.sin(angle)
        points.append((int(x), int(y)))
    return points

def bezier_curve(points, t):
    """Calculate point on Bezier curve at parameter t (0-1)"""
    n = len(points) - 1
    result = np.array([0.0, 0.0])
    
    for i, point in enumerate(points):
        bernstein = math.comb(n, i) * (t ** i) * ((1 - t) ** (n - i))
        result += bernstein * np.array(point)
    
    return tuple(result.astype(int))

def wave_function(time, frequency, amplitude, phase=0):
    """Generate wave value"""
    return amplitude * math.sin(2 * math.pi * frequency * time + phase)

def ease_in_out(t):
    """Ease in-out function for smooth animations"""
    return t * t * (3.0 - 2.0 * t)

def random_in_range(min_val, max_val):
    """Generate random value in range"""
    import random
    return random.uniform(min_val, max_val)

def map_range(value, in_min, in_max, out_min, out_max):
    """Map value from one range to another"""
    return (value - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

def gaussian_falloff(distance, max_distance):
    """Calculate Gaussian falloff based on distance"""
    if distance >= max_distance:
        return 0
    normalized_distance = distance / max_distance
    return math.exp(-normalized_distance * normalized_distance * 5)

def calculate_fps(frame_times):
    """Calculate FPS from frame time history"""
    if len(frame_times) < 2:
        return 0
    
    total_time = frame_times[-1] - frame_times[0]
    frame_count = len(frame_times) - 1
    
    if total_time <= 0:
        return 0
    
    return frame_count / total_time