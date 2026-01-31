import cairo
import math
import random

# Setup
width, height = 600, 600
surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
ctx = cairo.Context(surface)

# Background - Deep "Blueprint" Charcoal
ctx.set_source_rgb(0.02, 0.03, 0.05)
ctx.paint()

def to_cartesian(cx, cy, r, theta):
    return cx + r * math.cos(theta), cy + r * math.sin(theta)

def draw_glyph(ctx, x, y, size, type=0):
    """Draws clinical, Swiss-style geometric markers."""
    ctx.save()
    ctx.translate(x, y)
    if type == 0: # Crosshair
        ctx.move_to(-size, 0)
        ctx.line_to(size, 0)
        ctx.move_to(0, -size)
        ctx.line_to(0, size)
    elif type == 1: # Tiny Square
        ctx.rectangle(-size/2, -size/2, size, size)
    elif type == 2: # L-bracket
        ctx.move_to(size, 0)
        ctx.line_to(0, 0)
        ctx.line_to(0, size)
    ctx.stroke()
    ctx.restore()

# 1. ATMOSPHERIC LAYER: Spectral Washes
# Multiple overlapping radial gradients to simulate "interference patterns"
for _ in range(3):
    cx, cy = width * random.random(), height * random.random()
    grad = cairo.RadialGradient(cx, cy, 50, cx, cy, 400)
    # Spectral palette: Cyan, Deep Indigo, and a hint of Magenta
    grad.add_color_stop_rgba(0, 0.1, 0.4, 0.8, 0.15)
    grad.add_color_stop_rgba(0.5, 0.2, 0.1, 0.5, 0.05)
    grad.add_color_stop_rgba(1, 0, 0, 0, 0)
    ctx.set_source(grad)
    ctx.paint()

# 2. SYSTEMATIC GRID: Polar Transformation
cx, cy = width / 2, height / 2
rings = 14
spokes = 36
distortion_freq = 5
distortion_amp = 15

# Draw Radial Spokes with varying density
ctx.set_line_width(0.5)
for i in range(spokes):
    angle = (i / spokes) * 2 * math.pi
    
    # Introduce a "spectral" color variation based on angle
    intensity = 0.3 + 0.4 * math.sin(angle * 3)
    ctx.set_source_rgba(0.6, 0.8, 1.0, intensity)
    
    # Each spoke is made of segments to allow for radial distortion
    ctx.move_to(cx, cy)
    for r in range(0, 320, 10):
        # Radial distortion function
        offset = math.sin(r * 0.05 + angle * distortion_freq) * distortion_amp
        px, py = to_cartesian(cx, cy, r + offset, angle)
        ctx.line_to(px, py)
    ctx.stroke()

# 3. CLINICAL PRECISION: Concentric "Blueprint" Rings
for j in range(1, rings + 1):
    r_base = j * 22
    ctx.set_line_width(0.7 if j % 5 == 0 else 0.3)
    
    # Draw ring with periodic "gaps" and "dashes"
    ctx.new_path()
    for i in range(361):
        angle = math.radians(i)
        # Apply the same distortion to keep the grid coherent
        r_distorted = r_base + math.sin(r_base * 0.05 + angle * distortion_freq) * distortion_amp
        px, py = to_cartesian(cx, cy, r_distorted, angle)
        
        if i == 0:
            ctx.move_to(px, py)
        else:
            # Create rhythmic breaks in the lines
            if (i // 10) % 3 != 0:
                ctx.line_to(px, py)
            else:
                ctx.move_to(px, py)
    
    ctx.set_source_rgba(0.8, 0.9, 1.0, 0.6)
    ctx.stroke()

# 4. DATA NODES: Recursive Scaling & Primitives
# Placing "glyphs" at intersections where the mathematical logic dictates
random.seed(42) # Deterministic randomness for precision feel
for j in range(3, rings, 2):
    r_base = j * 22
    for i in range(0, 360, 20):
        angle = math.radians(i)
        
        # Calculate distorted coordinate
        r_distorted = r_base + math.sin(r_base * 0.05 + angle * distortion_freq) * distortion_amp
        px, py = to_cartesian(cx, cy, r_distorted, angle)
        
        # Draw technical markers
        ctx.set_line_width(0.5)
        ctx.set_source_rgba(1, 1, 1, 0.8)
        
        # Scale markers based on distance from center
        glyph_size = 1.5 + (j * 0.3)
        
        if random.random() > 0.4:
            draw_glyph(ctx, px, py, glyph_size, type=random.randint(0, 2))
            
        # Add tiny "labels" or connector lines for extra complexity
        if random.random() > 0.9:
            ctx.set_source_rgba(0.2, 0.8, 1.0, 0.9)
            ctx.arc(px, py, glyph_size * 1.5, 0, 2 * math.pi)
            ctx.stroke()
            
            # Secondary vector "outlier"
            ctx.move_to(px, py)
            ox, oy = to_cartesian(cx, cy, r_distorted + 30, angle + 0.1)
            ctx.line_to(ox, oy)
            ctx.stroke()

# 5. PERIPHERAL EXPANSION: Hatching & Texture
# Adds a "technical document" texture to the corners
ctx.set_source_rgba(0.5, 0.7, 1.0, 0.2)
ctx.set_line_width(0.2)
step = 8
for x in range(0, width, step):
    if x < 100 or x > width - 100:
        ctx.move_to(x, 0)
        ctx.line_to(x, height)
        ctx.stroke()
for y in range(0, height, step):
    if y < 100 or y > height - 100:
        ctx.move_to(0, y)
        ctx.line_to(width, y)
        ctx.stroke()

# Final focal glow
grad = cairo.RadialGradient(cx, cy, 10, cx, cy, 150)
grad.add_color_stop_rgba(0, 1, 1, 1, 0.1)
grad.add_color_stop_rgba(1, 1, 1, 1, 0)
ctx.set_source(grad)
ctx.arc(cx, cy, 150, 0, 2 * math.pi)
ctx.fill()
