from pathlib import Path
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv(Path(__file__).parent / '.env')

# API Keys
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
ANTHROPIC_API_KEY = os.getenv('ANTHROPIC_API_KEY')

# Paths
ENGINE_ROOT = Path(__file__).parent.parent
PROJECT_ROOT = ENGINE_ROOT.parent
OUTPUT_DIR = ENGINE_ROOT / 'output'
GALLERY_DIR = PROJECT_ROOT / 'gallery' / 'public' / 'gallery'
TEMP_DIR = Path('/tmp/generative_studio')
TEMP_DIR.mkdir(exist_ok=True)

# Display settings
DISPLAY_WIDTH = 800
DISPLAY_HEIGHT = 480
ARTWORK_SIZE = (800, 800)  # Generated artwork size

# Generation settings
SKETCHES_PER_PERIOD = 8
GENERATION_TIMEOUT = 10  # seconds per sketch

# Schedule (4 periods per day)
PERIODS = [
    {'start': '00:00', 'end': '06:00', 'number': 1},
    {'start': '06:00', 'end': '12:00', 'number': 2},
    {'start': '12:00', 'end': '18:00', 'number': 3},
    {'start': '18:00', 'end': '00:00', 'number': 4},
]
