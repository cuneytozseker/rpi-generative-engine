import cairo
import math
import random

# Setup
width, height = 600, 480
surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
ctx = cairo.Context(surface)

# Background - Deep Brutalist Black
ctx.set_source_rgb(0.02, 0.02, 0.03)
ctx.paint()

def get_voronoi_cell(seeds, index, width, height):
    """
    Computes a Voronoi cell as a list of points (convex polygon).
    Uses the intersection of half-planes defined by perpendicular bisectors.
    """
    p1 = seeds[index]
    # Start with a large bounding box
    cell = [
        (0, 0), (width, 0), (width, height), (0, height)
    ]
    
    for i, p2 in enumerate(seeds):
        if i == index:
            continue
        
        # Midpoint between p1 and p2
        mid_x = (p1[0] + p2[0]) / 2.0
        mid_y = (p1[1] + p2[1]) / 2.0
        
        # Normal vector from p1 to p2
        nx = p2[0] - p1[0]
        ny = p2[1] - p1[1]
        
        new_cell = []
        for j in range(len(cell)):
            a = cell[j]
            b = cell[(j + 1) % len(cell)]
            
            # Distance from point to bisector line: (x - mid_x) * nx + (y - mid_y) * ny = 0
            dist_a = (a[0] - mid_x) * nx + (a[1] - mid_y) * ny
            dist_b = (b[0] - mid_x) * nx + (b[1] - mid_y) * ny
            
            if dist_a <= 0:
                new_cell.append(a)
            
            if (dist_a <= 0 and dist_b > 0) or (dist_a > 0 and dist_b <= 0):
                # Intersection point
                t = dist_a / (dist_a - dist_b)
                ix = a[0] + t * (b[0] - a[0])
                iy = a[1] + t * (b[1] - a[1])
                new_cell.append((ix, iy))
        cell = new_cell
    return cell

# 1. Generate Seeds with "Centripetal Balance" 
# Using a logarithmic spiral / Fibonacci distribution for structured propagation
seeds = []
center_x, center_y = width / 2, height / 2
num_points = 64

for i in range(num_points):
    # Logarithmic spacing: denser at center
    angle = i * 0.5  # Golden angle approx or systematic increment
    radius = 40 * math.sqrt(i) * (1 + 0.1 * math.sin(i))
    
    x = center_x + math.cos(angle) * radius
    y = center_y + math.sin(angle) * radius
    
    # Add some jitter for organic variation within the system
    x += random.uniform(-10, 10)
    y += random.uniform(-10, 10)
    
    # Constrain to visible area
    if 0 <= x <= width and 0 <= y <= height:
        seeds.append((x, y))

# Add boundary corners to ensure edge coverage
seeds.extend([(0,0), (width,0), (0,height), (width,height)])

# 2. Draw Voronoi Cells with Gradients and Spectral Accents
for i in range(len(seeds)):
    cell = get_voronoi_cell(seeds, i, width, height)
    if not cell:
        continue
        
    # Draw Cell Shape
    ctx.move_to(cell[0][0], cell[0][1])
    for p in cell[1:]:
        ctx.line_to(p[0], p[1])
    ctx.close_path()
    
    # Calculate distance from center for hierarchical coloring
    sx, sy = seeds[i]
    dist_to_center = math.sqrt((sx - center_x)**2 + (sy - center_y)**2)
    norm_dist = min(dist_to_center / (width/2), 1.0)
    
    # Gradient Logic: Dark to subtly saturated
    # High-chroma signals near the center or at specific intervals
    grad = cairo.RadialGradient(sx, sy, 2, sx, sy, 150)
    
    if i % 7 == 0: # Spectral Signal Cells
        # Cyber-punk inspired high-chroma accents
        r, g, b = (0.9, 0.1, 0.4) if i % 2 == 0 else (0.1, 0.8, 0.9)
        grad.add_color_stop_rgba(0, r, g, b, 0.4)
        grad.add_color_stop_rgba(1, 0, 0, 0, 0)
    else: # Monochromatic Base
        shade = 0.1 + (1.0 - norm_dist) * 0.15
        grad.add_color_stop_rgba(0, shade, shade, shade + 0.05, 0.8)
        grad.add_color_stop_rgba(1, 0.02, 0.02, 0.05, 1.0)
        
    ctx.set_source(grad)
    ctx.fill_preserve()
    
    # Precision Outlines
    ctx.set_line_width(0.5)
    ctx.set_source_rgba(1, 1, 1, 0.15 - (norm_dist * 0.1))
    ctx.stroke()

# 3. Add Systematic Textures: Variable Interval Grid Overlay
ctx.set_line_width(0.3)
ctx.set_source_rgba(1, 1, 1, 0.05)
for i in range(0, width, 20):
    # Vertical lines with harmonic fading
    ctx.move_to(i, 0)
    ctx.line_to(i, height)
    ctx.stroke()

# 4. Data Markers: Density-driven "Signals"
for i, (sx, sy) in enumerate(seeds):
    if i % 3 == 0:
        # Small technical markers at seed locations
        size = 2 if i % 9 != 0 else 4
        ctx.set_source_rgba(1, 1, 1, 0.4)
        ctx.rectangle(sx - size/2, sy - size/2, size, size)
        ctx.fill()
        
        # Connecting "Logic" lines for centripetal feel
        if i < len(seeds) - 1:
            ctx.set_source_rgba(0.1, 0.8, 0.9, 0.2)
            ctx.set_line_width(0.2)
            ctx.move_to(sx, sy)
            ctx.line_to(center_x, center_y)
            ctx.stroke()

# 5. Swiss Design Border / Hierarchy
ctx.set_source_rgb(0, 0, 0)
ctx.set_line_width(15)
ctx.rectangle(0, 0, width, height)
ctx.stroke()

# Decorative corner crosshairs
def draw_crosshair(x, y):
    ctx.set_source_rgb(0.8, 0.8, 0.8)
    ctx.set_line_width(0.5)
    size = 10
    ctx.move_to(x - size, y); ctx.line_to(x + size, y)
    ctx.move_to(x, y - size); ctx.line_to(x, y + size)
    ctx.stroke()

draw_crosshair(30, 30)
draw_crosshair(width-30, height-30)

# Final contrast pass: Light Vignette
vignette = cairo.RadialGradient(center_x, center_y, 100, center_x, center_y, 400)
vignette.add_color_stop_rgba(0, 1, 1, 1, 0)
vignette.add_color_stop_rgba(1, 0, 0, 0, 0.3)
ctx.set_source(vignette)
ctx.paint()
