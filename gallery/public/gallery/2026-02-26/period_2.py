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

def get_voronoi_points(n, w, h):
    points = []
    for i in range(n):
        # Using a modulated grid for "Swiss entropy"
        # Points follow a general grid but are displaced by a vector field
        ix = i % 8
        iy = i // 8
        tx = (ix + 0.5) * (w / 8)
        ty = (iy + 0.5) * (h / 6)
        
        angle = math.sin(tx * 0.01) * math.cos(ty * 0.01) * math.pi * 2
        mag = 40.0
        px = tx + math.cos(angle) * mag + random.uniform(-20, 20)
        py = ty + math.sin(angle) * mag + random.uniform(-20, 20)
        points.append((px, py))
    return points

def clip_poly(poly, p1, p2):
    """Clips a polygon against the half-plane defined by the bisector of p1 and p2."""
    new_poly = []
    # Bisector line: points x such that dist(x, p1) == dist(x, p2)
    # Midpoint
    mx, my = (p1[0] + p2[0]) / 2, (p1[1] + p2[1]) / 2
    # Normal vector from p1 to p2
    nx, ny = p2[0] - p1[0], p2[1] - p1[1]

    for i in range(len(poly)):
        curr = poly[i]
        prev = poly[(i - 1) % len(poly)]
        
        # Dot product determines which side of the bisector the point is on
        # dot > 0 means it's closer to p2, dot < 0 means closer to p1
        def is_inside(p):
            return (p[0] - mx) * nx + (p[1] - my) * ny < 0

        if is_inside(curr):
            if not is_inside(prev):
                # Intersection
                t = ((mx - prev[0]) * nx + (my - prev[1]) * ny) / ((curr[0] - prev[0]) * nx + (curr[1] - prev[1]) * ny)
                new_poly.append((prev[0] + t * (curr[0] - prev[0]), prev[1] + t * (curr[1] - prev[1])))
            new_poly.append(curr)
        elif is_inside(prev):
            # Intersection
            t = ((mx - prev[0]) * nx + (my - prev[1]) * ny) / ((curr[0] - prev[0]) * nx + (curr[1] - prev[1]) * ny)
            new_poly.append((prev[0] + t * (curr[0] - prev[0]), prev[1] + t * (curr[1] - prev[1])))
    return new_poly

# 1. Background Schematic Grid
ctx.set_line_width(0.5)
ctx.set_source_rgba(0.1, 0.2, 0.4, 0.3)
for i in range(0, width, 20):
    ctx.move_to(i, 0)
    ctx.line_to(i, height)
ctx.stroke()
for j in range(0, height, 20):
    ctx.move_to(0, j)
    ctx.line_to(width, j)
ctx.stroke()

# 2. Generate Voronoi Geometry
pts = get_voronoi_points(48, width, height)

for i, p in enumerate(pts):
    # Start with canvas bounds
    cell = [(0, 0), (width, 0), (width, height), (0, height)]
    for j, other_p in enumerate(pts):
        if i == j: continue
        cell = clip_poly(cell, p, other_p)
    
    if not cell: continue

    # Draw Cell with Gradient (Visual Texture)
    ctx.move_to(cell[0][0], cell[0][1])
    for cp in cell[1:]:
        ctx.line_to(cp[0], cp[1])
    ctx.close_path()
    
    # Create a pulse effect based on position
    dist_center = math.sqrt((p[0]-width/2)**2 + (p[1]-height/2)**2)
    intensity = math.cos(dist_center * 0.02) * 0.5 + 0.5
    
    # Gradient: Deep Ultramarine to Obsidian
    grad = cairo.RadialGradient(p[0], p[1], 2, p[0], p[1], 150)
    grad.add_color_stop_rgba(0, 0.0, 0.4 * intensity, 0.9 * intensity, 0.15)
    grad.add_color_stop_rgba(1, 0.02, 0.02, 0.03, 0)
    
    ctx.set_source(grad)
    ctx.fill_preserve()
    
    # Hairline Borders
    ctx.set_source_rgba(0.5, 0.7, 1.0, 0.2 * intensity + 0.1)
    ctx.set_line_width(0.4)
    ctx.stroke()

# 3. Kinetic Flow Overlay (Dashed Lines)
random.seed(42)
for _ in range(15):
    ctx.set_source_rgba(0.8, 0.9, 1.0, 0.15)
    ctx.set_dash([random.uniform(2, 10), random.uniform(5, 15)])
    y_pos = random.uniform(0, height)
    ctx.move_to(0, y_pos)
    # Parametric curve through the "current"
    for x in range(0, width + 40, 40):
        wave = math.sin(x * 0.01 + y_pos) * 30
        ctx.line_to(x, y_pos + wave)
    ctx.set_line_width(0.8)
    ctx.stroke()
ctx.set_dash([]) # Reset dash

# 4. Notational Elements (The Schematic)
ctx.select_font_face("monospace", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)
ctx.set_font_size(8)

for i, p in enumerate(pts):
    if random.random() > 0.6:
        # Crosshair
        size = 4
        ctx.set_source_rgba(1, 1, 1, 0.4)
        ctx.set_line_width(0.5)
        ctx.move_to(p[0]-size, p[1])
        ctx.line_to(p[0]+size, p[1])
        ctx.move_to(p[0], p[1]-size)
        ctx.line_to(p[0], p[1]+size)
        ctx.stroke()
        
        # Numeric Labels (Simulated Metadata)
        if random.random() > 0.5:
            ctx.set_source_rgba(0.3, 0.6, 1.0, 0.6)
            label = f"{p[0]/10:.1f}:{p[1]/10:.1f}"
            ctx.move_to(p[0] + 6, p[1] - 6)
            ctx.show_text(label)

# 5. Global Texture Contrast
# Add a vertical "data bar" for Swiss-inspired hierarchy
ctx.set_source_rgba(0.0, 0.5, 1.0, 0.8)
ctx.rectangle(width - 40, 40, 2, height - 80)
ctx.fill()

ctx.set_source_rgba(1, 1, 1, 0.9)
ctx.set_font_size(12)
ctx.save()
ctx.translate(width - 30, height - 40)
ctx.rotate(-math.pi/2)
ctx.show_text("KINETIC_SCHEMATIC_V.04")
ctx.restore()

# Final Polish: Localized Heat Map highlights
for _ in range(5):
    cx, cy = random.uniform(0, width), random.uniform(0, height)
    heat = cairo.RadialGradient(cx, cy, 0, cx, cy, 100)
    heat.add_color_stop_rgba(0, 0.0, 0.8, 1.0, 0.05)
    heat.add_color_stop_rgba(1, 0, 0, 0, 0)
    ctx.set_source(heat)
    ctx.paint()

