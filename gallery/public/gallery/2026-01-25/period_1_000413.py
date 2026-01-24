import cairo
import math
import random

# Setup
width, height = 600, 480
surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
ctx = cairo.Context(surface)

# Background: Deep "Forensic" Black
ctx.set_source_rgb(0.02, 0.02, 0.03)
ctx.paint()

# Configuration
NUM_SEEDS = 22
SAMPLES_X = 80
SAMPLES_Y = 60
CELL_COLOR = (0.2, 0.5, 1.0) # International Klein Blue derivative

# 1. Generate Seeds with a "Clustered Density" logic
seeds = []
for _ in range(NUM_SEEDS):
    # Bias seeds towards a central-right axis for asymmetry
    x = random.gauss(width * 0.6, width * 0.25)
    y = random.gauss(height * 0.5, height * 0.3)
    seeds.append({'pos': (x, y), 'id': random.random()})

def get_closest(px, py):
    distances = []
    for i, s in enumerate(seeds):
        d = math.sqrt((px - s['pos'][0])**2 + (py - s['pos'][1])**2)
        distances.append((d, i))
    distances.sort()
    return distances[0], distances[1] # Return 1st and 2nd closest

# 2. Draw Digital Strata (The Voronoi Field via Density)
# Instead of smooth polygons, we use a grid of primitives that react to the Voronoi logic
grid_w = width / SAMPLES_X
grid_h = height / SAMPLES_Y

for i in range(SAMPLES_X):
    for j in range(SAMPLES_Y):
        px = i * grid_w + grid_w / 2
        py = j * grid_h + grid_h / 2
        
        (d1, idx1), (d2, idx2) = get_closest(px, py)
        
        # Determine "edge-ness" - ratio of distance to closest vs second closest
        # This creates the mathematical "Voronoi" border effect
        edge_factor = d1 / (d2 + 0.1)
        
        # Color based on seed identity for variation
        seed_val = seeds[idx1]['id']
        
        # Digital Forensic Aesthetic: Dithered density
        # Near edges, we use thin lines or empty space. Near centers, dense blocks.
        if edge_factor < 0.92:
            # Inside the cell
            # Map distance to a "gradient" of density
            intensity = 1.0 - (d1 / 180.0)
            intensity = max(0.1, min(1.0, intensity))
            
            ctx.set_source_rgba(
                CELL_COLOR[0] * seed_val * intensity,
                CELL_COLOR[1] * intensity,
                CELL_COLOR[2] * intensity + (1-intensity)*0.3,
                0.8
            )
            
            # Draw varied geometric primitives based on local "data"
            size_mod = (math.sin(px * 0.05) + math.cos(py * 0.05)) * 0.5 + 1.0
            rect_w = grid_w * 0.6 * intensity * size_mod
            rect_h = grid_h * 0.2 * intensity
            
            ctx.rectangle(px - rect_w/2, py - rect_h/2, rect_w, rect_h)
            ctx.fill()
        else:
            # On the "Border" - draw technical marking
            ctx.set_source_rgba(1, 1, 1, 0.4)
            ctx.set_line_width(0.4)
            ctx.arc(px, py, 0.5, 0, 2*math.pi)
            ctx.stroke()

# 3. Add Vector Connections (Node-Link system)
ctx.set_line_width(0.3)
ctx.set_source_rgba(1, 1, 1, 0.15)
for i in range(len(seeds)):
    for j in range(i + 1, len(seeds)):
        s1 = seeds[i]['pos']
        s2 = seeds[j]['pos']
        dist = math.sqrt((s1[0]-s2[0])**2 + (s1[1]-s2[1])**2)
        if dist < 140: # Only connect nearby seeds
            ctx.move_to(s1[0], s1[1])
            ctx.line_to(s2[0], s2[1])
            ctx.stroke()

# 4. Global Cartesian Grid Overlay (Swiss precision)
ctx.set_source_rgba(1, 1, 1, 0.05)
ctx.set_line_width(0.5)
grid_spacing = 40
for x in range(0, width, grid_spacing):
    ctx.move_to(x, 0)
    ctx.line_to(x, height)
    ctx.stroke()
for y in range(0, height, grid_spacing):
    ctx.move_to(0, y)
    ctx.line_to(width, y)
    ctx.stroke()

# 5. Technical Callouts (Recursive/Text-like noise)
random.seed(42) # Deterministic noise for callouts
for _ in range(12):
    tx = random.uniform(50, width-50)
    ty = random.uniform(50, height-50)
    
    # Draw a "crosshair" or "data block"
    ctx.set_source_rgba(1, 1, 1, 0.7)
    ctx.set_line_width(0.8)
    # Horizontal line
    ctx.move_to(tx - 15, ty)
    ctx.line_to(tx + 15, ty)
    # Little vertical tick
    ctx.move_to(tx - 15, ty - 2)
    ctx.line_to(tx - 15, ty + 2)
    ctx.stroke()
    
    # Micro-rectangles mimicking data segments
    for bit in range(4):
        if random.random() > 0.5:
            ctx.rectangle(tx - 12 + (bit * 7), ty + 4, 4, 2)
            ctx.fill()

# 6. Final Polish: Vignette/Depth
# Soft radial gradient to center the composition
rad_grad = cairo.RadialGradient(width/2, height/2, 100, width/2, height/2, 400)
rad_grad.add_color_stop_rgba(0, 0, 0, 0, 0)
rad_grad.add_color_stop_rgba(1, 0, 0, 0, 0.4)
ctx.set_source(rad_grad)
ctx.paint()

# "Scanning Line" - high contrast forensic artifact
ctx.set_source_rgba(1, 1, 1, 0.03)
ctx.rectangle(0, height * 0.7, width, 2)
ctx.fill()

