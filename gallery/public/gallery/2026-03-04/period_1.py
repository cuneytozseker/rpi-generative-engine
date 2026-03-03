import cairo
import math
import random

# Setup
width, height = 600, 480
surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
ctx = cairo.Context(surface)

# Background: Deep Obsidian
ctx.set_source_rgb(0.02, 0.02, 0.04)
ctx.paint()

# Constants
CENTER_X, CENTER_Y = width / 2, height / 2
RINGS = 24
SPOKES = 40
ACCENT_COLOR = (0.0, 0.95, 1.0) # Electric Cyan
SECONDARY_COLOR = (1.0, 0.27, 0.0) # International Orange
WHITE = (0.9, 0.9, 0.9)

def polar_to_cartesian(r, theta, distortion_factor=1.0):
    """Applies a radial distortion to the polar mapping."""
    # Harmonic distortion creates the 'informational' jitter
    r_offset = 15 * math.sin(theta * 6) * math.cos(r * 0.02)
    t_offset = 0.1 * math.sin(r * 0.05)
    
    final_r = r + r_offset * distortion_factor
    final_t = theta + t_offset * distortion_factor
    
    x = CENTER_X + final_r * math.cos(final_t)
    y = CENTER_Y + final_r * math.sin(final_t)
    return x, y

def draw_technical_node(x, y, size, style="cross"):
    ctx.set_line_width(0.5)
    if style == "cross":
        ctx.move_to(x - size, y)
        ctx.line_to(x + size, y)
        ctx.move_to(x, y - size)
        ctx.line_to(x, y + size)
        ctx.stroke()
    elif style == "box":
        ctx.rectangle(x - size/2, y - size/2, size, size)
        ctx.fill()

# 1. PRIMARY INFRASTRUCTURE: The distorted grid
# We draw the radial lines (spokes) first
for s in range(SPOKES):
    theta = (s / SPOKES) * 2 * math.pi
    ctx.set_source_rgba(0.2, 0.3, 0.4, 0.4)
    ctx.set_line_width(0.25)
    
    ctx.move_to(*polar_to_cartesian(20, theta))
    for r in range(20, 320, 10):
        ctx.line_to(*polar_to_cartesian(r, theta))
    ctx.stroke()

# 2. HARMONIC SUBDIVISIONS: Concentric rings with modulated weight
for r_idx in range(RINGS):
    r = 30 + (r_idx * 12)
    # Binary weight modulation: every 4th ring is structural/chunky
    is_structural = r_idx % 4 == 0
    
    if is_structural:
        ctx.set_source_rgba(*WHITE, 0.6)
        ctx.set_line_width(1.2)
    else:
        ctx.set_source_rgba(0.2, 0.3, 0.4, 0.3)
        ctx.set_line_width(0.4)
        
    ctx.new_sub_path()
    for s in range(SPOKES + 1):
        theta = (s / SPOKES) * 2 * math.pi
        px, py = polar_to_cartesian(r, theta)
        if s == 0: ctx.move_to(px, py)
        else: ctx.line_to(px, py)
    ctx.stroke()

# 3. DATA HOTSPOTS: Emergent texture through repetition
# High-density clusters near intersections
random.seed(42) # Deterministic randomness for systematic feel
for _ in range(180):
    r_step = random.randint(2, RINGS - 2)
    s_step = random.randint(0, SPOKES)
    
    r = 30 + (r_step * 12)
    theta = (s_step / SPOKES) * 2 * math.pi
    
    px, py = polar_to_cartesian(r, theta)
    
    # Logic: Closer to center = smaller, more precise artifacts
    dist_factor = r / 300
    
    if random.random() > 0.7:
        # High-key active accents
        ctx.set_source_rgb(*ACCENT_COLOR)
        draw_technical_node(px, py, 2 + (5 * dist_factor), "box")
    elif random.random() > 0.4:
        # Structural annotations
        ctx.set_source_rgba(*WHITE, 0.8)
        draw_technical_node(px, py, 3, "cross")
        
        # Binary 'data' blocks (Swiss style blocks)
        if random.random() > 0.8:
            ctx.set_source_rgba(*WHITE, 0.2)
            ctx.rectangle(px + 5, py - 2, 15 * dist_factor, 4)
            ctx.fill()

# 4. VECTOR RELATIONSHIPS: Connecting high-density nodes
ctx.set_line_width(0.7)
ctx.set_source_rgba(*SECONDARY_COLOR, 0.8)
for _ in range(8):
    # Select two random nodes and draw a 'logic path' between them
    r1, t1 = random.randint(40, 200), random.uniform(0, math.pi*2)
    r2, t2 = random.randint(40, 200), random.uniform(0, math.pi*2)
    
    p1 = polar_to_cartesian(r1, t1)
    p2 = polar_to_cartesian(r2, t2)
    
    ctx.move_to(*p1)
    # Draw a stepped path to simulate technical routing
    mid_r = (r1 + r2) / 2
    ctx.line_to(*polar_to_cartesian(mid_r, t1))
    ctx.line_to(*polar_to_cartesian(mid_r, t2))
    ctx.line_to(*p2)
    ctx.stroke()
    
    # Terminal nodes for the paths
    ctx.arc(p1[0], p1[1], 2, 0, 2*math.pi)
    ctx.fill()

# 5. PERIPHERAL ANNOTATIONS: Swiss-style framing
ctx.set_source_rgba(*WHITE, 0.4)
ctx.set_font_size(8)
for i in range(4):
    angle = i * (math.pi/2)
    tx, ty = polar_to_cartesian(280, angle)
    ctx.move_to(tx, ty)
    # Geometric markers at cardinal directions
    ctx.rectangle(tx-10, ty-1, 20, 2)
    ctx.fill()
    
# Final touch: subtle center void
ctx.set_operator(cairo.OPERATOR_DEST_OUT)
ctx.arc(CENTER_X, CENTER_Y, 25, 0, 2*math.pi)
ctx.fill()
ctx.set_operator(cairo.OPERATOR_OVER)

# Central nexus core
ctx.set_source_rgb(*ACCENT_COLOR)
ctx.set_line_width(1.0)
ctx.arc(CENTER_X, CENTER_Y, 15, 0, 2*math.pi)
ctx.stroke()
ctx.arc(CENTER_X, CENTER_Y, 2, 0, 2*math.pi)
ctx.fill()
