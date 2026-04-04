import cairo
import math
import random

# Setup
width, height = 600, 480
surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
ctx = cairo.Context(surface)

# Background - Dark neutral foundation
ctx.set_source_rgb(0.04, 0.04, 0.05)
ctx.paint()

def get_field_angle(x, y, seed_val):
    """Generates a pseudo-perlin flow field using trigonometric octaves."""
    scale1 = 0.005
    scale2 = 0.015
    angle = (math.sin(x * scale1 + seed_val) + 
             math.cos(y * scale1 - seed_val) + 
             math.sin((x + y) * scale2))
    return angle * math.pi

def draw_kinetic_particle(start_x, start_y, steps, base_color):
    ctx.save()
    
    x, y = start_x, start_y
    seed_val = random.uniform(0, 100)
    
    # Kinetic entropy: particles start ordered and become more jittered
    for i in range(steps):
        angle = get_field_angle(x, y, seed_val)
        
        # Calculate velocity with radial expansion influence
        dist_from_center = math.sqrt((x - width/2)**2 + (y - height/2)**2)
        expansion_force = 0.8
        
        vx = math.cos(angle) * 3 + (x - width/2) * 0.005 * expansion_force
        vy = math.sin(angle) * 3 + (y - height/2) * 0.005 * expansion_force
        
        # Add entropy/jitter as distance increases
        jitter = (dist_from_center / width) * 2.0
        vx += random.uniform(-jitter, jitter)
        vy += random.uniform(-jitter, jitter)
        
        new_x, new_y = x + vx, y + vy
        
        # Distance-based alpha for density modulation
        alpha = max(0, 1.0 - (dist_from_center / (width * 0.6)))
        
        # Modular Primitives: Occasionally draw a "structural fragment" instead of a line
        if i % 15 == 0 and random.random() > 0.7:
            # High-chroma spectral shifts
            if random.random() > 0.92:
                ctx.set_source_rgba(0.0, 0.9, 1.0, alpha * 0.8) # Cyan pulse
            elif random.random() > 0.92:
                ctx.set_source_rgba(1.0, 0.2, 0.4, alpha * 0.8) # Magenta pulse
            else:
                ctx.set_source_rgba(base_color[0], base_color[1], base_color[2], alpha * 0.5)
            
            # Draw a rectilinear fragment oriented to flow
            ctx.save()
            ctx.translate(x, y)
            ctx.rotate(angle)
            ctx.rectangle(-2, -1, random.uniform(5, 15), 1.5)
            ctx.fill()
            ctx.restore()
        else:
            # Standard flow path with optical blending
            ctx.set_source_rgba(base_color[0], base_color[1], base_color[2], alpha * 0.3)
            ctx.set_line_width(0.8)
            ctx.move_to(x, y)
            ctx.line_to(new_x, new_y)
            ctx.stroke()
            
        x, y = new_x, new_y
        
        # Stop if out of bounds
        if x < -50 or x > width + 50 or y < -50 or y > height + 50:
            break
            
    ctx.restore()

# 1. Create a diffuse atmospheric gradient in the background
lg = cairo.RadialGradient(width/2, height/2, 50, width/2, height/2, 400)
lg.add_color_stop_rgba(0, 0.15, 0.15, 0.2, 0.3)
lg.add_color_stop_rgba(1, 0.04, 0.04, 0.05, 0)
ctx.set_source(lg)
ctx.rectangle(0, 0, width, height)
ctx.fill()

# 2. Generate the flow trails
# Centralized order: start more particles near the center
num_particles = 450
for _ in range(num_particles):
    # Radial start distribution (Golden ratio inspired spiral or random disk)
    r = random.uniform(0, 40)
    theta = random.uniform(0, 2 * math.pi)
    start_x = width/2 + r * math.cos(theta)
    start_y = height/2 + r * math.sin(theta)
    
    # Systematic color variation (Desaturated greys with subtle warmth)
    gray_val = random.uniform(0.7, 0.9)
    base_color = (gray_val, gray_val, gray_val + random.uniform(-0.05, 0.05))
    
    draw_kinetic_particle(start_x, start_y, 120, base_color)

# 3. Add Crisp Structural Overlay (Swiss precision element)
# A subtle grid or coordinate markers to ground the entropy
ctx.set_line_width(0.5)
ctx.set_source_rgba(1, 1, 1, 0.15)
grid_spacing = 80
for i in range(1, int(width/grid_spacing)):
    # Vertical markers
    curr_x = i * grid_spacing
    ctx.move_to(curr_x, 20)
    ctx.line_to(curr_x, 30)
    ctx.stroke()
    
for j in range(1, int(height/grid_spacing)):
    # Horizontal markers
    curr_y = j * grid_spacing
    ctx.move_to(20, curr_y)
    ctx.line_to(30, curr_y)
    ctx.stroke()

# 4. Focal core accent
ctx.set_source_rgba(1, 1, 1, 0.05)
ctx.arc(width/2, height/2, 2, 0, 2 * math.pi)
ctx.fill()

# Final Polish: Add a subtle vignette-like fade at the edges
ctx.set_operator(cairo.OPERATOR_DEST_IN)
vg = cairo.RadialGradient(width/2, height/2, 100, width/2, height/2, 350)
vg.add_color_stop_rgba(0, 1, 1, 1, 1)
vg.add_color_stop_rgba(1, 1, 1, 1, 0)
ctx.set_source(vg)
ctx.paint()

