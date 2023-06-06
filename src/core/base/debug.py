import threading
import gc

class Debug:
    def __init__(self) -> None:
        self.debug_info = {}
    
    def update_debug_info(self):
        self.debug_info["gc"]["count"] = gc.get_count()
    
    def get_debug_info(self):
        return self.debug_info