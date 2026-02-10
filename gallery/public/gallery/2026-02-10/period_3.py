import cairo
import math
import random

# Setup
width, height = 600, 480
surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
ctx = cairo.Context(surface)

# Palette: Swiss-inspired High Contrast
COLOR_BG = (0.04, 0.04, 0.04)      # Deep neutral foundation
COLOR_ACCENT = (1.0, 0.27, 0.0)    # High-saturation Orange-Red
COLOR_IVORY = (1.0, 1.0, 0.94)     # Ivory highlight
COLOR_DARK = (0.15, 0.15, 0.15)    # Structural grey

# Background
ctx.set_source_rgb(*COLOR_BG)
ctx.paint()

def get_bisector(p1, p2):
    """Returns a line (point, normal) representing the perpendicular bisector."""
    mid = ((p1[0] + p2[0]) / 2, (p1[1] + p2[1]) / 2)
    dx = p2[0] - p1[0]
    dy = p2[1] - p1[1]
    # Normal is (dx, dy)
    return mid, (dx, dy)

def clip_polygon(poly, line_pt, line_norm):
    """Clips a polygon against a half-plane defined by a line point and normal."""
    new_poly = []
    if not poly: return []
    
    def is_inside(p):
        # Dot product of (p - line_pt) and line_norm
        return (p[0] - line_pt[0]) * line_norm[0] + (p[1] - line_pt[1]) * line_norm[1] < 0

    for i in range(len(poly)):
        p1 = poly[i]
        p2 = poly[(i + 1) % len(poly)]
        
        in1, in2 = is_inside(p1), is_inside(p2)
        
        if in1 and in2:
            new_poly.append(p2)
        elif in1 and not in2:
            # Intersection
            new_poly.append(intersect(p1, p2, line_pt, line_norm))
        elif not in1 and in2:
            # Intersection then p2
            new_poly.append(intersect(p1, p2, line_pt, line_norm))
            new_poly.append(p2)
            
    return new_poly

def intersect(p1, p2, lp, ln):
    """Line-line intersection helper."""
    dx, dy = p2[0] - p1[0], p2[1] - p1[1]
    # Parameter t where p1 + t*d is on the line
    # dot((p1 + t*d - lp), ln) = 0
    num = (lp[0] - p1[0]) * ln[0] + (lp[1] - p1[1]) * ln[1]
    den = dx * ln[0] + dy * ln[1]
    t = num / den if den != 0 else 0
    return (p1[0] + t * dx, p1[1] + t * dy)

def draw_voronoi_system(seeds, area_rect, depth=0):
    """Computes and renders Voronoi cells with gradients and Swiss aesthetics."""
    x, y, w, h = area_rect
    
    for i, p1 in enumerate(seeds):
        # Initial cell is the bounding box
        cell = [(x, y), (x+w, y), (x+w, y+h), (x, y+h)]
        
        for j, p2 in enumerate(seeds):
            if i == j: continue
            lp, ln = get_bisector(p1, p2)
            cell = clip_polygon(cell, lp, ln)
        
        if not cell: continue

        # Draw Cell Fill (Gradient)
        dist_to_center = math.sqrt((p1[0]-width/2)**2 + (p1[1]-height/2)**2)
        is_accent = random.random() < 0.1 or (depth > 0 and random.random() < 0.3)
        
        grad = cairo.RadialGradient(p1[0], p1[1], 2, p1[0], p1[1], 120)
        if is_accent:
            grad.add_color_stop_rgba(0, *COLOR_ACCENT, 0.8)
            grad.add_color_stop_rgba(1, *COLOR_ACCENT, 0.0)
        else:
            grad.add_color_stop_rgba(0, *COLOR_IVORY, 0.15)
            grad.add_color_stop_rgba(1, *COLOR_IVORY, 0.0)
            
        ctx.set_source(grad)
        ctx.move_to(cell[0][0], cell[0][1])
        for pt in cell[1:]: ctx.line_to(pt[0], pt[1])
        ctx.fill()

        # Draw Cell Borders (Modulated rhythmic dashes)
        ctx.set_line_width(0.5 if not is_accent else 1.2)
        if is_accent:
            ctx.set_source_rgba(*COLOR_ACCENT, 0.6)
            ctx.set_dash([]) # Solid
        else:
            ctx.set_source_rgba(*COLOR_IVORY, 0.3)
            ctx.set_dash([random.uniform(1, 5), random.uniform(2, 8)])
            
        ctx.move_to(cell[0][0], cell[0][1])
        for pt in cell[1:]: ctx.line_to(pt[0], pt[1])
        ctx.close_path()
        ctx.stroke()
        
        # Recursive Subdivision logic: occasional clusters
        if depth < 1 and random.random() < 0.15:
            # Create sub-seeds within this cell's bounding box roughly
            sub_seeds = []
            for _ in range(5):
                sub_seeds.append((p1[0] + random.uniform(-40, 40), 
                                  p1[1] + random.uniform(-40, 40)))
            draw_voronoi_system(sub_seeds, (x, y, w, h), depth + 1)

# Generate sophisticated seed distribution
# Mix of a jittered grid and some random clusters
seeds = []
grid_size = 80
for r in range(0, width + grid_size, grid_size):
    for c in range(0, height + grid_size, grid_size):
        if random.random() > 0.2: # Create some "voids"
            sx = r + random.uniform(-grid_size/2, grid_size/2)
            sy = c + random.uniform(-grid_size/2, grid_size/2)
            seeds.append((sx, sy))

# Primary Render
draw_voronoi_system(seeds, (0, 0, width, height))

# Final Swiss Touch: Technical Overlay
ctx.set_dash([])
ctx.set_source_rgba(*COLOR_IVORY, 0.1)
ctx.set_line_width(0.3)

# Fine horizontal lines (Grid hierarchy)
for i in range(0, height, 40):
    ctx.move_to(0, i)
    ctx.line_to(width, i)
ctx.stroke()

# Micro-Typography simulation (small bits of info)
for seed in random.sample(seeds, min(len(seeds), 12)):
    ctx.select_font_face("Monospace", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
    ctx.set_font_size(6)
    ctx.set_source_rgba(*COLOR_IVORY, 0.5)
    ctx.move_to(seed[0] + 5, seed[1] - 5)
    ctx.show_text(f"NODE_{hex(int(seed[0]+seed[1]))[2:].upper()}")

# Structural crosshair
ctx.set_source_rgba(*COLOR_ACCENT, 0.4)
ctx.set_line_width(1)
margin = 40
ctx.move_to(margin, margin)
ctx.line_to(margin + 20, margin)
ctx.move_to(margin, margin)
ctx.line_to(margin, margin + 20)
ctx.stroke()

ctx.move_to(width - margin, height - margin)
ctx.line_to(width - margin - 20, height - margin)
ctx.move_to(width - margin, height - margin)
ctx.line_to(width - margin, height - margin - 20)
ctx.stroke()
