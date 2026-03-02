import cairo
import math
import random

# Setup
width, height = 600, 480
surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
ctx = cairo.Context(surface)

# Background - Deep Charcoal for a high-contrast Swiss feel
ctx.set_source_rgb(0.05, 0.05, 0.05)
ctx.paint()

# Configuration for the Polar Swiss Grid
center_x, center_y = width / 2, height / 2
num_rings = 42
ring_spacing = 8
num_sectors = 72
phi = (1 + 5**0.5) / 2  # Golden ratio for harmonic proportions

def get_radial_distortion(r, theta):
    """Calculates a mathematical displacement to simulate fluid movement."""
    # Interference pattern using sine waves based on radius and angle
    wave1 = math.sin(theta * 6 + r * 0.02) * 15
    wave2 = math.cos(theta * 3 - r * 0.05) * 10
    return wave1 + wave2

def draw_discretized_arc(ctx, r, start_theta, end_theta, color, weight):
    """Draws a segment of an arc with a specific weight and color."""
    ctx.set_source_rgba(*color)
    ctx.set_line_width(weight)
    
    # Calculate points with distortion
    steps = 10
    step_size = (end_theta - start_theta) / steps
    
    first = True
    for i in range(steps + 1):
        angle = start_theta + i * step_size
        distortion = get_radial_distortion(r, angle)
        distorted_r = r + distortion
        
        x = center_x + distorted_r * math.cos(angle)
        y = center_y + distorted_r * math.sin(angle)
        
        if first:
            ctx.move_to(x, y)
            first = False
        else:
            ctx.line_to(x, y)
    ctx.stroke()

# 1. GENERATE THE UNDERLYING FLOW (Subtle structural layer)
for i in range(num_rings):
    r = 40 + i * ring_spacing
    alpha = 0.1 + (i / num_rings) * 0.2
    ctx.set_source_rgba(0.8, 0.8, 0.8, alpha)
    ctx.set_line_width(0.5)
    
    # Draw faint full rings as the mathematical scaffolding
    ctx.new_path()
    for s in range(361):
        angle = math.radians(s)
        dist = get_radial_distortion(r, angle)
        ctx.line_to(center_x + (r + dist) * math.cos(angle), 
                    center_y + (r + dist) * math.sin(angle))
    ctx.stroke()

# 2. GENERATE DISCRETIZED MODULES (The Swiss primitives)
# We iterate through a polar grid and decide whether to place a 'staccato' mark
for i in range(num_rings):
    r = 40 + i * ring_spacing
    angle_step = (2 * math.pi) / num_sectors
    
    for j in range(num_sectors):
        angle = j * angle_step
        
        # Systematic randomness: create clusters of activity
        # Density is modulated by a combination of angle and radius
        density_factor = math.sin(angle * 3) * math.cos(r * 0.01)
        if random.random() > 0.6 + (density_factor * 0.3):
            
            # Select color palette: Swiss Red, Teal, or Pure White
            rand_val = random.random()
            if rand_val > 0.95:
                color = (0.9, 0.1, 0.1, 0.9) # Swiss Red
            elif rand_val > 0.85:
                color = (0.2, 0.6, 0.7, 0.8) # Muted Teal
            else:
                color = (1.0, 1.0, 1.0, 0.7) # White
            
            # Vary the length of the "dash" based on the golden ratio
            arc_length = angle_step * (random.uniform(0.2, 0.8) if i % 2 == 0 else random.uniform(1.1, 2.5))
            line_weight = random.choice([1, 2, 4]) if i % 5 == 0 else 0.7
            
            draw_discretized_arc(ctx, r, angle, angle + arc_length, color, line_weight)

# 3. ADD RADIAL "GLITCH" STRIKES
# These provide the horizontal/vertical tension against the circular flow
for _ in range(12):
    angle = random.uniform(0, 2 * math.pi)
    r_start = random.uniform(40, 150)
    r_end = r_start + random.uniform(50, 200)
    
    ctx.set_source_rgba(1, 1, 1, 0.3)
    ctx.set_line_width(0.3)
    
    # A straight line in polar space becomes a radial strike
    dist_start = get_radial_distortion(r_start, angle)
    dist_end = get_radial_distortion(r_end, angle)
    
    ctx.move_to(center_x + (r_start + dist_start) * math.cos(angle),
                center_y + (r_start + dist_start) * math.sin(angle))
    ctx.line_to(center_x + (r_end + dist_end) * math.cos(angle),
                center_y + (r_end + dist_end) * math.sin(angle))
    ctx.stroke()

# 4. MICRO-RHYTHMIC DITHERING
# Adding tiny points to simulate texture and "digital dust"
for _ in range(1500):
    r = random.uniform(40, 320)
    angle = random.uniform(0, 2 * math.pi)
    dist = get_radial_distortion(r, angle)
    
    # Bias points toward the flow lines
    final_r = r + dist
    px = center_x + final_r * math.cos(angle)
    py = center_y + final_r * math.sin(angle)
    
    ctx.set_source_rgba(1, 1, 1, random.uniform(0.1, 0.5))
    ctx.arc(px, py, random.uniform(0.5, 1.2), 0, 2 * math.pi)
    ctx.fill()

# Final Border for Swiss precision
ctx.set_source_rgb(1, 1, 1)
ctx.set_line_width(20)
ctx.rectangle(0, 0, width, height)
ctx.stroke()

