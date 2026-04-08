import cairo
import math
import random

# Setup
width, height = 800, 800  # Increased for better detail
surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
ctx = cairo.Context(surface)

# Background: Deep Swiss Black
ctx.set_source_rgb(0.02, 0.02, 0.02)
ctx.paint()

# Configuration
CENTER_X, CENTER_Y = width // 2, height // 2
MAX_RADIUS = min(width, height) * 0.45
NUM_RINGS = 12
SUBDIVISIONS = 48

def get_polar_coords(r, theta, distortion=0):
    """Calculates Cartesian coordinates with a radial distortion field."""
    # Apply structural entropy: distortion increases with radius
    entropy = (r / MAX_RADIUS) ** 2 * distortion
    r_distorted = r + math.sin(theta * 8) * entropy * 10
    theta_distorted = theta + math.cos(r * 0.05) * entropy * 0.2
    
    x = CENTER_X + r_distorted * math.cos(theta_distorted)
    y = CENTER_Y + r_distorted * math.sin(theta_distorted)
    return x, y

def draw_sector_block(r, dr, theta, dtheta, weight, color=(1, 1, 1)):
    """Draws a curvilinear block based on polar coordinates."""
    ctx.set_source_rgba(*color)
    ctx.set_line_width(weight)
    
    # Define the four corners of the polar cell
    steps = 10
    
    # Outer arc
    for i in range(steps + 1):
        t = theta + (i / steps) * dtheta
        x, y = get_polar_coords(r + dr, t, distortion=1.5)
        if i == 0: ctx.move_to(x, y)
        else: ctx.line_to(x, y)
        
    # Inner arc (reverse)
    for i in range(steps, -1, -1):
        t = theta + (i / steps) * dtheta
        x, y = get_polar_coords(r, t, distortion=1.5)
        ctx.line_to(x, y)
        
    ctx.close_path()
    
    # Swiss logic: sometimes fill, sometimes stroke, sometimes both
    chance = random.random()
    if chance > 0.7:
        ctx.fill()
    elif chance > 0.3:
        ctx.stroke()
    else:
        # Data debris: draw only a fragment or a dot
        ctx.set_line_width(0.5)
        ctx.stroke()

def recursive_subdivide(r, dr, theta, dtheta, depth):
    """Recursively divides polar cells based on structural entropy rules."""
    # Influence field: higher entropy further from center or at specific angles
    influence = (r / MAX_RADIUS) + abs(math.sin(theta * 3)) * 0.5
    
    # Stop condition or continue subdividing
    if depth < 4 and (random.random() < 0.6 or influence < 0.4):
        # Decide whether to split radially or angularly
        if random.random() > 0.5:
            recursive_subdivide(r, dr/2, theta, dtheta, depth + 1)
            recursive_subdivide(r + dr/2, dr/2, theta, dtheta, depth + 1)
        else:
            recursive_subdivide(r, dr, theta, dtheta/2, depth + 1)
            recursive_subdivide(r, dr, theta + dtheta/2, dtheta/2, depth + 1)
    else:
        # Draw the primitive
        # Modulate color based on depth (hierarchy)
        gray = 0.3 + (depth * 0.15)
        alpha = 1.0 - (influence * 0.4)
        weight = 2.5 / (depth + 1)
        
        # Highlight specific 'data' points with pure white
        if random.random() > 0.92:
            draw_sector_block(r, dr * 0.8, theta, dtheta * 0.8, weight * 2, (1, 1, 1, 1))
        else:
            draw_sector_block(r, dr * 0.9, theta, dtheta * 0.9, weight, (gray, gray, gray, alpha))

# --- Main Composition Execution ---

# 1. Background Grid: Underlying systematic rhythm
ctx.set_line_width(0.2)
ctx.set_source_rgba(1, 1, 1, 0.1)
for r_step in range(0, int(MAX_RADIUS), 20):
    ctx.arc(CENTER_X, CENTER_Y, r_step, 0, 2 * math.pi)
    ctx.stroke()

# 2. Structural Layer: The transformed Swiss Grid
ring_width = MAX_RADIUS / NUM_RINGS
angle_step = (2 * math.pi) / SUBDIVISIONS

for i in range(NUM_RINGS):
    r = i * ring_width
    for j in range(SUBDIVISIONS):
        theta = j * angle_step
        
        # Skip certain areas to create negative space "valleys"
        if (math.sin(theta * 4) + math.cos(r * 0.02)) > -0.5:
            recursive_subdivide(r, ring_width, theta, angle_step, 0)

# 3. Floating "Structural Debris" (The peripheral dissipation)
for _ in range(200):
    r = random.uniform(MAX_RADIUS * 0.8, MAX_RADIUS * 1.2)
    theta = random.uniform(0, 2 * math.pi)
    size = random.uniform(1, 4)
    
    x, y = get_polar_coords(r, theta, distortion=3.0)
    
    ctx.set_source_rgba(1, 1, 1, random.uniform(0.2, 0.8))
    ctx.rectangle(x, y, size, size) # Small square "bits"
    ctx.fill()

# 4. Focal Accents: Geometric markers
ctx.set_source_rgb(1, 1, 1)
ctx.set_line_width(1.5)
for i in range(4):
    angle = i * (math.pi / 2)
    x1, y1 = get_polar_coords(MAX_RADIUS * 1.05, angle)
    x2, y2 = get_polar_coords(MAX_RADIUS * 1.15, angle)
    ctx.move_to(x1, y1)
    ctx.line_to(x2, y2)
    ctx.stroke()

# Final Polish: Center Void
ctx.set_source_rgb(0.02, 0.02, 0.02)
ctx.arc(CENTER_X, CENTER_Y, 15, 0, 2 * math.pi)
ctx.fill()
ctx.set_source_rgb(1, 1, 1)
ctx.set_line_width(0.5)
ctx.arc(CENTER_X, CENTER_Y, 15, 0, 2 * math.pi)
ctx.stroke()

# Clean up / Finalize happens outside
