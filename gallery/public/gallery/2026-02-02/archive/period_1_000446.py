import cairo
import math
import random

# Setup
width, height = 600, 480
surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
ctx = cairo.Context(surface)

# Background - Deep Matte Black
ctx.set_source_rgb(0.02, 0.02, 0.02)
ctx.paint()

# Configuration
center_x, center_y = width / 2, height / 2
rings = 40
segments = 72
max_radius = min(width, height) * 0.8
swiss_red = (0.89, 0.12, 0.09)
swiss_blue = (0.0, 0.47, 0.75)

def polar_to_cartesian(r, theta, distortion_factor):
    # Non-linear radial distortion: warp the radius based on angle and distance
    # Creates a "pinched" and "swirled" effect typical of gravitational lens or vector fields
    r_distorted = r + (math.sin(theta * 5 + r * 0.02) * distortion_factor)
    theta_distorted = theta + (math.cos(r * 0.05) * 0.1)
    
    x = center_x + r_distorted * math.cos(theta_distorted)
    y = center_y + r_distorted * math.sin(theta_distorted)
    return x, y

# 1. DRAW UNDERLYING DISTORTED RADIATING GRID
ctx.set_line_width(0.3)
for i in range(rings):
    # Logarithmic spacing for the rings to evoke depth
    r = math.pow(i / rings, 1.2) * max_radius
    
    # Change opacity and color based on radius
    alpha = 0.1 + (i / rings) * 0.4
    ctx.set_source_rgba(0.8, 0.8, 0.8, alpha)
    
    ctx.new_path()
    for j in range(segments + 1):
        theta = (j / segments) * 2 * math.pi
        # Distortion intensity increases toward the edges (entropy vs order)
        dist_amt = (i / rings) * 25 
        px, py = polar_to_cartesian(r, theta, dist_amt)
        
        if j == 0:
            ctx.move_to(px, py)
        else:
            ctx.line_to(px, py)
    ctx.stroke()

# 2. RADIAL "STACCATO" RAYS
# Simulating a mechanical data-plot with interrupted lines
for j in range(0, segments, 2):
    theta = (j / segments) * 2 * math.pi
    ctx.set_line_width(0.5 if j % 4 == 0 else 0.2)
    
    # Stochastic density: some lines are longer, some are dashed
    r_start = 20
    r_end = max_radius * (0.6 + random.random() * 0.4)
    
    curr_r = r_start
    while curr_r < r_end:
        step = random.uniform(5, 20)
        gap = random.uniform(2, 10)
        
        # Calculate distorted segment
        x1, y1 = polar_to_cartesian(curr_r, theta, (curr_r/max_radius) * 15)
        x2, y2 = polar_to_cartesian(curr_r + step, theta, ((curr_r+step)/max_radius) * 15)
        
        # Color logic: high-chroma accents on specific structural rays
        if j % 18 == 0:
            ctx.set_source_rgba(*swiss_red, 0.8)
        elif j % 12 == 0:
            ctx.set_source_rgba(*swiss_blue, 0.6)
        else:
            ctx.set_source_rgba(0.9, 0.9, 0.9, 0.3)
            
        ctx.move_to(x1, y1)
        ctx.line_to(x2, y2)
        ctx.stroke()
        
        curr_r += step + gap

# 3. RECURSIVE SUBDIVISION GLYPHS
# Placing "Swiss" geometric symbols at calculated intersections
for i in range(4, rings, 4):
    r = math.pow(i / rings, 1.2) * max_radius
    for j in range(0, segments, 6):
        theta = (j / segments) * 2 * math.pi
        dist_amt = (i / rings) * 20
        px, py = polar_to_cartesian(r, theta, dist_amt)
        
        # Hierarchical shapes based on position
        ctx.save()
        ctx.translate(px, py)
        ctx.rotate(theta + (i * 0.1)) # Align with the radial flow
        
        size = 2 + (i / rings) * 6
        
        if (i + j) % 12 == 0:
            # Swiss Cross / Plus sign
            ctx.set_source_rgb(*swiss_red)
            ctx.set_line_width(1.5)
            ctx.move_to(-size, 0); ctx.line_to(size, 0)
            ctx.move_to(0, -size); ctx.line_to(0, size)
            ctx.stroke()
        elif (i + j) % 8 == 0:
            # Small structural square
            ctx.set_source_rgb(1, 1, 1)
            ctx.rectangle(-size/2, -size/2, size, size)
            ctx.fill()
        else:
            # Tiny data point
            ctx.set_source_rgba(1, 1, 1, 0.5)
            ctx.arc(0, 0, 1, 0, 2 * math.pi)
            ctx.fill()
            
        ctx.restore()

# 4. OVERLAY VIGNETTE / ATMOSPHERIC GRADIENT
# Subtle radial gradient to focus the eye on the center transition
pattern = cairo.RadialGradient(center_x, center_y, 50, center_x, center_y, max_radius)
pattern.add_color_stop_rgba(0, 1, 1, 1, 0.05)
pattern.add_color_stop_rgba(0.8, 0, 0, 0, 0.0)
pattern.add_color_stop_rgba(1, 0, 0, 0, 0.4)

ctx.set_source(pattern)
ctx.rectangle(0, 0, width, height)
ctx.fill()

# 5. TECHNICAL MARGIN LINES
# Framing the composition with rigid orthogonal elements
ctx.set_source_rgba(1, 1, 1, 0.2)
ctx.set_line_width(0.5)
margin = 30
ctx.move_to(margin, margin)
ctx.line_to(width - margin, margin)
ctx.line_to(width - margin, height - margin)
ctx.line_to(margin, height - margin)
ctx.close_path()
ctx.stroke()

# Final micro-accents
for _ in range(10):
    ctx.set_source_rgba(1, 1, 1, 0.15)
    rx = random.randint(margin, width-margin)
    ry = random.randint(margin, height-margin)
    ctx.arc(rx, ry, 0.5, 0, 2*math.pi)
    ctx.fill()

