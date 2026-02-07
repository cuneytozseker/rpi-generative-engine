import cairo
import math
import random

# Setup: 600x480 canvas for a wide, cinematic Swiss layout
width, height = 600, 480
surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
ctx = cairo.Context(surface)

# Background: Deep Void
ctx.set_source_rgb(0.02, 0.02, 0.03)
ctx.paint()

def draw_technical_grid(ctx, w, h, step):
    """Adds a precise underlying orthographic grid for Swiss structural feel."""
    ctx.set_line_width(0.3)
    ctx.set_source_rgba(0.4, 0.4, 0.5, 0.5)
    
    # Vertical lines
    for x in range(0, w + 1, step):
        ctx.move_to(x, 0)
        ctx.line_to(x, h)
        ctx.stroke()
        
    # Horizontal lines
    for y in range(0, h + 1, step):
        ctx.move_to(0, y)
        ctx.line_to(w, y)
        ctx.stroke()
        
    # Subtle central markers
    ctx.set_line_width(1.0)
    ctx.move_to(w/2, 0)
    ctx.line_to(w/2, h)
    ctx.move_to(0, h/2)
    ctx.line_to(w, h/2)
    ctx.stroke()

def reaction_diffusion_approximation(ctx, w, h):
    """
    Simulates the aesthetic of reaction-diffusion patterns using 
    mathematical flow fields and XOR-based geometric interference.
    """
    # Use EXCLUSION operator to create the stark black/white inversion 
    # characteristic of complex mathematical intersections.
    ctx.set_operator(cairo.OPERATOR_EXCLUSION)
    
    # We create a series of 'growth' nodes
    num_paths = 45
    for i in range(num_paths):
        # Axial balance: paths often originate from a central vertical spine
        x = w/2 + (random.uniform(-50, 50))
        y = random.uniform(0, h)
        
        ctx.set_source_rgb(0.95, 0.95, 0.98)
        
        angle = random.uniform(0, math.pi * 2)
        ctx.move_to(x, y)
        
        # Progressive expansion: path length increases based on proximity to center
        steps = random.randint(40, 120)
        current_x, current_y = x, y
        
        ctx.new_path()
        ctx.move_to(current_x, current_y)
        
        for s in range(steps):
            # Stochastic flow field logic:
            # The direction is influenced by a sine-cosine field (Structured Flux)
            noise_val = math.sin(current_x * 0.01) + math.cos(current_y * 0.01)
            angle += (noise_val * 0.2) + random.uniform(-0.1, 0.1)
            
            # Step size varies to create visual rhythm
            dist = 4 + math.sin(s * 0.1) * 2
            current_x += math.cos(angle) * dist
            current_y += math.sin(angle) * dist
            
            # Wrap around boundaries
            current_x %= w
            current_y %= h
            
            # Vary line width for atmospheric depth (Precision vs Diffusion)
            width_mod = (math.sin(s * 0.05) + 1.2) * 2.5
            ctx.set_line_width(width_mod)
            
            # Draw segment
            ctx.line_to(current_x, current_y)
            
            # Periodically 'react' by placing a circle that creates the 'spot' pattern
            if s % 15 == 0:
                radius = random.uniform(5, 15)
                ctx.arc(current_x, current_y, radius, 0, math.pi * 2)
                ctx.fill()
                ctx.move_to(current_x, current_y)

        ctx.stroke()

def add_systematic_elements(ctx, w, h):
    """Adds minimalist Swiss design annotations and highlights."""
    ctx.set_operator(cairo.OPERATOR_OVER)
    
    # Add vibrant teal accents (Chromatic Intensity)
    ctx.set_source_rgb(0.0, 0.9, 0.8)
    for _ in range(12):
        rx = random.randint(50, w-50)
        ry = random.randint(50, h-50)
        ctx.arc(rx, ry, 1.5, 0, math.pi * 2)
        ctx.fill()
        
    # High-contrast 'measurements'
    ctx.set_source_rgb(1, 1, 1)
    ctx.set_line_width(0.5)
    margin = 40
    
    # Top-left hierarchy element
    ctx.move_to(margin, margin)
    ctx.line_to(margin + 60, margin)
    ctx.move_to(margin, margin)
    ctx.line_to(margin, margin + 60)
    ctx.stroke()
    
    # Bottom-right data-strip logic
    for i in range(5):
        h_bar = 2 + (i * 2)
        ctx.rectangle(w - margin - 20, h - margin - (i * 10), 20, 1)
        ctx.fill()

# Execution
draw_technical_grid(ctx, width, height, 40)
reaction_diffusion_approximation(ctx, width, height)
add_systematic_elements(ctx, width, height)

# Overlay a subtle gradient to simulate "Atmospheric Diffusion"
lg = cairo.LinearGradient(0, 0, width, height)
lg.add_color_stop_rgba(0, 1, 1, 1, 0.05)
lg.add_color_stop_rgba(0.5, 0, 0, 0, 0)
lg.add_color_stop_rgba(1, 1, 1, 1, 0.05)
ctx.set_operator(cairo.OPERATOR_OVER)
ctx.set_source(lg)
ctx.paint()

# Final hairline frame
ctx.set_source_rgb(1, 1, 1)
ctx.set_line_width(1.0)
ctx.rectangle(20, 20, width-40, height-40)
ctx.stroke()
