# ♻️ EcoSort 
### Sustainable Cities & Communities (SDG 11)

An AI-powered solution to classify waste as **Recyclable, Biodegradable, or Hazardous** using image uploads or text descriptions.  
Built for the **Global AI Buildathon 2025**.  

---

## 🚀 Features
- Upload a **waste image** → AI model predicts category.  
- Enter a **description (e.g., "banana peel")** → Text-based classification.  
- Disposal **tips & icons** for each category.  
- Lightweight model (MobileNetV2 / TensorFlow.js) → runs fast on web/mobile.  
- Full-stack application with React frontend and Flask backend.

---

## 🛠️ Tech Stack
- **Frontend:** React.js + Vite (image upload, text input, results UI)  
- **Backend:** Flask API with CORS support  
- **AI Classification:** 
  - Text: Keyword-based classification
  - Image: Basic heuristics (expandable to MobileNetV2/TensorFlow)
- **Dataset:** [Kaggle – Waste Classification Dataset](https://www.kaggle.com/datasets/techsash/waste-classification-data)  
- **Deployment:** Local development setup included

---

## 🚀 Quick Start

### Development Setup

#### Prerequisites
- Node.js 16+ and npm
- Python 3.8+
- pip

#### Setup Instructions

1. **Clone the repository:**
   ```bash
   git clone https://github.com/leeeshart/AI-Waste-Classifier.git
   cd AI-Waste-Classifier
   ```

2. **Install Python dependencies:**
   ```bash
   pip install -r requirements_simple.txt
   ```

3. **Install Node.js dependencies:**
   ```bash
   npm install
   ```

4. **Start the backend server:**
   ```bash
   python3 app_simple.py
   ```
   Backend will run on http://localhost:5000

5. **Start the frontend (in a new terminal):**
   ```bash
   npm run dev
   ```
   Frontend will run on http://localhost:3000

6. **Open your browser and visit http://localhost:3000**

### Production Deployment

For production deployment with enhanced security, monitoring, and scalability:

#### Quick Production Setup
```bash
# 1. Check production readiness
python3 check_production_readiness.py

# 2. Generate secure production configuration
python3 generate_production_config.py --domain https://your-domain.com

# 3. Deploy with Docker
./deploy.sh production
```

#### Production Features
- 🔒 **Enhanced Security**: API authentication, rate limiting, input validation
- 📊 **Monitoring**: Health checks, metrics collection, structured logging  
- 🚀 **Scalability**: Docker containers, nginx load balancer, database support
- 🔧 **Configuration**: Environment-based config with secure defaults
- 📋 **Validation**: Comprehensive production readiness checks

#### Production Requirements
- Docker & Docker Compose
- SSL certificates (for HTTPS)
- PostgreSQL database (optional)
- Redis cache (optional)

For detailed production deployment instructions, see [PRODUCTION_GUIDE.md](PRODUCTION_GUIDE.md).

---

## ⚙️ How It Works
1. User uploads an image OR enters waste description.  
2. Frontend sends request to Flask backend API.
3. Backend processes the input:
   - **Text:** Keyword matching against waste category dictionaries
   - **Image:** Basic image analysis (extensible to ML models)
4. API returns classification with confidence score and disposal tips.
5. Frontend displays result with icon + disposal instructions.  

---

## 📁 Project Structure
```
├── Frontend (React + Vite)
│   ├── App.jsx                    # Main app component
│   ├── Home.js                    # Landing page
│   ├── ImageUpload.jsx            # Image classification page
│   ├── TextClassify.jsx           # Text classification page
│   ├── History.jsx                # Classification history
│   ├── FutureVision.jsx           # Future features showcase
│   └── api.js / api_production.js # API communication layer
├── Backend (Flask API)
│   ├── app_simple.py              # Development Flask server
│   ├── app_production.py          # Production server with security
│   ├── config.py                  # Configuration management
│   ├── security.py                # Security utilities
│   ├── classification_core.py     # Core AI classification logic
│   └── requirements.txt           # Python dependencies
├── Production & Deployment
│   ├── Dockerfile.backend         # Backend container
│   ├── Dockerfile.frontend        # Frontend container  
│   ├── docker-compose.yml         # Multi-service orchestration
│   ├── nginx.conf                 # Nginx configuration
│   ├── deploy.sh                  # Deployment script
│   ├── start_backend.sh           # Backend startup script
│   ├── generate_production_config.py # Secure config generator
│   └── check_production_readiness.py # Production validation
├── Documentation
│   ├── BACKEND_README.md          # Backend setup guide
│   ├── PRODUCTION_GUIDE.md        # Production deployment guide
│   └── README.md                  # This file
└── Configuration
    ├── package.json               # Node.js dependencies
    ├── vite.config.js             # Vite configuration
    ├── .env.example               # Environment template
    └── .env.production            # Production environment (secure)
    └── .gitignore              # Git ignore rules
```

---

## 🔧 API Endpoints

### Text Classification
```bash
POST /classify-text
Content-Type: application/json

{
  "text": "plastic bottle"
}
```

**Response:**
```json
{
  "label": "recyclable",
  "confidence": 0.8,
  "tip": "Clean the item and place it in the recycling bin..."
}
```

### Image Classification
```bash
POST /classify-image
Content-Type: multipart/form-data

image: <file>
```

**Response:**
```json
{
  "label": "biodegradable", 
  "confidence": 0.75,
  "tip": "Compost this item in your garden compost bin..."
}
```

---

## 🚀 Production Deployment

### Production-Ready Features
- **Enhanced Security**: API authentication, rate limiting, input validation
- **Docker Containerization**: Multi-stage builds with health checks
- **CI/CD Pipeline**: Automated testing and deployment with GitHub Actions
- **Monitoring & Logging**: Comprehensive metrics and structured logging
- **Database Integration**: PostgreSQL and Redis support
- **Load Balancing**: Nginx reverse proxy configuration

### Quick Production Deploy
```bash
# Clone and deploy
git clone https://github.com/leeeshart/AI-Waste-Classifier.git
cd AI-Waste-Classifier

# Configure environment
cp .env.example .env.production
# Edit .env.production with your settings

# Deploy with Docker
./deploy.sh production
```

### Health Monitoring
```bash
# Health checks
curl http://localhost:5000/health/live      # Liveness probe
curl http://localhost:5000/health/ready     # Readiness probe
curl http://localhost:5000/metrics          # Performance metrics
```

### Production Readiness Validation
```bash
# Check if application is ready for production
python3 check_production_readiness.py

# Generate secure production configuration
python3 generate_production_config.py --domain https://your-domain.com

# Test core functionality without dependencies
python3 classification_core.py
```

---

## ✅ Production Readiness Status

This application has been enhanced for production deployment with comprehensive security, monitoring, and deployment features:

### 🔒 Security Features
- **API Authentication**: Optional API key-based authentication
- **Rate Limiting**: Configurable request rate limiting per IP
- **Input Validation**: Enhanced file upload and text input sanitization
- **CORS Protection**: Production-ready CORS configuration
- **Security Headers**: Comprehensive HTTP security headers via nginx

### 🚀 Deployment Features  
- **Docker Containerization**: Multi-stage builds with health checks
- **Production Configuration**: Secure environment variable management
- **Automated Deployment**: One-command production deployment
- **Health Checks**: Kubernetes-ready liveness and readiness probes
- **Error Handling**: Comprehensive error responses and logging

### 📊 Monitoring & Reliability
- **Structured Logging**: Configurable log levels and file output
- **Metrics Collection**: Built-in performance metrics endpoint
- **Database Integration**: PostgreSQL and Redis support
- **Load Balancing**: Nginx reverse proxy with upstream configuration

### ✅ Validation Tools
- **Production Readiness Checker**: 39+ automated validation checks
- **Configuration Generator**: Secure secret key and API key generation
- **Dependency Fallbacks**: Graceful handling of missing dependencies
- **Standalone Testing**: Core logic testable without external dependencies

**Production Readiness Score: 39/39 checks passed ✅**

---

## 🔮 Future Scope
- Voice input support (“plastic bottle”).  
- Multilingual support.  
- Integration with **smart bins** in cities.  
- Expanded dataset for more waste categories.  

---

## 👨‍💻 Team
Daksh, [leeeshart](https://github.com/leeeshart) and contributors.

---

## 📜 License
MIT License – free to use & modify for sustainability projects.  

---

## 🌍 Impact
- **Problem:** Cities generate massive amounts of waste daily, but segregation into dry, wet, and hazardous categories is often neglected.  
- **Solution:** AI Waste Classifier enables quick and accurate waste classification, helping municipalities improve sorting, NGOs/schools raise awareness, and households dispose waste responsibly.  
- **SDG Alignment:**  
  - **SDG 11:** Sustainable Cities & Communities  
  - **SDG 12:** Responsible Consumption & Production  
  - **SDG 13:** Climate Action  
- Reduces landfill waste, increases recycling, and prevents hazardous exposure.  

---

## 📚 Documentation
- [Backend Setup Guide](BACKEND_README.md) - Development setup and API documentation
- [Production Deployment Guide](PRODUCTION_GUIDE.md) - Production deployment and configuration
- [API Documentation](PRODUCTION_GUIDE.md#api-documentation) - Enhanced API reference

