import cairo
import math
import random

# Setup
width, height = 600, 480
surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
ctx = cairo.Context(surface)

# Background: Deep void
ctx.set_source_rgb(0.02, 0.02, 0.03)
ctx.paint()

# Configuration
center_x, center_y = width / 2, height / 2
rings = 40
spokes = 72
phi = (1 + math.sqrt(5)) / 2  # Golden ratio for spacing
accent_color = (1.0, 0.31, 0.0) # International Orange (Swiss/Brutalist accent)

def polar_to_cartesian(r, theta, distortion_factor=0):
    # Apply radial distortion based on a harmonic function
    r_distorted = r * (1 + distortion_factor * math.sin(theta * 6))
    x = center_x + r_distorted * math.cos(theta)
    y = center_y + r_distorted * math.sin(theta)
    return x, y

# 1. GENERATE THE NON-LINEAR GRID DATA
# Using a power function for radial growth to create central density and peripheral expansion
grid_points = []
for i in range(rings):
    ring_data = []
    # Progressively increase radius using a non-linear scale
    r = math.pow(i / rings, 1.2) * (width * 0.7)
    
    # Modulate radius with a "kinetic" wave
    r_modulation = 15 * math.sin(i * 0.2)
    
    for j in range(spokes):
        theta = (j / spokes) * 2 * math.pi
        # Add slight spiral twist
        theta += (i * 0.02) 
        
        x, y = polar_to_cartesian(r + r_modulation, theta, distortion_factor=0.05 * (i/rings))
        ring_data.append((x, y))
    grid_points.append(ring_data)

# 2. DRAW RELATIONAL NETWORKS (Background web)
ctx.set_line_width(0.3)
for i in range(1, rings):
    for j in range(spokes):
        # Connect to neighbors with varying opacity based on distance
        alpha = 0.1 + (0.4 * (1 - i/rings))
        ctx.set_source_rgba(0.8, 0.8, 0.9, alpha)
        
        p1 = grid_points[i][j]
        p2 = grid_points[i-1][(j + 1) % spokes] # Diagonal connection
        
        ctx.move_to(p1[0], p1[1])
        ctx.line_to(p2[0], p2[1])
        ctx.stroke()

# 3. DRAW PRIMARY AXIAL STRUCTURES
for j in range(0, spokes, 4):
    ctx.set_source_rgba(1, 1, 1, 0.6)
    ctx.set_line_width(0.7)
    ctx.move_to(center_x, center_y)
    for i in range(rings):
        p = grid_points[i][j]
        ctx.line_to(p[0], p[1])
    ctx.stroke()

# 4. LINE WEIGHT MODULATION & SYSTEMIC INTERRUPTIONS
for i in range(2, rings, 2):
    # Determine ring importance
    is_major = i % 8 == 0
    ctx.set_line_width(1.5 if is_major else 0.5)
    
    for j in range(spokes):
        p1 = grid_points[i][j]
        p2 = grid_points[i][(j + 1) % spokes]
        
        # Random algorithmic "interruption" (dither-like gaps)
        if random.random() > 0.1:
            if is_major and random.random() > 0.96:
                # Saturated Chromatic Accent
                ctx.set_source_rgb(*accent_color)
                ctx.set_line_width(3.0)
                ctx.arc(p1[0], p1[1], 2, 0, 2*math.pi)
                ctx.fill()
                ctx.move_to(p1[0], p1[1])
                ctx.line_to(p2[0], p2[1])
                ctx.stroke()
                ctx.set_line_width(1.5)
            else:
                ctx.set_source_rgba(1, 1, 1, 0.8 if is_major else 0.3)
                ctx.move_to(p1[0], p1[1])
                ctx.line_to(p2[0], p2[1])
                ctx.stroke()

# 5. GRANULAR DITHER PATTERNS (Digital artifacts)
# Creating texture through accumulated noise at intersections
for _ in range(1200):
    r_idx = random.randint(0, rings - 1)
    s_idx = random.randint(0, spokes - 1)
    px, py = grid_points[r_idx][s_idx]
    
    # Offset noise
    ox = random.uniform(-3, 3)
    oy = random.uniform(-3, 3)
    
    size = random.uniform(0.5, 1.5)
    opacity = random.uniform(0.2, 0.7)
    
    ctx.set_source_rgba(1, 1, 1, opacity)
    ctx.rectangle(px + ox, py + oy, size, size)
    ctx.fill()

# 6. CENTRAL ANCHOR (Swiss Precision)
ctx.set_source_rgb(1, 1, 1)
ctx.set_line_width(1)
ctx.arc(center_x, center_y, 4, 0, 2*math.pi)
ctx.stroke()
ctx.move_to(center_x - 15, center_y)
ctx.line_to(center_x + 15, center_y)
ctx.move_to(center_x, center_y - 15)
ctx.line_to(center_x, center_y + 15)
ctx.stroke()

# Framing elements
ctx.set_source_rgba(1, 1, 1, 0.05)
ctx.set_line_width(40)
ctx.rectangle(0, 0, width, height)
ctx.stroke()

