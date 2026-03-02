import cairo
import math
import random

# Setup
width, height = 600, 480
surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
ctx = cairo.Context(surface)

# Background - Deep Brutalist Charcoal
ctx.set_source_rgb(0.05, 0.05, 0.07)
ctx.paint()

# --- HELPER FUNCTIONS ---
def get_noise_angle(x, y, scale=0.005, octaves=3):
    """Generates a pseudo-Perlin flow angle using harmonic interference."""
    angle = 0
    for i in range(1, octaves + 1):
        freq = scale * i
        amp = 1.0 / i
        angle += (math.sin(x * freq + i) + math.cos(y * freq - i)) * amp
    return angle * math.pi

def draw_module(ctx, x, y, angle, size, color_tuple, weight):
    """Draws a modular Swiss-style primitive (a modulated cross/bar)."""
    r, g, b, a = color_tuple
    ctx.save()
    ctx.translate(x, y)
    ctx.rotate(angle)
    
    # Primary Stroke
    ctx.set_source_rgba(r, g, b, a)
    ctx.set_line_width(weight)
    ctx.move_to(-size, 0)
    ctx.line_to(size, 0)
    ctx.stroke()
    
    # Secondary Accent (Recursive modularity)
    if random.random() > 0.8:
        ctx.set_line_width(weight * 0.5)
        ctx.move_to(0, -size * 0.5)
        ctx.line_to(0, size * 0.5)
        ctx.stroke()
        
    ctx.restore()

# --- GENERATIVE CORE ---

# 1. Underlying Systematic Grid (Reference layer)
ctx.set_source_rgba(1, 1, 1, 0.03)
grid_size = 40
ctx.set_line_width(0.5)
for x in range(0, width, grid_size):
    ctx.move_to(x, 0)
    ctx.line_to(x, height)
    ctx.stroke()
for y in range(0, height, grid_size):
    ctx.move_to(0, y)
    ctx.line_to(width, y)
    ctx.stroke()

# 2. Flow Field Simulation
# We simulate particles that leave modular "decays" along their paths
num_particles = 120
steps = 60
particle_step_length = 8.0

for p in range(num_particles):
    # Start particles in a centralized dense cluster for "rhythmic expansion"
    px = width/2 + random.uniform(-50, 50)
    py = height/2 + random.uniform(-50, 50)
    
    # Spectral mapping based on starting distance from center
    dist_from_center = math.sqrt((px - width/2)**2 + (py - height/2)**2)
    hue_shift = dist_from_center / 100.0
    
    for s in range(steps):
        angle = get_noise_angle(px, py, scale=0.004)
        
        # Color Logic: Function of spatial position (Spectral Mapping)
        # Transitioning from Electric Cyan to Architectural Red
        r = 0.2 + (px / width) * 0.8
        g = 0.4 + (py / height) * 0.4
        b = 0.9 - (px / width) * 0.5
        alpha = 1.0 - (s / steps) # Fade out over time (Decay)
        
        # Line Weight Modulation
        weight = 0.5 + (math.sin(s * 0.2) + 1.0) * 1.2
        
        # Draw the module
        draw_module(ctx, px, py, angle, 4 + (s*0.1), (r, g, b, alpha * 0.6), weight)
        
        # Move particle
        px += math.cos(angle) * particle_step_length
        py += math.sin(angle) * particle_step_length
        
        # Boundary Wrap/Soft Kill
        if px < 0 or px > width or py < 0 or py > height:
            break

# 3. Geometric "Glitch" Overlays
# Adding high-contrast, hard-edged vector paths for "Surgical Precision"
for _ in range(12):
    ctx.set_source_rgba(1, 1, 1, 0.15)
    gx = random.randint(0, width)
    gy = random.randint(0, height)
    gw = random.randint(40, 150)
    gh = 1.5
    
    # Draw horizontal axis markers (Swiss design influence)
    ctx.rectangle(gx, gy, gw, gh)
    ctx.fill()
    
    # Add small numeric-style markers (Typography as visual element)
    if random.random() > 0.5:
        ctx.set_line_width(0.8)
        ctx.move_to(gx, gy - 5)
        ctx.line_to(gx, gy - 15)
        ctx.stroke()

# 4. Final Atmospheric Pass (Dithering/Grain effect)
for _ in range(2000):
    ctx.set_source_rgba(1, 1, 1, 0.05)
    rx = random.random() * width
    ry = random.random() * height
    ctx.rectangle(rx, ry, 1, 1)
    ctx.fill()

# Finish
