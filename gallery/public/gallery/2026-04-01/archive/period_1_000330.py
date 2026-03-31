import cairo
import math
import random

# Setup
width, height = 600, 600 # Square format works best for polar transformations
surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
ctx = cairo.Context(surface)

# Background: Deep Void
ctx.set_source_rgb(0.02, 0.02, 0.03) 
ctx.paint()

def draw_dither_pattern(ctx, x, y, w, h, density):
    """Creates a high-frequency binary noise effect (dithering)."""
    ctx.save()
    ctx.set_source_rgba(1, 1, 1, 0.7)
    for _ in range(int(w * h * density)):
        px = x + random.random() * w
        py = y + random.random() * h
        ctx.rectangle(px, py, 0.8, 0.8)
        ctx.fill()
    ctx.restore()

def polar_to_cartesian(cx, cy, r, theta):
    return cx + r * math.cos(theta), cy + r * math.sin(theta)

# Parameters
cx, cy = width / 2, height / 2
num_rings = 45
num_sectors = 36
max_radius = min(width, height) * 0.45
accent_color = (0.0, 0.8, 1.0) # Cyan spectral accent

# --- LOGARITHMIC RADIAL SYSTEM ---
for i in range(num_rings):
    # Logarithmic progression for spacing (Swiss precision)
    # Tighter at the center, expanding outwards (acceleration)
    t = i / num_rings
    r = math.pow(t, 1.4) * max_radius
    r_next = math.pow((i + 1) / num_rings, 1.4) * max_radius
    
    # Varying line weight based on distance (Atmospheric depth)
    line_weight = 0.2 + (1.0 - t) * 1.5
    ctx.set_line_width(line_weight)
    
    # Randomly skip rings to create "tectonic" gaps
    if random.random() < 0.15:
        continue

    for j in range(num_sectors):
        angle_start = (j / num_sectors) * 2 * math.pi
        angle_end = ((j + 1) / num_sectors) * 2 * math.pi
        
        # Radial distortion: add a jitter that increases with radius
        distortion = (math.sin(t * 10) * 0.05) * (1 - t)
        angle_start += distortion
        angle_end += distortion

        # DRAW SECTOR EDGES
        ctx.set_source_rgba(0.9, 0.9, 0.9, 0.4 + (t * 0.4))
        
        # Draw arcs
        ctx.arc(cx, cy, r, angle_start, angle_end)
        ctx.stroke()
        
        # DRAW RECURSIVE SUBDIVISIONS (Data Clusters)
        if random.random() < 0.08:
            # Create a "highlighted" cell
            ctx.set_source_rgba(*accent_color, 0.6)
            ctx.set_line_width(2.0)
            ctx.arc(cx, cy, r, angle_start, angle_end)
            ctx.stroke()
            
            # Add high-frequency noise inside the segment
            # Approximate cell bounds for dithering
            mid_angle = (angle_start + angle_end) / 2
            dx, dy = polar_to_cartesian(cx, cy, r, mid_angle)
            draw_dither_pattern(ctx, dx-2, dy-2, 4, 4, 0.5)

# --- STRETCHED DISTANCE FIELDS (Radial Rays) ---
ctx.set_line_width(0.3)
for j in range(num_sectors * 2):
    angle = (j / (num_sectors * 2)) * 2 * math.pi
    
    # Mathematical rhythm: Length varies by sine wave
    length_mod = 0.5 + 0.5 * math.sin(angle * 4)
    start_r = 20 + (10 * math.cos(angle * 8))
    end_r = max_radius * (0.8 + 0.4 * length_mod)
    
    x1, y1 = polar_to_cartesian(cx, cy, start_r, angle)
    x2, y2 = polar_to_cartesian(cx, cy, end_r, angle)
    
    # Gradient-like stroke
    ctx.set_source_rgba(1, 1, 1, 0.1)
    ctx.move_to(x1, y1)
    ctx.line_to(x2, y2)
    ctx.stroke()

# --- NON-UNIFORM ORTHOGONAL OVERLAY (The Grid Contrast) ---
# A faint, rigid Cartesian grid to contrast the fluid polar motion
ctx.set_line_width(0.5)
grid_step = 40
for x in range(0, width, grid_step):
    alpha = 0.05 if (x // grid_step) % 4 != 0 else 0.15
    ctx.set_source_rgba(1, 1, 1, alpha)
    ctx.move_to(x, 0)
    ctx.line_to(x, height)
    ctx.stroke()

for y in range(0, height, grid_step):
    alpha = 0.05 if (y // grid_step) % 4 != 0 else 0.15
    ctx.set_source_rgba(1, 1, 1, alpha)
    ctx.move_to(0, y)
    ctx.line_to(width, y)
    ctx.stroke()

# --- FINISHING ELEMENT: SYSTEM IDENTIFIER ---
# Mimicking Swiss typography layout with geometric primitives
ctx.set_source_rgb(1, 1, 1)
ctx.rectangle(40, height - 60, 20, 2) # Thick bar
ctx.fill()
ctx.set_line_width(0.5)
for i in range(5):
    ctx.move_to(40, height - 50 + (i * 4))
    ctx.line_to(80, height - 50 + (i * 4))
    ctx.stroke()

# Final focal accent (Volumetric Glow)
radial_grad = cairo.RadialGradient(cx, cy, 10, cx, cy, max_radius)
radial_grad.add_color_stop_rgba(0, 1, 1, 1, 0.05)
radial_grad.add_color_stop_rgba(0.5, 0, 0.8, 1, 0.02)
radial_grad.add_color_stop_rgba(1, 0, 0, 0, 0)
ctx.set_source(radial_grad)
ctx.rectangle(0, 0, width, height)
ctx.fill()
