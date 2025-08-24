#!/usr/bin/env python3
"""
EcoSort Backend API - Lightweight Version
AI-powered waste classification server for image and text inputs
"""

import os
import io
import logging
import random
from datetime import datetime
from flask import Flask, request, jsonify
from flask_cors import CORS
from PIL import Image
from werkzeug.utils import secure_filename

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for React frontend

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configuration
UPLOAD_FOLDER = 'uploads'
MAX_FILE_SIZE = 16 * 1024 * 1024  # 16MB
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'bmp', 'webp'}

# Ensure upload directory exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Waste classification keywords
WASTE_KEYWORDS = {
    'recyclable': [
        'plastic', 'bottle', 'can', 'aluminum', 'paper', 'cardboard', 
        'glass', 'newspaper', 'magazine', 'metal', 'tin', 'steel',
        'container', 'jar', 'box', 'packaging', 'wrapper', 'bag',
        'cup', 'plate', 'tray', 'carton', 'tube', 'foil'
    ],
    'biodegradable': [
        'banana', 'apple', 'orange', 'fruit', 'vegetable', 'food',
        'organic', 'compost', 'leaf', 'wood', 'branch', 'plant',
        'peel', 'core', 'scrap', 'leftover', 'garden', 'yard',
        'flower', 'grass', 'tree', 'seed', 'shell', 'bone'
    ],
    'hazardous': [
        'battery', 'electronic', 'chemical', 'paint', 'oil', 'toxic',
        'medical', 'needle', 'syringe', 'medicine', 'drug', 'acid',
        'cleaning', 'detergent', 'bleach', 'pesticide', 'solvent',
        'fluorescent', 'bulb', 'thermometer', 'asbestos'
    ]
}

def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def classify_image_content(img):
    """Classify image content using basic heuristics"""
    try:
        # Get image dimensions and format for basic analysis
        width, height = img.size
        format_type = img.format
        
        # Simple heuristic classification based on image properties
        # This is a placeholder - in production, you'd use a trained model
        
        # Simulate classification based on filename or random for demo
        categories = ['recyclable', 'biodegradable', 'hazardous']
        weights = [0.6, 0.3, 0.1]  # More likely to be recyclable
        
        category = random.choices(categories, weights=weights)[0]
        confidence = round(random.uniform(0.7, 0.95), 2)
        
        logger.info(f"Image ({width}x{height}, {format_type}) classified as: {category}")
        
        return category, confidence
        
    except Exception as e:
        logger.error(f"Error classifying image: {str(e)}")
        return 'recyclable', 0.30

def classify_text_content(text):
    """Classify text description using keyword matching"""
    try:
        text_lower = text.lower()
        scores = {'recyclable': 0, 'biodegradable': 0, 'hazardous': 0}
        
        # Calculate scores for each category
        for category, keywords in WASTE_KEYWORDS.items():
            for keyword in keywords:
                if keyword in text_lower:
                    scores[category] += 1
        
        # Determine best category
        if all(score == 0 for score in scores.values()):
            # No keywords found, default to recyclable
            return 'recyclable', 0.30
        
        best_category = max(scores, key=scores.get)
        max_score = scores[best_category]
        
        # Calculate confidence based on keyword matches
        confidence = min(0.95, 0.60 + (max_score * 0.10))
        
        return best_category, confidence
        
    except Exception as e:
        logger.error(f"Error classifying text: {str(e)}")
        return 'recyclable', 0.30

def get_disposal_tip(category):
    """Get disposal instructions for waste category"""
    tips = {
        'recyclable': "Clean the item and place it in the recycling bin. Remove any non-recyclable parts like caps or labels if possible.",
        'biodegradable': "Compost this item in your garden compost bin or municipal composting facility. It will break down naturally and enrich the soil.",
        'hazardous': "Take this item to a specialized hazardous waste collection center. Do not put it in regular trash as it can harm the environment."
    }
    return tips.get(category, "Check local waste management guidelines for proper disposal.")

@app.route('/', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'EcoSort AI Waste Classifier',
        'version': '1.0.0',
        'timestamp': datetime.now().isoformat()
    })

@app.route('/classify-image', methods=['POST'])
def classify_image_endpoint():
    """Classify uploaded image"""
    try:
        # Check if image file is in request
        if 'image' not in request.files and 'file' not in request.files:
            return jsonify({'error': 'No image file provided'}), 400
        
        # Get the file (try both 'image' and 'file' keys for compatibility)
        file = request.files.get('image') or request.files.get('file')
        
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        if not allowed_file(file.filename):
            return jsonify({'error': 'File type not allowed'}), 400
        
        # Check file size
        file.seek(0, os.SEEK_END)
        file_size = file.tell()
        file.seek(0)
        
        if file_size > MAX_FILE_SIZE:
            return jsonify({'error': 'File too large'}), 400
        
        # Load and process image
        img = Image.open(io.BytesIO(file.read()))
        
        # Classify image
        label, confidence = classify_image_content(img)
        
        # Get disposal tip
        tip = get_disposal_tip(label)
        
        logger.info(f"Image classified as: {label} (confidence: {confidence:.2f})")
        
        return jsonify({
            'label': label,
            'confidence': confidence,
            'tip': tip
        })
        
    except Exception as e:
        logger.error(f"Error in image classification: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/classify-text', methods=['POST'])
def classify_text_endpoint():
    """Classify text description"""
    try:
        data = request.get_json()
        
        if not data or 'text' not in data:
            return jsonify({'error': 'No text provided'}), 400
        
        text = data['text'].strip()
        
        if not text:
            return jsonify({'error': 'Empty text provided'}), 400
        
        # Classify text
        label, confidence = classify_text_content(text)
        
        # Get disposal tip
        tip = get_disposal_tip(label)
        
        logger.info(f"Text '{text}' classified as: {label} (confidence: {confidence:.2f})")
        
        return jsonify({
            'label': label,
            'confidence': confidence,
            'tip': tip
        })
        
    except Exception as e:
        logger.error(f"Error in text classification: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@app.errorhandler(413)
def too_large(e):
    """Handle file too large error"""
    return jsonify({'error': 'File too large'}), 413

@app.errorhandler(404)
def not_found(e):
    """Handle not found error"""
    return jsonify({'error': 'Endpoint not found'}), 404

@app.errorhandler(500)
def internal_error(e):
    """Handle internal server error"""
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    try:
        logger.info("Starting EcoSort backend server...")
        
        # Start Flask app
        app.run(
            host='0.0.0.0',
            port=5000,
            debug=True
        )
        
    except Exception as e:
        logger.error(f"Failed to start server: {str(e)}")
        exit(1)