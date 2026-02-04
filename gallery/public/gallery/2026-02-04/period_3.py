import cairo
import math
import random

# Setup
width, height = 600, 480
surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
ctx = cairo.Context(surface)

# Background - Deep Brutalist Charcoal
ctx.set_source_rgb(0.05, 0.05, 0.05)
ctx.paint()

def get_voronoi_seeds(cols, rows, jitter):
    """Generates a grid of seeds with systematic entropy."""
    seeds = []
    dx = width / cols
    dy = height / rows
    for i in range(cols + 1):
        for j in range(rows + 1):
            # Entropy increases based on distance from center
            dist_to_center = math.sqrt(((i/cols)-0.5)**2 + ((j/rows)-0.5)**2)
            local_jitter = jitter * dist_to_center * 2.0
            
            x = i * dx + random.uniform(-local_jitter, local_jitter)
            y = j * dy + random.uniform(-local_jitter, local_jitter)
            seeds.append((x, y))
    return seeds

def clip_polygon(poly, a, b):
    """Clips a polygon against the perpendicular bisector of segment ab."""
    def is_inside(p, a, b):
        # Returns True if p is on the same side of the bisector as a
        # Bisector passes through mid, normal is b-a
        mid_x, mid_y = (a[0] + b[0]) / 2, (a[1] + b[1]) / 2
        nx, ny = b[0] - a[0], b[1] - a[1]
        return (p[0] - mid_x) * nx + (p[1] - mid_y) * ny < 0

    def intersect(p1, p2, a, b):
        mid_x, mid_y = (a[0] + b[0]) / 2, (a[1] + b[1]) / 2
        nx, ny = b[0] - a[0], b[1] - a[1]
        # Line p1-p2: P = p1 + t(p2-p1)
        # Plane: (P - M) . N = 0
        dx, dy = p2[0] - p1[0], p2[1] - p1[1]
        denom = dx * nx + dy * ny
        if abs(denom) < 1e-9: return p1
        t = ((mid_x - p1[0]) * nx + (mid_y - p1[1]) * ny) / denom
        return (p1[0] + t * dx, p1[1] + t * dy)

    new_poly = []
    if not poly: return []
    for i in range(len(poly)):
        p1 = poly[i]
        p2 = poly[(i + 1) % len(poly)]
        if is_inside(p1, a, b):
            if is_inside(p2, a, b):
                new_poly.append(p2)
            else:
                new_poly.append(intersect(p1, p2, a, b))
        elif is_inside(p2, a, b):
            new_poly.append(intersect(p1, p2, a, b))
            new_poly.append(p2)
    return new_poly

# Parameters
cols, rows = 8, 6
seeds = get_voronoi_seeds(cols, rows, 45)

# Generate and Draw Cells
for i, s1 in enumerate(seeds):
    # Start with a bounding box for the cell
    cell = [(0, 0), (width, 0), (width, height), (0, height)]
    
    # Clip against all other seeds (Optimization: only nearby seeds, but this is fine for this scale)
    for j, s2 in enumerate(seeds):
        if i == j: continue
        # Only clip if reasonably close to keep it efficient and relevant
        dist_sq = (s1[0]-s2[0])**2 + (s1[1]-s2[1])**2
        if dist_sq < 250**2:
            cell = clip_polygon(cell, s1, s2)
    
    if len(cell) < 3: continue

    # Draw Cell Base
    ctx.move_to(cell[0][0], cell[0][1])
    for p in cell[1:]:
        ctx.line_to(p[0], p[1])
    ctx.close_path()
    
    # Gradient Fill - Systematic depth
    grad = cairo.LinearGradient(s1[0], s1[1], cell[0][0], cell[0][1])
    lum = random.uniform(0.1, 0.3)
    grad.add_color_stop_rgba(0, lum, lum, lum, 0.8)
    grad.add_color_stop_rgba(1, 0, 0, 0, 0.2)
    ctx.set_source(grad)
    ctx.fill_preserve()
    
    # Optical Gray Texture: Recursive insets
    ctx.set_line_width(0.3)
    for step in range(1, 6):
        shrink = step * 3.5
        ctx.set_source_rgba(1, 1, 1, 0.15 / step)
        ctx.save()
        # Visual trick: stroke inside with varying alpha to create "glow/depth"
        ctx.stroke_preserve()
        ctx.restore()
        
    # Main Cell Border
    ctx.set_source_rgba(1, 1, 1, 0.5)
    ctx.set_line_width(0.7)
    ctx.stroke()

# Networked Architecture Layer: Connecting seeds with hair-thin lines
ctx.set_line_width(0.2)
for i, s1 in enumerate(seeds):
    for j, s2 in enumerate(seeds[i+1:]):
        dist = math.sqrt((s1[0]-s2[0])**2 + (s1[1]-s2[1])**2)
        if 40 < dist < 110:
            ctx.set_source_rgba(1, 1, 1, (110-dist)/200)
            ctx.move_to(s1[0], s1[1])
            ctx.line_to(s2[0], s2[1])
            ctx.stroke()

# Focal Points - Systematic Nodes
for s in seeds:
    # Outer ring
    ctx.set_source_rgba(1, 1, 1, 0.2)
    ctx.arc(s[0], s[1], 2, 0, math.pi * 2)
    ctx.stroke()
    # Inner Core
    ctx.set_source_rgba(1, 1, 1, 0.8)
    ctx.arc(s[0], s[1], 0.8, 0, math.pi * 2)
    ctx.fill()

# Final Hierarchy Polish: A high-contrast rectangular frame (Swiss style)
ctx.set_line_width(20)
ctx.set_source_rgb(0, 0, 0)
ctx.rectangle(0, 0, width, height)
ctx.stroke()

ctx.set_line_width(1)
ctx.set_source_rgb(1, 1, 1)
ctx.rectangle(30, 30, width-60, height-60)
ctx.stroke()
