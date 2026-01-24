import cairo
import math
import random

# Setup
width, height = 600, 480
surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
ctx = cairo.Context(surface)

# Background - Deep Brutalist Black
ctx.set_source_rgb(0.02, 0.02, 0.02)
ctx.paint()

# --- HELPER FUNCTIONS ---

def get_noise_vector(x, y, scale=0.005, octaves=3):
    """Generates a flow angle using multi-octave trigonometric summation."""
    angle = 0
    freq = scale
    amp = 1.0
    for i in range(octaves):
        # A combination of sin/cos to simulate a pseudo-random flow field
        angle += math.sin(y * freq + i) * amp
        angle += math.cos(x * freq - i) * amp
        freq *= 2.1
        amp *= 0.5
    return angle

def draw_particle_trail(ctx, start_x, start_y, steps, step_size, line_width, alpha):
    """Draws an organic trail based on the vector field."""
    ctx.set_line_width(line_width)
    ctx.set_source_rgba(1, 1, 1, alpha)
    
    x, y = start_x, start_y
    ctx.move_to(x, y)
    
    for _ in range(steps):
        angle = get_noise_vector(x, y)
        x += math.cos(angle) * step_size
        y += math.sin(angle) * step_size
        
        # Keep particles within a reasonable bound
        if 0 <= x <= width and 0 <= y <= height:
            ctx.line_to(x, y)
        else:
            break
            
    ctx.stroke()

def draw_swiss_grid(ctx, spacing, weight, alpha):
    """Draws a subtle background coordinate system."""
    ctx.set_line_width(weight)
    ctx.set_source_rgba(0.4, 0.4, 0.4, alpha)
    
    # Vertical lines
    for x in range(0, width + 1, spacing):
        ctx.move_to(x, 0)
        ctx.line_to(x, height)
    
    # Horizontal lines
    for y in range(0, height + 1, spacing):
        ctx.move_to(0, y)
        ctx.line_to(width, y)
    ctx.stroke()

# --- GENERATIVE COMPOSITION ---

# 1. Background Grid (Systematic Foundation)
draw_swiss_grid(ctx, 40, 0.5, 0.15)
draw_swiss_grid(ctx, 120, 1.0, 0.2)

# 2. Recursive Subdivision for Density Variation
# We define regions where the particle density is higher to create visual hierarchy
regions = [
    (0, 0, width, height, 800, 0.05),        # Base layer: low density, very faint
    (50, 50, 200, 380, 400, 0.1),           # High density vertical band
    (300, 100, 250, 250, 500, 0.12),        # High density square block
    (100, 300, 400, 100, 300, 0.08)         # Lower horizontal weight
]

for (rx, ry, rw, rh, count, base_alpha) in regions:
    for _ in range(count):
        # Randomized start within the region
        px = rx + random.random() * rw
        py = ry + random.random() * rh
        
        # Varying trail properties
        steps = random.randint(20, 60)
        step_len = random.uniform(2, 5)
        l_width = random.uniform(0.1, 0.8)
        
        # Influence alpha by the center of the canvas to create a radial focus
        dist_to_center = math.sqrt((px - width/2)**2 + (py - height/2)**2)
        fade = max(0, 1 - (dist_to_center / (width/1.2)))
        
        draw_particle_trail(ctx, px, py, steps, step_len, l_width, base_alpha * fade)

# 3. Structural Elements (The "Swiss" Overlays)
# Accentuating the grid with heavier white strokes in specific intersections
ctx.set_source_rgba(1, 1, 1, 0.8)
ctx.set_line_width(1.5)
for i in range(3):
    lx = random.choice(range(0, width, 40))
    ly = random.choice(range(0, height, 40))
    ctx.move_to(lx - 10, ly)
    ctx.line_to(lx + 10, ly)
    ctx.move_to(lx, ly - 10)
    ctx.line_to(lx, ly + 10)
ctx.stroke()

# 4. Focal Point Details
# Adding small, dense clusters of points at the "nodes" of the flow
for _ in range(15):
    nx = random.uniform(0, width)
    ny = random.uniform(0, height)
    angle = get_noise_vector(nx, ny)
    
    # Draw a "Technical Marker"
    ctx.set_source_rgba(1, 1, 1, 0.5)
    ctx.set_line_width(0.5)
    ctx.arc(nx, ny, 2, 0, 2 * math.pi)
    ctx.stroke()
    
    # Small directional vector
    ctx.move_to(nx, ny)
    ctx.line_to(nx + math.cos(angle)*15, ny + math.sin(angle)*15)
    ctx.stroke()

# 5. Marginalia (Typography simulation)
ctx.set_source_rgba(1, 1, 1, 0.7)
ctx.select_font_face("sans-serif", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
ctx.set_font_size(10)

# Bottom-left metadata
ctx.move_to(20, height - 20)
ctx.show_text("REF: FS-2024 // SYSTEM_09")
ctx.move_to(20, height - 35)
ctx.set_font_size(8)
ctx.show_text("LATENT FLOW TOPOGRAPHY")

# Top-right coordinate marker
ctx.move_to(width - 80, 30)
ctx.show_text(f"X_{random.randint(100,999)} : Y_{random.randint(100,999)}")

# Final subtle vignette
gradient = cairo.RadialGradient(width/2, height/2, 100, width/2, height/2, 400)
gradient.add_color_stop_rgba(0, 0, 0, 0, 0)
gradient.add_color_stop_rgba(1, 0, 0, 0, 0.4)
ctx.set_source(gradient)
ctx.rectangle(0, 0, width, height)
ctx.fill()
