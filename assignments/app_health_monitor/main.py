#!/usr/bin/env python3
import requests
import time
import logging
from datetime import datetime
from typing import Dict, List, Optional

# Configure logging
logging.basicConfig(
    filename='app_health.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class AppHealthChecker:
    def __init__(self, urls: Dict[str, str], check_interval: int = 300):
        """
        Initialize the health checker with URLs to monitor.
        
        Args:
            urls: Dictionary of application names and their URLs
            check_interval: Time between checks in seconds (default 5 minutes)
        """
        self.urls = urls
        self.check_interval = check_interval
        self.status_history: Dict[str, List[bool]] = {app: [] for app in urls}
    
    def check_endpoint(self, url: str) -> tuple[bool, Optional[int], Optional[str]]:
        """Check if an endpoint is responding correctly."""
        try:
            response = requests.get(url, timeout=10)
            is_up = 200 <= response.status_code < 300
            return is_up, response.status_code, response.reason
        except requests.RequestException as e:
            return False, None, str(e)
    
    def update_status_history(self, app_name: str, is_up: bool):
        """Update the status history for an application."""
        history = self.status_history[app_name]
        history.append(is_up)
        # Keep only the last 10 status checks
        if len(history) > 10:
            history.pop(0)
    
    def calculate_uptime_percentage(self, app_name: str) -> float:
        """Calculate the uptime percentage based on status history."""
        history = self.status_history[app_name]
        if not history:
            return 0.0
        return (sum(1 for status in history if status) / len(history)) * 100
    
    def check_all_applications(self):
        """Check the health of all registered applications."""
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        results = {}
        
        for app_name, url in self.urls.items():
            is_up, status_code, reason = self.check_endpoint(url)
            self.update_status_history(app_name, is_up)
            uptime = self.calculate_uptime_percentage(app_name)
            
            status = "UP" if is_up else "DOWN"
            message = (
                f"{app_name}: {status} "
                f"(Status Code: {status_code or 'N/A'}, "
                f"Reason: {reason}, "
                f"Uptime: {uptime:.1f}%)"
            )
            
            # Log the result
            log_level = logging.INFO if is_up else logging.ERROR
            logging.log(log_level, message)
            
            # Print to console
            print(f"[{timestamp}] {message}")
            
            results[app_name] = {
                'status': status,
                'status_code': status_code,
                'reason': reason,
                'uptime': uptime
            }
        
        return results
    
    def run(self):
        """Run continuous health checks."""
        print(f"Starting health checks (interval: {self.check_interval} seconds)")
        try:
            while True:
                self.check_all_applications()
                time.sleep(self.check_interval)
        except KeyboardInterrupt:
            print("\nHealth checking stopped by user")

def main():
    # Define applications to monitor
    apps = {
        'Main Website': 'https://example.com',
        'API Server': 'https://api.example.com/health',
        'Admin Panel': 'https://admin.example.com/status'
    }
    
    # Create and run the health checker
    checker = AppHealthChecker(apps, check_interval=300)
    checker.run()

if __name__ == "__main__":
    main()