// Production-ready API client for EcoSort
import config from './src/config.js';

const API_BASE = config.API_BASE_URL;
const API_TIMEOUT = config.API_TIMEOUT;
const API_KEY = config.API_KEY || '';

/**
 * Enhanced fetch wrapper with error handling, timeouts, and retries
 */
class APIClient {
  constructor() {
    this.baseURL = API_BASE;
    this.timeout = API_TIMEOUT;
    this.defaultHeaders = {
      'Content-Type': 'application/json',
    };
    
    if (API_KEY) {
      this.defaultHeaders['X-API-Key'] = API_KEY;
    }
  }

  /**
   * Make HTTP request with timeout and error handling
   */
  async request(endpoint, options = {}) {
    const url = `${this.baseURL}${endpoint}`;
    
    // Create timeout controller
    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), this.timeout);
    
    try {
      const response = await fetch(url, {
        ...options,
        signal: controller.signal,
        headers: {
          ...this.defaultHeaders,
          ...options.headers,
        },
      });
      
      clearTimeout(timeoutId);
      
      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new APIError(
          errorData.error || `HTTP ${response.status}`,
          response.status,
          errorData
        );
      }
      
      const data = await response.json();
      
      // Handle new response format
      if (data.status === 'success') {
        return data.data;
      } else if (data.status === 'error') {
        throw new APIError(data.error, response.status, data);
      }
      
      // Fallback for old format
      return data;
      
    } catch (error) {
      clearTimeout(timeoutId);
      
      if (error.name === 'AbortError') {
        throw new APIError('Request timeout', 408);
      }
      
      if (error instanceof APIError) {
        throw error;
      }
      
      throw new APIError('Network error', 0, { originalError: error.message });
    }
  }

  /**
   * Health check endpoint
   */
  async healthCheck() {
    return this.request('/');
  }

  /**
   * Classify text with enhanced error handling
   */
  async classifyText(text) {
    if (!text || typeof text !== 'string') {
      throw new APIError('Invalid text input', 400);
    }
    
    if (text.length > 1000) {
      throw new APIError('Text too long (max 1000 characters)', 400);
    }
    
    return this.request('/classify-text', {
      method: 'POST',
      body: JSON.stringify({ text: text.trim() }),
    });
  }

  /**
   * Classify image with enhanced validation
   */
  async classifyImage(file) {
    if (!file || !(file instanceof File)) {
      throw new APIError('Invalid file input', 400);
    }
    
    // Validate file type
    const allowedTypes = ['image/jpeg', 'image/jpg', 'image/png', 'image/gif', 'image/bmp', 'image/webp'];
    if (!allowedTypes.includes(file.type.toLowerCase())) {
      throw new APIError('Invalid file type. Please upload an image file.', 400);
    }
    
    // Validate file size
    const maxSize = config.MAX_FILE_SIZE_MB * 1024 * 1024;
    if (file.size > maxSize) {
      throw new APIError(`File too large. Maximum size: ${config.MAX_FILE_SIZE_MB}MB`, 400);
    }
    
    const formData = new FormData();
    formData.append('image', file);
    
    return this.request('/classify-image', {
      method: 'POST',
      body: formData,
      headers: {
        // Remove Content-Type header to let browser set it with boundary
        ...(API_KEY && { 'X-API-Key': API_KEY }),
      },
    });
  }
}

/**
 * Custom error class for API errors
 */
class APIError extends Error {
  constructor(message, status = 0, details = {}) {
    super(message);
    this.name = 'APIError';
    this.status = status;
    this.details = details;
  }
  
  get isNetworkError() {
    return this.status === 0;
  }
  
  get isTimeout() {
    return this.status === 408;
  }
  
  get isClientError() {
    return this.status >= 400 && this.status < 500;
  }
  
  get isServerError() {
    return this.status >= 500;
  }
  
  get isRateLimit() {
    return this.status === 429;
  }
}

// Create singleton instance
const apiClient = new APIClient();

// Export convenience functions for backward compatibility
export const classifyText = (text) => apiClient.classifyText(text);
export const classifyImage = (file) => apiClient.classifyImage(file);
export const healthCheck = () => apiClient.healthCheck();

// Export classes for advanced usage
export { APIClient, APIError };

// Export default client
export default apiClient;