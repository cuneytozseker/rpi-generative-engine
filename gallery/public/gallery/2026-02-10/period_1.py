import cairo
import math
import random

# Setup
width, height = 600, 480
surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
ctx = cairo.Context(surface)

# Background: Deep matte charcoal for high contrast
ctx.set_source_rgb(0.02, 0.02, 0.05)
ctx.paint()

def get_dist(p1, p2):
    return math.sqrt((p1[0]-p2[0])**2 + (p1[1]-p2[1])**2)

def clip_polygon(poly, a, b, c):
    """Clips a polygon by a line ax + by + c <= 0"""
    new_poly = []
    if not poly: return []
    for i in range(len(poly)):
        p1 = poly[i]
        p2 = poly[(i + 1) % len(poly)]
        
        d1 = a * p1[0] + b * p1[1] + c
        d2 = a * p2[0] + b * p2[1] + c
        
        if d1 <= 0:
            if d2 <= 0:
                new_poly.append(p2)
            else:
                # Intersection
                t = d1 / (d1 - d2)
                new_poly.append((p1[0] + t * (p2[0] - p1[0]), p1[1] + t * (p2[1] - p1[1])))
        elif d2 <= 0:
            # Intersection
            t = d1 / (d1 - d2)
            new_poly.append((p1[0] + t * (p2[0] - p1[0]), p1[1] + t * (p2[1] - p1[1])))
            new_poly.append(p2)
    return new_poly

# 1. Generate Nodal Seeds (Jittered Grid for Digital Formalism)
points = []
cols, rows = 8, 6
spacing_x = width / cols
spacing_y = height / rows

for i in range(cols + 1):
    for j in range(rows + 1):
        px = i * spacing_x + random.uniform(-spacing_x*0.4, spacing_x*0.4)
        py = j * spacing_y + random.uniform(-spacing_y*0.4, spacing_y*0.4)
        points.append((px, py))

# 2. Draw Voronoi Cells with Gradients
for i, p in enumerate(points):
    # Start with canvas bounds
    cell = [(0,0), (width, 0), (width, height), (0, height)]
    
    # Clip by every other point's bisector
    # To optimize and keep it visually clean, only check nearby points
    nearby = sorted(points, key=lambda other: get_dist(p, other))[1:12]
    
    for other in nearby:
        # Perpendicular bisector between p and other
        # Midpoint M
        mx, my = (p[0] + other[0]) / 2, (p[1] + other[1]) / 2
        # Normal vector (dx, dy)
        dx, dy = other[0] - p[0], other[1] - p[1]
        # Line eq: dx(x - mx) + dy(y - my) = 0  => dx*x + dy*y - (dx*mx + dy*my) = 0
        a, b = dx, dy
        c = -(dx * mx + dy * my)
        cell = clip_polygon(cell, a, b, c)

    if len(cell) > 2:
        # Draw the cell
        ctx.move_to(cell[0][0], cell[0][1])
        for cp in cell[1:]:
            ctx.line_to(cp[0], cp[1])
        ctx.close_path()
        
        # Gradient logic: from seed towards a random edge
        angle = random.uniform(0, math.pi * 2)
        grad = cairo.LinearGradient(p[0], p[1], p[0] + math.cos(angle)*100, p[1] + math.sin(angle)*100)
        
        # Color palette: Cyan, Electric Blue, White, Black
        base_hue = random.choice([0.1, 0.5, 0.6]) # Swiss-style limited range
        grad.add_color_stop_rgba(0, base_hue, 0.8, 1.0, 0.4) # Transparent center
        grad.add_color_stop_rgba(1, 0, 0, 0, 0.0)
        
        ctx.set_source(grad)
        ctx.fill_preserve()
        
        # Precision stroke
        ctx.set_source_rgba(0.8, 0.9, 1.0, 0.15)
        ctx.set_line_width(0.5)
        ctx.stroke()

# 3. Nodal Connections (Proximity Network)
ctx.set_line_width(0.3)
for p1 in points:
    for p2 in points:
        d = get_dist(p1, p2)
        if 20 < d < 120:
            ctx.set_source_rgba(1, 1, 1, (1 - d/120) * 0.3)
            ctx.move_to(p1[0], p1[1])
            ctx.line_to(p2[0], p2[1])
            ctx.stroke()

# 4. Digital Blueprint Artifacts
for p in points:
    # Small crosshair at nodes
    ctx.set_source_rgba(1, 1, 1, 0.6)
    ctx.set_line_width(1.0)
    size = 3
    ctx.move_to(p[0] - size, p[1]); ctx.line_to(p[0] + size, p[1])
    ctx.move_to(p[0], p[1] - size); ctx.line_to(p[0], p[1] + size)
    ctx.stroke()
    
    # Tiny numerical labels (simulating data)
    if random.random() > 0.7:
        ctx.set_source_rgba(0.5, 0.7, 1.0, 0.5)
        ctx.select_font_face("monospace", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)
        ctx.set_font_size(6)
        ctx.move_to(p[0] + 5, p[1] - 5)
        ctx.show_text(f"{p[0]:.1f}")

# 5. Global Geometric Overlay (Vector Field Hint)
ctx.set_source_rgba(1, 1, 1, 0.03)
for i in range(0, width, 20):
    ctx.move_to(i, 0)
    ctx.line_to(i, height)
ctx.stroke()

# Finishing: Subtle vignette
vig = cairo.RadialGradient(width/2, height/2, 100, width/2, height/2, width*0.7)
vig.add_color_stop_rgba(0, 0, 0, 0, 0)
vig.add_color_stop_rgba(1, 0, 0, 0, 0.6)
ctx.set_source(vig)
ctx.paint()
