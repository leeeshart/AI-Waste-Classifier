# EcoSort Backend Setup Guide

## Overview
The EcoSort backend is a Flask-based API server that provides AI-powered waste classification for both images and text descriptions.

## Installation

### Prerequisites
- Python 3.7+
- pip (Python package manager)

### Quick Setup

1. **Install dependencies:**
   ```bash
   pip install -r requirements_simple.txt
   ```

2. **Start the backend server:**
   ```bash
   python3 app_simple.py
   ```

   The server will start on `http://localhost:5000`

3. **Start the frontend (in a separate terminal):**
   ```bash
   npm install
   npm run dev
   ```

   The frontend will start on `http://localhost:3000`

## API Endpoints

### Health Check
- **URL:** `GET /`
- **Description:** Check if the server is running
- **Response:**
  ```json
  {
    "status": "healthy",
    "service": "EcoSort AI Waste Classifier",
    "version": "1.0.0",
    "timestamp": "2025-08-24T11:24:57.242150"
  }
  ```

### Text Classification
- **URL:** `POST /classify-text`
- **Description:** Classify waste based on text description
- **Request Body:**
  ```json
  {
    "text": "plastic bottle"
  }
  ```
- **Response:**
  ```json
  {
    "label": "recyclable",
    "confidence": 0.8,
    "tip": "Clean the item and place it in the recycling bin. Remove any non-recyclable parts like caps or labels if possible."
  }
  ```

### Image Classification
- **URL:** `POST /classify-image`
- **Description:** Classify waste based on uploaded image
- **Request:** Form data with image file
- **Response:**
  ```json
  {
    "label": "biodegradable",
    "confidence": 0.75,
    "tip": "Compost this item in your garden compost bin or municipal composting facility. It will break down naturally and enrich the soil."
  }
  ```

## Waste Categories

The system classifies waste into three categories:

1. **Recyclable**: Items that can be recycled (plastic, glass, paper, metal)
2. **Biodegradable**: Organic waste that can be composted (food scraps, yard waste)
3. **Hazardous**: Items requiring special disposal (batteries, chemicals, electronics)

## Features

- **Text Classification**: Uses keyword matching to classify waste descriptions
- **Image Classification**: Analyzes uploaded images (currently uses basic heuristics)
- **CORS Support**: Enabled for frontend integration
- **Error Handling**: Comprehensive error responses
- **File Validation**: Checks file types and sizes for image uploads

## Testing

### Test Text Classification
```bash
curl -X POST http://localhost:5000/classify-text \
  -H "Content-Type: application/json" \
  -d '{"text": "banana peel"}'
```

### Test Image Classification
```bash
curl -X POST -F "image=@/path/to/image.jpg" http://localhost:5000/classify-image
```

## Development

### File Structure
```
├── app_simple.py          # Main Flask application (development)
├── app_production.py      # Production Flask application
├── requirements_simple.txt # Basic dependencies
├── requirements.txt       # Full dependencies for production
├── start_backend.sh       # Startup script
└── uploads/               # Directory for uploaded images
```

### Adding New Features

1. **New Keywords**: Edit `WASTE_KEYWORDS` dictionary in `app_simple.py`
2. **Better Image Classification**: Replace the simple classification in `classify_image_content()` with a trained ML model
3. **Database Integration**: Add database support for storing classification history

## Production Deployment

For production, consider:
- Using a production WSGI server (gunicorn, uWSGI)
- Adding authentication and rate limiting
- Using a proper database for storing results
- Implementing caching for better performance
- Adding monitoring and logging

### Example Production Command
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app_simple:app
```

## Troubleshooting

### Common Issues

1. **Port Already in Use**: Change the port in `app_simple.py` line 224
2. **CORS Errors**: Ensure flask-cors is installed and CORS is properly configured
3. **File Upload Errors**: Check file size limits and allowed extensions
4. **Module Not Found**: Make sure all dependencies are installed

### Debug Mode
The server runs in debug mode by default. For production, set `debug=False` in the `app.run()` call.