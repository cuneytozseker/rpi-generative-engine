import cairo
import math
import random

# Setup
width, height = 600, 480
surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
ctx = cairo.Context(surface)

# Background: Deep technical void
ctx.set_source_rgb(0.02, 0.02, 0.05)
ctx.paint()

def draw_truchet_tile(x, y, size, rotation, weight, color, alpha):
    """Draws a multi-layered concentric Truchet tile."""
    r, g, b = color
    ctx.set_source_rgba(r, g, b, alpha)
    ctx.set_line_width(weight)
    
    ctx.save()
    ctx.translate(x + size/2, y + size/2)
    ctx.rotate(rotation * (math.pi / 2))
    ctx.translate(-size/2, -size/2)
    
    # Draw multiple concentric arcs for "Technical Fluidity"
    # This creates the sense of "Dynamic Vector Fields"
    steps = 4
    for i in range(1, steps + 1):
        radius = (size / steps) * i * 0.5
        # Variation in dash patterns for "Hard-Edge Precision" vs "Atmospheric Diffusion"
        if i % 2 == 0:
            ctx.set_dash([size * 0.1, size * 0.05])
        else:
            ctx.set_dash([])
            
        # Top-left arc
        ctx.arc(0, 0, radius, 0, math.pi / 2)
        ctx.stroke()
        
        # Bottom-right arc
        ctx.arc(size, size, radius, math.pi, 1.5 * math.pi)
        ctx.stroke()
        
        # Terminal Nodes: tiny dots at the end of some paths
        if i == steps:
            ctx.set_dash([])
            ctx.arc(0, radius, 1.5, 0, 2 * math.pi)
            ctx.arc(radius, 0, 1.5, 0, 2 * math.pi)
            ctx.fill()
            
    ctx.restore()

# 1. LAYER ONE: "Atmospheric Diffusion"
# Large, faint, blurry-esque paths to create a sense of depth
ctx.set_operator(cairo.OPERATOR_SCREEN)
grid_size_bg = 120
for i in range(width // grid_size_bg + 1):
    for j in range(height // grid_size_bg + 1):
        x = i * grid_size_bg
        y = j * grid_size_bg
        rot = random.choice([0, 1, 2, 3])
        # Saturated Monochromatic Base (Cyan/Indigo)
        draw_truchet_tile(x, y, grid_size_bg, rot, 4.0, (0.1, 0.3, 0.6), 0.15)

# 2. LAYER TWO: "Rhythmic Serialism"
# The core grid, modulated by a mathematical progression
ctx.set_operator(cairo.OPERATOR_ADD)
grid_size = 40
cols = width // grid_size
rows = height // grid_size

for i in range(cols):
    for j in range(rows):
        x = i * grid_size
        y = j * grid_size
        
        # Logic for rotation based on a "Vector Field" simulation
        # Using sine/cosine to create wave-like flow instead of pure randomness
        angle_factor = math.sin(i * 0.2) + math.cos(j * 0.3)
        rot = int(abs(angle_factor * 2)) % 4
        
        # Chromatic Pulsing: color shifts slightly across the canvas
        r = 0.2 + 0.1 * math.sin(i * 0.5)
        g = 0.5 + 0.4 * math.sin(j * 0.3)
        b = 0.8 + 0.2 * math.cos(i * 0.1)
        
        # Vary weight based on distance from center (Asymmetric Progression)
        dist_from_center = math.sqrt((i - cols/2)**2 + (j - rows/2)**2)
        weight = 0.5 + (1.5 * (1 - (dist_from_center / (cols/2))))
        
        draw_truchet_tile(x, y, grid_size, rot, max(0.2, weight), (r, g, b), 0.6)

# 3. LAYER THREE: "Technical Annotations"
# Swiss-style grid markers and coordinate-based points
ctx.set_operator(cairo.OPERATOR_OVER)
ctx.set_source_rgba(1, 1, 1, 0.4)
ctx.set_line_width(0.5)

# Vertical rulers
for x in range(0, width, 100):
    ctx.move_to(x, 0)
    ctx.line_to(x, 15)
    ctx.stroke()
    # Mock technical text/labels
    ctx.rectangle(x + 2, 5, 12, 2)
    ctx.fill()

# Lateral flow lines: "Ghosted" repetitions
for _ in range(12):
    y_pos = random.randint(0, height)
    ctx.set_source_rgba(0.9, 0.9, 1.0, 0.1)
    ctx.move_to(0, y_pos)
    ctx.line_to(width, y_pos)
    ctx.stroke()

# 4. FINAL ACCENTS: "Luminous Terminal Nodes"
# High contrast points to anchor the composition
for _ in range(25):
    ctx.set_source_rgba(1.0, 0.9, 0.4, 0.8) # Warm accent highlight
    px = random.randrange(0, width, grid_size)
    py = random.randrange(0, height, grid_size)
    ctx.arc(px, py, 1.2, 0, 2 * math.pi)
    ctx.fill()
    
    # Small crosshair for diagrammatic look
    ctx.set_line_width(0.3)
    ctx.move_to(px - 5, py)
    ctx.line_to(px + 5, py)
    ctx.move_to(px, py - 5)
    ctx.line_to(px, py + 5)
    ctx.stroke()

# Final border to emphasize Swiss containment
ctx.set_source_rgba(1, 1, 1, 0.1)
ctx.set_line_width(20)
ctx.rectangle(0, 0, width, height)
ctx.stroke()
