#!/bin/bash

# EcoSort Production Deployment Script

set -e  # Exit on any error

echo "🚀 Starting EcoSort Production Deployment..."

# Configuration
DEPLOY_ENV=${1:-production}
PROJECT_NAME="ecosort"
BACKUP_DIR="backups/$(date +%Y%m%d_%H%M%S)"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check prerequisites
check_prerequisites() {
    print_status "Checking prerequisites..."
    
    if ! command -v docker &> /dev/null; then
        print_error "Docker is required but not installed."
        exit 1
    fi
    
    if ! command -v docker-compose &> /dev/null; then
        print_error "Docker Compose is required but not installed."
        exit 1
    fi
    
    print_status "Prerequisites check passed ✓"
}

# Create necessary directories
setup_directories() {
    print_status "Setting up directories..."
    
    mkdir -p logs uploads models nginx/ssl backups
    chmod 755 logs uploads models
    
    print_status "Directories created ✓"
}

# Environment setup
setup_environment() {
    print_status "Setting up environment for: $DEPLOY_ENV"
    
    if [[ "$DEPLOY_ENV" == "production" ]]; then
        if [[ ! -f .env.production ]]; then
            print_warning "No .env.production found, copying from example"
            cp .env.example .env.production
            print_warning "Please update .env.production with production values"
        fi
        cp .env.production .env
    else
        cp .env.example .env
    fi
    
    print_status "Environment configured ✓"
}

# Build and deploy
deploy() {
    print_status "Building and deploying services..."
    
    # Stop existing services
    docker-compose down
    
    # Build images
    docker-compose build --no-cache
    
    # Start services
    docker-compose up -d
    
    print_status "Services deployed ✓"
}

# Health check
health_check() {
    print_status "Performing health checks..."
    
    # Wait for services to start
    sleep 10
    
    # Check backend health
    if curl -f http://localhost:5000/health/live &> /dev/null; then
        print_status "Backend health check passed ✓"
    else
        print_error "Backend health check failed ✗"
        exit 1
    fi
    
    # Check frontend health
    if curl -f http://localhost:3000/health &> /dev/null; then
        print_status "Frontend health check passed ✓"
    else
        print_error "Frontend health check failed ✗"
        exit 1
    fi
}

# Show deployment status
show_status() {
    print_status "Deployment Status:"
    docker-compose ps
    
    echo ""
    print_status "Access URLs:"
    echo "Frontend: http://localhost:3000"
    echo "Backend API: http://localhost:5000"
    echo "Health Check: http://localhost:5000/health/live"
}

# Main deployment process
main() {
    echo "EcoSort Production Deployment"
    echo "============================="
    
    check_prerequisites
    setup_directories
    setup_environment
    deploy
    health_check
    show_status
    
    print_status "🎉 Deployment completed successfully!"
    print_warning "Remember to:"
    echo "  - Update .env.production with secure values"
    echo "  - Configure SSL certificates in nginx/ssl/"
    echo "  - Set up monitoring and logging"
    echo "  - Configure backup procedures"
}

# Cleanup function for graceful shutdown
cleanup() {
    print_warning "Deployment interrupted. Cleaning up..."
    docker-compose down
    exit 1
}

# Set trap for cleanup
trap cleanup INT TERM

# Run main function
main "$@"