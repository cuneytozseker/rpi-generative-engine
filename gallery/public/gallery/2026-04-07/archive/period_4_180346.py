import cairo
import math
import random

# Setup
width, height = 600, 480
surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
ctx = cairo.Context(surface)

# Background - Deep ink black
ctx.set_source_rgb(0.02, 0.02, 0.03)
ctx.paint()

def get_resonance(x, y, attractors):
    """Calculates interference value based on distance to multiple harmonic nodes."""
    val = 0
    for ax, ay, freq, phase in attractors:
        dist = math.sqrt((x - ax)**2 + (y - ay)**2)
        # Non-linear wave propagation
        val += math.sin(dist * freq + phase)
    return val / len(attractors)

# Configuration for the "Structural Pulse"
cols, rows = 100, 80
cell_w = width / cols
cell_h = height / rows

# Create harmonic nodes (attractors) to simulate reaction-diffusion interference
nodes = [
    (width * 0.3, height * 0.4, 0.12, 0),
    (width * 0.7, height * 0.6, 0.08, math.pi/2),
    (width * 0.5, height * 0.5, 0.05, math.pi)
]

# LAYER 1: Diffused Glow (Atmospheric base)
ctx.set_operator(cairo.OPERATOR_ADD)
for i in range(cols):
    for j in range(rows):
        x = i * cell_w + cell_w/2
        y = j * cell_h + cell_h/2
        
        res = get_resonance(x, y, nodes)
        
        # Mapping resonance to a visual weight
        # Only draw in 'constructive' interference zones
        if res > 0.3:
            alpha = (res - 0.3) * 0.15
            ctx.set_source_rgba(0.2, 0.4, 0.8, alpha) # Subtle spectral blue
            ctx.arc(x, y, cell_w * 2, 0, 2 * math.pi)
            ctx.fill()

# LAYER 2: Structural Resonance Grid (Systematic repetition)
ctx.set_operator(cairo.OPERATOR_OVER)
ctx.set_line_width(0.5)

for i in range(cols):
    for j in range(rows):
        x = i * cell_w + cell_w/2
        y = j * cell_h + cell_h/2
        
        res = get_resonance(x, y, nodes)
        
        # Normalize resonance to 0-1 range for styling
        norm_res = (res + 1) / 2
        
        # Swiss design logic: spacing and size modulated by function
        if res > 0:
            # Color logic: Stark white with occasional spectral burst
            if random.random() > 0.98 and res > 0.6:
                ctx.set_source_rgb(1.0, 0.2, 0.3) # Chromatic burst (red)
            else:
                ctx.set_source_rgb(0.95, 0.95, 0.98) # Razor-sharp white
            
            # The "Reaction" - drawing nodes
            radius = (res ** 2) * (cell_w * 0.6)
            ctx.arc(x, y, radius, 0, 2 * math.pi)
            ctx.stroke()
            
            # The "Diffusion" - connecting neighboring nodes in high-resonance areas
            if res > 0.5:
                ctx.set_line_width(0.2)
                ctx.set_source_rgba(0.9, 0.9, 1.0, 0.4)
                # Connect to right neighbor
                if i < cols - 1:
                    ctx.move_to(x, y)
                    ctx.line_to(x + cell_w, y)
                    ctx.stroke()
                # Connect to bottom neighbor
                if j < rows - 1:
                    ctx.move_to(x, y)
                    ctx.line_to(x, y + cell_h)
                    ctx.stroke()

# LAYER 3: Mathematical Hierarchy (Overlays and Grid Annotations)
ctx.set_source_rgba(1.0, 1.0, 1.0, 0.1)
ctx.set_line_width(1.0)

# Vertical 'axis' lines using golden ratio proportions
phi = (1 + 5**0.5) / 2
v_line = width / phi
ctx.move_to(v_line, 0)
ctx.line_to(v_line, height)
ctx.stroke()

# Textural noise/Brutalist detail
for _ in range(200):
    tx = random.uniform(0, width)
    ty = random.uniform(0, height)
    ctx.set_source_rgba(1, 1, 1, random.uniform(0.1, 0.3))
    ctx.rectangle(tx, ty, 1, 1)
    ctx.fill()

# Centralized expansion focal point (The "Pulse")
ctx.set_line_width(0.3)
ctx.set_source_rgba(1, 1, 1, 0.5)
for r in range(50, 400, 40):
    # Logarithmic or power-based spacing
    radius = (r / 400)**1.5 * 300
    ctx.arc(width/2, height/2, radius, 0, 2 * math.pi)
    ctx.set_dash([2, 10])
    ctx.stroke()

# Final high-contrast "Razor" edge
ctx.set_dash([])
ctx.set_line_width(2)
ctx.set_source_rgb(1, 1, 1)
ctx.rectangle(20, 20, width-40, height-40)
ctx.stroke()

