import cairo
import math
import random

# Setup
width, height = 600, 480
surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
ctx = cairo.Context(surface)

# Background - Swiss Neutral (Parchment White)
ctx.set_source_rgb(0.96, 0.96, 0.95)
ctx.paint()

def get_voronoi_points(cols, rows, jitter_strength):
    points = []
    dx = width / (cols + 1)
    dy = height / (rows + 1)
    for i in range(1, cols + 1):
        for j in range(1, rows + 1):
            # Entropy increases towards the bottom right
            entropy = (i / cols + j / rows) / 2 * jitter_strength
            px = i * dx + random.uniform(-entropy, entropy)
            py = j * dy + random.uniform(-entropy, entropy)
            points.append((px, py))
    return points

def clip_polygon(poly, a, b, c):
    """Clips a polygon against a line ax + by + c <= 0."""
    def inside(p):
        return a * p[0] + b * p[1] + c <= 0

    def intersect(p1, p2):
        # Line p1-p2: x = p1.x + t(p2.x - p1.x)
        # Find t where a(p1.x + t(dx)) + b(p1.y + t(dy)) + c = 0
        dx, dy = p2[0] - p1[0], p2[1] - p1[1]
        denom = a * dx + b * dy
        if denom == 0: return p1
        t = -(a * p1[0] + b * p1[1] + c) / denom
        return (p1[0] + t * dx, p1[1] + t * dy)

    new_poly = []
    if not poly: return []
    for i in range(len(poly)):
        p1 = poly[i - 1]
        p2 = poly[i]
        if inside(p2):
            if not inside(p1):
                new_poly.append(intersect(p1, p2))
            new_poly.append(p2)
        elif inside(p1):
            new_poly.append(intersect(p1, p2))
    return new_poly

# Parameters
cols, rows = 8, 6
points = get_voronoi_points(cols, rows, 45)
accent_color = (0.9, 0.1, 0.05) # Swiss Red

# Draw Voronoi Cells
for i, p in enumerate(points):
    # Start with canvas bounds
    cell = [(0, 0), (width, 0), (width, height), (0, height)]
    
    # Clip against all other points
    for j, p_other in enumerate(points):
        if i == j: continue
        # Perpendicular bisector between p and p_other
        # Midpoint M
        mx, my = (p[0] + p_other[0]) / 2, (p[1] + p_other[1]) / 2
        # Normal vector n = p_other - p
        nx, ny = p_other[0] - p[0], p_other[1] - p[1]
        # Line equation: nx(x - mx) + ny(y - my) <= 0
        # nx*x + ny*y - (nx*mx + ny*my) <= 0
        c = -(nx * mx + ny * my)
        cell = clip_polygon(cell, nx, ny, c)

    if len(cell) > 2:
        # Style: Entropy-based Color
        dist_factor = (p[0] + p[1]) / (width + height)
        
        # Fill with a subtle gradient
        lg = cairo.LinearGradient(p[0], p[1], cell[0][0], cell[0][1])
        if random.random() > 0.85:
            # Random high-frequency accent
            lg.add_color_stop_rgba(0, *accent_color, 0.8)
            lg.add_color_stop_rgba(1, *accent_color, 0.2)
        else:
            shade = 0.2 + (dist_factor * 0.4)
            lg.add_color_stop_rgba(0, shade, shade, shade, 0.15)
            lg.add_color_stop_rgba(1, shade, shade, shade, 0.02)
        
        ctx.set_source(lg)
        ctx.move_to(cell[0][0], cell[0][1])
        for cp in cell[1:]:
            ctx.line_to(cp[0], cp[1])
        ctx.close_path()
        ctx.fill_preserve()
        
        # Stroke - Precise mechanical lines
        ctx.set_source_rgba(0, 0, 0, 0.7)
        ctx.set_line_width(0.4)
        ctx.stroke()

        # Internal "Rigidity" markers: A small cross at each site
        ctx.set_source_rgb(0, 0, 0)
        size = 2
        ctx.move_to(p[0]-size, p[1]); ctx.line_to(p[0]+size, p[1])
        ctx.move_to(p[0], p[1]-size); ctx.line_to(p[0], p[1]+size)
        ctx.set_line_width(0.5)
        ctx.stroke()

# Background Texture - Halftone dots (Technical Dithering)
ctx.set_source_rgba(0, 0, 0, 0.05)
dot_spacing = 10
for x in range(0, width, dot_spacing):
    for y in range(0, height, dot_spacing):
        ctx.arc(x, y, 0.5, 0, 2 * math.pi)
        ctx.fill()

# Geometric Hierarchy - Overlaid "Technical" Grid
ctx.set_line_width(0.2)
ctx.set_source_rgba(0, 0, 0, 0.3)
for i in range(4):
    lx = (i+1) * (width/5)
    ctx.move_to(lx, 20); ctx.line_to(lx, height-20)
    ctx.stroke()

# Final accent: Entropy balance frame
ctx.set_line_width(2)
ctx.set_source_rgb(0, 0, 0)
ctx.rectangle(20, 20, width-40, height-40)
ctx.stroke()

# Typography-like element (Structural label)
ctx.select_font_face("Sans", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
ctx.set_font_size(10)
ctx.move_to(30, 40)
ctx.show_text("SYSTEM-04 // ENTROPIC VORONOI")
ctx.move_to(30, 52)
ctx.set_font_size(7)
ctx.show_text("COORDINATES: " + str(hex(id(points)))[-8:])
