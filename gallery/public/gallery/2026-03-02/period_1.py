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

def get_bisector(p1, p2):
    """Returns a line (point, normal) representing the perpendicular bisector of p1 and p2."""
    mid = ((p1[0] + p2[0]) / 2, (p1[1] + p2[1]) / 2)
    dx = p2[0] - p1[0]
    dy = p2[1] - p1[1]
    # Normal points from p1 towards p2
    return mid, (dx, dy)

def clip_poly(poly, bisector_pt, bisector_norm):
    """Clips a convex polygon against a half-plane defined by a point and a normal."""
    new_poly = []
    if not poly: return []
    
    for i in range(len(poly)):
        p1 = poly[i]
        p2 = poly[(i + 1) % len(poly)]
        
        # Dot product determines which side of the line the point is on
        def dist(p):
            return (p[0] - bisector_pt[0]) * bisector_norm[0] + (p[1] - bisector_pt[1]) * bisector_norm[1]
        
        d1 = dist(p1)
        d2 = dist(p2)
        
        if d1 <= 0: # Inside (closer to seed)
            if d2 <= 0:
                new_poly.append(p2)
            else: # Exiting
                t = d1 / (d1 - d2)
                new_poly.append((p1[0] + t * (p2[0] - p1[0]), p1[1] + t * (p2[1] - p1[1])))
        else: # Outside
            if d2 <= 0: # Entering
                t = d1 / (d1 - d2)
                new_poly.append((p1[0] + t * (p2[0] - p1[0]), p1[1] + t * (p2[1] - p1[1])))
                new_poly.append(p2)
    return new_poly

# 1. Generate Seeds using a perturbed recursive grid (Swiss logic)
seeds = []
cols, rows = 6, 5
for i in range(cols):
    for j in range(rows):
        # Jittered grid placement
        x = (i + 0.5 + random.uniform(-0.3, 0.3)) * (width / cols)
        y = (j + 0.5 + random.uniform(-0.3, 0.3)) * (height / rows)
        seeds.append((x, y))

# 2. Draw Subtle Background Grid
ctx.set_source_rgba(1, 1, 1, 0.05)
ctx.set_line_width(0.5)
for i in range(0, width, 40):
    ctx.move_to(i, 0); ctx.line_to(i, height)
for j in range(0, height, 40):
    ctx.move_to(0, j); ctx.line_to(width, j)
ctx.stroke()

# 3. Compute and Draw Voronoi Cells
for i, s1 in enumerate(seeds):
    # Start with canvas as the initial polygon
    cell_poly = [(0, 0), (width, 0), (width, height), (0, height)]
    
    for j, s2 in enumerate(seeds):
        if i == j: continue
        b_pt, b_norm = get_bisector(s1, s2)
        cell_poly = clip_poly(cell_poly, b_pt, b_norm)
    
    if not cell_poly: continue

    # Draw the Cell
    ctx.move_to(cell_poly[0][0], cell_poly[0][1])
    for p in cell_poly[1:]:
        ctx.line_to(p[0], p[1])
    ctx.close_path()
    
    # Gradient based on seed position - Swiss bi-tonal palette
    grad = cairo.LinearGradient(s1[0], s1[1], cell_poly[0][0], cell_poly[0][1])
    v = random.uniform(0.1, 0.4)
    grad.add_color_stop_rgba(0, v, v, v + 0.1, 0.8)
    grad.add_color_stop_rgba(1, 0, 0, 0, 0)
    
    ctx.set_source(grad)
    ctx.fill_preserve()
    
    # Cell border
    ctx.set_source_rgba(1, 1, 1, 0.3)
    ctx.set_line_width(0.8)
    ctx.stroke()

    # 4. Granular Density Layer (Dithering/Noise)
    # Add tiny technical marks inside cells
    ctx.set_source_rgba(1, 1, 1, 0.15)
    area_approx = len(cell_poly) * 100 # Simple heuristic
    for _ in range(int(area_approx / 10)):
        rx = random.uniform(min(p[0] for p in cell_poly), max(p[0] for p in cell_poly))
        ry = random.uniform(min(p[1] for p in cell_poly), max(p[1] for p in cell_poly))
        # Point-in-polygon check (simplified) would go here; using small rectangles for texture
        ctx.rectangle(rx, ry, 1, 1)
    ctx.fill()

# 5. Connective Tissue (Delaunay-ish thin lines)
ctx.set_line_width(0.2)
ctx.set_source_rgba(0.8, 0.9, 1.0, 0.2)
for i, s1 in enumerate(seeds):
    for j, s2 in enumerate(seeds):
        dist = math.sqrt((s1[0]-s2[0])**2 + (s1[1]-s2[1])**2)
        if dist < 150: # Only connect nearby seeds
            ctx.move_to(s1[0], s1[1])
            ctx.line_to(s2[0], s2[1])
ctx.stroke()

# 6. Technical Overlay / Annotations
ctx.set_source_rgb(1, 1, 1)
for s in seeds:
    # Small crosshair at seed
    size = 3
    ctx.set_line_width(0.5)
    ctx.move_to(s[0] - size, s[1]); ctx.line_to(s[0] + size, s[1])
    ctx.move_to(s[0], s[1] - size); ctx.line_to(s[0], s[1] + size)
    ctx.stroke()
    
    # Pseudo-coordinates (tiny bits of digital erosion)
    if random.random() > 0.7:
        ctx.select_font_face("Monospace", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)
        ctx.set_font_size(6)
        ctx.move_to(s[0] + 5, s[1] - 5)
        ctx.show_text(f"{s[0]:.0f}:{s[1]:.0f}")

# Final polish: Global noise/grain
for _ in range(2000):
    ctx.set_source_rgba(1, 1, 1, random.uniform(0, 0.05))
    ctx.rectangle(random.uniform(0, width), random.uniform(0, height), 1, 1)
    ctx.fill()

# Final output is handled by the environment
