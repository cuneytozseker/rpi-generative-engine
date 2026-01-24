import cairo
import math
import random

# Setup
width, height = 600, 480
surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
ctx = cairo.Context(surface)

# Background - Deep Matte Black
ctx.set_source_rgb(0.02, 0.02, 0.02)
ctx.paint()

def get_voronoi_points(cols, rows, jitter):
    points = []
    dx = width / cols
    dy = height / rows
    for i in range(cols + 1):
        for j in range(rows + 1):
            px = i * dx + random.uniform(-jitter, jitter)
            py = j * dy + random.uniform(-jitter, jitter)
            points.append((px, py))
    return points

def clip_polygon(poly, a, b, c):
    """Clips a convex polygon against the line ax + by + c <= 0."""
    def dist(p):
        return a * p[0] + b * p[1] + c

    new_poly = []
    if not poly:
        return []
    
    for i in range(len(poly)):
        p1 = poly[i]
        p2 = poly[(i + 1) % len(poly)]
        d1 = dist(p1)
        d2 = dist(p2)

        if d1 <= 0:
            new_poly.append(p1)
        
        if (d1 > 0 and d2 <= 0) or (d1 <= 0 and d2 > 0):
            # Intersection point
            t = d1 / (d1 - d2)
            nx = p1[0] + t * (p2[0] - p1[0])
            ny = p1[1] + t * (p2[1] - p1[1])
            new_poly.append((nx, ny))
    return new_poly

def draw_technical_marks(ctx, x, y, size):
    """Draws small Swiss-style crosshairs or coordinates."""
    ctx.set_line_width(0.5)
    ctx.move_to(x - size, y)
    ctx.line_to(x + size, y)
    ctx.move_to(x, y - size)
    ctx.line_to(x, y + size)
    ctx.stroke()

# Parameters
cols, rows = 6, 5
points = get_voronoi_points(cols, rows, 40)
bounding_box = [(0, 0), (width, 0), (width, height), (0, height)]

# Generate Voronoi Cells
cells = []
for i, p1 in enumerate(points):
    cell = bounding_box
    for j, p2 in enumerate(points):
        if i == j: continue
        # Midpoint
        mx, my = (p1[0] + p2[0]) / 2, (p1[1] + p2[1]) / 2
        # Normal vector p1 -> p2
        nx, ny = p2[0] - p1[0], p2[1] - p1[1]
        # Line equation: nx*x + ny*y - (nx*mx + ny*my) <= 0
        # This keeps the side containing p1
        c = -(nx * mx + ny * my)
        cell = clip_polygon(cell, nx, ny, c)
    if cell:
        cells.append((p1, cell))

# Render Layers
# Layer 1: Cellular Gradients and Textures
for i, (center, poly) in enumerate(cells):
    if not poly: continue
    
    # Create a gradient based on position
    grad = cairo.LinearGradient(poly[0][0], poly[0][1], center[0], center[1])
    intensity = (center[0] / width) * 0.4
    grad.add_color_stop_rgba(0, 1, 1, 1, 0.0)
    grad.add_color_stop_rgba(1, 1, 1, 1, 0.1 + intensity)
    
    ctx.set_source(grad)
    ctx.move_to(poly[0][0], poly[0][1])
    for p in poly[1:]:
        ctx.line_to(p[0], p[1])
    ctx.fill()

    # Internal Systematic Pattern (Hatching)
    # The density of lines creates an "earned grey"
    ctx.save()
    ctx.set_line_width(0.3)
    ctx.set_source_rgba(1, 1, 1, 0.15)
    
    # Clip to cell
    ctx.move_to(poly[0][0], poly[0][1])
    for p in poly[1:]:
        ctx.line_to(p[0], p[1])
    ctx.clip()
    
    # Draw horizontal hatching based on Y coordinate logic
    step = 3 + (i % 5)
    for h in range(0, height, step):
        ctx.move_to(0, h)
        ctx.line_to(width, h)
    ctx.stroke()
    ctx.restore()

# Layer 2: Geometric Outlines and Connections
for center, poly in cells:
    if not poly: continue
    
    # Draw cell borders
    ctx.set_source_rgba(1, 1, 1, 0.8)
    ctx.set_line_width(1.2)
    ctx.move_to(poly[0][0], poly[0][1])
    for p in poly[1:]:
        ctx.line_to(p[0], p[1])
    ctx.close_path()
    ctx.stroke()
    
    # Draw centroid anchors
    ctx.set_source_rgb(1, 1, 1)
    ctx.arc(center[0], center[1], 1.5, 0, 2 * math.pi)
    ctx.fill()
    
    # Add small aesthetic "data" marks
    if random.random() > 0.6:
        ctx.set_source_rgba(0.9, 0.1, 0.1, 0.8) # Accent Swiss Red
        draw_technical_marks(ctx, center[0] + 10, center[1] - 10, 4)

# Layer 3: Global Network Overlay
# Draw very faint lines between points that are close to each other
ctx.set_line_width(0.4)
ctx.set_source_rgba(1, 1, 1, 0.2)
for i, p1 in enumerate(points):
    for j, p2 in enumerate(points):
        if i >= j: continue
        dist = math.sqrt((p1[0]-p2[0])**2 + (p1[1]-p2[1])**2)
        if dist < 120:
            ctx.move_to(p1[0], p1[1])
            ctx.line_to(p2[0], p2[1])
            ctx.stroke()

# Final Hierarchy: Outer Frame
ctx.set_source_rgb(1, 1, 1)
ctx.set_line_width(10)
ctx.rectangle(0, 0, width, height)
ctx.stroke()

# Small typography-like detail (Swiss grid markers)
ctx.set_source_rgb(1, 1, 1)
for x in range(0, width + 1, 100):
    ctx.set_line_width(1)
    ctx.move_to(x, 0)
    ctx.line_to(x, 15)
    ctx.stroke()
