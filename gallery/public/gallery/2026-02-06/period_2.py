import cairo
import math
import random

# Setup
width, height = 600, 480
surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
ctx = cairo.Context(surface)

# Background - Deep Charcoal
ctx.set_source_rgb(0.05, 0.05, 0.07)
ctx.paint()

def get_voronoi_cells(seeds, width, height):
    """
    Computes Voronoi cells by clipping a bounding box against 
    perpendicular bisectors of seed points.
    """
    cells = []
    for i, p1 in enumerate(seeds):
        # Start with the canvas boundary as the initial polygon
        poly = [(0, 0), (width, 0), (width, height), (0, height)]
        
        for j, p2 in enumerate(seeds):
            if i == j:
                continue
            
            # Midpoint and direction of the perpendicular bisector
            mid_x, mid_y = (p1[0] + p2[0]) / 2, (p1[1] + p2[1]) / 2
            dx, dy = p2[0] - p1[0], p2[1] - p1[1]
            
            new_poly = []
            for k in range(len(poly)):
                a = poly[k]
                b = poly[(k + 1) % len(poly)]
                
                # Evaluation of point relative to bisector line
                # (x - mid_x) * dx + (y - mid_y) * dy < 0 is the half-plane containing p1
                def is_inside(p):
                    return (p[0] - mid_x) * dx + (p[1] - mid_y) * dy < 0
                
                if is_inside(a):
                    if is_inside(b):
                        new_poly.append(b)
                    else:
                        # Intersection point
                        t = ((mid_x - a[0]) * dx + (mid_y - a[1]) * dy) / ((b[0] - a[0]) * dx + (b[1] - a[1]) * dy)
                        new_poly.append((a[0] + t * (b[0] - a[0]), a[1] + t * (b[1] - a[1])))
                else:
                    if is_inside(b):
                        # Intersection point
                        t = ((mid_x - a[0]) * dx + (mid_y - a[1]) * dy) / ((b[0] - a[0]) * dx + (b[1] - a[1]) * dy)
                        new_poly.append((a[0] + t * (b[0] - a[0]), a[1] + t * (b[1] - a[1])))
                        new_poly.append(b)
            poly = new_poly
        cells.append(poly)
    return cells

# Generate Seeds with "Structural Tension" (Cluster-Grid Hybrid)
seeds = []
grid_size = 4
for i in range(grid_size):
    for j in range(grid_size):
        # Base grid position with significant random displacement
        x = (i + 0.5) * (width / grid_size) + random.uniform(-60, 60)
        y = (j + 0.5) * (height / grid_size) + random.uniform(-60, 60)
        seeds.append((x, y))

# Additional "Noise" seeds for complexity
for _ in range(12):
    seeds.append((random.uniform(0, width), random.uniform(0, height)))

# Calculate Cells
voronoi_cells = get_voronoi_cells(seeds, width, height)

# Draw Underlying Subtle Grid (Swiss Precision)
ctx.set_line_width(0.5)
ctx.set_source_rgba(1, 1, 1, 0.05)
grid_spacing = 40
for x in range(0, width, grid_spacing):
    ctx.move_to(x, 0)
    ctx.line_to(x, height)
ctx.stroke()
for y in range(0, height, grid_spacing):
    ctx.move_to(0, y)
    ctx.line_to(width, y)
ctx.stroke()

# Draw Voronoi Cells
for i, poly in enumerate(voronoi_cells):
    if not poly: continue
    
    # 1. Fill with Value-Ramp Gradient
    seed = seeds[i]
    grad = cairo.RadialGradient(seed[0], seed[1], 5, seed[0], seed[1], 150)
    base_val = random.uniform(0.1, 0.2)
    grad.add_color_stop_rgba(0, base_val, base_val, base_val + 0.05, 0.4)
    grad.add_color_stop_rgba(1, 0, 0, 0, 0)
    
    ctx.new_path()
    for pt in poly:
        ctx.line_to(pt[0], pt[1])
    ctx.close_path()
    ctx.set_source(grad)
    ctx.fill()

    # 2. Emergent Texture: Fine Hatching inside cells
    ctx.save()
    ctx.new_path()
    for pt in poly: ctx.line_to(pt[0], pt[1])
    ctx.close_path()
    ctx.clip()
    
    ctx.set_line_width(0.3)
    ctx.set_source_rgba(0.8, 0.8, 0.9, 0.15)
    angle = (i * math.pi / 7) # Systematic variation
    step = 4
    for d in range(-600, 1200, step):
        ctx.move_to(d * math.cos(angle), d * math.sin(angle))
        ctx.line_to(d * math.cos(angle) - 1000 * math.sin(angle), 
                    d * math.sin(angle) + 1000 * math.cos(angle))
    ctx.stroke()
    ctx.restore()

    # 3. Structural Outlines
    ctx.set_line_width(0.6)
    ctx.set_source_rgba(1, 1, 1, 0.25)
    ctx.new_path()
    for pt in poly:
        ctx.line_to(pt[0], pt[1])
    ctx.close_path()
    ctx.stroke()

# Chromatic Accents & Data Nodes
for i, seed in enumerate(seeds):
    # Draw small "data nodes"
    ctx.set_source_rgba(1, 1, 1, 0.7)
    ctx.arc(seed[0], seed[1], 1.2, 0, math.pi*2)
    ctx.fill()
    
    # Randomly highlight specific nodes with high-chroma accents
    if random.random() > 0.85:
        accent_colors = [(1, 0.2, 0.2), (0.2, 0.6, 1.0), (1, 0.8, 0)]
        color = random.choice(accent_colors)
        
        # Small geometric marker
        ctx.set_source_rgb(*color)
        ctx.rectangle(seed[0] - 4, seed[1] - 4, 8, 2)
        ctx.fill()
        
        # Connectivity line
        ctx.set_line_width(0.4)
        ctx.set_source_rgba(*color, 0.4)
        ctx.move_to(seed[0], seed[1])
        ctx.line_to(seed[0], height - 20)
        ctx.stroke()

# Technical Artifacts (Typography/Labels)
ctx.select_font_face("Monospace", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)
ctx.set_font_size(8)
ctx.set_source_rgba(1, 1, 1, 0.4)
for i in range(5):
    ctx.move_to(20, 20 + i*12)
    ctx.show_text(f"NODE_SYS_REF: 0x{random.randint(1000, 9999)}")

ctx.move_to(width - 120, height - 20)
ctx.show_text("STRUCTURAL_LOGIC_V.04")

# Add a final "Atmospheric" layer (Moiré interference)
ctx.set_line_width(0.2)
ctx.set_source_rgba(1, 1, 1, 0.03)
for i in range(0, width, 2):
    ctx.move_to(i, 0)
    ctx.line_to(width - i, height)
ctx.stroke()

# Final Border
ctx.set_line_width(20)
ctx.set_source_rgb(0.05, 0.05, 0.07)
ctx.rectangle(0, 0, width, height)
ctx.stroke()

