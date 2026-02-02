import cairo
import math
import random

# Setup
width, height = 600, 480
surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
ctx = cairo.Context(surface)

# Background - Deep Void
ctx.set_source_rgb(0.02, 0.02, 0.03)
ctx.paint()

def draw_angular_grid(cx, cy, angle_offset, line_count, spacing, color, weight, entropy_factor=0):
    """
    Draws a series of parallel lines rotated by a specific angle.
    entropy_factor introduces stochastic jitter to the line paths.
    """
    ctx.save()
    ctx.translate(cx, cy)
    ctx.rotate(angle_offset)
    
    r, g, b, a = color
    ctx.set_source_rgba(r, g, b, a)
    ctx.set_line_width(weight)

    # Calculate span to cover the canvas regardless of rotation
    max_dim = int(math.sqrt(width**2 + height**2))
    
    for i in range(-max_dim // spacing, max_dim // spacing):
        x = i * spacing
        
        # Introduce systematic variance: lines get thicker or thinner based on index
        current_weight = weight * (1.0 + 0.5 * math.sin(i * 0.2))
        ctx.set_line_width(current_weight)
        
        # Break the line into segments to allow for entropy (bending/jitter)
        segments = 10
        seg_h = max_dim / segments
        
        ctx.move_to(x, -max_dim/2)
        for s in range(segments + 1):
            y = -max_dim/2 + s * seg_h
            jitter = (random.random() - 0.5) * entropy_factor if s > 0 else 0
            # Exponential drift towards the edges
            drift = (i * 0.05) * (s / segments)**2 * entropy_factor
            ctx.line_to(x + jitter + drift, y)
            
        ctx.stroke()
    ctx.restore()

def draw_data_glyphs(grid_size, chance):
    """Adds small geometric primitives at grid intersections to suggest system metadata."""
    ctx.set_source_rgb(0.9, 0.9, 0.9)
    ctx.set_line_width(0.5)
    
    for x in range(0, width, grid_size):
        for y in range(0, height, grid_size):
            if random.random() < chance:
                size = random.choice([2, 4, 8])
                # Swiss style markers
                if random.random() > 0.5:
                    ctx.rectangle(x - size/2, y - size/2, size, size)
                else:
                    ctx.move_to(x - size, y)
                    ctx.line_to(x + size, y)
                    ctx.move_to(x, y - size)
                    ctx.line_to(x, y + size)
                ctx.stroke()

# --- Composition Logic ---

# 1. Base Grid Layer (The "Order")
# High frequency, low opacity lines providing the structural foundation
draw_angular_grid(width/2, height/2, math.radians(15), 120, 4, (0.8, 0.8, 0.8, 0.15), 0.5)

# 2. Interference Layer A (The "Moiré Generator")
# Rotated slightly away from the base to create visual beating/interference
draw_angular_grid(width/2, height/2, math.radians(16.5), 100, 6, (0.9, 0.9, 1.0, 0.4), 0.7)

# 3. Interference Layer B (The "Entropy")
# Much higher entropy factor at a distinct angle
draw_angular_grid(width/2, height/2, math.radians(-12), 80, 12, (0.7, 0.7, 0.7, 0.2), 1.2, entropy_factor=1.5)

# 4. Selective Chromatic Accents
# Punctuating the grid with high-contrast Swiss Red
ctx.set_source_rgba(1.0, 0.1, 0.1, 0.8)
for _ in range(5):
    rx = random.randint(100, width-100)
    ry = random.randint(100, height-100)
    ctx.arc(rx, ry, 3, 0, 2*math.pi)
    ctx.fill()
    # Connecting threads
    ctx.set_line_width(0.3)
    ctx.move_to(rx, 0)
    ctx.line_to(rx, height)
    ctx.stroke()

# 5. Overlaid Focal Subdivision
# Creating a central 'safe zone' of geometric clarity
ctx.set_source_rgba(0.02, 0.02, 0.03, 0.6) # Semi-transparent mask
ctx.arc(width/2, height/2, 120, 0, 2*math.pi)
ctx.fill()

# Re-draw a very clean, high-contrast grid inside the focal point
ctx.save()
ctx.arc(width/2, height/2, 120, 0, 2*math.pi)
ctx.clip()
draw_angular_grid(width/2, height/2, 0, 40, 10, (1.0, 1.0, 1.0, 0.9), 1.0)
draw_angular_grid(width/2, height/2, math.radians(90), 40, 10, (1.0, 1.0, 1.0, 0.9), 1.0)
ctx.restore()

# 6. Technical Detailing (Glyphs)
# Scattered at the edges to simulate data decay
draw_data_glyphs(40, 0.12)

# 7. Final Framing
ctx.set_source_rgb(1, 1, 1)
ctx.set_line_width(20)
ctx.rectangle(0, 0, width, height)
ctx.stroke() # Internal border feel

# Signature Swiss element: Thin vertical rule on the right
ctx.set_source_rgb(1, 1, 1)
ctx.set_line_width(1)
ctx.move_to(width - 40, 40)
ctx.line_to(width - 40, height - 40)
ctx.stroke()

