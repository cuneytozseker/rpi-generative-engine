import cairo
import math
import random

# Setup
width, height = 600, 480
surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
ctx = cairo.Context(surface)

# Background - Deep "Ink Blue" black for a technical blueprint feel
ctx.set_source_rgb(0.02, 0.02, 0.05)
ctx.paint()

def get_noise(x, y):
    """Simple harmonic noise to simulate flow fields for reaction-diffusion aesthetics."""
    v1 = math.sin(x * 0.02 + y * 0.01)
    v2 = math.cos(y * 0.015 - x * 0.005)
    v3 = math.sin(math.sqrt(x*x + y*y) * 0.01)
    return (v1 + v2 + v3) / 3.0

# 1. THE SYSTEMATIC GRID (Swiss Design layer)
ctx.set_line_width(0.5)
grid_size = 40
for i in range(0, width + 1, grid_size):
    # Vertical grid
    ctx.set_source_rgba(1, 1, 1, 0.1)
    ctx.move_to(i, 0)
    ctx.line_to(i, height)
    ctx.stroke()
    
    # Technical markers
    if i % (grid_size * 2) == 0:
        ctx.set_source_rgba(1, 1, 1, 0.4)
        ctx.select_font_face("monospace", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)
        ctx.set_font_size(8)
        ctx.move_to(i + 2, 10)
        ctx.show_text(f"LN_{i:03d}")

for j in range(0, height + 1, grid_size):
    # Horizontal grid
    ctx.set_source_rgba(1, 1, 1, 0.1)
    ctx.move_to(0, j)
    ctx.line_to(width, j)
    ctx.stroke()

# 2. THE REACTION-DIFFUSION APPROXIMATION (The Organic layer)
# We use agent-based paths that follow a field but avoid "over-crowding" 
# to mimic the inhibitory nature of RD systems.
ctx.set_line_cap(cairo.LINE_CAP_ROUND)

seeds = 180
for _ in range(seeds):
    x = random.uniform(0, width)
    y = random.uniform(0, height)
    
    # Each "worm" represents a reaction strand
    ctx.set_source_rgba(1, 1, 1, random.uniform(0.6, 0.9))
    ctx.set_line_width(random.uniform(1.5, 4.0))
    
    ctx.move_to(x, y)
    
    steps = random.randint(10, 40)
    for _ in range(steps):
        angle = get_noise(x, y) * math.pi * 4
        dist = 5
        
        # Calculate next step
        nx = x + math.cos(angle) * dist
        ny = y + math.sin(angle) * dist
        
        # Draw step
        ctx.line_to(nx, ny)
        
        # Update current
        x, y = nx, ny
        
    ctx.stroke()

# 3. INTERFACE ELEMENTS (The "Blueprint" aesthetic)
# Crosshairs and structural nodes
for _ in range(12):
    nx = random.randint(0, width // grid_size) * grid_size
    ny = random.randint(0, height // grid_size) * grid_size
    
    # Node circles
    ctx.set_source_rgb(1, 1, 1)
    ctx.arc(nx, ny, 2, 0, 2 * math.pi)
    ctx.fill()
    
    # Connecting thin vector lines
    ctx.set_line_width(0.3)
    ctx.set_source_rgba(1, 1, 1, 0.5)
    ctx.move_to(nx, ny)
    ctx.line_to(nx + 40, ny - 40)
    ctx.line_to(nx + 100, ny - 40)
    ctx.stroke()
    
    # Annotations
    ctx.set_font_size(7)
    ctx.move_to(nx + 45, ny - 45)
    ctx.show_text(f"REF_{random.randint(1000, 9999)}")

# 4. SPECTRAL GRADIENT HIGHLIGHTS
# Simulating the "internal glow" mentioned in the brief
gradient = cairo.LinearGradient(0, 0, width, height)
gradient.add_color_stop_rgba(0.0, 1.0, 1.0, 1.0, 0.0)
gradient.add_color_stop_rgba(0.5, 0.2, 0.5, 1.0, 0.15) # Subtle blue/violet glow
gradient.add_color_stop_rgba(1.0, 1.0, 1.0, 1.0, 0.0)

ctx.set_source(gradient)
ctx.rectangle(0, 0, width, height)
ctx.fill()

# 5. FINAL CONTRAST OVERLAY
# Stark white geometric primitives placed with Swiss precision
ctx.set_source_rgb(1, 1, 1)
ctx.set_line_width(2)
# Bottom margin technical block
ctx.rectangle(20, height - 40, 120, 20)
ctx.stroke()
ctx.set_font_size(10)
ctx.move_to(25, height - 26)
ctx.show_text("SYSTEMATIC_FLUIDITY // v.01")

# Small repeated glyphs
for k in range(5):
    ctx.rectangle(width - 100 + (k * 15), height - 30, 8, 8)
    if k % 2 == 0:
        ctx.fill()
    else:
        ctx.stroke()

# Clean up / Final line for crispness
ctx.set_source_rgba(1, 1, 1, 0.05)
ctx.set_line_width(1)
ctx.move_to(0, height * 0.7)
ctx.line_to(width, height * 0.7)
ctx.stroke()

