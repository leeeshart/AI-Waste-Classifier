#!/usr/bin/env python3
"""
Monitoring and metrics utilities for EcoSort Backend API
"""

import time
import logging
from collections import defaultdict, Counter
from datetime import datetime, timedelta
from functools import wraps
from flask import request, g
import psutil
import os

logger = logging.getLogger(__name__)


class MetricsCollector:
    """Collect and store application metrics"""
    
    def __init__(self):
        self.request_count = Counter()
        self.response_times = defaultdict(list)
        self.error_count = Counter()
        self.classification_stats = Counter()
        self.start_time = time.time()
    
    def record_request(self, endpoint: str, method: str, status_code: int, response_time: float):
        """Record request metrics"""
        self.request_count[f"{method}:{endpoint}"] += 1
        self.response_times[endpoint].append(response_time)
        
        if status_code >= 400:
            self.error_count[f"{status_code}:{endpoint}"] += 1
    
    def record_classification(self, classification_type: str, label: str, confidence: float):
        """Record classification metrics"""
        self.classification_stats[f"{classification_type}:{label}"] += 1
    
    def get_uptime(self) -> float:
        """Get application uptime in seconds"""
        return time.time() - self.start_time
    
    def get_system_metrics(self) -> dict:
        """Get system resource metrics"""
        process = psutil.Process(os.getpid())
        
        return {
            'cpu_percent': psutil.cpu_percent(interval=1),
            'memory_percent': psutil.virtual_memory().percent,
            'disk_usage_percent': psutil.disk_usage('/').percent,
            'process_memory_mb': process.memory_info().rss / 1024 / 1024,
            'process_cpu_percent': process.cpu_percent(),
            'open_files': len(process.open_files()),
        }
    
    def get_metrics_summary(self) -> dict:
        """Get comprehensive metrics summary"""
        total_requests = sum(self.request_count.values())
        total_errors = sum(self.error_count.values())
        error_rate = (total_errors / total_requests * 100) if total_requests > 0 else 0
        
        # Calculate average response times
        avg_response_times = {}
        for endpoint, times in self.response_times.items():
            if times:
                avg_response_times[endpoint] = {
                    'avg': sum(times) / len(times),
                    'min': min(times),
                    'max': max(times),
                    'count': len(times)
                }
        
        return {
            'uptime_seconds': self.get_uptime(),
            'total_requests': total_requests,
            'total_errors': total_errors,
            'error_rate_percent': round(error_rate, 2),
            'requests_by_endpoint': dict(self.request_count),
            'errors_by_type': dict(self.error_count),
            'classification_stats': dict(self.classification_stats),
            'response_times': avg_response_times,
            'system_metrics': self.get_system_metrics()
        }


# Global metrics collector instance
metrics = MetricsCollector()


def monitor_requests(f):
    """Decorator to monitor request metrics"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        start_time = time.time()
        g.start_time = start_time
        
        try:
            response = f(*args, **kwargs)
            status_code = getattr(response, 'status_code', 200)
        except Exception as e:
            status_code = 500
            raise
        finally:
            response_time = time.time() - start_time
            endpoint = request.endpoint or 'unknown'
            method = request.method
            
            metrics.record_request(endpoint, method, status_code, response_time)
            
            # Log slow requests
            if response_time > 2.0:  # 2 seconds threshold
                logger.warning(f"Slow request: {method} {endpoint} took {response_time:.3f}s")
        
        return response
    
    return decorated_function


def monitor_classification(classification_type: str):
    """Decorator to monitor classification metrics"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            result = f(*args, **kwargs)
            
            # Extract label and confidence from result
            if isinstance(result, tuple) and len(result) >= 2:
                label, confidence = result[0], result[1]
                metrics.record_classification(classification_type, label, confidence)
            
            return result
        
        return decorated_function
    
    return decorator


class HealthChecker:
    """Health check utilities"""
    
    @staticmethod
    def check_disk_space(threshold_percent: float = 90.0) -> dict:
        """Check available disk space"""
        usage = psutil.disk_usage('/')
        used_percent = (usage.used / usage.total) * 100
        
        return {
            'status': 'healthy' if used_percent < threshold_percent else 'warning',
            'used_percent': round(used_percent, 2),
            'free_gb': round(usage.free / (1024**3), 2),
            'total_gb': round(usage.total / (1024**3), 2)
        }
    
    @staticmethod
    def check_memory(threshold_percent: float = 90.0) -> dict:
        """Check memory usage"""
        memory = psutil.virtual_memory()
        
        return {
            'status': 'healthy' if memory.percent < threshold_percent else 'warning',
            'used_percent': memory.percent,
            'available_gb': round(memory.available / (1024**3), 2),
            'total_gb': round(memory.total / (1024**3), 2)
        }
    
    @staticmethod
    def check_upload_directory(upload_folder: str) -> dict:
        """Check upload directory status"""
        try:
            if not os.path.exists(upload_folder):
                return {'status': 'error', 'message': 'Upload directory does not exist'}
            
            if not os.access(upload_folder, os.R_OK | os.W_OK):
                return {'status': 'error', 'message': 'Upload directory not accessible'}
            
            # Check number of files in upload directory
            file_count = len([f for f in os.listdir(upload_folder) 
                            if os.path.isfile(os.path.join(upload_folder, f))])
            
            return {
                'status': 'healthy',
                'file_count': file_count,
                'path': upload_folder
            }
            
        except Exception as e:
            return {'status': 'error', 'message': str(e)}
    
    @classmethod
    def comprehensive_health_check(cls, upload_folder: str) -> dict:
        """Perform comprehensive health check"""
        checks = {
            'disk_space': cls.check_disk_space(),
            'memory': cls.check_memory(),
            'upload_directory': cls.check_upload_directory(upload_folder),
            'metrics': {
                'status': 'healthy',
                'uptime_hours': round(metrics.get_uptime() / 3600, 2),
                'total_requests': sum(metrics.request_count.values()),
                'error_rate': metrics.get_metrics_summary()['error_rate_percent']
            }
        }
        
        # Determine overall status
        statuses = [check.get('status', 'unknown') for check in checks.values()]
        if 'error' in statuses:
            overall_status = 'unhealthy'
        elif 'warning' in statuses:
            overall_status = 'degraded'
        else:
            overall_status = 'healthy'
        
        return {
            'overall_status': overall_status,
            'timestamp': datetime.now().isoformat(),
            'checks': checks
        }


class AlertManager:
    """Simple alert manager for critical issues"""
    
    def __init__(self):
        self.alert_history = []
        self.alert_thresholds = {
            'error_rate': 5.0,  # 5% error rate
            'response_time': 5.0,  # 5 seconds
            'memory_usage': 90.0,  # 90% memory usage
            'disk_usage': 95.0,  # 95% disk usage
        }
    
    def check_alerts(self) -> list:
        """Check for alert conditions"""
        alerts = []
        
        # Check error rate
        summary = metrics.get_metrics_summary()
        if summary['error_rate_percent'] > self.alert_thresholds['error_rate']:
            alerts.append({
                'type': 'error_rate',
                'severity': 'high',
                'message': f"High error rate: {summary['error_rate_percent']:.2f}%",
                'timestamp': datetime.now().isoformat()
            })
        
        # Check system resources
        system_metrics = summary['system_metrics']
        if system_metrics['memory_percent'] > self.alert_thresholds['memory_usage']:
            alerts.append({
                'type': 'memory_usage',
                'severity': 'medium',
                'message': f"High memory usage: {system_metrics['memory_percent']:.2f}%",
                'timestamp': datetime.now().isoformat()
            })
        
        if system_metrics['disk_usage_percent'] > self.alert_thresholds['disk_usage']:
            alerts.append({
                'type': 'disk_usage',
                'severity': 'high',
                'message': f"High disk usage: {system_metrics['disk_usage_percent']:.2f}%",
                'timestamp': datetime.now().isoformat()
            })
        
        # Store alert history
        self.alert_history.extend(alerts)
        
        # Keep only recent alerts (last 24 hours)
        cutoff_time = datetime.now() - timedelta(hours=24)
        self.alert_history = [
            alert for alert in self.alert_history
            if datetime.fromisoformat(alert['timestamp']) > cutoff_time
        ]
        
        return alerts


# Global alert manager instance
alert_manager = AlertManager()