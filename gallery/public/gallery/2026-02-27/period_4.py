import cairo
import math
import random

# Setup
width, height = 600, 480
surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
ctx = cairo.Context(surface)

# Background - Deep charcoal for high contrast
ctx.set_source_rgb(0.02, 0.02, 0.03)
ctx.paint()

def get_spectral_color(t):
    """Returns a thermal/spectral color based on a 0.0-1.0 input."""
    # Transitions: Blue -> Cyan -> Green -> Yellow -> Red
    if t < 0.25:
        return (0, t * 4, 1)
    elif t < 0.5:
        return (0, 1, 1 - (t - 0.25) * 4)
    elif t < 0.75:
        return ((t - 0.5) * 4, 1, 0)
    else:
        return (1, 1 - (t - 0.75) * 4, 0)

def clip_poly(poly, p1, p2):
    """Sutherland-Hodgman clipping of a polygon against a line bisector."""
    new_poly = []
    # Bisector line normal (points towards p1)
    nx = p1[0] - p2[0]
    ny = p1[1] - p2[1]
    # Midpoint
    mx = (p1[0] + p2[0]) / 2
    my = (p1[1] + p2[1]) / 2
    
    def is_inside(p):
        return (p[0] - mx) * nx + (p[1] - my) * ny > 0

    for i in range(len(poly)):
        curr = poly[i]
        prev = poly[(i - 1) % len(poly)]
        
        # Intersection calculation
        dx, dy = curr[0] - prev[0], curr[1] - prev[1]
        denom = (dx * nx + dy * ny)
        if abs(denom) > 0.0001:
            t = ((mx - prev[0]) * nx + (my - prev[1]) * ny) / denom
            intersect = (prev[0] + t * dx, prev[1] + t * dy)
            
            if is_inside(curr):
                if not is_inside(prev):
                    new_poly.append(intersect)
                new_poly.append(curr)
            elif is_inside(prev):
                new_poly.append(intersect)
    return new_poly

# 1. Generate Points: Systematic jittered grid
points = []
cols, rows = 8, 6
spacing_x = width / cols
spacing_y = height / rows
for r in range(rows + 1):
    for c in range(cols + 1):
        # Swiss precision with controlled displacement
        off_x = (random.random() - 0.5) * spacing_x * 0.8
        off_y = (random.random() - 0.5) * spacing_y * 0.8
        points.append((c * spacing_x + off_x, r * spacing_y + off_y))

# 2. Draw Systematic Grid Layer (Background detail)
ctx.set_source_rgba(1, 1, 1, 0.05)
ctx.set_line_width(0.5)
for i in range(0, width, 20):
    ctx.move_to(i, 0); ctx.line_to(i, height); ctx.stroke()
for i in range(0, height, 20):
    ctx.move_to(0, i); ctx.line_to(width, i); ctx.stroke()

# 3. Construct and draw Voronoi Cells
for i, p in enumerate(points):
    # Initial bounding box for the cell
    cell = [(0,0), (width, 0), (width, height), (0, height)]
    
    # Clip against every other point's bisector
    for j, other_p in enumerate(points):
        if i == j: continue
        # Optimization: only clip against reasonably close points
        dist_sq = (p[0]-other_p[0])**2 + (p[1]-other_p[1])**2
        if dist_sq < 250**2:
            cell = clip_poly(cell, p, other_p)
    
    if len(cell) < 3: continue

    # Geometric logic: Drawing the cell
    ctx.move_to(cell[0][0], cell[0][1])
    for pt in cell[1:]:
        ctx.line_to(pt[0], pt[1])
    ctx.close_path()
    
    # Spectral Gradient: Distance-based logic
    dist_norm = math.sqrt(p[0]**2 + p[1]**2) / math.sqrt(width**2 + height**2)
    r, g, b = get_spectral_color(dist_norm)
    
    # Radial gradient from seed point to create "glow"
    grad = cairo.RadialGradient(p[0], p[1], 2, p[0], p[1], 120)
    grad.add_color_stop_rgba(0, r, g, b, 0.6)
    grad.add_color_stop_rgba(0.7, r, g, b, 0.1)
    grad.add_color_stop_rgba(1, r, g, b, 0)
    
    ctx.set_source(grad)
    ctx.fill_preserve()
    
    # Precise white borders (Swiss aesthetic)
    ctx.set_source_rgba(1, 1, 1, 0.2)
    ctx.set_line_width(0.7)
    ctx.stroke()
    
    # Center markers (crosshairs)
    ctx.set_source_rgba(1, 1, 1, 0.4)
    size = 3
    ctx.move_to(p[0]-size, p[1]); ctx.line_to(p[0]+size, p[1])
    ctx.move_to(p[0], p[1]-size); ctx.line_to(p[0], p[1]+size)
    ctx.stroke()

# 4. Global Interference: Flow-driven overlay
ctx.set_line_width(0.3)
for i in range(15):
    y_pos = height * (i / 15)
    ctx.set_source_rgba(1, 1, 1, 0.1)
    ctx.move_to(0, y_pos)
    for x in range(0, width + 10, 10):
        # Interferometric logic: Sine wave modulated by x-pos
        wave = math.sin(x * 0.01 + i) * 15
        ctx.line_to(x, y_pos + wave)
    ctx.stroke()

# 5. Typographic/Data Elements
ctx.select_font_face("Monospace", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
ctx.set_font_size(10)
ctx.set_source_rgb(0.8, 0.8, 0.8)
ctx.move_to(20, height - 20)
ctx.show_text("SPECTRAL_SYSTEM_V.01 // GRID_REF_204")
ctx.move_to(width - 160, height - 20)
ctx.show_text("COORD_MAPPING: ISO-71")

# Finish
