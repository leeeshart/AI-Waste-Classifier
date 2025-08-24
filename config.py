#!/usr/bin/env python3
"""
Production configuration and utilities for EcoSort Backend API
"""

import os
import logging
from typing import Dict, Any
from dotenv import load_dotenv

class Config:
    """Base configuration class"""
    
    def __init__(self, env_file: str = None):
        if env_file:
            load_dotenv(env_file)
        else:
            load_dotenv()
    
    # Flask Configuration
    FLASK_ENV = os.getenv('FLASK_ENV', 'development')
    DEBUG = os.getenv('FLASK_DEBUG', 'True').lower() == 'true'
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    
    # Server Configuration
    HOST = os.getenv('HOST', '0.0.0.0')
    PORT = int(os.getenv('PORT', 5000))
    
    # API Configuration
    API_KEY = os.getenv('API_KEY')
    RATE_LIMIT_PER_MINUTE = int(os.getenv('RATE_LIMIT_PER_MINUTE', 60))
    MAX_FILE_SIZE_MB = int(os.getenv('MAX_FILE_SIZE_MB', 16))
    
    # CORS Configuration
    CORS_ORIGINS = os.getenv('CORS_ORIGINS', 'http://localhost:3000').split(',')
    
    # Logging Configuration
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    LOG_FILE = os.getenv('LOG_FILE', 'logs/app.log')
    
    # Database Configuration
    DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///ecosort.db')
    
    # ML Model Configuration
    USE_TENSORFLOW_MODEL = os.getenv('USE_TENSORFLOW_MODEL', 'False').lower() == 'true'
    MODEL_PATH = os.getenv('MODEL_PATH', 'models/')
    
    # Monitoring Configuration
    ENABLE_METRICS = os.getenv('ENABLE_METRICS', 'False').lower() == 'true'
    METRICS_PORT = int(os.getenv('METRICS_PORT', 9090))
    
    # Security Configuration
    ALLOWED_EXTENSIONS = set(os.getenv('ALLOWED_EXTENSIONS', 'png,jpg,jpeg,gif,bmp,webp').split(','))
    UPLOAD_FOLDER = os.getenv('UPLOAD_FOLDER', 'uploads')
    
    @property
    def MAX_FILE_SIZE_BYTES(self) -> int:
        return self.MAX_FILE_SIZE_MB * 1024 * 1024
    
    def setup_logging(self) -> None:
        """Setup application logging"""
        # Create logs directory if it doesn't exist
        log_dir = os.path.dirname(self.LOG_FILE) if '/' in self.LOG_FILE else 'logs'
        os.makedirs(log_dir, exist_ok=True)
        
        # Configure logging
        log_level = getattr(logging, self.LOG_LEVEL.upper(), logging.INFO)
        
        logging.basicConfig(
            level=log_level,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(self.LOG_FILE),
                logging.StreamHandler()
            ]
        )
    
    def validate(self) -> Dict[str, Any]:
        """Validate configuration and return status"""
        errors = []
        warnings = []
        
        # Check required configurations for production
        if self.FLASK_ENV == 'production':
            if self.SECRET_KEY == 'dev-secret-key-change-in-production':
                errors.append("SECRET_KEY must be changed for production")
            
            if not self.API_KEY:
                warnings.append("API_KEY not set - authentication disabled")
            
            if self.DEBUG:
                warnings.append("DEBUG mode is enabled in production")
        
        # Check upload folder
        if not os.path.exists(self.UPLOAD_FOLDER):
            try:
                os.makedirs(self.UPLOAD_FOLDER, exist_ok=True)
            except Exception as e:
                errors.append(f"Cannot create upload folder: {e}")
        
        return {
            'valid': len(errors) == 0,
            'errors': errors,
            'warnings': warnings
        }


class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    FLASK_ENV = 'development'


class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    FLASK_ENV = 'production'
    
    def __init__(self):
        super().__init__('.env.production')


class TestingConfig(Config):
    """Testing configuration"""
    DEBUG = True
    FLASK_ENV = 'testing'
    UPLOAD_FOLDER = 'test_uploads'


def get_config(env: str = None) -> Config:
    """Get configuration based on environment"""
    if env is None:
        env = os.getenv('FLASK_ENV', 'development')
    
    configs = {
        'development': DevelopmentConfig,
        'production': ProductionConfig,
        'testing': TestingConfig
    }
    
    return configs.get(env, DevelopmentConfig)()