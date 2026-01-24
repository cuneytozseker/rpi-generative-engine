import cairo
import math
import random

# Setup
width, height = 600, 480
surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
ctx = cairo.Context(surface)

# Background - Deep Charcoal
ctx.set_source_rgb(0.02, 0.02, 0.03)
ctx.paint()

def draw_deformed_grid(ctx, width, height, angle, spacing, color, complexity):
    """Draws a grid of lines that subtly deform and glitch based on position."""
    ctx.save()
    ctx.translate(width / 2, height / 2)
    ctx.rotate(angle)
    ctx.translate(-width, -height) # Overscan to cover rotation gaps
    
    line_count = int((width * 2) / spacing)
    
    for i in range(line_count):
        x = i * spacing
        
        # Systematic variation in line weight based on index harmonics
        weight = 0.3 + (math.sin(i * 0.1) + 1) * 0.4
        ctx.set_line_width(weight)
        
        # High-contrast palette with slight transparency for interference depth
        ctx.set_source_rgba(color[0], color[1], color[2], 0.7)
        
        ctx.move_to(x, 0)
        
        # Segmented lines to allow for "glitching" at the margins
        steps = 20
        segment_h = (height * 2) / steps
        for s in range(steps + 1):
            curr_y = s * segment_h
            
            # Stochastic displacement (the "dissonance")
            # Increases as we move away from the center (centrifugal dispersion)
            dist_from_mid = abs(curr_y - height) / height
            jitter = (random.random() - 0.5) * complexity * dist_from_mid
            
            # Apply a wave function to the grid to enhance Moiré complexity
            wave = math.sin(curr_y * 0.01 + i * 0.05) * 2.0
            
            ctx.line_to(x + jitter + wave, curr_y)
            
        ctx.stroke()
        
        # Occasional "bitmapped block" - Cellular Modularity
        if random.random() < 0.02:
            ctx.set_source_rgba(color[0], color[1], color[2], 0.9)
            block_size = random.uniform(2, 5)
            ctx.rectangle(x - block_size/2, random.uniform(0, height * 2), block_size, block_size * 3)
            ctx.fill()
            
    ctx.restore()

def draw_nodal_network(ctx, width, height, count):
    """Adds a layer of thin connectivity representing data corruption/noise."""
    ctx.set_line_width(0.15)
    ctx.set_source_rgba(0.9, 0.9, 1.0, 0.4)
    
    points = []
    for _ in range(count):
        points.append((random.uniform(50, width-50), random.uniform(50, height-50)))
    
    for i, p1 in enumerate(points):
        # Connect to nearby points to create clusters
        for p2 in points[i+1:]:
            dist = math.sqrt((p1[0]-p2[0])**2 + (p1[1]-p2[1])**2)
            if dist < 60:
                ctx.move_to(p1[0], p1[1])
                ctx.line_to(p2[0], p2[1])
                ctx.stroke()
                
        # Draw small square nodes
        ctx.rectangle(p1[0]-1, p1[1]-1, 2, 2)
        ctx.fill()

# Main Compositional Execution

# Layer 1: The primary rigid system (Pure White)
draw_deformed_grid(ctx, width, height, math.radians(15), 6, (0.95, 0.95, 0.95), 1.5)

# Layer 2: The interfering system (Slightly offset and rotated)
# The interaction between Layer 1 and 2 creates the Moiré effect
ctx.set_operator(cairo.OPERATOR_ADD) # Additive blending for luminosity
draw_deformed_grid(ctx, width, height, math.radians(18.5), 5.8, (0.8, 0.8, 1.0), 3.0)
ctx.set_operator(cairo.OPERATOR_OVER)

# Layer 3: Systematic breakdown - Nodal connectivity
# This represents the "nodal network" logic from the brief
draw_nodal_network(ctx, width, height, 80)

# Final Polish: Swiss-style Border/Margin logic
ctx.set_source_rgb(0.02, 0.02, 0.03)
margin = 40
ctx.set_line_width(margin * 2)
# Create a frame to focus the centrifugal chaos
ctx.rectangle(0, 0, width, height)
ctx.stroke()

# Subtle geometric accents in the corners (Typography-like precision)
ctx.set_source_rgb(0.9, 0.1, 0.2) # High-contrast saturated ink (Red)
ctx.set_line_width(1.0)
corner_size = 20
# Top Left
ctx.move_to(margin, margin)
ctx.line_to(margin + corner_size, margin)
ctx.move_to(margin, margin)
ctx.line_to(margin, margin + corner_size)
# Bottom Right
ctx.move_to(width - margin, height - margin)
ctx.line_to(width - margin - corner_size, height - margin)
ctx.move_to(width - margin, height - margin)
ctx.line_to(width - margin, height - margin - corner_size)
ctx.stroke()

# Modular "bit-blocks" in the margin
for i in range(5):
    ctx.rectangle(margin + 5, height - margin + 10 + (i*6), 4, 2)
    ctx.fill()

