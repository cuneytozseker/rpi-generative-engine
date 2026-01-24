import httpx
import json
from datetime import datetime, timedelta

class StatusPublisher:
    def __init__(self, blob_token: str):
        self.token = blob_token
        self.url = "https://blob.vercel-storage.com"
    
    async def update(self, agent: str, task: str, progress: str = None):
        """Push status update to Vercel Blob"""
        status = {
            'agent': agent,
            'task': task,
            'progress': progress,
            'timestamp': datetime.now().isoformat(),
            'next_cycle': self._calculate_next_cycle()
        }
        
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                # Using the standard Vercel Blob PUT structure
                # Note: 'x-add-random-suffix': '0' ensures we overwrite the same file
                response = await client.put(
                    f"{self.url}/status.json",
                    headers={
                        'Authorization': f'Bearer {self.token}',
                        'x-content-type': 'application/json',
                        'x-add-random-suffix': '0'
                    },
                    content=json.dumps(status)
                )
                
                if response.status_code in [200, 201]:
                    print(f"✓ Status updated: {agent} - {task}")
                    return True
                else:
                    print(f"✗ Status update failed: {response.status_code} - {response.text}")
                    return False
                    
        except Exception as e:
            print(f"✗ Status update error: {e}")
            return False
    
    def _calculate_next_cycle(self):
        """Calculate next 6-hour cycle time"""
        now = datetime.now()
        next_hours = [0, 6, 12, 18]
        
        for hour in next_hours:
            next_time = now.replace(hour=hour, minute=0, second=0, microsecond=0)
            if next_time > now:
                delta = next_time - now
                hours = delta.seconds // 3600
                minutes = (delta.seconds % 3600) // 60
                return f"in {hours}h {minutes}m"
        
        # Next cycle is tomorrow at 00:00
        tomorrow = now + timedelta(days=1)
        next_time = tomorrow.replace(hour=0, minute=0, second=0, microsecond=0)
        delta = next_time - now
        hours = delta.seconds // 3600
        return f"in {hours}h"
