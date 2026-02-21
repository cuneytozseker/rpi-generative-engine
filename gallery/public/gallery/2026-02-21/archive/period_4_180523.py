import cairo
import math
import random

# Setup
width, height = 600, 480
surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
ctx = cairo.Context(surface)

# Background: Warm Swiss-style canvas
ctx.set_source_rgb(0.97, 0.96, 0.94) 
ctx.paint()

def draw_stochastic_grid(ctx, angle, spacing, color, weight, seed):
    """
    Draws a grid of modulated segments that respond to a central vector field.
    The 'erosion' is achieved by probabilistic segment skipping.
    """
    random.seed(seed)
    ctx.save()
    ctx.translate(width / 2, height / 2)
    ctx.rotate(angle)
    
    # Expand range to cover corners after rotation
    limit = int(max(width, height) * 1.2)
    
    for x in range(-limit, limit, spacing):
        ctx.set_line_width(weight)
        
        # Determine segment length based on distance from center (Radial logic)
        y = -limit
        while y < limit:
            # Distance from center for modulation
            dist = math.sqrt(x**2 + y**2)
            norm_dist = dist / (limit)
            
            # Stochastic emergence: segments are more likely to appear near the core
            # and become fragmented/eroded towards the margins.
            if random.random() > (norm_dist * 1.1):
                # Calculate a slight flow perturbation based on a sine field
                flow_offset = math.sin(x * 0.01 + y * 0.01) * 5
                
                # Segment length influenced by radial position
                seg_len = random.uniform(5, 20) * (1.0 - norm_dist * 0.5)
                
                # Apply color: mostly primary, but occasional "chromatic segmentation"
                if random.random() > 0.98:
                    ctx.set_source_rgb(0.9, 0.2, 0.1) # Swiss Red accent
                elif random.random() > 0.98:
                    ctx.set_source_rgb(0.1, 0.3, 0.5) # Muted Blue accent
                else:
                    ctx.set_source_rgba(color[0], color[1], color[2], 0.8)
                
                ctx.move_to(x + flow_offset, y)
                ctx.line_to(x + flow_offset, y + seg_len)
                ctx.stroke()
                
                y += seg_len + random.uniform(2, 5) # Variable gap
            else:
                y += spacing * 0.5 # Skip space
                
    ctx.restore()

# 1. Base Layer: A subtle dithered point cloud for texture
ctx.set_source_rgba(0.1, 0.1, 0.1, 0.1)
for _ in range(3000):
    rx = random.gauss(width/2, width/4)
    ry = random.gauss(height/2, height/4)
    ctx.arc(rx, ry, 0.5, 0, 2 * math.pi)
    ctx.fill()

# 2. First Angular Grid: The "Fixed" Structure
# Using high-density parallel lines to facilitate Moiré interference
draw_stochastic_grid(
    ctx, 
    angle=math.radians(15), 
    spacing=6, 
    color=(0.1, 0.1, 0.1), 
    weight=0.75, 
    seed=42
)

# 3. Second Angular Grid: The "Rotating" Influence
# A slight 2.5-degree offset creates the characteristic interference patterns
draw_stochastic_grid(
    ctx, 
    angle=math.radians(17.5), 
    spacing=6, 
    color=(0.1, 0.1, 0.1), 
    weight=0.75, 
    seed=88
)

# 4. Focal Core: Structural primitives
# Rectilinear blocks that anchor the composition as per Swiss principles
ctx.set_source_rgb(0.1, 0.1, 0.1)
rect_size = 40
ctx.rectangle(width/2 - rect_size/2, height/2 - rect_size/2, rect_size, rect_size)
ctx.fill()

# Accent glyphs: Small dashes following the Golden Ratio for spacing
phi = 1.618
for i in range(5):
    offset = 60 * (phi ** i)
    if offset < width/2:
        ctx.set_line_width(2)
        ctx.set_source_rgb(0.9, 0.2, 0.1) # Red accent
        ctx.move_to(width/2 + offset, height/2 - 10)
        ctx.line_to(width/2 + offset, height/2 + 10)
        ctx.stroke()

# 5. Final pass: Digital erosion / noise overlay
# Simulates a "printed" or "risograph" texture over the whole composition
for _ in range(1000):
    ctx.set_source_rgba(0.97, 0.96, 0.94, 0.4) # Background color dots
    ctx.arc(random.random() * width, random.random() * height, 0.8, 0, 2 * math.pi)
    ctx.fill()

