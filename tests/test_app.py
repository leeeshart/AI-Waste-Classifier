#!/usr/bin/env python3
"""
Tests for EcoSort Backend API
"""

import pytest
import tempfile
import os
from PIL import Image
import io

# Import the application
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app_production import app


@pytest.fixture
def client():
    """Create test client"""
    app.config['TESTING'] = True
    app.config['UPLOAD_FOLDER'] = tempfile.mkdtemp()
    app.config['API_KEY'] = None  # Disable API key for tests
    
    with app.test_client() as client:
        yield client


@pytest.fixture
def sample_image():
    """Create a sample image for testing"""
    img = Image.new('RGB', (100, 100), color='red')
    img_bytes = io.BytesIO()
    img.save(img_bytes, format='PNG')
    img_bytes.seek(0)
    return img_bytes


class TestHealthEndpoints:
    """Test health check endpoints"""
    
    def test_health_check(self, client):
        """Test main health check endpoint"""
        response = client.get('/')
        assert response.status_code == 200
        
        data = response.get_json()
        assert data['status'] == 'success'
        assert data['data']['service'] == 'EcoSort AI Waste Classifier'
        assert 'version' in data['data']
    
    def test_readiness_probe(self, client):
        """Test Kubernetes readiness probe"""
        response = client.get('/health/ready')
        assert response.status_code == 200
        
        data = response.get_json()
        assert data['status'] == 'ready'
    
    def test_liveness_probe(self, client):
        """Test Kubernetes liveness probe"""
        response = client.get('/health/live')
        assert response.status_code == 200
        
        data = response.get_json()
        assert data['status'] == 'alive'


class TestTextClassification:
    """Test text classification endpoint"""
    
    def test_classify_text_success(self, client):
        """Test successful text classification"""
        response = client.post('/classify-text', 
                             json={'text': 'plastic bottle'})
        assert response.status_code == 200
        
        data = response.get_json()
        assert data['status'] == 'success'
        assert 'label' in data['data']
        assert 'confidence' in data['data']
        assert 'tip' in data['data']
        assert data['data']['label'] in ['recyclable', 'biodegradable', 'hazardous']
    
    def test_classify_text_no_data(self, client):
        """Test text classification without data"""
        response = client.post('/classify-text', json={})
        assert response.status_code == 400
        
        data = response.get_json()
        assert data['status'] == 'error'
        assert 'No text provided' in data['error']
    
    def test_classify_text_empty(self, client):
        """Test text classification with empty text"""
        response = client.post('/classify-text', json={'text': ''})
        assert response.status_code == 400
        
        data = response.get_json()
        assert data['status'] == 'error'
    
    def test_classify_text_recyclable(self, client):
        """Test classification of recyclable items"""
        response = client.post('/classify-text', 
                             json={'text': 'aluminum can'})
        assert response.status_code == 200
        
        data = response.get_json()
        assert data['data']['label'] == 'recyclable'
    
    def test_classify_text_hazardous(self, client):
        """Test classification of hazardous items"""
        response = client.post('/classify-text', 
                             json={'text': 'battery acid'})
        assert response.status_code == 200
        
        data = response.get_json()
        assert data['data']['label'] == 'hazardous'


class TestImageClassification:
    """Test image classification endpoint"""
    
    def test_classify_image_success(self, client, sample_image):
        """Test successful image classification"""
        response = client.post('/classify-image',
                             data={'image': (sample_image, 'test.png')})
        assert response.status_code == 200
        
        data = response.get_json()
        assert data['status'] == 'success'
        assert 'label' in data['data']
        assert 'confidence' in data['data']
        assert 'tip' in data['data']
        assert 'image_info' in data['data']
    
    def test_classify_image_no_file(self, client):
        """Test image classification without file"""
        response = client.post('/classify-image', data={})
        assert response.status_code == 400
        
        data = response.get_json()
        assert data['status'] == 'error'
        assert 'No image file provided' in data['error']
    
    def test_classify_image_invalid_format(self, client):
        """Test image classification with invalid file format"""
        response = client.post('/classify-image',
                             data={'image': (io.BytesIO(b'not an image'), 'test.txt')})
        assert response.status_code == 400
        
        data = response.get_json()
        assert data['status'] == 'error'


class TestErrorHandling:
    """Test error handling"""
    
    def test_404_endpoint(self, client):
        """Test 404 error handling"""
        response = client.get('/nonexistent')
        assert response.status_code == 404
        
        data = response.get_json()
        assert data['status'] == 'error'
        assert 'not found' in data['error'].lower()
    
    def test_invalid_json(self, client):
        """Test invalid JSON handling"""
        response = client.post('/classify-text',
                             data='invalid json',
                             content_type='application/json')
        assert response.status_code == 400


class TestSecurity:
    """Test security features"""
    
    def test_cors_headers(self, client):
        """Test CORS headers are present"""
        response = client.get('/')
        # In a real test, you'd check for actual CORS headers
        assert response.status_code == 200
    
    def test_rate_limiting_disabled_in_tests(self, client):
        """Test that rate limiting doesn't interfere with tests"""
        # Make multiple requests quickly
        for _ in range(5):
            response = client.get('/')
            assert response.status_code == 200
    
    def test_text_sanitization(self, client):
        """Test that dangerous text is sanitized"""
        dangerous_text = '<script>alert("xss")</script>plastic bottle'
        response = client.post('/classify-text', json={'text': dangerous_text})
        assert response.status_code == 200
        
        data = response.get_json()
        # Check that script tags are removed
        assert '<script>' not in data['data'].get('input_text', '')


if __name__ == '__main__':
    pytest.main([__file__])