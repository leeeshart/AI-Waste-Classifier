#!/usr/bin/env python3
"""
Security and validation utilities for EcoSort Backend API
"""

import functools
import time
from collections import defaultdict, deque
from typing import Dict, Any, Optional
from flask import request, jsonify, current_app
from PIL import Image
import logging

logger = logging.getLogger(__name__)

class RateLimiter:
    """Simple in-memory rate limiter"""
    
    def __init__(self, max_requests: int = 60, window_minutes: int = 1):
        self.max_requests = max_requests
        self.window_seconds = window_minutes * 60
        self.requests = defaultdict(deque)
    
    def is_allowed(self, key: str) -> bool:
        """Check if request is allowed for given key (IP address)"""
        now = time.time()
        window_start = now - self.window_seconds
        
        # Remove old requests
        while self.requests[key] and self.requests[key][0] < window_start:
            self.requests[key].popleft()
        
        # Check if under limit
        if len(self.requests[key]) < self.max_requests:
            self.requests[key].append(now)
            return True
        
        return False


def rate_limit(per_minute: int = 60):
    """Rate limiting decorator"""
    limiter = RateLimiter(max_requests=per_minute, window_minutes=1)
    
    def decorator(f):
        @functools.wraps(f)
        def wrapper(*args, **kwargs):
            # Get client IP
            client_ip = request.environ.get('HTTP_X_FORWARDED_FOR', request.remote_addr)
            
            if not limiter.is_allowed(client_ip):
                logger.warning(f"Rate limit exceeded for IP: {client_ip}")
                return jsonify({
                    'error': 'Rate limit exceeded',
                    'message': f'Maximum {per_minute} requests per minute allowed'
                }), 429
            
            return f(*args, **kwargs)
        return wrapper
    return decorator


def require_api_key(f):
    """API key authentication decorator"""
    @functools.wraps(f)
    def wrapper(*args, **kwargs):
        api_key = current_app.config.get('API_KEY')
        
        # Skip authentication if no API key configured
        if not api_key:
            return f(*args, **kwargs)
        
        # Check API key in headers
        provided_key = request.headers.get('X-API-Key') or request.headers.get('Authorization')
        
        if provided_key and provided_key.replace('Bearer ', '') == api_key:
            return f(*args, **kwargs)
        
        logger.warning(f"Unauthorized API access attempt from {request.remote_addr}")
        return jsonify({
            'error': 'Unauthorized',
            'message': 'Valid API key required'
        }), 401
    
    return wrapper


def validate_file(file) -> Optional[str]:
    """Validate uploaded file"""
    if not file:
        return "No file provided"
    
    if file.filename == '':
        return "No file selected"
    
    # Check file extension
    allowed_extensions = current_app.config.get('ALLOWED_EXTENSIONS', {'png', 'jpg', 'jpeg', 'gif'})
    if not ('.' in file.filename and 
            file.filename.rsplit('.', 1)[1].lower() in allowed_extensions):
        return f"File type not allowed. Allowed types: {', '.join(allowed_extensions)}"
    
    # Check file size
    file.seek(0, 2)  # Seek to end
    file_size = file.tell()
    file.seek(0)  # Reset to beginning
    
    max_size = current_app.config.get('MAX_FILE_SIZE_BYTES', 16 * 1024 * 1024)
    if file_size > max_size:
        return f"File too large. Maximum size: {max_size / (1024*1024):.1f}MB"
    
    # Validate image file
    try:
        img = Image.open(file)
        img.verify()  # Verify it's a valid image
        file.seek(0)  # Reset file pointer
        
        # Check image dimensions (prevent extremely large images)
        if img.size[0] * img.size[1] > 100_000_000:  # 100 megapixels
            return "Image dimensions too large"
            
    except Exception as e:
        logger.warning(f"Invalid image file: {e}")
        return "Invalid image file"
    
    return None


def sanitize_text_input(text: str) -> str:
    """Sanitize text input"""
    if not text:
        return ""
    
    # Remove dangerous characters and limit length
    text = text.strip()[:1000]  # Limit to 1000 characters
    
    # Remove potential script injections (basic protection)
    dangerous_patterns = ['<script', '</script', 'javascript:', 'onload=', 'onerror=']
    for pattern in dangerous_patterns:
        text = text.replace(pattern.lower(), '')
        text = text.replace(pattern.upper(), '')
    
    return text


def log_request():
    """Log incoming requests"""
    def decorator(f):
        @functools.wraps(f)
        def wrapper(*args, **kwargs):
            start_time = time.time()
            
            # Log request
            logger.info(f"Request: {request.method} {request.path} from {request.remote_addr}")
            
            try:
                response = f(*args, **kwargs)
                duration = time.time() - start_time
                
                # Log response
                status_code = getattr(response, 'status_code', 200)
                logger.info(f"Response: {status_code} in {duration:.3f}s")
                
                return response
            except Exception as e:
                duration = time.time() - start_time
                logger.error(f"Error in {duration:.3f}s: {str(e)}")
                raise
        
        return wrapper
    return decorator


def create_error_response(error: str, status_code: int = 400) -> tuple:
    """Create standardized error response"""
    return jsonify({
        'error': error,
        'timestamp': time.time(),
        'status': 'error'
    }), status_code


def create_success_response(data: Dict[str, Any], message: str = None) -> Dict[str, Any]:
    """Create standardized success response"""
    response = {
        'status': 'success',
        'timestamp': time.time(),
        'data': data
    }
    
    if message:
        response['message'] = message
    
    return response