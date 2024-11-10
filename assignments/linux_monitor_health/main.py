#!/usr/bin/env python3
import psutil
import time
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(
    filename='system_health.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class SystemMonitor:
    def __init__(self, thresholds):
        self.thresholds = thresholds
    
    def check_cpu_usage(self):
        cpu_percent = psutil.cpu_percent(interval=1)
        if cpu_percent > self.thresholds['cpu']:
            self.alert(f"High CPU Usage: {cpu_percent}%")
        return cpu_percent
    
    def check_memory_usage(self):
        memory = psutil.virtual_memory()
        memory_percent = memory.percent
        if memory_percent > self.thresholds['memory']:
            self.alert(f"High Memory Usage: {memory_percent}%")
        return memory_percent
    
    def check_disk_space(self):
        disk = psutil.disk_usage('/')
        disk_percent = disk.percent
        if disk_percent > self.thresholds['disk']:
            self.alert(f"High Disk Usage: {disk_percent}%")
        return disk_percent
    
    def check_process_count(self):
        process_count = len(list(psutil.process_iter()))
        if process_count > self.thresholds['processes']:
            self.alert(f"High Process Count: {process_count}")
        return process_count
    
    def alert(self, message):
        print(f"ALERT: {message}")
        logging.warning(message)
    
    def monitor(self):
        metrics = {
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'cpu': self.check_cpu_usage(),
            'memory': self.check_memory_usage(),
            'disk': self.check_disk_space(),
            'processes': self.check_process_count()
        }
        
        # Log all metrics
        logging.info(
            f"CPU: {metrics['cpu']}%, "
            f"Memory: {metrics['memory']}%, "
            f"Disk: {metrics['disk']}%, "
            f"Processes: {metrics['processes']}"
        )
        
        return metrics

def main():
    # Define thresholds
    thresholds = {
        'cpu': 80,        # 80% CPU usage
        'memory': 85,     # 85% memory usage
        'disk': 90,       # 90% disk usage
        'processes': 300  # 300 processes
    }
    
    monitor = SystemMonitor(thresholds)
    
    try:
        while True:
            monitor.monitor()
            time.sleep(60)  # Check every minute
            
    except KeyboardInterrupt:
        print("\nMonitoring stopped by user")
        
if __name__ == "__main__":
    main()