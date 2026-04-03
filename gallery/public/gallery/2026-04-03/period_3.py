import cairo
import math
import random

# Setup
width, height = 600, 480
surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
ctx = cairo.Context(surface)

# Color Palette: Synthetic Entropy (Deep Charcoal, Slate, Ochre, Bone)
COLOR_BG = (0.05, 0.05, 0.07)
COLOR_GRID = (0.2, 0.2, 0.25, 0.3)
COLOR_FLOW = (0.9, 0.9, 0.95, 0.15)
COLOR_ACCENT = (0.85, 0.5, 0.2, 0.8) # Ochre
COLOR_MUTE = (0.4, 0.45, 0.5, 0.6)   # Slate

# Background
ctx.set_source_rgb(*COLOR_BG)
ctx.paint()

# Deterministic "Flow" function to simulate vector field
def get_angle(x, y, seed):
    scale = 0.003
    v1 = math.sin(x * scale + seed) * math.cos(y * scale - seed)
    v2 = math.sin((x + y) * scale * 1.5 + seed) * 0.5
    return (v1 + v2) * math.pi * 2

# Recursive Grid Subdivision
rects = []
def subdivide(x, y, w, h, depth):
    if depth > 0 and (w * h > 5000 or random.random() > 0.4):
        if w > h:
            split = w * random.uniform(0.3, 0.7)
            subdivide(x, y, split, h, depth - 1)
            subdivide(x + split, y, w - split, h, depth - 1)
        else:
            split = h * random.uniform(0.3, 0.7)
            subdivide(x, y, w, split, depth - 1)
            subdivide(x, y + split, w, h - split, depth - 1)
    else:
        rects.append((x, y, w, h))

subdivide(20, 20, width - 40, height - 40, 5)

# 1. Draw "Blueprint" Skeleton
ctx.set_line_width(0.5)
for x, y, w, h in rects:
    ctx.set_source_rgba(*COLOR_GRID)
    ctx.rectangle(x, y, w, h)
    ctx.stroke()
    
    # Metadata: Small corners/markers
    if w > 40:
        ctx.set_source_rgba(*COLOR_MUTE)
        marker_size = 3
        ctx.move_to(x, y + marker_size); ctx.line_to(x, y); ctx.line_to(x + marker_size, y)
        ctx.stroke()

# 2. Particle Flow Fields (The Entropy)
# We only spawn particles in specific high-density zones to create asymmetry
active_zones = random.sample(rects, len(rects) // 3)

for zone in active_zones:
    zx, zy, zw, zh = zone
    # Number of particles based on zone size
    num_particles = int(zw * zh / 100)
    
    for _ in range(num_particles):
        px = zx + random.random() * zw
        py = zy + random.random() * zh
        
        ctx.set_source_rgba(*COLOR_FLOW)
        ctx.set_line_width(0.4)
        ctx.move_to(px, py)
        
        # Trace path
        steps = random.randint(20, 60)
        for _ in range(steps):
            angle = get_angle(px, py, 42)
            step_size = 4
            
            # Entropy: slight variation in step
            px += math.cos(angle) * step_size
            py += math.sin(angle) * step_size
            
            # Constraint: Keep lines somewhat bound to local logic
            # Quantize movement occasionally
            if random.random() > 0.98:
                px = round(px / 10) * 10
                py = round(py / 10) * 10
                
            ctx.line_to(px, py)
            
            if not (0 <= px <= width and 0 <= py <= height):
                break
        ctx.stroke()

# 3. Structural Anchors (Dithered Blocks & Nodes)
for _ in range(12):
    r = random.choice(rects)
    x, y, w, h = r
    
    # Accent Blocks
    if random.random() > 0.7:
        ctx.set_source_rgba(*COLOR_ACCENT)
        block_w = min(w, 15)
        ctx.rectangle(x, y, block_w, 2)
        ctx.fill()
        
    # Floating Nodes
    ctx.set_source_rgba(*COLOR_MUTE)
    nx, ny = x + random.random() * w, y + random.random() * h
    ctx.arc(nx, ny, 1.5, 0, math.pi * 2)
    ctx.fill()
    
    # Connecting "Technical" lines
    if random.random() > 0.5:
        ctx.set_line_width(0.3)
        ctx.move_to(nx, ny)
        ctx.line_to(nx + random.uniform(-50, 50), ny)
        ctx.stroke()

# 4. Final Polish: Digital "Grain" or Metadata
ctx.select_font_face("Monospace", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
ctx.set_font_size(6)
for i in range(5):
    tx, ty = random.randint(50, width-50), random.randint(50, height-50)
    ctx.set_source_rgba(1, 1, 1, 0.4)
    ctx.move_to(tx, ty)
    ctx.show_text(f"SYS_ENTROPY_0{i} // {hex(random.randint(0, 255))}")

# Border to frame the "workspace"
ctx.set_source_rgba(1, 1, 1, 0.1)
ctx.set_line_width(1)
ctx.rectangle(10, 10, width-20, height-20)
ctx.stroke()

# Clean up context (surface handled externally)
