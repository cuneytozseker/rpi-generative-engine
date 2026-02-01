import cairo
import math
import random

# Setup
width, height = 600, 480
surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
ctx = cairo.Context(surface)

# Background: Deep Charcoal for a brutalist foundation
ctx.set_source_rgb(0.02, 0.02, 0.03)
ctx.paint()

# Configuration
cx, cy = width // 2, height // 2
num_rings = 42
num_spokes = 80
max_radius = min(width, height) * 0.8
golden_ratio = (1 + 5**0.5) / 2

def polar_to_cartesian(r, theta, distortion_factor=0.0):
    """Transforms polar coordinates with a radial harmonic distortion."""
    # Harmonic distortion based on angle and radius
    harmonic = math.sin(theta * 6) * math.cos(r * 0.02) * distortion_factor
    r_distorted = r + harmonic
    
    x = cx + r_distorted * math.cos(theta)
    y = cy + r_distorted * math.sin(theta)
    return x, y

# 1. LAYER: Ethereal Spectral Aura (Background Noise)
# Large, faint arcs following the vector field
ctx.set_line_width(0.5)
for i in range(15):
    r_base = random.uniform(50, max_radius)
    ctx.set_source_rgba(0.2, 0.4, 0.6, 0.05)
    ctx.arc(cx, cy, r_base, 0, 2 * math.pi)
    ctx.stroke()

# 2. LAYER: The Harmonic Grid (Swiss Precision)
# Drawing the radial grid with increasing "entropy" as it moves outward
for i in range(1, num_rings):
    r = (i / num_rings) * max_radius
    entropy = (i / num_rings) ** 2  # Entropy increases non-linearly
    
    # Ring Segmenting
    for j in range(num_spokes):
        theta1 = (j / num_spokes) * 2 * math.pi
        theta2 = ((j + 1) / num_spokes) * 2 * math.pi
        
        # Calculate distorted positions
        x1, y1 = polar_to_cartesian(r, theta1, distortion_factor=20 * entropy)
        x2, y2 = polar_to_cartesian(r, theta2, distortion_factor=20 * entropy)
        
        # Visual Hierarchy: Varying line weight and color based on radius
        alpha = 0.7 - (entropy * 0.5)
        if i % 5 == 0:
            ctx.set_source_rgba(0.9, 0.9, 0.9, alpha) # Bright primary rings
            ctx.set_line_width(0.8)
        else:
            ctx.set_source_rgba(0.5, 0.5, 0.6, alpha * 0.5) # Subtle secondary rings
            ctx.set_line_width(0.3)
            
        ctx.move_to(x1, y1)
        ctx.line_to(x2, y2)
        ctx.stroke()

# 3. LAYER: Data-Driven Surges (Ribbons)
# Continuous paths that follow the "flow" of the harmonic entropy
for _ in range(12):
    ctx.set_source_rgba(1.0, 0.3, 0.1, 0.15) # Heat-mapped accent (Vibrant Orange)
    ctx.set_line_width(1.2)
    
    current_r = random.uniform(20, 100)
    current_theta = random.uniform(0, 2 * math.pi)
    
    ctx.move_to(*polar_to_cartesian(current_r, current_theta))
    
    for _ in range(50):
        current_r += 6
        current_theta += 0.1 * math.sin(current_r * 0.05)
        nx, ny = polar_to_cartesian(current_r, current_theta, distortion_factor=30)
        ctx.line_to(nx, ny)
        
    ctx.stroke()

# 4. LAYER: Mathematical Glyphs (Topographical Anchors)
# Small geometric symbols at specific intersections to ground the composition
for i in range(5, num_rings, 4):
    for j in range(0, num_spokes, 8):
        r = (i / num_rings) * max_radius
        theta = (j / num_spokes) * 2 * math.pi
        
        x, y = polar_to_cartesian(r, theta, distortion_factor=20 * (i/num_rings))
        
        # Draw a small "glyph" (Swiss-style cross or square)
        size = 2.5 * (1 - (i/num_rings)) # Get smaller as they move out
        
        ctx.set_source_rgba(1, 1, 1, 0.9)
        ctx.set_line_width(0.7)
        
        # Cross glyph
        ctx.move_to(x - size, y)
        ctx.line_to(x + size, y)
        ctx.move_to(x, y - size)
        ctx.line_to(x, y + size)
        ctx.stroke()

# 5. LAYER: Stippling & Texture (The Decay)
# Adding "dust" to represent the dissolution of the grid
for _ in range(800):
    r = random.uniform(0, max_radius)
    theta = random.uniform(0, 2 * math.pi)
    # Concentration of particles increases with radius
    if random.random() < (r / max_radius):
        x, y = polar_to_cartesian(r, theta, distortion_factor=40)
        
        # Earthy mid-tone neutral
        ctx.set_source_rgba(0.7, 0.6, 0.5, random.uniform(0.1, 0.4))
        ctx.arc(x, y, random.uniform(0.2, 0.8), 0, 2 * math.pi)
        ctx.fill()

# Final focal highlight (The "Core")
ctx.set_source_rgba(1, 1, 1, 0.05)
for i in range(10):
    ctx.arc(cx, cy, 5 + i * 4, 0, 2 * math.pi)
    ctx.fill()

