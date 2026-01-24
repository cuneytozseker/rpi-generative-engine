import cairo
import math
import random
from pathlib import Path
import traceback
import signal

class SafeExecutor:
    """Safely execute generated cairo code"""
    
    def __init__(self, timeout=10):
        self.timeout = timeout
        self.allowed_imports = {
            'cairo': cairo,
            'math': math,
            'random': random,
        }
    
    def execute(self, code: str, output_path: Path) -> tuple[bool, str]:
        """Execute generated code and save to output_path"""
        
        # Create isolated namespace
        namespace = self.allowed_imports.copy()
        
        # Timeout handler
        def timeout_handler(signum, frame):
            raise TimeoutError(f"Execution exceeded {self.timeout}s")
        
        signal.signal(signal.SIGALRM, timeout_handler)
        signal.alarm(self.timeout)
        
        try:
            # Execute code
            exec(code, namespace)
            
            # Check if surface was created
            if 'surface' not in namespace:
                return False, "Code didn't create 'surface' variable"
            
            # Save output
            surface = namespace['surface']
            surface.write_to_png(str(output_path))
            
            return True, "Success"
            
        except TimeoutError as e:
            return False, str(e)
        except Exception as e:
            return False, f"Error: {traceback.format_exc()}"
        finally:
            signal.alarm(0)  # Cancel alarm
