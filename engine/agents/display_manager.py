from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
import subprocess
from config.settings import DISPLAY_WIDTH, DISPLAY_HEIGHT

class DisplayManager:
    def __init__(self):
        self.width = DISPLAY_WIDTH
        self.height = DISPLAY_HEIGHT
        self.display_image = Path('/tmp/current_display.png')

    def show_artwork(self, image: Path, title: str, period: str, metadata: dict = None):
        """Display artwork on TFT with info panel"""

        # Load artwork
        artwork = Image.open(image)

        # Create display buffer
        display = Image.new('RGB', (self.width, self.height), (20, 20, 20))

        # Paste artwork to left side (it is now 600x480 natively)
        display.paste(artwork, (0, 0))

        # Draw info panel on right side (200px wide)
        self._draw_info_panel(display, title, period, metadata)

        # Save
        display.save(self.display_image)

        # Update physical display using feh
        self._update_display()

    def _draw_info_panel(self, display: Image, title: str, period: str, metadata: dict):
        """Draw metadata on right panel"""
        draw = ImageDraw.Draw(display)

        # Load fonts
        try:
            title_font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 18)   
            body_font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 14)
            small_font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 12)        
        except:
            title_font = body_font = small_font = ImageFont.load_default()

        # Dark panel background
        draw.rectangle([600, 0, 800, 480], fill=(30, 30, 30))

        x, y = 615, 20

        # Header
        draw.text((x, y), "SELECTED", font=small_font, fill=(150, 150, 150))
        y += 25

        # Period
        draw.text((x, y), period, font=title_font, fill=(255, 255, 255))
        y += 35

        # Title (wrapped)
        for line in self._wrap_text(title, body_font, 170):
            draw.text((x, y), line, font=body_font, fill=(200, 200, 200))
            y += 22

        y += 20

        # Metadata
        if metadata:
            if 'score' in metadata:
                draw.text((x, y), f"Score: {metadata['score']}/10", font=small_font, fill=(150, 150, 150))
                y += 20

            if 'reasoning' in metadata:
                draw.text((x, y), "Why:", font=small_font, fill=(150, 150, 150))
                y += 18
                for line in self._wrap_text(metadata['reasoning'], small_font, 170)[:6]:
                    draw.text((x, y), line, font=small_font, fill=(180, 180, 180))
                    y += 16

        # Timestamp
        from datetime import datetime
        draw.text((x, 450), datetime.now().strftime("%H:%M"), font=small_font, fill=(100, 100, 100))      

    def _wrap_text(self, text: str, font, max_width: int) -> list[str]:
        """Wrap text to fit width"""
        words = text.split()
        lines = []
        current = []

        for word in words:
            # Handle potential None from getbbox or older PIL versions
            bbox = font.getbbox( ' '.join(current + [word]))
            w = bbox[2] - bbox[0]
            if w <= max_width:
                current.append(word)
            else:
                if current:
                    lines.append(' '.join(current))
                current = [word]

        if current:
            lines.append(' '.join(current))

        return lines

    def _update_display(self):
        """Update the persistent display service"""
        # We just need to restart the service so it picks up the new /tmp/current_display.png
        subprocess.run(["sudo systemctl restart art-display.service"], shell=True)