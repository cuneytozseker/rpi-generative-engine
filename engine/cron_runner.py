#!/usr/bin/env python3
import asyncio
from datetime import datetime
from pathlib import Path
import sys

# Add engine directory to path
sys.path.insert(0, str(Path(__file__).parent))

from agents.generator import GeneratorAgent
from agents.curator import CuratorAgent
from agents.executor import SafeExecutor
from agents.display_manager import DisplayManager
from upload import GalleryUploader
from config.settings import OUTPUT_DIR, SKETCHES_PER_PERIOD

async def run_period():
    """Execute one generation period"""
    
    timestamp = datetime.now()
    period_num = (timestamp.hour // 6) + 1
    
    # Setup output directory
    output_dir = OUTPUT_DIR / str(timestamp.date()) / f"period_{period_num}"
    output_dir.mkdir(parents=True, exist_ok=True)
    
    print(f"{ '='*60}")
    print(f"🎨 Starting Period {period_num} - {timestamp.strftime('%Y-%m-%d %H:%M')}")
    print(f"{ '='*60}\n")
    
    # 1. Generate sketches
    print(f"Generating {SKETCHES_PER_PERIOD} sketches...")
    generator = GeneratorAgent()
    sketches = await generator.generate_batch(SKETCHES_PER_PERIOD)
    print(f"✓ Generated {len(sketches)} sketches\n")
    
    # 2. Execute and render
    print("Rendering sketches...")
    executor = SafeExecutor()
    rendered = []
    
    for sketch in sketches:
        output_path = output_dir / f"{sketch['id']}.png"
        success, msg = executor.execute(sketch['code'], output_path)
        
        if success:
            print(f"  ✓ {sketch['id']}")
            rendered.append({
                **sketch,
                'image': output_path
            })
            
            # Save source code
            (output_dir / f"{sketch['id']}.py").write_text(sketch['code'])
        else:
            print(f"  ✗ {sketch['id']}: {msg}")
    
    print(f"\n✓ Successfully rendered {len(rendered)}/{len(sketches)} sketches\n")
    
    if not rendered:
        print("❌ No sketches rendered successfully. Exiting.")
        return
    
    # 3. Curate best
    print("Evaluating with Claude Sonnet...")
    curator = CuratorAgent()
    best = await curator.select_best(rendered)
    print(f"\n✨ Selected: {best['id']}")
    print(f"   Theme: {best['theme']}")
    print(f"   Score: {best.get('score', 'N/A')}/10\n")
    
    # 4. Update display
    print("Updating TFT display...")
    display = DisplayManager()
    display.show_artwork(
        image=best['image'],
        title=best['theme'],
        period=f"Period {period_num}",
        metadata={
            'score': best.get('score'),
            'reasoning': best.get('reasoning')
        }
    )
    print("✓ Display updated\n")
    
    # 5. Upload/Git Push
    print("Pushing to GitHub gallery...")
    uploader = GalleryUploader()
    msg = await uploader.post(
        image=best['image'],
        code=best['code'],
        metadata={
            'date': str(timestamp.date()),
            'period': period_num,
            'theme': best['theme'],
            'score': best.get('score'),
            'reasoning': best.get('reasoning')
        }
    )
    print(f"✓ {msg}\n")
    
    # 6. Update taste profile
    curator.update_taste(best)
    print("✓ Taste profile updated\n")
    
    print(f"{ '='*60}")
    print(f"✅ Period {period_num} complete!")
    print(f"{ '='*60}\n")

if __name__ == "__main__":
    asyncio.run(run_period())
