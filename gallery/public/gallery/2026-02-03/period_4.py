import cairo
import math
import random

# Setup
width, height = 600, 480
surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
ctx = cairo.Context(surface)

# Background - Deep charcoal for a clinical, brutalist foundation
ctx.set_source_rgb(0.02, 0.02, 0.03)
ctx.paint()

# Configuration
cx, cy = width / 2, height / 2
rings = 18
slices = 48
max_radius = min(width, height) * 0.45

def get_polar_point(r_idx, t_idx, total_rings, total_slices):
    """
    Calculates a point in polar space with radial distortion and 
    sinusoidal fanning to simulate 'structural emergence'.
    """
    # Normalized coordinates
    nr = r_idx / total_rings
    nt = t_idx / total_slices
    
    # Base radius with non-linear spacing (Golden Ratio influence)
    r = max_radius * (math.pow(nr, 1.2))
    
    # Angle with a rhythmic twist
    angle = nt * 2 * math.pi
    
    # Radial distortion: apply a wave based on angle and radius
    # This creates the 'fanning' and 'unfolding' effect
    distortion_freq = 6
    distortion_amp = 15 * nr * math.sin(nt * math.pi * 2 * 3)
    r += distortion_amp
    
    # Twist the coordinate system based on depth
    angle += math.sin(nr * math.pi) * 0.2
    
    x = cx + r * math.cos(angle)
    y = cy + r * math.sin(angle)
    return x, y

# --- Layer 1: The Atmospheric "Signal" (Soft diffusion) ---
ctx.set_line_width(0.5)
for r in range(rings):
    for s in range(slices):
        x, y = get_polar_point(r, s, rings, slices)
        
        # Color based on density/radius (Spectral shift)
        # Deep Indigo to Cyan
        alpha = (r / rings) * 0.3
        ctx.set_source_rgba(0.2, 0.4, 0.8, alpha)
        
        # Draw subtle connection to next node
        nx, ny = get_polar_point(r, (s + 1) % slices, rings, slices)
        ctx.move_to(x, y)
        ctx.line_to(nx, ny)
        ctx.stroke()

# --- Layer 2: Structural Grid (Swiss Precision) ---
# Emphasizing hierarchy through varied line weights
for s in range(0, slices, 2):
    # Determine line weight based on slice index (rhythmic intervals)
    weight = 1.2 if s % 8 == 0 else 0.4
    ctx.set_line_width(weight)
    
    # Set color: High contrast White/Grey
    intensity = 0.8 if s % 8 == 0 else 0.4
    ctx.set_source_rgba(intensity, intensity, intensity + 0.1, 0.7)
    
    ctx.move_to(*get_polar_point(1, s, rings, slices))
    for r in range(1, rings + 1):
        ctx.line_to(*get_polar_point(r, s, rings, slices))
    ctx.stroke()

# --- Layer 3: Emergent Lattices (Point-to-Point Connectivity) ---
# Connect nodes across the grid to form complex vector networks
ctx.set_line_width(0.3)
for r in range(4, rings, 3):
    for s in range(slices):
        if (s + r) % 5 == 0:
            x1, y1 = get_polar_point(r, s, rings, slices)
            # Connect to a distant neighbor in the grid
            x2, y2 = get_polar_point((r + 2) % rings, (s + 12) % slices, rings, slices)
            
            # Saturated spectral "Heat" color
            ctx.set_source_rgba(1.0, 0.2, 0.4, 0.4)
            ctx.move_to(x1, y1)
            ctx.line_to(x2, y2)
            ctx.stroke()

# --- Layer 4: Discrete Geometric Nodes (Tile Logic) ---
# Adding small precision markers at intersections
for r in range(rings):
    for s in range(slices):
        if r % 2 == 0 and s % 4 == 0:
            x, y = get_polar_point(r, s, rings, slices)
            
            # Use color as a scalar indicator of density
            radius_factor = r / rings
            ctx.set_source_rgb(0.9, 0.9, 1.0)
            
            # Draw a tiny technical "plus" sign or square
            size = 1.5 * radius_factor
            ctx.rectangle(x - size, y - size, size * 2, size * 2)
            ctx.fill()

# --- Layer 5: Peripheral "Dust" (Texture and Noise) ---
# Highlighting the negative space with mathematical jitter
for _ in range(200):
    r_rand = random.uniform(rings * 0.7, rings)
    t_rand = random.uniform(0, slices)
    x, y = get_polar_point(r_rand, t_rand, rings, slices)
    
    ctx.set_source_rgba(1, 1, 1, random.uniform(0.1, 0.5))
    ctx.arc(x + random.uniform(-2, 2), y + random.uniform(-2, 2), 0.5, 0, 2 * math.pi)
    ctx.fill()

# Border / Frame (Minimalist Swiss framing)
ctx.set_source_rgb(0.8, 0.8, 0.8)
ctx.set_line_width(1)
ctx.rectangle(20, 20, width - 40, height - 40)
ctx.stroke()

