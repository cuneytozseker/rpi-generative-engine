import cairo
import math
import random

# Setup
width, height = 600, 480
surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
ctx = cairo.Context(surface)

# Background: Deep, monochromatic void
ctx.set_source_rgb(0.02, 0.02, 0.05)
ctx.paint()

# Configuration
center_x, center_y = width * 0.45, height * 0.55  # Asymmetric origin
num_rings = 42
num_rays = 64
phi = (1 + 5**0.5) / 2  # Golden ratio for spacing

def polar_to_cartesian(r, theta, offset_x, offset_y):
    x = offset_x + r * math.cos(theta)
    y = offset_y + r * math.sin(theta)
    return x, y

def draw_distorted_grid():
    # 1. ATMOSPHERIC KINESIS: Soft focus background layer
    # Creates a "spectral luminosity" effect through many low-opacity strokes
    for i in range(num_rings):
        r_base = (i ** 1.6) * 1.8  # Exponential expansion
        ctx.set_line_width(0.3)
        
        # Color mapping: Temperature shift from deep violet to cyan
        r_val = 0.2 + 0.3 * (i / num_rings)
        g_val = 0.1 + 0.5 * (i / num_rings)
        b_val = 0.5 + 0.5 * (i / num_rings)
        
        ctx.set_source_rgba(r_val, g_val, b_val, 0.15)
        
        ctx.new_path()
        for j in range(num_rays + 1):
            theta = (j / num_rays) * 2 * math.pi
            # Apply radial distortion based on angle and distance
            distortion = math.sin(theta * 5 + i * 0.2) * (i * 0.5)
            r = r_base + distortion
            x, y = polar_to_cartesian(r, theta, center_x, center_y)
            if j == 0:
                ctx.move_to(x, y)
            else:
                ctx.line_to(x, y)
        ctx.stroke()

    # 2. SYSTEMIC MAPPING: The Swiss-inspired rigid elements
    # Hair-line precision grid points and connectors
    for i in range(2, num_rings, 3):
        r_base = (i ** 1.6) * 1.8
        
        for j in range(num_rays):
            if random.random() > 0.7: continue # Strategic negative space
            
            theta = (j / num_rays) * 2 * math.pi
            distortion = math.sin(theta * 5 + i * 0.2) * (i * 0.5)
            r = r_base + distortion
            x, y = polar_to_cartesian(r, theta, center_x, center_y)
            
            # Draw "Relational Nodes" - small blocks aligned to the flow
            ctx.save()
            ctx.translate(x, y)
            ctx.rotate(theta + math.pi/2)
            
            # High-contrast white/cyan nodes
            ctx.set_source_rgba(0.8, 0.9, 1.0, 0.8)
            node_w = 1.5 + (i * 0.1)
            node_h = 4 + (i * 0.2)
            ctx.rectangle(-node_w/2, -node_h/2, node_w, node_h)
            ctx.fill()
            
            # Hair-line vectors connecting outward
            if i < num_rings - 3:
                ctx.restore()
                ctx.save()
                next_r = ((i+3) ** 1.6) * 1.8 + math.sin(theta * 5 + (i+3) * 0.2) * ((i+3) * 0.5)
                nx, ny = polar_to_cartesian(next_r, theta, center_x, center_y)
                ctx.set_source_rgba(1, 1, 1, 0.2)
                ctx.set_line_width(0.5)
                ctx.move_to(x, y)
                ctx.line_to(nx, ny)
                ctx.stroke()
            
            ctx.restore()

    # 3. ELASTIC RIGOR: Wavefronts
    # Bold, precise arcs that define the rhythmic field
    ctx.set_line_width(0.8)
    for i in range(5, num_rings, 8):
        r_base = (i ** 1.6) * 1.8
        
        # Draw fragmented arcs
        segments = 12
        for s in range(segments):
            start_angle = (s / segments) * 2 * math.pi
            end_angle = start_angle + (random.uniform(0.1, 0.4))
            
            ctx.set_source_rgba(1, 1, 1, 0.6)
            ctx.new_path()
            
            # Step through the arc to apply distortion to the path
            steps = 20
            for step in range(steps + 1):
                angle = start_angle + (end_angle - start_angle) * (step / steps)
                distortion = math.sin(angle * 5 + i * 0.2) * (i * 0.5)
                r = r_base + distortion
                x, y = polar_to_cartesian(r, angle, center_x, center_y)
                if step == 0:
                    ctx.move_to(x, y)
                else:
                    ctx.line_to(x, y)
            ctx.stroke()

    # 4. FOCAL ORIGIN: High density core
    # A concentrated cluster of data points at the center
    for i in range(15):
        angle = random.uniform(0, 2 * math.pi)
        dist = random.uniform(0, 20)
        x, y = polar_to_cartesian(dist, angle, center_x, center_y)
        
        ctx.set_source_rgb(1, 1, 1)
        ctx.arc(x, y, random.uniform(0.5, 2.0), 0, 2 * math.pi)
        ctx.fill()

# Execution
draw_distorted_grid()

# Subtle grain/noise overlay using tiny random rectangles
for _ in range(1000):
    ctx.set_source_rgba(1, 1, 1, 0.03)
    ctx.rectangle(random.randint(0, width), random.randint(0, height), 1, 1)
    ctx.fill()

