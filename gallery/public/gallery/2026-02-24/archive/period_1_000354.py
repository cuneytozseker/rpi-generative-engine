import cairo
import math
import random

# Setup
width, height = 600, 480
surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
ctx = cairo.Context(surface)

# Background - Deep midnight/Black for high contrast
ctx.set_source_rgb(0.02, 0.02, 0.03)
ctx.paint()

# --- GENERATIVE STRATEGY: COMPUTED TOPOGRAPHY ---
# Instead of drawing continuous Voronoi cells, we sample the space 
# with discrete "Unit Replacements" (crosses and dots) to create a 
# field that feels like a digital scan or a mathematical map.

# 1. Generate Non-Linear Seed Points (Topographic Density)
num_seeds = 32
seeds = []
# Create clusters using a modified golden spiral to ensure non-uniformity
for i in range(num_seeds):
    angle = i * math.pi * (3 - math.sqrt(5))  # Golden angle
    radius = math.sqrt(i / num_seeds) * (min(width, height) * 0.45)
    # Add a bit of jitter to break the perfect spiral
    off_x = (random.random() - 0.5) * 80
    off_y = (random.random() - 0.5) * 80
    px = width / 2 + math.cos(angle) * radius + off_x
    py = height / 2 + math.sin(angle) * radius + off_y
    # Assign a jewel-tone accent color to some seeds
    color = (random.uniform(0.1, 0.3), random.uniform(0.6, 0.9), random.uniform(0.7, 1.0)) # Cyan/Jewel range
    seeds.append({'pos': (px, py), 'color': color, 'id': i})

# 2. Sample Grid for "Discrete Unit Replacement"
grid_size = 8
for x in range(0, width, grid_size):
    for y in range(0, height, grid_size):
        # Find the two closest seeds (to calculate Voronoi boundaries)
        dists = []
        for s in seeds:
            d = math.sqrt((x - s['pos'][0])**2 + (y - s['pos'][1])**2)
            dists.append((d, s))
        
        dists.sort(key=lambda x: x[0])
        d1, s1 = dists[0] # Closest
        d2, s2 = dists[1] # Second closest
        
        # Proximity to cell boundary (0.0 at center, 1.0 at edge)
        edge_proximity = d1 / (d2 + 0.001)
        
        # Aesthetic Logic: Functional Chromaticism
        # We use high contrast (white/grey) for the structure, 
        # and jewel tones for the "active" nodes.
        if edge_proximity > 0.92:
            # Near boundary: Draw small binary grain (dots)
            ctx.set_source_rgba(0.8, 0.8, 0.8, 0.4)
            ctx.arc(x, y, 0.8, 0, math.pi * 2)
            ctx.fill()
        else:
            # Inside cell: Draw symbols with varying density
            # Symbol size based on distance to seed
            size = (1.0 - (d1 / 300.0)) * 2.5
            size = max(0.5, size)
            
            # Use seed-specific logic for "visual rhythm"
            if s1['id'] % 3 == 0:
                # Type A: Small Crosses
                ctx.set_source_rgba(0.4, 0.4, 0.45, 0.6)
                ctx.set_line_width(0.5)
                ctx.move_to(x - size, y)
                ctx.line_to(x + size, y)
                ctx.move_to(x, y - size)
                ctx.line_to(x, y + size)
                ctx.stroke()
            elif s1['id'] % 3 == 1:
                # Type B: Vertical ticks
                ctx.set_source_rgba(0.6, 0.6, 0.7, 0.5)
                ctx.set_line_width(0.7)
                ctx.move_to(x, y - size)
                ctx.line_to(x, y + size)
                ctx.stroke()
            else:
                # Type C: Micro-circles
                ctx.set_source_rgba(0.3, 0.3, 0.35, 0.4)
                ctx.arc(x, y, size * 0.5, 0, math.pi * 2)
                ctx.stroke()

# 3. Layer: Interstitial Connections (Topographic Lines)
# Draw faint lines connecting seeds to suggest a hidden network
ctx.set_line_width(0.3)
for i in range(len(seeds)):
    s1 = seeds[i]
    for j in range(i + 1, len(seeds)):
        s2 = seeds[j]
        dist = math.sqrt((s1['pos'][0]-s2['pos'][0])**2 + (s1['pos'][1]-s2['pos'][1])**2)
        if dist < 120:
            ctx.set_source_rgba(1, 1, 1, (1.0 - dist/120.0) * 0.2)
            ctx.move_to(s1['pos'][0], s1['pos'][1])
            ctx.line_to(s2['pos'][0], s2['pos'][1])
            ctx.stroke()

# 4. Layer: Data Markers (Seed Points)
# High-contrast "terminal points" at seed locations
for s in seeds:
    px, py = s['pos']
    
    # Outer Glow / Data Circle
    ctx.set_source_rgba(s['color'][0], s['color'][1], s['color'][2], 0.15)
    ctx.arc(px, py, 12, 0, math.pi * 2)
    ctx.fill()
    
    # Inner Precision Point
    ctx.set_source_rgb(s['color'][0], s['color'][1], s['color'][2])
    ctx.arc(px, py, 1.5, 0, math.pi * 2)
    ctx.fill()
    
    # Technical marking (Swiss style)
    ctx.set_source_rgba(1, 1, 1, 0.6)
    ctx.set_line_width(0.5)
    length = 6
    ctx.move_to(px - length, py - length)
    ctx.line_to(px - length + 2, py - length)
    ctx.move_to(px - length, py - length)
    ctx.line_to(px - length, py - length + 2)
    ctx.stroke()

# 5. Global Texture Overly (Digital Grain)
# Adds a subtle scanline effect to reinforce the brutalist/technical feel
ctx.set_source_rgba(1, 1, 1, 0.03)
ctx.set_line_width(1)
for i in range(0, height, 4):
    ctx.move_to(0, i)
    ctx.line_to(width, i)
    ctx.stroke()

# Final Hierarchy: A border to ground the composition (Swiss grid style)
ctx.set_source_rgb(1, 1, 1)
ctx.set_line_width(1)
margin = 20
ctx.rectangle(margin, margin, width - margin*2, height - margin*2)
ctx.stroke()

