import cairo
import math
import random

# Setup
width, height = 600, 480
surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
ctx = cairo.Context(surface)

# Background - Deep Charcoal
ctx.set_source_rgb(0.05, 0.05, 0.05)
ctx.paint()

# Configuration for the Polar Swiss Grid
center_x, center_y = width / 2, height / 2
max_radius = min(width, height) * 0.45
rings = 18
divisions = 48
accent_color = (0.9, 0.1, 0.1)  # Swiss Red
base_color = (0.95, 0.95, 0.95) # Off-white

def get_distorted_coords(r_idx, t_idx):
    """
    Applies radial distortion to the grid points.
    The distortion uses a harmonic function to create a rhythmic 'pulse'.
    """
    angle = (t_idx / divisions) * (2 * math.pi)
    
    # Calculate base radius
    r_norm = r_idx / rings
    radius = r_norm * max_radius
    
    # Mathematical distortion: Sine-based displacement
    # This creates a 'wobble' that increases with radius
    distortion = math.sin(angle * 6) * (r_norm * 15)
    distortion += math.cos(r_norm * 10) * 10
    
    final_r = radius + distortion
    
    x = center_x + final_r * math.cos(angle)
    y = center_y + final_r * math.sin(angle)
    return x, y

# --- Layer 1: The Underlying Geometric Structure ---
ctx.set_line_width(0.4)
ctx.set_source_rgba(base_color[0], base_color[1], base_color[2], 0.2)

for r in range(1, rings + 1):
    for t in range(divisions):
        p1 = get_distorted_coords(r, t)
        p2 = get_distorted_coords(r, (t + 1) % divisions)
        p3 = get_distorted_coords(r - 1, t)
        
        ctx.move_to(*p1)
        ctx.line_to(*p2)
        ctx.stroke()
        
        ctx.move_to(*p1)
        ctx.line_to(*p3)
        ctx.stroke()

# --- Layer 2: Modular Blocks (Swiss Grid Logic) ---
# We treat the polar grid as a series of 'cells' [r, t]
random.seed(42) # Deterministic for composition precision

for r in range(2, rings):
    for t in range(divisions):
        # Probability-based generation of modules
        chance = random.random()
        
        # Draw solid modules (Hierarchy)
        if chance > 0.85:
            ctx.set_source_rgba(base_color[0], base_color[1], base_color[2], 0.8)
            if random.random() > 0.9:
                ctx.set_source_rgba(accent_color[0], accent_color[1], accent_color[2], 0.9)
            
            p1 = get_distorted_coords(r, t)
            p2 = get_distorted_coords(r, t + 1)
            p3 = get_distorted_coords(r + 1, t + 1)
            p4 = get_distorted_coords(r + 1, t)
            
            ctx.move_to(*p1)
            ctx.line_to(*p2)
            ctx.line_to(*p3)
            ctx.line_to(*p4)
            ctx.close_path()
            ctx.fill()

# --- Layer 3: Dynamic Line Weights (Visual Rhythm) ---
for r in [4, 8, 12, 16]: # Selected 'hero' rings
    ctx.set_line_width(1.5)
    ctx.set_source_rgba(base_color[0], base_color[1], base_color[2], 0.6)
    
    for t in range(divisions):
        if t % 4 == 0: # Create a rhythmic broken line
            p1 = get_distorted_coords(r, t)
            p2 = get_distorted_coords(r, t + 2)
            
            # Using arcs for smooth distorted connections
            # But calculating mid-points for precision
            ctx.move_to(*p1)
            mid_t = t + 1
            pmid = get_distorted_coords(r, mid_t)
            ctx.curve_to(p1[0], p1[1], pmid[0], pmid[1], p2[0], p2[1])
            ctx.stroke()

# --- Layer 4: Radial Accents (Brutalist Lines) ---
ctx.set_line_width(3.0)
ctx.set_source_rgb(*accent_color)
for t in range(0, divisions, 12): # Every 90 degrees approx
    start_r = random.randint(2, 6)
    end_r = start_r + random.randint(5, 10)
    
    p_start = get_distorted_coords(start_r, t)
    p_end = get_distorted_coords(end_r, t)
    
    ctx.move_to(*p_start)
    ctx.line_to(*p_end)
    ctx.stroke()

# --- Layer 5: Fine Typographic-like Detail ---
# Adding small 'markers' at the intersections
ctx.set_source_rgb(1, 1, 1)
for r in range(rings):
    for t in range(0, divisions, 2):
        if random.random() > 0.7:
            x, y = get_distorted_coords(r, t)
            size = 1.2
            ctx.rectangle(x - size/2, y - size/2, size, size)
            ctx.fill()

# Final Border - Swiss Style
ctx.set_line_width(20)
ctx.set_source_rgb(0.05, 0.05, 0.05)
ctx.move_to(0, 0)
ctx.line_to(width, 0)
ctx.line_to(width, height)
ctx.line_to(0, height)
ctx.close_path()
ctx.set_line_width(40)
ctx.stroke()

