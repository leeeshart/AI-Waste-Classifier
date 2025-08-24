#!/bin/bash

# EcoSort Backend Startup Script

set -e  # Exit on any error

echo "🌱 Starting EcoSort AI Waste Classifier Backend..."

# Configuration
MODE=${1:-development}
PORT=${PORT:-5000}
HOST=${HOST:-0.0.0.0}

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    print_error "Python 3 is required but not installed."
    exit 1
fi

# Check mode and set environment
if [[ "$MODE" == "production" ]]; then
    print_status "Starting in PRODUCTION mode"
    export FLASK_ENV=production
    export FLASK_DEBUG=False
    
    # Check for production configuration
    if [[ ! -f .env.production ]]; then
        print_warning "No .env.production found, generating one..."
        python3 generate_production_config.py --output .env.production --force
        print_warning "Please review and update .env.production before running in production!"
    fi
    
    APP_FILE="app_production.py"
else
    print_status "Starting in DEVELOPMENT mode"
    export FLASK_ENV=development
    export FLASK_DEBUG=True
    APP_FILE="app.py"
fi

# Create necessary directories
print_status "Setting up directories..."
mkdir -p uploads logs models

# Install dependencies in development mode
if [[ "$MODE" != "production" ]]; then
    # Create virtual environment if it doesn't exist
    if [ ! -d "venv" ]; then
        print_status "Creating virtual environment..."
        python3 -m venv venv
    fi

    # Activate virtual environment
    print_status "Activating virtual environment..."
    source venv/bin/activate

    # Install dependencies
    print_status "Installing dependencies..."
    pip install -r requirements.txt
fi

# Validate configuration
print_status "Validating configuration..."
python3 -c "
from config import get_config
config = get_config()
status = config.validate()
if not status['valid']:
    print('❌ Configuration validation failed:')
    for error in status['errors']:
        print(f'  - {error}')
    exit(1)
else:
    print('✅ Configuration validation passed')
    if status['warnings']:
        for warning in status['warnings']:
            print(f'⚠️  {warning}')
"

# Start the appropriate server
if [[ "$MODE" == "production" ]]; then
    if command -v gunicorn &> /dev/null; then
        print_status "Starting with Gunicorn (Production)"
        exec gunicorn --bind ${HOST}:${PORT} --workers 4 --timeout 120 --access-logfile logs/access.log --error-logfile logs/error.log app_production:app
    else
        print_warning "Gunicorn not found, falling back to Flask development server"
        exec python3 app_production.py
    fi
else
    print_status "Starting Flask development server on http://${HOST}:${PORT}"
    exec python3 ${APP_FILE}
fi