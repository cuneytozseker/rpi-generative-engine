import cairo
import math
import random

# Setup: Harmonic Disruption - Polar Swiss Grid
width, height = 600, 480
surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
ctx = cairo.Context(surface)

# Background: Deep charcoal for a brutalist feel
ctx.set_source_rgb(0.05, 0.05, 0.07)
ctx.paint()

def polar_to_cartesian(cx, cy, r, theta):
    return cx + r * math.cos(theta), cy + r * math.sin(theta)

def draw_distorted_grid():
    cx, cy = width / 2, height / 2
    max_radius = min(width, height) * 0.8
    
    num_rings = 42
    num_sectors = 80
    
    # Palette: Swiss-inspired high contrast with probabilistic chroma
    colors = [
        (0.95, 0.95, 0.95), # Off-white
        (0.8, 0.1, 0.1),    # Swiss Red
        (0.1, 0.3, 0.8),    # Electric Blue
        (0.9, 0.8, 0.1)     # Signal Yellow
    ]

    # 1. Background Texture (Digital Grain/Stippling)
    for _ in range(3000):
        ctx.set_source_rgba(1, 1, 1, random.uniform(0.05, 0.15))
        rx = random.uniform(0, width)
        ry = random.uniform(0, height)
        ctx.arc(rx, ry, 0.5, 0, 2 * math.pi)
        ctx.fill()

    # 2. Mathematical System: Non-linear Grid Subdivisions
    for i in range(1, num_rings):
        # Harmonic spacing for radius
        norm_i = i / num_rings
        r = math.pow(norm_i, 1.2) * max_radius
        
        # Determine rhythmic behavior for this ring
        is_bold = i % 5 == 0
        is_dashed = i % 3 == 0
        
        # Sector loop
        for j in range(num_sectors):
            theta_start = (j / num_sectors) * 2 * math.pi
            theta_end = ((j + 1) / num_sectors) * 2 * math.pi
            
            # Harmonic Distortion Logic:
            # Radius is perturbed by a combination of angle and radial index
            def get_distorted_r(angle, radius_idx):
                wave = math.sin(angle * 8 + radius_idx * 0.2) * 4
                interference = math.cos(angle * 3 - radius_idx * 0.5) * 6
                return r + wave + interference

            r1 = get_distorted_r(theta_start, i)
            r2 = get_distorted_r(theta_end, i)
            
            x1, y1 = polar_to_cartesian(cx, cy, r1, theta_start)
            x2, y2 = polar_to_cartesian(cx, cy, r2, theta_end)

            # Probabilistic Palette Injection
            dice = random.random()
            if dice > 0.985:
                ctx.set_source_rgb(*random.choice(colors[1:]))
                ctx.set_line_width(2.5)
            elif dice > 0.8:
                ctx.set_source_rgba(0.9, 0.9, 0.9, 0.6)
                ctx.set_line_width(0.4)
            else:
                ctx.set_source_rgba(0.5, 0.5, 0.6, 0.3)
                ctx.set_line_width(0.2)

            # Modulated Discretization: Draw segments instead of continuous lines
            if not is_dashed or (j % 2 == 0):
                ctx.move_to(x1, y1)
                ctx.line_to(x2, y2)
                ctx.stroke()

            # Radial "Spines" (The Skeleton)
            if j % 10 == 0:
                inner_r = get_distorted_r(theta_start, i - 1)
                ix, iy = polar_to_cartesian(cx, cy, inner_r, theta_start)
                
                ctx.set_line_width(0.15 if not is_bold else 0.8)
                ctx.set_source_rgba(1, 1, 1, 0.2 if not is_bold else 0.5)
                ctx.move_to(ix, iy)
                ctx.line_to(x1, y1)
                ctx.stroke()

    # 3. Floating Focal Anchors (Brutalist Geometry)
    for _ in range(5):
        angle = random.uniform(0, 2 * math.pi)
        dist = random.uniform(50, max_radius * 0.7)
        fx, fy = polar_to_cartesian(cx, cy, dist, angle)
        
        # Small geometric "data points"
        ctx.set_source_rgb(0.95, 0.95, 0.95)
        size = random.uniform(2, 5)
        ctx.rectangle(fx - size/2, fy - size/2, size, size)
        ctx.fill()
        
        # Technical callouts (simulated hierarchy)
        ctx.set_line_width(0.5)
        ctx.move_to(fx, fy)
        ctx.line_to(fx + random.choice([-20, 20]), fy - 20)
        ctx.stroke()

    # 4. Global Warp: Overlaying a subtle flow field with fine lines
    ctx.set_line_width(0.1)
    for k in range(120):
        curr_x = random.uniform(0, width)
        curr_y = random.uniform(0, height)
        ctx.set_source_rgba(1, 1, 1, 0.1)
        ctx.move_to(curr_x, curr_y)
        for _ in range(15):
            # Simple vector flow
            angle = math.atan2(curr_y - cy, curr_x - cx) + math.pi/2
            curr_x += math.cos(angle) * 5
            curr_y += math.sin(angle) * 5
            ctx.line_to(curr_x, curr_y)
        ctx.stroke()

draw_distorted_grid()
