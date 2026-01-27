import cairo
import math
import random

# Setup
width, height = 600, 480
surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
ctx = cairo.Context(surface)

# Swiss-inspired Palette
COLOR_BG = (0.96, 0.96, 0.96)      # Off-white
COLOR_COBALT = (0.0, 0.28, 0.67)   # Deep Cobalt
COLOR_ACCENT = (1.0, 0.27, 0.0)    # Spectral Orange/Red
COLOR_DARK = (0.05, 0.05, 0.05)    # Near Black

# Background
ctx.set_source_rgb(*COLOR_BG)
ctx.paint()

def get_distance(p1, p2):
    return math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)

def generate_points(n, w, h):
    """Generates points with a density bias towards the center (Dissipation)."""
    points = []
    for _ in range(n):
        # Biasing towards center using Gaussian-like distribution
        x = w/2 + (random.uniform(-1, 1) * random.random()) * (w/2.2)
        y = h/2 + (random.uniform(-1, 1) * random.random()) * (h/2.2)
        points.append((x, y))
    return points

def get_voronoi_cell(point, points, bounds):
    """Calculates a Voronoi cell by clipping a bounding box with bisectors."""
    x0, y0, x1, y1 = bounds
    # Start with a large rectangle as the initial polygon
    cell_poly = [(x0, y0), (x1, y0), (x1, y1), (x0, y1)]
    
    px, py = point
    
    for other in points:
        if other == point:
            continue
        
        ox, oy = other
        # Perpendicular bisector between (px, py) and (ox, oy)
        # Midpoint
        mx, my = (px + ox) / 2, (py + oy) / 2
        # Normal vector
        nx, ny = ox - px, oy - py
        
        new_poly = []
        for i in range(len(cell_poly)):
            p1 = cell_poly[i]
            p2 = cell_poly[(i + 1) % len(cell_poly)]
            
            # Check if points are on the 'inside' of the bisector half-plane
            # dot((pt - m), n) < 0 means it's on the side of the original point
            d1 = (p1[0] - mx) * nx + (p1[1] - my) * ny
            d2 = (p2[0] - mx) * nx + (p2[1] - my) * ny
            
            if d1 <= 0:
                new_poly.append(p1)
            
            if (d1 <= 0 and d2 > 0) or (d1 > 0 and d2 <= 0):
                # Intersection point
                t = d1 / (d1 - d2)
                ix = p1[0] + t * (p2[0] - p1[0])
                iy = p1[1] + t * (p2[1] - p1[1])
                new_poly.append((ix, iy))
        cell_poly = new_poly
        if not cell_poly: break
    return cell_poly

# Parameters
num_points = 54
bounds = (20, 20, width - 20, height - 20)
points = generate_points(num_points, width, height)

# Render logic
for i, p in enumerate(points):
    cell = get_voronoi_cell(p, points, bounds)
    if not cell: continue

    # Calculate density for color modulation
    dist_to_nearest = min([get_distance(p, other) for other in points if other != p])
    density_factor = max(0, min(1, 1.0 - (dist_to_nearest / 80.0)))
    
    # Draw logic: Modular precision vs atmospheric dissipation
    ctx.set_line_join(cairo.LINE_JOIN_MITER)
    
    # 1. Base Cell Fill (Subtle transparency)
    ctx.move_to(cell[0][0], cell[0][1])
    for pt in cell[1:]:
        ctx.line_to(pt[0], pt[1])
    ctx.close_path()
    
    # Spectral bloom logic
    if density_factor > 0.6:
        ctx.set_source_rgba(COLOR_ACCENT[0], COLOR_ACCENT[1], COLOR_ACCENT[2], 0.1 * density_factor)
        ctx.fill_preserve()
    
    ctx.set_source_rgba(COLOR_COBALT[0], COLOR_COBALT[1], COLOR_COBALT[2], 0.05)
    ctx.fill()

    # 2. Recursive Subdivisions (Concentric outlines)
    # This creates the "modular" feel and simulates depth
    num_layers = int(4 + 12 * (1 - density_factor))
    for layer in range(num_layers):
        scale = 1.0 - (layer / num_layers)
        ctx.save()
        ctx.translate(p[0], p[1])
        ctx.scale(scale, scale)
        ctx.translate(-p[0], -p[1])
        
        ctx.move_to(cell[0][0], cell[0][1])
        for pt in cell[1:]:
            ctx.line_to(pt[0], pt[1])
        ctx.close_path()
        
        # Line weight dissipates with distance from center
        weight = 0.2 + (0.8 * density_factor)
        ctx.set_line_width(weight / scale) # Adjust for scale
        
        # Color transitions: High density gets Cobalt/Accent, Low gets light gray
        if density_factor > 0.7 and layer % 2 == 0:
            ctx.set_source_rgba(*COLOR_ACCENT, 0.8)
        else:
            alpha = 0.1 + (0.7 * density_factor)
            ctx.set_source_rgba(COLOR_COBALT[0], COLOR_COBALT[1], COLOR_COBALT[2], alpha)
            
        ctx.stroke()
        ctx.restore()

    # 3. Micro-Typography / Grid Labels
    if random.random() > 0.85:
        ctx.select_font_face("Monospace", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
        ctx.set_font_size(6)
        ctx.set_source_rgb(*COLOR_DARK)
        ctx.move_to(p[0] + 4, p[1] - 4)
        ctx.show_text(f"{p[0]:.0f}.{p[1]:.0f}")

# 4. Global "Modular" Overlays
# Fine grid lines for Swiss precision
ctx.set_line_width(0.3)
ctx.set_source_rgba(0, 0, 0, 0.1)
grid_spacing = 40
for x in range(0, width, grid_spacing):
    ctx.move_to(x, 0)
    ctx.line_to(x, height)
    ctx.stroke()
for y in range(0, height, grid_spacing):
    ctx.move_to(0, y)
    ctx.line_to(width, y)
    ctx.stroke()

# 5. Atmospheric Texture: Moire Dots
# Sparse dither pattern in negative spaces
for _ in range(1200):
    tx = random.uniform(0, width)
    ty = random.uniform(0, height)
    # Only draw dots in low density areas
    is_dense = any(get_distance((tx, ty), p) < 40 for p in points)
    if not is_dense:
        ctx.arc(tx, ty, 0.6, 0, 2 * math.pi)
        ctx.set_source_rgba(*COLOR_COBALT, 0.4)
        ctx.fill()

# Final Border for Swiss structure
ctx.set_line_width(12)
ctx.set_source_rgb(*COLOR_BG)
ctx.rectangle(0, 0, width, height)
ctx.stroke()
ctx.set_line_width(1)
ctx.set_source_rgb(*COLOR_DARK)
ctx.rectangle(10, 10, width-20, height-20)
ctx.stroke()
