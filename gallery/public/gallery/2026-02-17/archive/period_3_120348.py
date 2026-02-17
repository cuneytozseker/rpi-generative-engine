import cairo
import math
import random

# Setup
width, height = 600, 480
surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
ctx = cairo.Context(surface)

# Background - Stark White (Swiss Parchment)
ctx.set_source_rgb(0.96, 0.96, 0.95)
ctx.paint()

def generate_field(w, h, scale):
    """Generates a pseudo-Reaction-Diffusion field using interference patterns."""
    cols, rows = int(w / scale), int(h / scale)
    field = [[0.0 for _ in range(rows)] for _ in range(cols)]
    
    # Layering multiple harmonic frequencies to simulate RD-like Turing patterns
    seeds = [(random.uniform(0.05, 0.15), random.uniform(0, math.pi*2)) for _ in range(8)]
    
    for i in range(cols):
        for j in range(rows):
            val = 0
            x, y = i * scale, j * scale
            for freq, phase in seeds:
                # Combining spatial sine waves with varying orientations
                angle = seeds.index((freq, phase)) * (math.pi / 4)
                nx = x * math.cos(angle) + y * math.sin(angle)
                val += math.sin(nx * freq + phase)
            
            # Non-linear thresholding to create "organic" blobs
            field[i][j] = 1.0 if val > 0.8 else 0.0
    return field

# Parameters
grid_scale = 6
field = generate_field(width, height, grid_scale)

# 1. THE UNDERLYING GRID (Rigid Logic)
ctx.set_line_width(0.2)
ctx.set_source_rgba(0.1, 0.1, 0.1, 0.1)
for x in range(0, width, 40):
    ctx.move_to(x, 0)
    ctx.line_to(x, height)
    ctx.stroke()
for y in range(0, height, 40):
    ctx.move_to(0, y)
    ctx.line_to(width, y)
    ctx.stroke()

# 2. THE REACTION-DIFFUSION RENDERING (Fluid Entropy)
cols = len(field)
rows = len(field[0])

for i in range(1, cols - 1):
    for j in range(1, rows - 1):
        x = i * grid_scale
        y = j * grid_scale
        
        # Determine if we are in an "Active" zone
        if field[i][j] == 1.0:
            # Check neighbors to find edges
            is_edge = any(field[i+dx][j+dy] == 0 for dx, dy in [(-1,0), (1,0), (0,-1), (0,1)])
            
            if is_edge:
                # "Technical Sublime" - Thin filaments at transitions
                ctx.set_source_rgb(0, 0, 0)
                ctx.set_line_width(0.4)
                ctx.set_dash([random.uniform(1, 4), random.uniform(1, 2)]) # Stochastic dashing
                ctx.rectangle(x, y, grid_scale, grid_scale)
                ctx.stroke()
                ctx.set_dash([]) # Reset
            else:
                # Solid "Systemic" blocks
                ctx.set_source_rgb(0, 0, 0)
                # Randomly omit some blocks for texture (porosity)
                if random.random() > 0.05:
                    ctx.rectangle(x, y, grid_scale - 0.5, grid_scale - 0.5)
                    ctx.fill()

# 3. TECHNICAL OVERLAYS (Swiss precision)
# Coordinate markers and high-frequency data peaks
for _ in range(12):
    tx = random.randint(0, cols-1)
    ty = random.randint(0, rows-1)
    px, py = tx * grid_scale, ty * grid_scale
    
    # Crosshair markers
    ctx.set_source_rgb(1.0, 0.2, 0.1) # Accent color (data peak)
    ctx.set_line_width(1.0)
    length = 15
    ctx.move_to(px - length, py)
    ctx.line_to(px + length, py)
    ctx.move_to(px, py - length)
    ctx.line_to(px, py + length)
    ctx.stroke()
    
    # Small Annotation (simulated typography)
    ctx.set_source_rgb(0, 0, 0)
    ctx.rectangle(px + 4, py + 4, 20, 2)
    ctx.fill()
    ctx.rectangle(px + 4, py + 8, 12, 2)
    ctx.fill()

# 4. ORTHOGONAL SNAPPING CONNECTORS
# Creating a sense of "mapping" between disparate clusters
ctx.set_line_width(0.3)
ctx.set_source_rgb(0, 0, 0)
for _ in range(5):
    start_x = random.choice([0, width])
    start_y = random.randint(0, height)
    ctx.move_to(start_x, start_y)
    
    curr_x, curr_y = start_x, start_y
    for _ in range(4): # 4-step orthogonal path
        if random.random() > 0.5:
            curr_x += random.choice([-100, 100])
        else:
            curr_y += random.choice([-100, 100])
        ctx.line_to(curr_x, curr_y)
    ctx.stroke()

# 5. MARGINALIA (The Blueprint feel)
ctx.set_line_width(2.0)
ctx.move_to(20, 20)
ctx.line_to(100, 20)
ctx.stroke()
ctx.set_line_width(0.5)
ctx.move_to(20, 30)
ctx.line_to(80, 30)
ctx.stroke()

# Final Polish: Global texture via subtle stochastic points
for _ in range(1000):
    ctx.set_source_rgba(0, 0, 0, random.uniform(0.1, 0.4))
    rx, ry = random.random() * width, random.random() * height
    ctx.rectangle(rx, ry, 0.5, 0.5)
    ctx.fill()

