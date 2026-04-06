import cairo
import math
import random

# Setup
width, height = 600, 480
surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
ctx = cairo.Context(surface)

# Background: Deep Obsidian
ctx.set_source_rgb(0.02, 0.02, 0.03)
ctx.paint()

# Noise System Configuration
GRID_SIZE = 40
COLS = width // GRID_SIZE + 2
ROWS = height // GRID_SIZE + 2

# Generate a grid of random vectors (angles) for the flow field
angles = [[random.uniform(0, math.pi * 2) for _ in range(ROWS)] for _ in range(COLS)]

def get_angle(x, y):
    # Bilinear interpolation of angles from the grid
    gx = x / GRID_SIZE
    gy = y / GRID_SIZE
    x0 = int(gx)
    y0 = int(gy)
    x1 = min(x0 + 1, COLS - 1)
    y1 = min(y0 + 1, ROWS - 1)
    
    sx = gx - x0
    sy = gy - y0
    
    # Smoothstep interpolation
    sx = sx * sx * (3 - 2 * sx)
    sy = sy * sy * (3 - 2 * sy)
    
    a0 = angles[x0][y0]
    a1 = angles[x1][y0]
    a2 = angles[x0][y1]
    a3 = angles[x1][y1]
    
    interp_top = a0 + sx * (a1 - a0)
    interp_bottom = a2 + sx * (a3 - a2)
    return interp_top + sy * (interp_bottom - interp_top)

# 1. Background Grid (Swiss Precision)
ctx.set_line_width(0.3)
ctx.set_source_rgba(0.2, 0.3, 0.4, 0.2)
for i in range(0, width, 40):
    ctx.move_to(i, 0)
    ctx.line_to(i, height)
    ctx.stroke()
for j in range(0, height, 40):
    ctx.move_to(0, j)
    ctx.line_to(width, j)
    ctx.stroke()

# 2. Flow Field Trails (Organic Emergence)
num_particles = 1200
steps = 60
step_length = 4

for p in range(num_particles):
    # Start particles near center or in clusters for "gravitational pull" effect
    if random.random() > 0.3:
        px = random.gauss(width/2, 100)
        py = random.gauss(height/2, 80)
    else:
        px = random.uniform(0, width)
        py = random.uniform(0, height)
        
    # Varied stroke weights for visual hierarchy
    weight = random.choice([0.1, 0.4, 0.8])
    ctx.set_line_width(weight)
    
    # Colors: Primarily whites/cyans with rare luminous accents
    if random.random() > 0.98:
        ctx.set_source_rgba(0.0, 1.0, 0.8, 0.6) # Cyan accent
    else:
        alpha = random.uniform(0.1, 0.5)
        ctx.set_source_rgba(0.9, 0.95, 1.0, alpha)

    ctx.move_to(px, py)
    for _ in range(steps):
        angle = get_angle(px, py)
        # Add a slight bias towards the horizontal for a "technical diagram" look
        angle = (angle + math.atan2(0, 1)) / 2 if random.random() > 0.7 else angle
        
        px += math.cos(angle) * step_length
        py += math.sin(angle) * step_length
        
        if 0 <= px <= width and 0 <= py <= height:
            ctx.line_to(px, py)
        else:
            break
    ctx.stroke()

# 3. Metadata Layer (Systematic Logic)
def draw_data_point(x, y, label):
    # Crosshair
    ctx.set_line_width(0.5)
    ctx.set_source_rgb(1, 1, 1)
    size = 4
    ctx.move_to(x - size, y)
    ctx.line_to(x + size, y)
    ctx.move_to(x, y - size)
    ctx.line_to(x, y + size)
    ctx.stroke()
    
    # Metadata "string" (simulated text)
    ctx.set_source_rgba(0.8, 0.8, 1.0, 0.8)
    ctx.rectangle(x + 6, y - 6, 20, 2) # Block 1
    ctx.rectangle(x + 6, y - 2, 12, 2) # Block 2
    ctx.fill()

# Place metadata at specific grid intersections
for _ in range(8):
    mx = random.randint(1, (width // GRID_SIZE) - 1) * GRID_SIZE
    my = random.randint(1, (height // GRID_SIZE) - 1) * GRID_SIZE
    draw_data_point(mx, my, "SEC_DATA")

# 4. Global Borders & Scale Bar
ctx.set_line_width(1.0)
ctx.set_source_rgb(1, 1, 1)
margin = 20
ctx.rectangle(margin, margin, width - margin*2, height - margin*2)
ctx.stroke()

# Scale bar (bottom right)
sb_x, sb_y = width - 120, height - 40
ctx.move_to(sb_x, sb_y)
ctx.line_to(sb_x + 80, sb_y)
ctx.move_to(sb_x, sb_y - 5)
ctx.line_to(sb_x, sb_y + 5)
ctx.move_to(sb_x + 40, sb_y - 3)
ctx.line_to(sb_x + 40, sb_y + 3)
ctx.move_to(sb_x + 80, sb_y - 5)
ctx.line_to(sb_x + 80, sb_y + 5)
ctx.stroke()

# Micro-texture: Sparse dots/dithering
for _ in range(200):
    ctx.set_source_rgba(1, 1, 1, random.uniform(0.1, 0.4))
    rx, ry = random.random() * width, random.random() * height
    ctx.arc(rx, ry, 0.5, 0, math.pi * 2)
    ctx.fill()

# Final Polish: Luminous nodal highlights
ctx.set_operator(cairo.OPERATOR_ADD)
for _ in range(15):
    ctx.set_source_rgba(0.2, 0.4, 0.8, 0.2)
    lx, ly = random.uniform(0, width), random.uniform(0, height)
    ctx.arc(lx, ly, random.uniform(10, 30), 0, math.pi*2)
    ctx.fill()

