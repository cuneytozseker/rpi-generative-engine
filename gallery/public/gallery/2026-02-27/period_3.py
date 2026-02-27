import cairo
import math
import random

# Setup
width, height = 600, 480
surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
ctx = cairo.Context(surface)

# Background: Off-white "Paper"
ctx.set_source_rgb(0.96, 0.96, 0.94)
ctx.paint()

# Colors: Technical Cobalt and Stark Black
COBALT = (0.05, 0.2, 0.6)
BLACK = (0.1, 0.1, 0.1)
GREY = (0.4, 0.4, 0.4)

def draw_truchet_tile(x, y, size, variant, color, weight, alpha=1.0):
    """Draws a specific Truchet tile variant at (x, y)."""
    ctx.save()
    ctx.translate(x + size/2, y + size/2)
    # Random rotation for variety
    ctx.rotate(random.choice([0, math.pi/2, math.pi, 3*math.pi/2]))
    ctx.translate(-size/2, -size/2)
    
    r, g, b = color
    ctx.set_source_rgba(r, g, b, alpha)
    ctx.set_line_width(weight)
    
    if variant == 0: # Arcs
        ctx.arc(0, 0, size/2, 0, math.pi/2)
        ctx.stroke()
        ctx.arc(size, size, size/2, math.pi, 3*math.pi/2)
        ctx.stroke()
    elif variant == 1: # Diagonals
        ctx.move_to(0, 0)
        ctx.line_to(size, size)
        ctx.stroke()
    elif variant == 2: # "Dithered" cross
        step = size / 4
        for i in range(1, 4):
            ctx.move_to(i * step, 0)
            ctx.line_to(i * step, size)
            ctx.move_to(0, i * step)
            ctx.line_to(size, i * step)
        ctx.set_line_width(weight * 0.5)
        ctx.stroke()
    
    ctx.restore()

def draw_technical_marking(x, y, size):
    """Adds 'technical archeology' annotations."""
    ctx.set_source_rgba(0.1, 0.1, 0.1, 0.6)
    ctx.set_line_width(0.5)
    
    # Crosshair
    length = size * 0.2
    ctx.move_to(x - length, y)
    ctx.line_to(x + length, y)
    ctx.move_to(x, y - length)
    ctx.line_to(x, y + length)
    ctx.stroke()
    
    # Random "Coordinate" snippet
    if random.random() > 0.7:
        ctx.select_font_face("monospace", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)
        ctx.set_font_size(size * 0.15)
        ctx.move_to(x + 5, y - 5)
        ctx.show_text(f"{x:.0f}.{y:.0f}")

# --- LAYER 1: Large structural arcs (The "Blueprint") ---
grid_size = 120
ctx.set_line_cap(cairo.LINE_CAP_ROUND)
for i in range(width // grid_size + 1):
    for j in range(height // grid_size + 1):
        # Introduce entropy: skip some tiles to create "voids"
        if random.random() > 0.2:
            draw_truchet_tile(i * grid_size, j * grid_size, grid_size, 0, COBALT, 4.0, 0.3)

# --- LAYER 2: Medium density subdivision (The "System") ---
grid_size = 40
for i in range(width // grid_size):
    for j in range(height // grid_size):
        # Logic: Denser patterns in the center, decaying towards edges
        dist_to_center = math.sqrt(((i*grid_size - width/2)**2 + (j*grid_size - height/2)**2))
        prob = 1.0 - (dist_to_center / (width * 0.8))
        
        if random.random() < prob:
            variant = random.choice([0, 1])
            alpha = random.uniform(0.4, 0.8)
            draw_truchet_tile(i * grid_size, j * grid_size, grid_size, variant, BLACK, 1.2, alpha)

# --- LAYER 3: Micro-structure (The "Dithered Decay") ---
grid_size = 10
for i in range(width // grid_size):
    for j in range(height // grid_size):
        if random.random() > 0.94:
            draw_truchet_tile(i * grid_size, j * grid_size, grid_size, 2, BLACK, 0.3, 0.4)

# --- LAYER 4: Fragments and "Fractures" ---
# Drawing irregular polygons as "clipping" masks for high-density fills
for _ in range(5):
    ctx.save()
    fx, fy = random.randint(0, width), random.randint(0, height)
    fw, fh = random.randint(40, 150), random.randint(40, 150)
    
    # Draw a dense block of info
    ctx.rectangle(fx, fy, fw, fh)
    ctx.clip()
    
    # Fill with dithered pattern
    sub_grid = 5
    ctx.set_source_rgba(0.05, 0.2, 0.6, 0.15)
    for sx in range(fx, fx+fw, sub_grid):
        for sy in range(fy, fy+fh, sub_grid):
            if (sx+sy) % (sub_grid*2) == 0:
                ctx.rectangle(sx, sy, sub_grid, sub_grid)
    ctx.fill()
    
    # Boundary of the fracture
    ctx.set_source_rgba(0, 0, 0, 0.8)
    ctx.set_line_width(0.5)
    ctx.rectangle(fx, fy, fw, fh)
    ctx.stroke()
    ctx.restore()

# --- LAYER 5: Technical Annotations ---
# Placing coordinate markers and node links
nodes = []
for _ in range(20):
    nx, ny = random.randint(20, width-20), random.randint(20, height-20)
    nodes.append((nx, ny))
    draw_technical_marking(nx, ny, 30)

# Connect some nodes with hair-line paths
ctx.set_source_rgba(0.1, 0.1, 0.1, 0.2)
ctx.set_line_width(0.3)
for i in range(len(nodes)-1):
    if random.random() > 0.6:
        ctx.move_to(*nodes[i])
        # Orthogonal paths (Swiss/Technical feel)
        mid_x = nodes[i+1][0]
        ctx.line_to(mid_x, nodes[i][1])
        ctx.line_to(*nodes[i+1])
        ctx.stroke()

# Final Frame: Thin border to ground the composition
ctx.set_source_rgb(0, 0, 0)
ctx.set_line_width(2)
ctx.rectangle(10, 10, width-20, height-20)
ctx.stroke()

# Add a small "system signature" block
ctx.rectangle(width-60, height-40, 30, 10)
ctx.fill()
ctx.set_source_rgb(1, 1, 1)
ctx.select_font_face("sans-serif", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
ctx.set_font_size(6)
ctx.move_to(width-58, height-33)
ctx.show_text("VER 4.2.0")

