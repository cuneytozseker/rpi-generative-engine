import cairo
import math
import random

# Setup
width, height = 600, 480
surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
ctx = cairo.Context(surface)

# Background: High-contrast dark void
ctx.set_source_rgb(0.02, 0.02, 0.03) 
ctx.paint()

def get_noise(x, y, scale=0.005):
    """
    Simulates a vector field using harmonic trigonometric summation.
    Produces smooth, organic flow without external dependencies.
    """
    val = math.sin(x * scale) + math.cos(y * scale)
    val += math.sin((x + y) * scale * 0.5) * 0.5
    val += math.cos((x - y) * scale * 2.0) * 0.2
    return val * math.pi # Returns an angle

def draw_flow_particle(x, y, length, steps, base_alpha):
    """
    Draws a kinetic trail following the vector field.
    """
    ctx.move_to(x, y)
    curr_x, curr_y = x, y
    
    for i in range(steps):
        angle = get_noise(curr_x, curr_y)
        
        # Calculate velocity based on noise
        vx = math.cos(angle) * length
        vy = math.sin(angle) * length
        
        # Interaction: Color shift based on angle (harmonic energy)
        # Shift from cool (cyan) to warm (amber)
        t = (angle + math.pi) / (2 * math.pi)
        r = 0.5 + 0.5 * math.cos(2 * math.pi * (t + 0.0))
        g = 0.8 + 0.2 * math.cos(2 * math.pi * (t + 0.3))
        b = 0.9 + 0.1 * math.cos(2 * math.pi * (t + 0.6))
        
        # Fade out towards the end of the trail
        alpha = base_alpha * (1.0 - (i / steps))
        
        ctx.set_source_rgba(r, g, b, alpha)
        
        new_x = curr_x + vx
        new_y = curr_y + vy
        
        ctx.line_to(new_x, new_y)
        ctx.set_line_width(0.4 + (1.0 - i/steps) * 0.8)
        ctx.stroke()
        
        curr_x, curr_y = new_x, new_y
        ctx.move_to(curr_x, curr_y)

def recursive_subdivision(x, y, w, h, depth):
    """
    Implements a quadtree-style grid subdivision with 
    logarithmic density toward the center.
    """
    center_dist = math.sqrt((x + w/2 - width/2)**2 + (y + h/2 - height/2)**2)
    normalized_dist = center_dist / (width * 0.7)
    
    # Subdivide if we are deep or close to the center (rhythmic expansion)
    should_subdivide = depth < 5 and (random.random() > normalized_dist or depth < 2)
    
    if should_subdivide:
        nw, nh = w / 2, h / 2
        recursive_subdivision(x, y, nw, nh, depth + 1)
        recursive_subdivision(x + nw, y, nw, nh, depth + 1)
        recursive_subdivision(x, y + nh, nw, nh, depth + 1)
        recursive_subdivision(x + nw, y + nh, nw, nh, depth + 1)
    else:
        # Drawing Logic within the subdivision
        # Vector precision: Draw grid boundaries faintly
        ctx.set_source_rgba(1, 1, 1, 0.05)
        ctx.set_line_width(0.5)
        ctx.rectangle(x, y, w, h)
        ctx.stroke()
        
        # Kinetic flow logic
        num_particles = int(10 * (6 - depth))
        for _ in range(num_particles):
            px = x + random.random() * w
            py = y + random.random() * h
            
            # Use atmospheric diffusion: multiple layers of low alpha
            draw_flow_particle(
                px, py, 
                length=random.uniform(2, 5), 
                steps=random.randint(5, 15), 
                base_alpha=random.uniform(0.1, 0.4)
            )

# Execute the Generative System
random.seed(42) # For deterministic elegance

# 1. Background layer of faint, large-scale flow
for _ in range(100):
    draw_flow_particle(
        random.random() * width, 
        random.random() * height, 
        length=15, steps=30, base_alpha=0.03
    )

# 2. Main recursive structure
recursive_subdivision(20, 20, width - 40, height - 40, 0)

# 3. Final Swiss design accents (Typography-like geometric markers)
ctx.set_source_rgba(1, 1, 1, 0.8)
ctx.set_line_width(1.5)
margin = 30
# Corner marks
markers = [
    (margin, margin, 10, 0), 
    (width-margin, margin, -10, 0),
    (margin, height-margin, 10, 0),
    (width-margin, height-margin, -10, 0)
]
for mx, my, dx, dy in markers:
    ctx.move_to(mx, my)
    ctx.line_to(mx + dx, my)
    ctx.move_to(mx, my)
    ctx.line_to(mx, my + (10 if dy == 0 and my < height/2 else -10))
    ctx.stroke()

# 4. Center crosshair
ctx.set_source_rgba(1, 1, 1, 0.3)
ctx.move_to(width/2 - 5, height/2)
ctx.line_to(width/2 + 5, height/2)
ctx.move_to(width/2, height/2 - 5)
ctx.line_to(width/2, height/2 + 5)
ctx.stroke()

# Final atmospheric pass: very thin white lines to unify the composition
ctx.set_line_width(0.2)
ctx.set_source_rgba(1, 1, 1, 0.1)
for i in range(0, width, 80):
    ctx.move_to(i, 0)
    ctx.line_to(i, height)
    ctx.stroke()
