import os
from datetime import datetime, timedelta

class FileManager:
    def __init__(self, base_dir: str, days_to_keep: int):
        self.base_dir = base_dir
        self.days_to_keep = days_to_keep
        os.makedirs(base_dir, exist_ok=True)

    def cleanup_old_files(self):
        now = datetime.now()
        for filename in os.listdir(self.base_dir):
            path = os.path.join(self.base_dir, filename)
            if os.path.isfile(path):
                file_time = datetime.fromtimestamp(os.path.getmtime(path))
                if (now - file_time) > timedelta(days=self.days_to_keep):
                    os.remove(path)

    def get_safe_path(self, filename: str) -> str:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        return os.path.join(self.base_dir, f"{timestamp}_{filename}")
