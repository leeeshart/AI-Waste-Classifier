#!/usr/bin/env python3
"""
Production Configuration Generator for EcoSort AI Waste Classifier
Generates secure configuration values for production deployment
"""

import secrets
import string
import os
import argparse


def generate_secret_key(length=64):
    """Generate a secure secret key"""
    alphabet = string.ascii_letters + string.digits + "!@#$%^&*"
    return ''.join(secrets.choice(alphabet) for _ in range(length))


def generate_api_key(length=32):
    """Generate a secure API key"""
    return secrets.token_urlsafe(length)


def create_production_config(domain=None, database_url=None):
    """Create production configuration with secure defaults"""
    
    secret_key = generate_secret_key()
    api_key = generate_api_key()
    
    config_template = f"""# Production Configuration for EcoSort AI Waste Classifier
# Generated on: {os.popen('date').read().strip()}
# WARNING: Keep this file secure and never commit to version control

# Flask Configuration
FLASK_ENV=production
FLASK_DEBUG=False
SECRET_KEY={secret_key}

# Server Configuration
HOST=0.0.0.0
PORT=5000

# API Configuration
API_KEY={api_key}
RATE_LIMIT_PER_MINUTE=100
MAX_FILE_SIZE_MB=16

# CORS Configuration
CORS_ORIGINS={domain or 'https://your-frontend-domain.com'}

# Logging Configuration
LOG_LEVEL=WARNING
LOG_FILE=logs/app.log

# Database Configuration
DATABASE_URL={database_url or 'postgresql://ecosort:change_this_password@localhost/ecosort'}

# ML Model Configuration
USE_TENSORFLOW_MODEL=True
MODEL_PATH=models/

# Monitoring Configuration
ENABLE_METRICS=True
METRICS_PORT=9090

# Security Configuration
ALLOWED_EXTENSIONS=png,jpg,jpeg,gif,bmp,webp
UPLOAD_FOLDER=uploads

# Additional Production Settings
# Uncomment and configure as needed:
# REDIS_URL=redis://localhost:6379/0
# CELERY_BROKER_URL=redis://localhost:6379/0
# SENTRY_DSN=your-sentry-dsn-here
# SSL_CERT_PATH=/path/to/ssl/cert.pem
# SSL_KEY_PATH=/path/to/ssl/key.pem
"""
    
    return config_template, secret_key, api_key


def main():
    parser = argparse.ArgumentParser(description='Generate production configuration')
    parser.add_argument('--domain', help='Frontend domain for CORS')
    parser.add_argument('--database-url', help='Database URL')
    parser.add_argument('--output', default='.env.production.new', help='Output file')
    parser.add_argument('--force', action='store_true', help='Overwrite existing file')
    
    args = parser.parse_args()
    
    if os.path.exists(args.output) and not args.force:
        print(f"❌ File {args.output} already exists. Use --force to overwrite.")
        return 1
    
    config, secret_key, api_key = create_production_config(args.domain, args.database_url)
    
    with open(args.output, 'w') as f:
        f.write(config)
    
    print(f"✅ Production configuration generated: {args.output}")
    print("\n📝 Important notes:")
    print("1. Review and update the configuration values as needed")
    print("2. Never commit this file to version control")
    print("3. Store secrets securely (consider using environment variables or secret managers)")
    print("4. Update CORS_ORIGINS with your actual domain")
    print("5. Configure proper database connection string")
    
    print(f"\n🔑 Generated credentials:")
    print(f"API Key: {api_key}")
    print(f"Secret Key: {secret_key[:16]}...")
    
    print(f"\n🚀 To use this configuration:")
    print(f"1. mv {args.output} .env.production")
    print("2. Review and customize the values")
    print("3. Deploy with: ./deploy.sh production")
    
    return 0


if __name__ == '__main__':
    exit(main())