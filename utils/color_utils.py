"""
Color manipulation utilities for AR Chemistry Flame Test Simulator
"""

import math
import numpy as np

def rgb_to_hsv(r, g, b):
    """Convert RGB to HSV color space"""
    r, g, b = r/255.0, g/255.0, b/255.0
    max_val = max(r, g, b)
    min_val = min(r, g, b)
    diff = max_val - min_val
    
    # Value
    v = max_val
    
    # Saturation
    s = 0 if max_val == 0 else diff / max_val
    
    # Hue
    if diff == 0:
        h = 0
    elif max_val == r:
        h = (60 * ((g - b) / diff) + 360) % 360
    elif max_val == g:
        h = (60 * ((b - r) / diff) + 120) % 360
    else:
        h = (60 * ((r - g) / diff) + 240) % 360
    
    return h, s, v

def hsv_to_rgb(h, s, v):
    """Convert HSV to RGB color space"""
    c = v * s
    x = c * (1 - abs(((h / 60) % 2) - 1))
    m = v - c
    
    if 0 <= h < 60:
        r, g, b = c, x, 0
    elif 60 <= h < 120:
        r, g, b = x, c, 0
    elif 120 <= h < 180:
        r, g, b = 0, c, x
    elif 180 <= h < 240:
        r, g, b = 0, x, c
    elif 240 <= h < 300:
        r, g, b = x, 0, c
    else:
        r, g, b = c, 0, x
    
    r, g, b = (r + m) * 255, (g + m) * 255, (b + m) * 255
    return int(r), int(g), int(b)

def blend_colors(color1, color2, factor):
    """Blend two colors with given factor (0-1)"""
    r1, g1, b1 = color1
    r2, g2, b2 = color2
    
    r = int(r1 * (1 - factor) + r2 * factor)
    g = int(g1 * (1 - factor) + g2 * factor)
    b = int(b1 * (1 - factor) + b2 * factor)
    
    return (r, g, b)

def adjust_brightness(color, factor):
    """Adjust color brightness by factor"""
    r, g, b = color
    return (
        min(255, max(0, int(r * factor))),
        min(255, max(0, int(g * factor))),
        min(255, max(0, int(b * factor)))
    )

def adjust_saturation(color, factor):
    """Adjust color saturation by factor"""
    r, g, b = color
    h, s, v = rgb_to_hsv(r, g, b)
    s = min(1.0, max(0.0, s * factor))
    return hsv_to_rgb(h, s, v)

def color_temperature_to_rgb(temperature_k):
    """Convert color temperature (Kelvin) to RGB"""
    # Simplified algorithm for flame colors
    temp = temperature_k / 100
    
    if temp <= 66:
        red = 255
        green = min(255, max(0, 99.4708025861 * math.log(temp) - 161.1195681661))
    else:
        red = min(255, max(0, 329.698727446 * (temp - 60) ** -0.1332047592))
        green = min(255, max(0, 288.1221695283 * (temp - 60) ** -0.0755148492))
    
    if temp >= 66:
        blue = 255
    elif temp <= 19:
        blue = 0
    else:
        blue = min(255, max(0, 138.5177312231 * math.log(temp - 10) - 305.0447927307))
    
    return (int(blue), int(green), int(red))  # BGR format

def wavelength_to_rgb(wavelength_nm):
    """Convert wavelength (nanometers) to RGB color"""
    # Visible spectrum: 380-750 nm
    wavelength = max(380, min(750, wavelength_nm))
    
    if 380 <= wavelength < 440:
        red = -(wavelength - 440) / (440 - 380)
        green = 0.0
        blue = 1.0
    elif 440 <= wavelength < 490:
        red = 0.0
        green = (wavelength - 440) / (490 - 440)
        blue = 1.0
    elif 490 <= wavelength < 510:
        red = 0.0
        green = 1.0
        blue = -(wavelength - 510) / (510 - 490)
    elif 510 <= wavelength < 580:
        red = (wavelength - 510) / (580 - 510)
        green = 1.0
        blue = 0.0
    elif 580 <= wavelength < 645:
        red = 1.0
        green = -(wavelength - 645) / (645 - 580)
        blue = 0.0
    else:  # 645 <= wavelength <= 750
        red = 1.0
        green = 0.0
        blue = 0.0
    
    # Intensity falloff near edges
    if 380 <= wavelength < 420:
        factor = 0.3 + 0.7 * (wavelength - 380) / (420 - 380)
    elif 420 <= wavelength < 700:
        factor = 1.0
    else:  # 700 <= wavelength <= 750
        factor = 0.3 + 0.7 * (750 - wavelength) / (750 - 700)
    
    red = int(255 * red * factor)
    green = int(255 * green * factor)
    blue = int(255 * blue * factor)
    
    return (blue, green, red)  # BGR format

def create_flame_gradient(base_color, steps=10):
    """Create flame color gradient from cool to hot"""
    colors = []
    b, g, r = base_color
    
    for i in range(steps):
        factor = i / (steps - 1)
        
        # Add heat (yellow/white) as we go up
        heat_factor = factor * 0.7
        new_r = min(255, int(r + heat_factor * (255 - r)))
        new_g = min(255, int(g + heat_factor * (255 - g) * 0.8))
        new_b = min(255, int(b + heat_factor * 50))
        
        colors.append((new_b, new_g, new_r))
    
    return colors

def mix_chemical_colors(color1, color2, mixing_type='average'):
    """Mix two chemical colors using different algorithms"""
    if mixing_type == 'average':
        return blend_colors(color1, color2, 0.5)
    
    elif mixing_type == 'additive':
        # RGB additive mixing
        r1, g1, b1 = color1
        r2, g2, b2 = color2
        return (
            min(255, r1 + r2),
            min(255, g1 + g2),
            min(255, b1 + b2)
        )
    
    elif mixing_type == 'subtractive':
        # Approximate subtractive mixing
        r1, g1, b1 = color1
        r2, g2, b2 = color2
        return (
            int((r1 * r2) / 255),
            int((g1 * g2) / 255),
            int((b1 * b2) / 255)
        )
    
    elif mixing_type == 'realistic':
        # More realistic chemical mixing
        # Dominant color wins but mixed
        r1, g1, b1 = color1
        r2, g2, b2 = color2
        
        # Find dominant color channel
        intensity1 = max(r1, g1, b1)
        intensity2 = max(r2, g2, b2)
        
        if intensity1 > intensity2:
            return blend_colors(color1, color2, 0.3)
        else:
            return blend_colors(color2, color1, 0.3)
    
    return blend_colors(color1, color2, 0.5)

def generate_flame_flicker_color(base_color, time_factor, intensity=0.1):
    """Generate flickering flame color variation"""
    r, g, b = base_color
    
    # Add random variation
    variation = intensity * math.sin(time_factor * 10) * 50
    
    r = max(0, min(255, int(r + variation)))
    g = max(0, min(255, int(g + variation * 0.8)))
    b = max(0, min(255, int(b + variation * 0.5)))
    
    return (b, g, r)

def get_complementary_color(color):
    """Get complementary color"""
    r, g, b = color
    return (255 - b, 255 - g, 255 - r)

def get_analogous_colors(color, count=3):
    """Get analogous colors in color wheel"""
    r, g, b = color
    h, s, v = rgb_to_hsv(r, g, b)
    
    colors = []
    step = 30  # degrees
    
    for i in range(count):
        new_h = (h + i * step) % 360
        new_color = hsv_to_rgb(new_h, s, v)
        colors.append(new_color)
    
    return colors

def calculate_color_distance(color1, color2):
    """Calculate perceptual distance between colors"""
    r1, g1, b1 = color1
    r2, g2, b2 = color2
    
    # Simple Euclidean distance in RGB space
    return math.sqrt((r1 - r2)**2 + (g1 - g2)**2 + (b1 - b2)**2)

def normalize_color(color):
    """Normalize color values to 0-255 range"""
    r, g, b = color
    return (
        max(0, min(255, int(r))),
        max(0, min(255, int(g))),
        max(0, min(255, int(b)))
    )