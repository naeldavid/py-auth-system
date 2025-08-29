import json
import os
import shutil
from datetime import datetime
import schedule
import time

class BackupManager:
    def __init__(self, data_dir="data", backup_dir="backups"):
        self.data_dir = data_dir
        self.backup_dir = backup_dir
        os.makedirs(backup_dir, exist_ok=True)
    
    def create_backup(self):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = f"{self.backup_dir}/backup_{timestamp}"
        
        try:
            shutil.copytree(self.data_dir, backup_path)
            print(f"Backup created: {backup_path}")
            self._cleanup_old_backups()
            return True
        except Exception as e:
            print(f"Backup failed: {e}")
            return False
    
    def _cleanup_old_backups(self, keep_count=10):
        backups = sorted([d for d in os.listdir(self.backup_dir) if d.startswith("backup_")])
        while len(backups) > keep_count:
            old_backup = backups.pop(0)
            shutil.rmtree(f"{self.backup_dir}/{old_backup}")
    
    def start_scheduled_backups(self):
        schedule.every().day.at("02:00").do(self.create_backup)
        while True:
            schedule.run_pending()
            time.sleep(3600)  # Check every hour