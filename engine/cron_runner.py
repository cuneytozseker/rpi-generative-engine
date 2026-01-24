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
from agents.status_publisher import StatusPublisher
from upload import GalleryUploader
from config.settings import OUTPUT_DIR, SKETCHES_PER_PERIOD, VERCEL_BLOB_TOKEN

async def run_period():
    """Execute one generation period"""

    timestamp = datetime.now()
    period_num = (timestamp.hour // 6) + 1
    
    # Initialize status publisher
    status = StatusPublisher(VERCEL_BLOB_TOKEN)

    # Setup output directory
    output_dir = OUTPUT_DIR / str(timestamp.date()) / f"period_{period_num}"
    output_dir.mkdir(parents=True, exist_ok=True)
    
    print(f"{ '='*60}")
    print(f"🎨 Starting Period {period_num} - {timestamp.strftime('%Y-%m-%d %H:%M')}")
    print(f"{ '='*60}\n")
    
    # 1. Generate sketches
    await status.update('Generator', 'Generating sketches', f'0/{SKETCHES_PER_PERIOD}')
    print(f"Generating {SKETCHES_PER_PERIOD} sketches...")
    generator = GeneratorAgent()
    sketches = await generator.generate_batch(SKETCHES_PER_PERIOD)
    print(f"✓ Generated {len(sketches)} sketches\n")
    
    # 2. Execute and render
    await status.update('Executor', 'Rendering sketches', f'0/{len(sketches)}')
    print("Rendering sketches...")
    executor = SafeExecutor()
    rendered = []
    
    for idx, sketch in enumerate(sketches):
        await status.update('Executor', 'Rendering sketches', f'{idx+1}/{len(sketches)}')
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
        await status.update('Idle', 'No sketches rendered', 'Waiting for next cycle')
        print("❌ No sketches rendered successfully. Exiting.")
        return
    
    # 3. Curate best
    await status.update('Curator', 'Evaluating with Claude Sonnet')
    print("Evaluating with Claude Sonnet...")
    curator = CuratorAgent()
    best = await curator.select_best(rendered)
    print(f"\n✨ Selected: {best['id']}")
    print(f"   Theme: {best['theme']}")
    print(f"   Score: {best.get('score', 'N/A')}/10\n")
    
    # 4. Update display
    await status.update('Display', 'Updating TFT screen')
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
    await status.update('Uploader', 'Pushing to GitHub gallery')
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
    
    # 7. Set status to idle
    await status.update('Idle', 'Waiting for next cycle')

    print(f"{ '='*60}")
    print(f"✅ Period {period_num} complete!")
    print(f"{ '='*60}\n")

if __name__ == "__main__":
    asyncio.run(run_period())