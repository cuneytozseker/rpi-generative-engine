import cairo
import math
import random

# Setup
width, height = 600, 480
surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
ctx = cairo.Context(surface)

# Background: Deep Cobalt Technical Schematic
ctx.set_source_rgb(0.02, 0.05, 0.1)
ctx.paint()

# Configuration
ISO_ANGLE = math.pi / 6  # 30 degrees
SCALE = 22
COLS, ROWS, DEPTH = 12, 12, 8
OFFSET_X, OFFSET_Y = width / 2, height / 2.2

def iso_projection(x, y, z):
    """Project 3D coordinates to 2D isometric space."""
    px = (x - y) * math.cos(ISO_ANGLE) * SCALE
    py = (x + y) * math.sin(ISO_ANGLE) * SCALE - (z * SCALE * 1.1)
    return px + OFFSET_X, py + OFFSET_Y

def draw_rhombus(ctx, x, y, type="top", color=(1, 1, 1, 1)):
    """Draw one of the three faces of an isometric cube."""
    ctx.set_source_rgba(*color)
    ctx.move_to(x, y)
    
    dx = math.cos(ISO_ANGLE) * SCALE
    dy = math.sin(ISO_ANGLE) * SCALE
    
    if type == "top":
        ctx.line_to(x + dx, y - dy)
        ctx.line_to(x + 2 * dx, y)
        ctx.line_to(x + dx, y + dy)
    elif type == "left":
        ctx.line_to(x, y + SCALE * 1.1)
        ctx.line_to(x + dx, y + dy + SCALE * 1.1)
        ctx.line_to(x + dx, y + dy)
    elif type == "right":
        ctx.line_to(x - dx, y + dy)
        ctx.line_to(x - dx, y + dy + SCALE * 1.1)
        ctx.line_to(x, y + SCALE * 1.1)
        
    ctx.close_path()
    ctx.fill()

# 1. Background Grid: Faint "Shattered Matrix" Lines
ctx.set_line_width(0.5)
ctx.set_source_rgba(0.2, 0.4, 0.8, 0.15)
for i in range(-15, 15):
    # Longitudinal lines
    x1, y1 = iso_projection(i, -15, 0)
    x2, y2 = iso_projection(i, 15, 0)
    ctx.move_to(x1, y1); ctx.line_to(x2, y2); ctx.stroke()
    # Latitudinal lines
    x1, y1 = iso_projection(-15, i, 0)
    x2, y2 = iso_projection(15, i, 0)
    ctx.move_to(x1, y1); ctx.line_to(x2, y2); ctx.stroke()

# 2. Procedural Crystal Generation
# We iterate through a 3D grid and decide whether to draw a cube based on "clustering logic"
lattice_data = []
for z in range(DEPTH):
    for y in range(ROWS):
        for x in range(COLS):
            # Distance from center for clustering effect
            dist = math.sqrt((x-COLS/2)**2 + (y-ROWS/2)**2 + (z-DEPTH/2)**2)
            probability = math.exp(-dist * 0.35) # Gaussian-like falloff
            
            if random.random() < probability:
                lattice_data.append((x, y, z))

# Sort cubes by depth (Painter's algorithm: back to front)
# In Isometric, back cubes are those with lower x+y and lower z
lattice_data.sort(key=lambda p: (p[0] + p[1], p[2]))

# 3. Draw Cubes with Depth Shadows
for x, y, z in lattice_data:
    px, py = iso_projection(x, y, z)
    
    # Colors for isometric faces based on light source from top-left
    # Cobalt schematic palette
    top_c = (0.4, 0.7, 1.0, 0.9)    # Brightest
    left_c = (0.15, 0.3, 0.6, 0.9)   # Mid
    right_c = (0.05, 0.15, 0.4, 0.9) # Shadow
    
    # Draw faces
    draw_rhombus(ctx, px, py - SCALE * 1.1, "top", top_c)
    draw_rhombus(ctx, px, py - SCALE * 1.1, "left", left_c)
    draw_rhombus(ctx, px + math.cos(ISO_ANGLE)*SCALE, py - SCALE*1.1 + math.sin(ISO_ANGLE)*SCALE, "right", right_c)
    
    # Wireframe highlights for a "technical" look
    ctx.set_source_rgba(1, 1, 1, 0.3)
    ctx.set_line_width(0.7)
    ctx.move_to(px, py - SCALE * 1.1)
    ctx.line_to(px, py)
    ctx.stroke()

# 4. Connecting "Data-Mass" Lines
# Draw lines between nearby nodes to simulate a network
ctx.set_line_width(0.3)
ctx.set_source_rgba(0.5, 0.8, 1.0, 0.4)
for i in range(len(lattice_data)):
    p1 = lattice_data[i]
    # Check a few subsequent neighbors in the list
    for j in range(i+1, min(i+15, len(lattice_data))):
        p2 = lattice_data[j]
        # Manhattan distance check
        if abs(p1[0]-p2[0]) + abs(p1[1]-p2[1]) + abs(p1[2]-p2[2]) <= 1:
            x1, y1 = iso_projection(*p1)
            x2, y2 = iso_projection(*p2)
            ctx.move_to(x1, y1 - SCALE * 0.5)
            ctx.line_to(x2, y2 - SCALE * 0.5)
            ctx.stroke()

# 5. Visual "Noise" and Annotations
# Small '+' symbols at random grid intersections to enhance schematic feel
for _ in range(40):
    rx, ry = random.randint(0, COLS), random.randint(0, ROWS)
    rz = random.randint(0, DEPTH)
    px, py = iso_projection(rx, ry, rz)
    
    ctx.set_source_rgba(0.8, 0.9, 1.0, 0.6)
    ctx.set_line_width(1.0)
    size = 3
    ctx.move_to(px - size, py); ctx.line_to(px + size, py)
    ctx.move_to(px, py - size); ctx.line_to(px, py + size)
    ctx.stroke()

# 6. Framing: Minimalist Geometric Legend
ctx.set_source_rgb(0.3, 0.5, 0.8)
ctx.rectangle(20, 20, 150, 2)
ctx.fill()
ctx.set_source_rgba(0.3, 0.5, 0.8, 0.5)
for i in range(5):
    ctx.rectangle(20 + (i*30), 28, 10, 2)
    ctx.fill()

# Finish
