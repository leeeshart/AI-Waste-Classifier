import React, { useState, useRef } from 'react';
import Lottie from 'lottie-react';
import ecoAnimation from './assets/Animation.json';
import { classifyImage, classifyText } from './api.js';

const Home = ({ onNavigate }) => {
  const [isLoading, setIsLoading] = useState(false);
  const [showTextModal, setShowTextModal] = useState(false);
  const [textInput, setTextInput] = useState('');
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);
  const fileInputRef = useRef(null);

  const handleImageUpload = async (event) => {
    const file = event.target.files[0];
    if (!file) return;

    setIsLoading(true);
    setError(null);
    setResult(null);

    try {
      const data = await classifyImage(file);
      setResult(data);
    } catch (err) {
      setError('Failed to classify image. Please try again.');
      console.error('Image classification error:', err);
    } finally {
      setIsLoading(false);
    }
  };

  const handleTextClassification = async () => {
    if (!textInput.trim()) return;

    setIsLoading(true);
    setError(null);
    setResult(null);

    try {
      const data = await classifyText(textInput.trim());
      setResult(data);
      setShowTextModal(false);
      setTextInput('');
    } catch (err) {
      setError('Failed to classify text. Please try again.');
      console.error('Text classification error:', err);
    } finally {
      setIsLoading(false);
    }
  };

  const getLabelEmoji = (label) => {
    switch (label?.toLowerCase()) {
      case 'recyclable':
        return '♻️';
      case 'biodegradable':
        return '🌱';
      case 'hazardous':
        return '☣️';
      default:
        return '❓';
    }
  };

  const getLabelColor = (label) => {
    switch (label?.toLowerCase()) {
      case 'recyclable':
        return 'border-green-500';
      case 'biodegradable':
        return 'border-yellow-500';
      case 'hazardous':
        return 'border-red-500';
      default:
        return 'border-gray-500';
    }
  };

  const clearResult = () => {
    setResult(null);
    setError(null);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-green-500 via-green-400 to-blue-500 flex flex-col items-center justify-center px-6 py-8 relative overflow-hidden">
      {/* Background Pattern */}
      <div className="absolute inset-0 opacity-10">
        <div className="absolute top-20 left-20 w-32 h-32 bg-white rounded-full"></div>
        <div className="absolute bottom-20 right-20 w-24 h-24 bg-white rounded-full"></div>
        <div className="absolute top-1/2 left-10 w-16 h-16 bg-white rounded-full"></div>
        <div className="absolute top-1/3 right-10 w-20 h-20 bg-white rounded-full"></div>
      </div>

      {/* Lottie Animation */}
      <div className="flex justify-center mb-8 z-10">
        <div className="w-48 sm:w-56 md:w-64">
          <Lottie
            animationData={ecoAnimation}
            autoplay={true}
            loop={true}
            style={{ width: '100%', height: 'auto' }}
          />
        </div>
      </div>

      {/* Header Section */}
      <div className="text-center mb-12 z-10">
        <h1 className="text-5xl font-bold text-white mb-3 drop-shadow-lg tracking-wide">
          EcoSort
        </h1>
        <p className="text-xl text-white/90 font-medium tracking-wide">
          Snap. Classify. Dispose Right.
        </p>
      </div>

      {/* Action Buttons */}
      <div className="flex flex-col sm:flex-row gap-4 mb-8 z-10">
        <button
          onClick={() => fileInputRef.current?.click()}
          disabled={isLoading}
          className="flex items-center space-x-3 bg-green-500 hover:bg-green-600 disabled:bg-green-400 text-white px-8 py-4 rounded-xl text-lg font-semibold shadow-lg hover:shadow-xl transition-all duration-200 transform hover:scale-105"
        >
          <span className="text-2xl">📸</span>
          <span>Upload / Capture Waste Image</span>
        </button>

        <button
          onClick={() => setShowTextModal(true)}
          disabled={isLoading}
          className="flex items-center space-x-3 bg-blue-500 hover:bg-blue-600 disabled:bg-blue-400 text-white px-8 py-4 rounded-xl text-lg font-semibold shadow-lg hover:shadow-xl transition-all duration-200 transform hover:scale-105"
        >
          <span className="text-2xl">⌨️</span>
          <span>Describe an Object</span>
        </button>
      </div>

      {/* Hidden File Input */}
      <input
        ref={fileInputRef}
        type="file"
        accept="image/*"
        onChange={handleImageUpload}
        className="hidden"
      />

      {/* Navigation Buttons */}
      <div className="flex flex-col sm:flex-row gap-4 mb-8 z-10">
        <button
          onClick={() => onNavigate('history')}
          className="bg-white/20 hover:bg-white/30 text-white px-6 py-3 rounded-lg font-medium transition-all duration-200"
        >
          View History & Stats 📊
        </button>
        <button
          onClick={() => onNavigate('futureVision')}
          className="bg-white/20 hover:bg-white/30 text-white px-6 py-3 rounded-lg font-medium transition-all duration-200"
        >
          Future Vision 🌍
        </button>
      </div>

      {/* Loading State */}
      {isLoading && (
        <div className="bg-white/90 backdrop-blur-sm rounded-lg p-6 shadow-lg z-20">
          <div className="flex items-center space-x-3">
            <div className="animate-spin rounded-full h-6 w-6 border-b-2 border-green-500"></div>
            <span className="text-lg font-medium text-gray-700">Analyzing...</span>
          </div>
        </div>
      )}

      {/* Result Card */}
      {result && (
        <div className={`bg-white/95 backdrop-blur-sm rounded-lg p-6 shadow-lg border-l-4 ${getLabelColor(result.label)} z-20 max-w-md w-full`}>
          <div className="flex items-center justify-between mb-4">
            <h3 className="text-xl font-bold text-gray-800">
              {getLabelEmoji(result.label)} {result.label}
            </h3>
            <button
              onClick={clearResult}
              className="text-gray-500 hover:text-gray-700 text-xl"
            >
              ×
            </button>
          </div>
          
          <div className="mb-4">
            <p className="text-sm text-gray-600 mb-2">Confidence:</p>
            <div className="w-full bg-gray-200 rounded-full h-2">
              <div 
                className="bg-green-500 h-2 rounded-full transition-all duration-500"
                style={{ width: `${result.confidence}%` }}
              ></div>
            </div>
            <p className="text-sm text-gray-700 mt-1">{result.confidence}%</p>
          </div>

          <div className="mb-4">
            <p className="text-sm text-gray-600 mb-2">Disposal Tip:</p>
            <p className="text-gray-800">{result.tip}</p>
          </div>

          <button
            onClick={clearResult}
            className="w-full bg-green-500 hover:bg-green-600 text-white py-2 px-4 rounded-lg font-medium transition-colors duration-200"
          >
            Got it!
          </button>
        </div>
      )}

      {/* Error Message */}
      {error && (
        <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded-lg z-20 max-w-md w-full">
          <div className="flex items-center justify-between">
            <span>{error}</span>
            <button
              onClick={clearResult}
              className="text-red-700 hover:text-red-900 text-xl font-bold"
            >
              ×
            </button>
          </div>
        </div>
      )}

      {/* Text Input Modal */}
      {showTextModal && (
        <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4">
          <div className="bg-white rounded-lg p-6 w-full max-w-md">
            <h3 className="text-xl font-bold text-gray-800 mb-4">Describe an Object</h3>
            <input
              type="text"
              value={textInput}
              onChange={(e) => setTextInput(e.target.value)}
              placeholder="Type object name e.g. plastic bottle"
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent mb-4"
              onKeyPress={(e) => e.key === 'Enter' && handleTextClassification()}
            />
            <div className="flex space-x-3">
              <button
                onClick={() => {
                  setShowTextModal(false);
                  setTextInput('');
                }}
                className="flex-1 px-4 py-2 text-gray-600 border border-gray-300 rounded-lg hover:bg-gray-50 transition-colors duration-200"
              >
                Cancel
              </button>
              <button
                onClick={handleTextClassification}
                disabled={!textInput.trim() || isLoading}
                className="flex-1 px-4 py-2 bg-blue-500 hover:bg-blue-600 disabled:bg-blue-300 text-white rounded-lg font-medium transition-colors duration-200"
              >
                Classify
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Footer */}
      <div className="text-center mt-8 z-10">
        <p className="text-white/70 text-sm">
          EcoSort © 2025 – AI for Sustainable Cities (SDG 11)
        </p>
      </div>
    </div>
  );
};

export default Home;
