import cairo
import math
import random

# Setup
width, height = 600, 480
surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
ctx = cairo.Context(surface)

# Background: Deep Swiss Black
ctx.set_source_rgb(0.05, 0.05, 0.05)
ctx.paint()

# Configuration
center_x, center_y = width / 2, height / 2
rings = 42
segments = 72
inner_radius = 40
outer_radius = 320
phi = (1 + 5**0.5) / 2  # Golden ratio for harmonic spacing

def polar_to_cartesian(r, theta):
    return center_x + r * math.cos(theta), center_y + r * math.sin(theta)

def draw_fragment(r, theta, dr, dt, weight, color_type):
    """Draws a quantized rectangular primitive in polar space."""
    # Radial distortion: apply a quantized drift based on angle and radius
    distortion = math.sin(theta * 4 + r * 0.01) * 10
    r_distorted = r + distortion
    
    # Calculate four corners of the polar "rectangle"
    p1 = polar_to_cartesian(r_distorted, theta)
    p2 = polar_to_cartesian(r_distorted + dr, theta)
    p3 = polar_to_cartesian(r_distorted + dr, theta + dt)
    p4 = polar_to_cartesian(r_distorted, theta + dt)
    
    # Systematic Color Palette (High contrast staccato)
    if color_type < 0.05: # Rare accent
        ctx.set_source_rgb(0.9, 0.1, 0.1) # Swiss Red
    elif color_type < 0.4:
        ctx.set_source_rgb(0.95, 0.95, 0.95) # High-key White
    else:
        ctx.set_source_rgb(0.4, 0.4, 0.4) # Neutral Gray
        
    ctx.set_line_width(weight)
    
    # Draw the cell
    ctx.move_to(*p1)
    ctx.line_to(*p2)
    ctx.line_to(*p3)
    ctx.line_to(*p4)
    ctx.close_path()
    
    # Randomly decide between fill (solid) and stroke (wireframe/dithered)
    if random.random() > 0.7:
        ctx.stroke()
    else:
        ctx.fill()

# Main Generative Loop
for i in range(rings):
    # Logarithmic radial spacing for perspective depth
    r = inner_radius + (outer_radius - inner_radius) * (i / rings)**1.5
    dr = (outer_radius / rings) * (i / rings + 0.5)
    
    # Modulate segment count based on radius to maintain density (Visual Grayscale)
    current_segments = int(segments * (i / rings + 0.5))
    dt = (2 * math.pi) / current_segments
    
    for j in range(current_segments):
        theta = j * dt
        
        # Determine presence based on a mathematical field (interference pattern)
        # This creates the "calculated dissolution"
        logic_gate = math.sin(i * 0.2) * math.cos(j * 0.1) + (random.random() * 0.4)
        
        if logic_gate > -0.2:
            # Recursive subdivision logic: break some cells into 4 smaller ones
            if logic_gate > 0.6 and i % 3 == 0:
                # Small cluster (Granular density modulation)
                sub_dr = dr / 2
                sub_dt = dt / 2
                for sr in [0, 1]:
                    for st in [0, 1]:
                        draw_fragment(
                            r + sr * sub_dr, 
                            theta + st * sub_dt, 
                            sub_dr * 0.8, 
                            sub_dt * 0.8, 
                            0.5, 
                            random.random()
                        )
            else:
                # Standard cell
                # Stroke weight increases with radius to balance visual mass
                stroke_w = 0.2 + (i / rings) * 1.5
                
                # Jitter: Digital rigidity vs Organic entropy
                jitter_theta = theta + (random.uniform(-0.02, 0.02) * (i / rings))
                
                draw_fragment(r, jitter_theta, dr * 0.7, dt * 0.7, stroke_w, random.random())

# Overlay: Fine-line technical grid (Swiss precision)
ctx.set_source_rgba(1, 1, 1, 0.1)
ctx.set_line_width(0.3)
for r_line in [inner_radius, outer_radius, (inner_radius + outer_radius)/2]:
    ctx.arc(center_x, center_y, r_line, 0, 2 * math.pi)
    ctx.stroke()

# Final systemic accent: A single "glitch" axis
ctx.set_source_rgb(0.9, 0.1, 0.1)
ctx.set_line_width(1.0)
angle_accent = math.pi * 1.25
ctx.move_to(*polar_to_cartesian(inner_radius - 20, angle_accent))
ctx.line_to(*polar_to_cartesian(outer_radius + 40, angle_accent))
ctx.stroke()

# Add a small block of "metadata" (Typography-like element)
ctx.rectangle(20, height - 40, 30, 20)
ctx.fill()
ctx.set_source_rgb(1, 1, 1)
ctx.move_to(60, height - 25)
ctx.set_font_size(10)
ctx.select_font_face("sans-serif", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
ctx.show_text("SYSTEM_FRAG_V.01 // 600x480")

