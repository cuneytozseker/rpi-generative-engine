import cairo
import math
import random

# Setup
width, height = 600, 480
surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
ctx = cairo.Context(surface)

# Background - Deep Charcoal
ctx.set_source_rgb(0.05, 0.05, 0.07)
ctx.paint()

# Helper for Polar Transformation
def get_polar_coords(cx, cy, r, angle_deg):
    angle_rad = math.radians(angle_deg)
    x = cx + r * math.cos(angle_rad)
    y = cy + r * math.sin(angle_rad)
    return x, y

def draw_distorted_arc(ctx, cx, cy, r, start_angle, end_angle, steps=20):
    """Draws an arc with subtle radial noise/oscillation."""
    for i in range(steps + 1):
        t = i / steps
        angle = start_angle + t * (end_angle - start_angle)
        # Parametric distortion: radius varies with angle and sine harmonics
        distortion = math.sin(angle * 0.1) * 5 + math.cos(angle * 0.05) * 2
        curr_r = r + distortion
        x, y = get_polar_coords(cx, cy, curr_r, angle)
        if i == 0:
            ctx.move_to(x, y)
        else:
            ctx.line_to(x, y)

# Composition Parameters
center_x, center_y = width // 2, height // 2
rings = 42
slices = 60
max_radius = min(width, height) * 0.8
accent_color = (1.0, 0.2, 0.1) # International Orange (Swiss Punctuation)
highlight_color = (0.0, 0.8, 0.9) # Logic Blue

# 1. BASE GRID: Subtle Radial Structure
ctx.set_line_width(0.3)
for i in range(rings):
    # Variable Frequency: Rings get denser towards the center (Centripetal Tension)
    normalized_i = i / rings
    r = max_radius * math.pow(normalized_i, 1.5)
    
    alpha = 0.1 + (0.4 * (1 - normalized_i))
    ctx.set_source_rgba(0.8, 0.8, 0.8, alpha)
    
    # Draw ring segments
    for s in range(slices):
        if random.random() > 0.3: # Interrupted lines for rhythm
            angle_start = (s / slices) * 360
            angle_end = ((s + 0.8) / slices) * 360
            draw_distorted_arc(ctx, center_x, center_y, r, angle_start, angle_end)
            ctx.stroke()

# 2. SYNTHETIC TOPOGRAPHY: Recursive "Blocks" and Density Modulation
for i in range(12):
    r_idx = random.randint(5, rings - 5)
    s_idx = random.randint(0, slices)
    
    # Mapping index to non-linear radius
    r = max_radius * math.pow(r_idx / rings, 1.5)
    angle = (s_idx / slices) * 360
    
    # Block size
    thickness = random.uniform(2, 12)
    arc_len = random.uniform(5, 30)
    
    # Draw "Aliased" Block (mimicking digital dithering through segmented layering)
    ctx.set_source_rgba(0.9, 0.9, 0.9, 0.8)
    ctx.set_line_width(thickness)
    draw_distorted_arc(ctx, center_x, center_y, r, angle, angle + arc_len)
    ctx.stroke()
    
    # Chromatic Punctuation: Logic Nodes
    if random.random() > 0.6:
        ctx.set_source_rgb(*accent_color)
        px, py = get_polar_coords(center_x, center_y, r, angle)
        ctx.arc(px, py, 1.5, 0, 2 * math.pi)
        ctx.fill()

# 3. VECTOR PATHFINDING: Radial Connectors
ctx.set_line_width(0.5)
for s in range(slices):
    if s % 3 == 0: # Systematic spacing
        angle = (s / slices) * 360
        # Create a path that skips certain rings
        current_r = 20
        ctx.move_to(*get_polar_coords(center_x, center_y, current_r, angle))
        
        while current_r < max_radius:
            step = random.uniform(10, 50)
            current_r += step
            # Slight angular drift for "Organic" feel
            angle += random.uniform(-2, 2)
            
            if random.random() > 0.2:
                ctx.set_source_rgba(1, 1, 1, 0.4)
                ctx.line_to(*get_polar_coords(center_x, center_y, current_r, angle))
                ctx.stroke()
                
                # Add a small perpendicular "tick" (Swiss precision)
                tx, ty = get_polar_coords(center_x, center_y, current_r, angle)
                ctx.move_to(tx, ty)
                tx2, ty2 = get_polar_coords(center_x, center_y, current_r + 5, angle + 90)
                ctx.line_to(tx2, ty2)
                ctx.stroke()
            
            ctx.move_to(*get_polar_coords(center_x, center_y, current_r, angle))

# 4. OVERLAY: High Contrast Data Clusters
for _ in range(10):
    cluster_angle = random.uniform(0, 360)
    cluster_r = random.uniform(50, max_radius)
    
    # Draw a "logic cluster" - small dense rectangles
    for _ in range(5):
        ctx.set_source_rgba(0.0, 0.8, 0.9, 0.6) # Highlight color
        w = random.uniform(2, 8)
        h = random.uniform(10, 25)
        
        # Position slightly offset from cluster center
        cx = cluster_x = cluster_r + random.uniform(-20, 20)
        ca = cluster_a = cluster_angle + random.uniform(-5, 5)
        
        x, y = get_polar_coords(center_x, center_y, cx, ca)
        
        ctx.save()
        ctx.translate(x, y)
        ctx.rotate(math.radians(ca)) # Align to the radial vector
        ctx.rectangle(-w/2, -h/2, w, h)
        ctx.fill()
        ctx.restore()

# 5. FINAL TEXTURE: Atmospheric Grain / Fine Lines
ctx.set_source_rgba(1, 1, 1, 0.05)
ctx.set_line_width(0.1)
for i in range(200):
    r1 = random.uniform(0, max_radius)
    ang = random.uniform(0, 360)
    x, y = get_polar_coords(center_x, center_y, r1, ang)
    ctx.arc(x, y, 0.5, 0, 2*math.pi)
    ctx.stroke()

# Clean border for Swiss aesthetic
ctx.set_source_rgb(0.05, 0.05, 0.07)
ctx.set_line_width(30)
ctx.rectangle(0, 0, width, height)
ctx.stroke()

# Surface is finalized.
