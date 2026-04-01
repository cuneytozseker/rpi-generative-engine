import cairo
import math
import random

# Setup
width, height = 600, 480
surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
ctx = cairo.Context(surface)

# Background: Off-white "Swiss" paper texture
ctx.set_source_rgb(0.96, 0.95, 0.93)
ctx.paint()

# Configuration
cx, cy = width // 2, height // 2
rings = 18
base_rotation = random.uniform(0, math.pi * 2)

def polar_to_cartesian(r, theta):
    x = cx + r * math.cos(theta)
    y = cy + r * math.sin(theta)
    return x, y

def draw_warped_rect(r, theta, dr, dtheta, color, alpha=1.0):
    """Draws a 'pixel' unit warped by polar coordinates."""
    ctx.set_source_rgba(color[0], color[1], color[2], alpha)
    
    # Calculate corner points
    p1 = polar_to_cartesian(r, theta)
    p2 = polar_to_cartesian(r + dr, theta)
    p3 = polar_to_cartesian(r + dr, theta + dtheta)
    p4 = polar_to_cartesian(r, theta + dtheta)
    
    ctx.move_to(*p1)
    ctx.line_to(*p2)
    # Arc for the outer edge to maintain circularity
    ctx.arc(cx, cy, r + dr, theta, theta + dtheta)
    ctx.line_to(*p4)
    # Arc for the inner edge
    ctx.arc_negative(cx, cy, r, theta + dtheta, theta)
    ctx.close_path()
    ctx.fill()

# --- GENERATIVE SYSTEM ---

# 1. Background Grid: Faint structural guides
ctx.set_line_width(0.3)
ctx.set_source_rgba(0.2, 0.2, 0.2, 0.1)
for i in range(1, 10):
    ctx.arc(cx, cy, i * 40, 0, 2 * math.pi)
    ctx.stroke()

# 2. Centrifugal Flow Logic
for i in range(rings):
    r_inner = 20 + (i * 18)
    r_outer = r_inner + 12
    
    # Entropy increases with radius: density decreases, jitter increases
    entropy = (i / rings) ** 1.5
    density_factor = max(4, int(40 * (1 - entropy * 0.8)))
    
    # Swiss Accented Palette
    colors = [
        (0.1, 0.1, 0.1), # Deep Charcoal
        (0.1, 0.1, 0.1), # Repeated for weight
        (0.8, 0.1, 0.1), # Swiss Red accent
        (0.2, 0.3, 0.4), # Muted Blue-Grey
    ]
    
    for j in range(density_factor):
        angle_step = (2 * math.pi) / density_factor
        theta = j * angle_step + (entropy * random.uniform(-0.1, 0.1))
        
        # Systematic Skip: controlled randomness to create "erosion"
        if random.random() < (entropy * 0.7):
            continue
            
        # Recursive subdivision logic for visual richness
        sub_divs = 1 if i < 5 else random.choice([1, 2, 3])
        for s in range(sub_divs):
            curr_r = r_inner + (s * (r_outer - r_inner) / sub_divs)
            curr_dr = (r_outer - r_inner) / sub_divs
            
            # Draw primary structural units
            color = random.choice(colors)
            alpha = 0.9 - (entropy * 0.5)
            
            # The "Warp": distorting the theta based on radius
            warp_theta = theta + (math.sin(i * 0.5) * 0.2)
            
            draw_warped_rect(curr_r, warp_theta, curr_dr * 0.8, angle_step * 0.6, color, alpha)
            
            # 3. Visual Texture: Computational Grain
            # Adding "stutter" lines along the radial paths
            if random.random() > 0.4:
                ctx.set_source_rgba(0.1, 0.1, 0.1, 0.4)
                ctx.set_line_width(0.5)
                # Fragmented stroke
                p_start = polar_to_cartesian(curr_r, warp_theta)
                p_end = polar_to_cartesian(curr_r + curr_dr * 2, warp_theta + (entropy * 0.1))
                ctx.move_to(*p_start)
                ctx.line_to(*p_end)
                ctx.stroke()

# 4. Focal Point: The "Imploded" Core
# Denser, high-frequency elements in the center
for k in range(40):
    ctx.set_source_rgba(0.1, 0.1, 0.1, 0.8)
    radius = random.uniform(5, 30)
    ang = random.uniform(0, 2 * math.pi)
    size = random.uniform(1, 4)
    x, y = polar_to_cartesian(radius, ang)
    ctx.rectangle(x, y, size, size)
    ctx.fill()

# 5. Global Rhythmic Movement: Vector "Vines"
# Long, thin strokes that follow the centrifugal flow
ctx.set_line_width(0.2)
for m in range(12):
    angle = (m / 12) * 2 * math.pi
    ctx.set_source_rgba(0.1, 0.1, 0.1, 0.3)
    ctx.move_to(cx, cy)
    
    # Create a curved path radiating outward
    pts = []
    for step in range(10):
        dist = step * 40
        a = angle + math.log(step + 1) * 0.5
        pts.append(polar_to_cartesian(dist, a))
        
    for p in pts:
        ctx.line_to(p[0], p[1])
    ctx.stroke()

# Finishing touch: A subtle "Swiss Grid" border overlay
ctx.set_source_rgba(0.1, 0.1, 0.1, 0.05)
ctx.set_line_width(1)
grid_size = 40
for x in range(0, width, grid_size):
    ctx.move_to(x, 0)
    ctx.line_to(x, height)
    ctx.stroke()
for y in range(0, height, grid_size):
    ctx.move_to(0, y)
    ctx.line_to(width, y)
    ctx.stroke()

