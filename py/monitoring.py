import psutil
import time
from datetime import datetime
import json

class SystemMonitor:
    def __init__(self):
        self.metrics = []
    
    def collect_metrics(self):
        return {
            'timestamp': datetime.now().isoformat(),
            'cpu_percent': psutil.cpu_percent(),
            'memory_percent': psutil.virtual_memory().percent,
            'disk_usage': psutil.disk_usage('/').percent,
            'active_connections': len(psutil.net_connections()),
            'process_count': len(psutil.pids())
        }
    
    def log_metrics(self):
        metrics = self.collect_metrics()
        self.metrics.append(metrics)
        
        # Keep only last 1000 entries
        if len(self.metrics) > 1000:
            self.metrics = self.metrics[-1000:]
        
        # Save to file
        with open('logs/system_metrics.json', 'w') as f:
            json.dump(self.metrics, f, indent=2)
    
    def get_health_status(self):
        metrics = self.collect_metrics()
        status = "healthy"
        
        if metrics['cpu_percent'] > 80:
            status = "warning"
        if metrics['memory_percent'] > 85:
            status = "critical"
        
        return status, metrics