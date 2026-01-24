import cairo
import math
import random

# Setup
width, height = 600, 480
surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
ctx = cairo.Context(surface)

# Background: Deep ink blue for a technical "blueprint" feel
ctx.set_source_rgb(0.02, 0.03, 0.08)
ctx.paint()

# --- Mathematical Utilities ---

# Simple Deterministic Noise-like function (pseudo-perlin)
# Based on a grid of random vectors and bilinear interpolation
random.seed(42)
grid_size = 40
cols, rows = (width // grid_size) + 1, (height // grid_size) + 1
vectors = [[(random.uniform(-1, 1), random.uniform(-1, 1)) for _ in range(rows)] for _ in range(cols)]

def get_vector(x, y):
    # Scale coordinates to grid
    gx = x / grid_size
    gy = y / grid_size
    ix, iy = int(gx), int(gy)
    fx, fy = gx - ix, gy - iy
    
    # Bilinear interpolation of vectors
    v1 = vectors[ix % cols][iy % rows]
    v2 = vectors[(ix + 1) % cols][iy % rows]
    v3 = vectors[ix % cols][(iy + 1) % rows]
    v4 = vectors[(ix + 1) % cols][(iy + 1) % rows]
    
    # Smoothstep interpolation
    sx = fx * fx * (3 - 2 * fx)
    sy = fy * fy * (3 - 2 * fy)
    
    vx = v1[0]*(1-sx)*(1-sy) + v2[0]*sx*(1-sy) + v3[0]*(1-sx)*sy + v4[0]*sx*sy
    vy = v1[1]*(1-sx)*(1-sy) + v2[1]*sx*(1-sy) + v3[1]*(1-sx)*sy + v4[1]*sx*sy
    return vx, vy

# --- Layer 1: The Systematic Grid ---
ctx.set_line_width(0.5)
for x in range(0, width, grid_size):
    for y in range(0, height, grid_size):
        # Draw tiny technical crosshairs
        ctx.set_source_rgba(0.2, 0.4, 0.6, 0.3)
        size = 2
        ctx.move_to(x - size, y); ctx.line_to(x + size, y)
        ctx.move_to(x, y - size); ctx.line_to(x, y + size)
        ctx.stroke()
        
        # Subtle coordinate text simulation
        if random.random() > 0.9:
            ctx.set_source_rgba(0.5, 0.7, 1.0, 0.4)
            ctx.rectangle(x + 2, y + 2, 8, 1.5)
            ctx.fill()

# --- Layer 2: Emergent Entropy (Flow Field Trails) ---
def draw_trail(start_x, start_y, steps, color):
    ctx.set_source_rgba(*color)
    x, y = start_x, start_y
    ctx.move_to(x, y)
    
    for i in range(steps):
        vx, vy = get_vector(x, y)
        # Add a global horizontal bias (Swiss precision progression)
        dx = vx * 10 + 2.5 
        dy = vy * 10
        
        x += dx
        y += dy
        
        # Modulate line width based on progression
        ctx.set_line_width(0.3 + (i / steps) * 1.2)
        ctx.line_to(x, y)
        
        # Occasionally draw a node point
        if i % 15 == 0 and random.random() > 0.7:
            ctx.stroke()
            ctx.arc(x, y, 1.5, 0, 2 * math.pi)
            ctx.fill()
            ctx.move_to(x, y)
            
    ctx.stroke()

# Draw multiple batches of particles
for _ in range(80):
    start_x = random.uniform(-50, width * 0.4)
    start_y = random.uniform(0, height)
    # Spectral gradient logic: vary from cyan to deep magenta
    alpha = random.uniform(0.1, 0.6)
    r = 0.2 + (start_y / height) * 0.5
    g = 0.6 - (start_x / width) * 0.3
    b = 0.9
    draw_trail(start_x, start_y, 40, (r, g, b, alpha))

# --- Layer 3: Euclidean Overlays (The "Anchors") ---
# Create data-informed nodes where the flow "converges"
for _ in range(12):
    nx = random.randint(2, cols-3) * grid_size
    ny = random.randint(2, rows-3) * grid_size
    
    # Outer ring
    ctx.set_source_rgba(1, 1, 1, 0.15)
    ctx.set_line_width(1)
    ctx.arc(nx, ny, 25, 0, 2 * math.pi)
    ctx.stroke()
    
    # Inner technical dial
    ctx.set_source_rgba(0.0, 0.8, 1.0, 0.8)
    ctx.set_line_width(2)
    angle = random.uniform(0, math.pi)
    ctx.arc(nx, ny, 5, angle, angle + math.pi/2)
    ctx.stroke()
    
    # Connecting geometric lines
    ctx.set_source_rgba(1, 1, 1, 0.05)
    ctx.set_line_width(0.5)
    ctx.move_to(nx, 0)
    ctx.line_to(nx, height)
    ctx.stroke()

# --- Layer 4: Final Atmospheric Polish ---
# A subtle gradient overlay to provide depth
gradient = cairo.LinearGradient(0, 0, width, height)
gradient.add_color_stop_rgba(0, 1, 1, 1, 0.05)
gradient.add_color_stop_rgba(0.5, 0, 0, 0, 0)
gradient.add_color_stop_rgba(1, 0, 0.5, 1, 0.05)
ctx.set_source(gradient)
ctx.paint()

# Marginalia / Typographic Elements
ctx.set_source_rgb(1, 1, 1)
ctx.select_font_face("sans-serif", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
ctx.set_font_size(8)
ctx.move_to(20, height - 20)
ctx.show_text("SYSTEMATIC_FLUIDITY_V.01 // GRID_REF: 40px")
ctx.rectangle(20, height - 15, 150, 1)
ctx.fill()

