import cairo
import math
import random

# Setup
width, height = 600, 600 # Square format for radial symmetry
surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
ctx = cairo.Context(surface)

# Constants
CENTER_X, CENTER_Y = width / 2, height / 2
MAX_RADIUS = min(width, height) * 0.45
BG_COLOR = (0.05, 0.05, 0.05)
ACCENT_COLORS = [
    (1.0, 0.2, 0.2), # Red
    (0.0, 0.8, 1.0), # Cyan
    (1.0, 0.9, 0.0)  # Yellow
]

# Background
ctx.set_source_rgb(*BG_COLOR)
ctx.paint()

def polar_to_cartesian(r, theta):
    x = CENTER_X + r * math.cos(theta)
    y = CENTER_Y + r * math.sin(theta)
    return x, y

def draw_data_packet(r, theta, size, color):
    """Draws a 'chromatic punctuation' node at a specific coordinate."""
    ctx.save()
    x, y = polar_to_cartesian(r, theta)
    ctx.translate(x, y)
    ctx.rotate(theta) # Align with the radial axis
    ctx.set_source_rgb(*color)
    ctx.rectangle(-size/2, -size/2, size, size * 2)
    ctx.fill()
    ctx.restore()

def draw_radial_structure():
    # 1. Structural Grid: Non-linear radial rings (Logarithmic distribution)
    # This creates the 'centripetal' density towards the center.
    rings = 40
    for i in range(1, rings + 1):
        # Logarithmic spacing: denser near center
        norm = i / rings
        r = MAX_RADIUS * (math.log(1 + norm * 9) / math.log(10))
        
        # Line properties based on depth
        opacity = 0.1 + (1.0 - norm) * 0.6
        ctx.set_source_rgba(0.9, 0.9, 0.9, opacity)
        ctx.set_line_width(0.2 + (1.0 - norm) * 0.8)
        
        # Segmented arcs to create entropic fragmentation
        segments = 12
        for s in range(segments):
            start_angle = (s / segments) * 2 * math.pi
            end_angle = ((s + 0.7) / segments) * 2 * math.pi
            
            # Randomly drop segments as we move outward (entropy)
            if random.random() > (norm * 0.6):
                ctx.arc(CENTER_X, CENTER_Y, r, start_angle, end_angle)
                ctx.stroke()

    # 2. Angular Spoke System
    spokes = 64
    for i in range(spokes):
        theta = (i / spokes) * 2 * math.pi
        
        # Varying lengths using a sine-modulated stochastic function
        length_factor = 0.5 + 0.5 * math.sin(theta * 4) * random.uniform(0.7, 1.0)
        r_start = MAX_RADIUS * 0.05
        r_end = MAX_RADIUS * length_factor
        
        ctx.set_source_rgba(0.8, 0.8, 0.8, 0.2)
        ctx.set_line_width(0.3)
        
        x1, y1 = polar_to_cartesian(r_start, theta)
        x2, y2 = polar_to_cartesian(r_end, theta)
        
        ctx.move_to(x1, y1)
        ctx.line_to(x2, y2)
        ctx.stroke()
        
        # 3. Frequency Modulation: Tiny point placements along spokes
        # Denser near the center nexus
        point_count = int(15 * (1 - length_factor * 0.5))
        for p in range(point_count):
            dot_r = r_start + (r_end - r_start) * (p / point_count)**2 # Squared for density shift
            dx, dy = polar_to_cartesian(dot_r, theta)
            ctx.set_source_rgba(1, 1, 1, 0.6)
            ctx.arc(dx, dy, 0.6, 0, 2 * math.pi)
            ctx.fill()

    # 4. Chromatic Punctuation (Data Packets)
    # Placed at intersections of the logic grid
    for _ in range(24):
        # Pick random logic points
        r_idx = random.randint(5, rings-5)
        norm_r = r_idx / rings
        r_pos = MAX_RADIUS * (math.log(1 + norm_r * 9) / math.log(10))
        
        t_idx = random.randint(0, spokes)
        theta_pos = (t_idx / spokes) * 2 * math.pi
        
        color = random.choice(ACCENT_COLORS)
        packet_size = 2 + (1.0 - norm_r) * 4
        
        draw_data_packet(r_pos, theta_pos, packet_size, color)
        
        # Connect some packets with "hard" structural lines
        if random.random() > 0.7:
            ctx.set_source_rgba(*color, 0.4)
            ctx.set_line_width(0.5)
            next_r = r_pos * 1.15
            nx, ny = polar_to_cartesian(next_r, theta_pos)
            ctx.move_to(*polar_to_cartesian(r_pos, theta_pos))
            ctx.line_to(nx, ny)
            ctx.stroke()

    # 5. Central Nexus
    # The high-density gravitational core
    ctx.set_source_rgb(1, 1, 1)
    ctx.set_line_width(1.5)
    ctx.arc(CENTER_X, CENTER_Y, MAX_RADIUS * 0.02, 0, 2 * math.pi)
    ctx.stroke()
    
    # Outer "Swiss" frame elements
    ctx.set_source_rgba(1, 1, 1, 0.1)
    ctx.set_line_width(1)
    ctx.rectangle(40, 40, width-80, height-80)
    ctx.stroke()

# Execute Drawing
draw_radial_structure()

# Fine technical annotations (simulating metadata)
ctx.set_source_rgba(1, 1, 1, 0.4)
ctx.select_font_face("sans-serif", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
ctx.set_font_size(8)
ctx.move_to(45, 55)
ctx.show_text("REF_SYS: POLAR_GRID_V.08")
ctx.move_to(45, 65)
ctx.show_text("STRUCTURAL_DENSITY: 0.842")
ctx.move_to(45, height - 45)
ctx.show_text("CENTRIPETAL_FORCE_NULL")

