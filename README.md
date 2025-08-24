# ♻️ EcoSort 
### AI-Powered Waste Classification for Sustainable Cities

An intelligent solution to classify waste as **Recyclable, Biodegradable, or Hazardous** using image uploads or text descriptions. Built to support SDG 11 (Sustainable Cities & Communities).

## 🚀 Features
- **Image Classification**: Upload waste images for AI-powered categorization
- **Text Classification**: Enter waste descriptions for instant classification  
- **Smart Disposal Tips**: Get category-specific disposal instructions
- **Full-Stack Application**: React frontend + Flask backend
- **Fast & Lightweight**: Optimized for web and mobile devices

## 🛠️ Tech Stack
- **Frontend**: React.js + Vite
- **Backend**: Flask API with CORS support  
- **AI Classification**: Keyword-based text analysis + extensible image processing
- **Deployment**: Docker + local development setup

## 🚀 Quick Start

### Prerequisites
- Node.js 16+ and npm
- Python 3.7+

### Setup Instructions

1. **Clone and setup:**
   ```bash
   git clone https://github.com/leeeshart/AI-Waste-Classifier.git
   cd AI-Waste-Classifier
   pip install -r requirements_simple.txt
   npm install
   ```

2. **Start the application:**
   ```bash
   # Terminal 1: Start backend
   python3 app_simple.py
   
   # Terminal 2: Start frontend  
   npm run dev
   ```

3. **Access the application:**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:5000

## ⚙️ How It Works
1. **Input**: User uploads an image or enters waste description
2. **Processing**: Flask backend analyzes the input using keyword matching (text) or image analysis  
3. **Classification**: System returns waste category with confidence score and disposal tips
4. **Display**: Frontend shows results with icons and disposal instructions

## 📁 Project Structure
```
├── Frontend Components
│   ├── App.jsx                 # Main app component
│   ├── Home.jsx                # Landing page
│   ├── ImageUpload.jsx         # Image classification interface
│   ├── TextClassify.jsx        # Text classification interface
│   ├── History.jsx             # Classification history
│   ├── FutureVision.jsx        # Future features showcase
│   └── api.js                  # API communication layer
├── Backend
│   ├── app_simple.py           # Main Flask server
│   ├── app_production.py       # Production-ready server
│   ├── security.py             # Security utilities
│   └── monitoring.py           # Application monitoring
├── Configuration
│   ├── package.json            # Node.js dependencies
│   ├── requirements_simple.txt # Basic Python dependencies  
│   ├── requirements.txt        # Full Python dependencies
│   ├── docker-compose.yml      # Docker configuration
│   └── vite.config.js          # Vite build configuration
└── Documentation
    ├── README.md               # This file
    ├── BACKEND_README.md       # Backend setup guide
    └── PRODUCTION_GUIDE.md     # Production deployment guide
```

## 🔧 API Endpoints

### Text Classification
```bash
POST /classify-text
Content-Type: application/json

{"text": "plastic bottle"}
```

### Image Classification  
```bash
POST /classify-image
Content-Type: multipart/form-data

image: <file>
```

**Response Format:**
```json
{
  "label": "recyclable|biodegradable|hazardous",
  "confidence": 0.8,
  "tip": "Disposal instructions..."
}
```

> 📚 For detailed API documentation, see [Production Guide](PRODUCTION_GUIDE.md#api-documentation)

## 🚀 Production Deployment

For production deployment with Docker, security features, monitoring, and scaling:

```bash
git clone https://github.com/leeeshart/AI-Waste-Classifier.git
cd AI-Waste-Classifier
./deploy.sh production
```

**Production Features:**
- API authentication & rate limiting
- Docker containerization with health checks
- Monitoring & structured logging  
- Load balancing with Nginx

> 📚 Complete production guide: [PRODUCTION_GUIDE.md](PRODUCTION_GUIDE.md)

## 🔮 Future Scope
- Voice input support and multilingual classification
- Integration with smart city waste management systems  
- Expanded ML models for more waste categories
- Mobile app development

## 👨‍💻 Contributors
Built by [leeeshart](https://github.com/leeeshart) and contributors for sustainable waste management.

## 🌍 Impact
**Problem**: Poor waste segregation in cities leads to environmental issues and inefficient resource management.

**Solution**: AI-powered classification enables:
- Better waste sorting for municipalities  
- Educational awareness for schools and communities
- Responsible disposal practices for households

**SDG Alignment**: Supports UN Sustainable Development Goals 11 (Sustainable Cities), 12 (Responsible Consumption), and 13 (Climate Action).

## 📚 Documentation
- [Backend Setup Guide](BACKEND_README.md) - Development setup and API documentation
- [Production Deployment Guide](PRODUCTION_GUIDE.md) - Production deployment and configuration

## 📜 License
MIT License – free to use and modify for sustainability projects.

