import cairo
import math
import random

# Setup
width, height = 600, 480
surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
ctx = cairo.Context(surface)

# Background: Midnight Indigo
ctx.set_source_rgb(0.02, 0.02, 0.08)
ctx.paint()

def get_thermal_color(val, alpha=1.0):
    """Maps 0.0-1.0 to a teal-to-magenta thermal gradient."""
    # Teal: (0, 0.9, 0.9) to Magenta: (0.9, 0, 0.6)
    r = val * 0.9
    g = (1.0 - val) * 0.9
    b = 0.6 + (val * 0.3) if val > 0.5 else 0.9 - (val * 0.3)
    return (r, g, b, alpha)

def polar_to_cartesian(cx, cy, r, theta):
    return cx + r * math.cos(theta), cy + r * math.sin(theta)

# Composition Parameters
center_x, center_y = width // 2, height // 2
rings = 24
slices = 72
max_radius = 320

# 1. UNDERLAY: The "Technical" Swiss Grid (Cartesian ghost)
ctx.set_line_width(0.3)
ctx.set_source_rgba(1, 1, 1, 0.1)
grid_spacing = 40
for x in range(0, width, grid_spacing):
    ctx.move_to(x, 0)
    ctx.line_to(x, height)
    ctx.stroke()
for y in range(0, height, grid_spacing):
    ctx.move_to(0, y)
    ctx.line_to(width, y)
    ctx.stroke()

# 2. CORE SYSTEM: Polar Transformation with Radial Distortion
# We iterate through a grid but map it to polar space with a sine-wave displacement
for i in range(rings):
    r_base = (i / rings) * max_radius
    # Amplitude of distortion increases with radius
    distortion_amp = (i / rings) ** 2 * 45 
    
    for j in range(slices):
        theta_base = (j / slices) * 2 * math.pi
        
        # Mathematical Resonance: Distortion factor based on theta and radius
        # Frequency of the wave increases towards the outer edge
        freq = 6 + (i // 4)
        offset = math.sin(theta_base * freq + (i * 0.2)) * distortion_amp
        r_distorted = r_base + offset
        
        # Calculate color based on distortion intensity
        color_factor = abs(offset) / 45
        ctx.set_source_rgba(*get_thermal_color(color_factor, 0.6))
        
        # Draw fan-like rays (radial segments)
        next_r = r_distorted + 10
        x1, y1 = polar_to_cartesian(center_x, center_y, r_distorted, theta_base)
        x2, y2 = polar_to_cartesian(center_x, center_y, next_r, theta_base + 0.02)
        
        ctx.set_line_width(0.8)
        ctx.move_to(x1, y1)
        ctx.line_to(x2, y2)
        ctx.stroke()
        
        # 3. INTERACTIVE NODES: Technical Markers
        # Only draw at specific intervals to maintain Swiss hierarchy
        if i % 4 == 0 and j % 6 == 0:
            ctx.set_source_rgba(1, 1, 1, 0.8)
            node_size = 1.5
            ctx.arc(x1, y1, node_size, 0, 2 * math.pi)
            ctx.fill()
            
            # Tiny label lines (Precision indicators)
            ctx.set_line_width(0.4)
            ctx.move_to(x1, y1)
            ctx.line_to(x1 + 5, y1 - 5)
            ctx.stroke()

# 4. ATMOSPHERIC LAYER: Overlapping "Spectral" Orbits
ctx.set_operator(cairo.OPERATOR_ADD) # Additive blending for glow effect
for k in range(5):
    ctx.set_source_rgba(0.1, 0.4, 0.5, 0.05)
    orbit_r = 50 + (k * 60)
    ctx.set_line_width(12 - k * 2)
    
    # Draw fragmented, distorted arcs
    for step in range(0, 360, 15):
        angle = math.radians(step)
        drift = math.sin(angle * 3 + k) * 10
        ctx.arc(center_x, center_y, orbit_r + drift, angle, angle + 0.1)
        ctx.stroke()

# 5. SYMMETRY BREAK: Harmonic Slicing
# Vertical "razor" paths that cut through the resonance
ctx.set_operator(cairo.OPERATOR_OVER)
for m in range(3):
    slice_x = center_x - 100 + (m * 100)
    ctx.set_source_rgba(1, 1, 1, 0.15)
    ctx.set_line_width(1.5)
    ctx.move_to(slice_x, 50)
    ctx.line_to(slice_x, height - 50)
    ctx.stroke()
    
    # Add data-points along the slice
    for n in range(10):
        py = 50 + (n * 40)
        ctx.rectangle(slice_x - 2, py, 4, 1)
        ctx.fill()

# 6. BORDER/FRAME: Swiss Minimalism
ctx.set_source_rgb(1, 1, 1)
ctx.set_line_width(1)
margin = 20
ctx.rectangle(margin, margin, width - margin*2, height - margin*2)
ctx.stroke()

# Small technical "Metadata" block in corner
ctx.set_source_rgba(1, 1, 1, 0.5)
ctx.select_font_face("sans-serif", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
ctx.set_font_size(8)
ctx.move_to(margin + 10, height - margin - 15)
ctx.show_text("SYS_REF: POLAR_GRID_V.08")
ctx.move_to(margin + 10, height - margin - 5)
ctx.show_text("DISTORTION_LATENCY: 12.4ms")

# Final touch: subtle noise or grain would go here if using pixel-level tools
# but in vector Cairo, we rely on thin, high-density line clusters.

