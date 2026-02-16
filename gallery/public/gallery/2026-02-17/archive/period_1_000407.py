import cairo
import math
import random

# Setup
width, height = 600, 480
surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
ctx = cairo.Context(surface)

# Background - Deep charcoal for high contrast
ctx.set_source_rgb(0.02, 0.02, 0.03)
ctx.paint()

def draw_truchet_arc(x, y, size, orientation, weight, color):
    r, g, b, a = color
    ctx.set_source_rgba(r, g, b, a)
    ctx.set_line_width(weight)
    ctx.set_line_cap(cairo.LINE_CAP_ROUND)
    
    if orientation == 0:
        # Arcs connecting top-left to top-right and bottom-left to bottom-right (simplified variants)
        ctx.arc(x, y, size/2, 0, math.pi/2)
        ctx.stroke()
        ctx.arc(x + size, y + size, size/2, math.pi, 3*math.pi/2)
        ctx.stroke()
    else:
        ctx.arc(x + size, y, size/2, math.pi/2, math.pi)
        ctx.stroke()
        ctx.arc(x, y + size, size/2, 3*math.pi/2, 2*math.pi)
        ctx.stroke()

def draw_glitch_block(x, y, size, entropy):
    """Draws a 'digital decay' block consisting of stippled lines or small rects."""
    num_elements = int(10 * entropy)
    for _ in range(num_elements):
        ctx.set_source_rgba(1, 1, 1, random.uniform(0.1, 0.5))
        h = random.uniform(1, 4)
        ctx.rectangle(x + random.uniform(0, size), y + random.uniform(0, size), random.uniform(2, size/2), h)
        ctx.fill()

def generate_composition():
    layers = [
        {"size": 120, "weight": 8, "alpha": 0.15, "dash": None},
        {"size": 60, "weight": 3, "alpha": 0.4, "dash": [2, 10]},
        {"size": 30, "weight": 1.5, "alpha": 0.7, "dash": None},
        {"size": 15, "weight": 0.75, "alpha": 0.9, "dash": [1, 2]}
    ]
    
    center_x, center_y = width / 2, height / 2
    max_dist = math.sqrt(center_x**2 + center_y**2)

    for layer in layers:
        size = layer["size"]
        rows = int(height / size) + 1
        cols = int(width / size) + 1
        
        for i in range(cols):
            for j in range(rows):
                x = i * size
                y = j * size
                
                # Calculate distance-based entropy (0.0 at center, 1.0 at edges)
                dist = math.sqrt((x + size/2 - center_x)**2 + (y + size/2 - center_y)**2)
                entropy = dist / max_dist
                
                # Determine "Thermal" Color based on entropy and position
                # Swiss Red (1.0, 0.1, 0.1) vs Electric Blue (0.1, 0.6, 1.0)
                if random.random() < 0.05 * (1 - entropy): # Bursts near center
                    color = (1.0, 0.2, 0.2, layer["alpha"])
                elif random.random() < 0.03: # Random glitches
                    color = (0.2, 0.7, 1.0, layer["alpha"])
                else:
                    color = (0.9, 0.9, 0.95, layer["alpha"])
                
                # Apply texture/dashing
                if layer["dash"]:
                    ctx.set_dash(layer["dash"])
                else:
                    ctx.set_dash([])

                # Decision: Draw Truchet, Glitch, or Empty space
                # At the center, we follow order. At edges, we dissolve.
                decision = random.random()
                
                if decision < (0.1 * entropy):
                    # Dissolve into entropy (glitch marks)
                    draw_glitch_block(x, y, size, entropy)
                elif decision < 0.9:
                    # Maintain the systemic Truchet grid
                    orientation = random.randint(0, 1)
                    
                    # Mathematical variation: subtly shift lines based on entropy
                    offset_x = math.sin(entropy * math.pi) * (5 * entropy)
                    draw_truchet_arc(x + offset_x, y, size, orientation, layer["weight"], color)
                else:
                    # Negative space / skip tile
                    pass

    # Final "Voxel" Grain Overlay
    # Adds a subtle digital texture across the whole surface
    for _ in range(2000):
        gx = random.uniform(0, width)
        gy = random.uniform(0, height)
        ga = random.uniform(0, 0.1)
        ctx.set_source_rgba(1, 1, 1, ga)
        ctx.rectangle(gx, gy, 1, 1)
        ctx.fill()

    # Border frame (Swiss minimalist style)
    ctx.set_source_rgb(1, 1, 1)
    ctx.set_line_width(20)
    ctx.set_dash([])
    ctx.rectangle(0, 0, width, height)
    ctx.stroke()

generate_composition()
