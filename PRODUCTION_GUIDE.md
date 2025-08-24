# EcoSort Production Deployment Guide

## Overview

This guide covers the production deployment of EcoSort AI Waste Classifier with enhanced security, monitoring, and scalability features.

## Production Features

### ✅ Security Enhancements
- **Environment Configuration**: Secure environment variable management
- **API Authentication**: Optional API key authentication
- **Rate Limiting**: Configurable request rate limiting
- **Input Validation**: Enhanced input sanitization and validation
- **CORS Protection**: Production-ready CORS configuration
- **File Upload Security**: Secure file validation and processing

### ✅ Performance & Reliability
- **Production WSGI Server**: Gunicorn with multiple workers
- **Enhanced Error Handling**: Comprehensive error responses
- **Request/Response Logging**: Structured logging with levels
- **Health Checks**: Kubernetes-ready health endpoints
- **Monitoring**: Built-in metrics collection and alerting

### ✅ Deployment & Infrastructure
- **Docker Containerization**: Multi-stage builds for production
- **Docker Compose**: Complete orchestration setup
- **CI/CD Pipeline**: GitHub Actions workflow
- **Database Integration**: PostgreSQL and Redis support
- **Reverse Proxy**: Nginx configuration included

## Quick Start

### 1. Environment Setup

```bash
# Copy environment configuration
cp .env.example .env.production

# Update with your production values
nano .env.production
```

### 2. Docker Deployment

```bash
# Deploy with Docker Compose
./deploy.sh production

# Or manually
docker-compose up -d
```

### 3. Manual Deployment

```bash
# Install dependencies
pip install -r requirements.txt
npm install

# Build frontend
npm run build:production

# Start with Gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app_production:app
```

## Configuration

### Environment Variables

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `FLASK_ENV` | Environment mode | `development` | No |
| `FLASK_DEBUG` | Debug mode | `True` | No |
| `SECRET_KEY` | Flask secret key | Generated | **Yes** |
| `API_KEY` | API authentication key | None | No |
| `RATE_LIMIT_PER_MINUTE` | Rate limit | `60` | No |
| `CORS_ORIGINS` | Allowed origins | `http://localhost:3000` | No |
| `DATABASE_URL` | Database connection | SQLite | No |
| `LOG_LEVEL` | Logging level | `INFO` | No |

### Production Settings

For production deployment, ensure:

```bash
FLASK_ENV=production
FLASK_DEBUG=False
SECRET_KEY=your-secure-secret-key
API_KEY=your-api-key
CORS_ORIGINS=https://your-domain.com
```

## API Documentation

### Enhanced Endpoints

#### Health Checks

```bash
# Main health check
GET /
Response: Enhanced health information with features

# Kubernetes readiness probe
GET /health/ready

# Kubernetes liveness probe  
GET /health/live

# Comprehensive health check
GET /health/comprehensive
```

#### Classification Endpoints

```bash
# Text classification
POST /classify-text
Headers: X-API-Key: your-api-key (if enabled)
Body: {"text": "plastic bottle"}

# Image classification
POST /classify-image
Headers: X-API-Key: your-api-key (if enabled)
Body: multipart/form-data with image file
```

#### Monitoring

```bash
# Metrics endpoint (if enabled)
GET /metrics
Response: Application metrics in JSON format
```

### Response Format

All responses follow this standardized format:

```json
{
  "status": "success|error",
  "timestamp": 1640995200.123,
  "data": {
    // Response data
  },
  "message": "Optional message"
}
```

## Security Considerations

### API Authentication

Enable API key authentication for production:

```bash
# Set API key
export API_KEY="your-secure-api-key"

# Use in requests
curl -H "X-API-Key: your-secure-api-key" \
     -X POST http://localhost:5000/classify-text \
     -d '{"text":"plastic bottle"}'
```

### Rate Limiting

Configure rate limiting per IP:

```bash
# 100 requests per minute
export RATE_LIMIT_PER_MINUTE=100
```

### CORS Configuration

Restrict origins in production:

```bash
# Single origin
export CORS_ORIGINS="https://yourdomain.com"

# Multiple origins
export CORS_ORIGINS="https://yourdomain.com,https://app.yourdomain.com"
```

## Monitoring & Logging

### Application Metrics

The application collects comprehensive metrics:

- Request counts and response times
- Error rates and types
- Classification statistics
- System resource usage
- Custom alerts

### Health Monitoring

Built-in health checks monitor:

- Disk space usage
- Memory consumption
- Upload directory status
- Application uptime
- Error rates

### Logging

Structured logging includes:

- Request/response logging
- Error tracking
- Performance monitoring
- Security events

## Deployment Options

### Docker Deployment

```bash
# Production deployment
docker-compose -f docker-compose.yml up -d

# With custom environment
docker-compose --env-file .env.production up -d
```

### Kubernetes Deployment

```yaml
# Example Kubernetes configuration
apiVersion: apps/v1
kind: Deployment
metadata:
  name: ecosort-backend
spec:
  replicas: 3
  selector:
    matchLabels:
      app: ecosort-backend
  template:
    metadata:
      labels:
        app: ecosort-backend
    spec:
      containers:
      - name: backend
        image: ecosort:latest
        ports:
        - containerPort: 5000
        env:
        - name: FLASK_ENV
          value: production
        - name: SECRET_KEY
          valueFrom:
            secretKeyRef:
              name: ecosort-secrets
              key: secret-key
        livenessProbe:
          httpGet:
            path: /health/live
            port: 5000
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /health/ready
            port: 5000
          initialDelaySeconds: 5
          periodSeconds: 5
```

### Cloud Deployment

#### AWS

```bash
# Using AWS ECS/Fargate
aws ecs create-service \
  --cluster ecosort-cluster \
  --service-name ecosort-backend \
  --task-definition ecosort-task:1 \
  --desired-count 2
```

#### Google Cloud

```bash
# Using Google Cloud Run
gcloud run deploy ecosort-backend \
  --image gcr.io/project-id/ecosort:latest \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated
```

## Performance Tuning

### Gunicorn Configuration

```bash
# Optimal worker configuration
gunicorn -w $((2 * $(nproc) + 1)) \
         -b 0.0.0.0:5000 \
         --timeout 120 \
         --keep-alive 2 \
         --max-requests 1000 \
         --max-requests-jitter 50 \
         app_production:app
```

### Database Optimization

```bash
# PostgreSQL connection pooling
export DATABASE_URL="postgresql://user:pass@host:5432/db?sslmode=require"

# Redis caching
export REDIS_URL="redis://localhost:6379/0"
```

## Troubleshooting

### Common Issues

1. **High Error Rate**
   - Check logs: `docker-compose logs backend`
   - Review metrics: `curl localhost:5000/metrics`
   - Verify configuration: `curl localhost:5000/`

2. **Performance Issues**
   - Monitor system resources
   - Check database connections
   - Review rate limiting settings

3. **Authentication Errors**
   - Verify API key configuration
   - Check CORS settings
   - Review request headers

### Log Analysis

```bash
# View application logs
tail -f logs/app.log

# Docker logs
docker-compose logs -f backend

# Filter error logs
grep "ERROR" logs/app.log
```

## Backup and Recovery

### Database Backup

```bash
# PostgreSQL backup
pg_dump $DATABASE_URL > backup_$(date +%Y%m%d).sql

# Restore
psql $DATABASE_URL < backup_20240101.sql
```

### Configuration Backup

```bash
# Backup environment and configs
tar -czf config_backup_$(date +%Y%m%d).tar.gz \
    .env.production \
    docker-compose.yml \
    nginx.conf
```

## Scaling

### Horizontal Scaling

```bash
# Scale backend containers
docker-compose up -d --scale backend=3

# Load balancer configuration (nginx)
upstream backend {
    server backend_1:5000;
    server backend_2:5000;
    server backend_3:5000;
}
```

### Vertical Scaling

```yaml
# Docker resource limits
services:
  backend:
    deploy:
      resources:
        limits:
          cpus: '2.0'
          memory: 4G
        reservations:
          cpus: '1.0'
          memory: 2G
```

## Support

For issues and support:

1. Check the [troubleshooting section](#troubleshooting)
2. Review application logs
3. Open an issue on [GitHub](https://github.com/leeeshart/AI-Waste-Classifier/issues)
4. Contact the development team

## License

MIT License - see [LICENSE](LICENSE) file for details.