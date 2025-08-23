import React, { useState } from 'react';

const ImageUpload = ({ onNavigate }) => {
  const [selectedFile, setSelectedFile] = useState(null);
  const [previewUrl, setPreviewUrl] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);

  const handleFileSelect = (event) => {
    const file = event.target.files[0];
    if (file) {
      setSelectedFile(file);
      setPreviewUrl(URL.createObjectURL(file));
      setResult(null);
      setError(null);
    }
  };

  const getLabelEmoji = (label) => {
    switch (label.toLowerCase()) {
      case 'recyclable':
        return '♻️';
      case 'biodegradable':
        return '🌱';
      case 'hazardous':
        return '☣️';
      default:
        return '♻️';
    }
  };

  const getBorderColor = (label) => {
    switch (label.toLowerCase()) {
      case 'recyclable':
        return 'border-l-green-500';
      case 'biodegradable':
        return 'border-l-yellow-500';
      case 'hazardous':
        return 'border-l-red-500';
      default:
        return 'border-l-gray-500';
    }
  };

  const getDisposalTipHindi = (label) => {
    switch (label.toLowerCase()) {
      case 'recyclable':
        return 'इसे रीसाइक्लिंग बिन में डालें';
      case 'biodegradable':
        return 'इसे कंपोस्ट बिन में डालें';
      case 'hazardous':
        return 'इसे विशेष हानिकारक अपशिष्ट संग्रह केंद्र में ले जाएं';
      default:
        return 'उचित निपटान के लिए स्थानीय नियमों की जांच करें';
    }
  };

  const handleClassify = async () => {
    if (!selectedFile) {
      setError('Please select an image first');
      return;
    }

    setIsLoading(true);
    setError(null);

    try {
      const formData = new FormData();
      formData.append('image', selectedFile);

      const response = await fetch('http://localhost:3000/classify-image', {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      setResult(data);
    } catch (err) {
      setError('Failed to classify image. Please try again.');
      console.error('Classification error:', err);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-green-500 via-green-400 to-blue-500 p-6 relative overflow-hidden">
      <div className="max-w-2xl mx-auto">
        {/* Background Pattern */}
        <div className="absolute inset-0 opacity-10">
          <div className="absolute top-20 left-20 w-32 h-32 bg-white rounded-full"></div>
          <div className="absolute bottom-20 right-20 w-24 h-24 bg-white rounded-full"></div>
          <div className="absolute top-1/2 left-10 w-16 h-16 bg-white rounded-full"></div>
          <div className="absolute top-1/3 right-10 w-20 h-20 bg-white rounded-full"></div>
        </div>

        {/* Header */}
        <div className="text-center mb-8 z-10">
          <div className="flex items-center justify-center mb-4 relative">
            <button
              onClick={() => onNavigate('home')}
              className="absolute left-0 text-white hover:text-blue-200 font-medium flex items-center space-x-2 transition-colors bg-black/20 hover:bg-black/30 px-3 py-2 rounded-lg"
            >
              <span>←</span>
              <span>Back to Home</span>
            </button>
          </div>
          <h1 className="text-4xl font-bold text-white mb-2 drop-shadow-lg">
            Upload Waste Image ♻️
          </h1>
        </div>

        {/* Upload Card */}
        <div className="bg-white rounded-xl border border-gray-200 shadow-lg p-8 mb-8">
          <div className="space-y-6">
            {/* File Input */}
            <div className="border-2 border-dashed border-gray-300 rounded-xl p-8 text-center hover:border-green-400 transition-colors">
              <input
                type="file"
                accept="image/*"
                onChange={handleFileSelect}
                className="hidden"
                id="file-upload"
              />
              <label
                htmlFor="file-upload"
                className="cursor-pointer flex flex-col items-center space-y-4"
              >
                <div className="text-4xl">📁</div>
                <div className="text-lg font-medium text-gray-700">
                  {selectedFile ? selectedFile.name : 'Click to select image or drag and drop'}
                </div>
                <div className="text-sm text-gray-500">
                  Supports: JPG, PNG, GIF
                </div>
              </label>
            </div>

            {/* Image Preview */}
            {previewUrl && (
              <div className="text-center">
                <img
                  src={previewUrl}
                  alt="Preview"
                  className="max-w-full h-64 object-contain rounded-lg border border-gray-200"
                />
              </div>
            )}

            {/* Classify Button */}
            <button
              onClick={handleClassify}
              disabled={!selectedFile || isLoading}
              className={`w-full py-4 px-8 rounded-xl font-semibold text-lg transition-all duration-300 ${
                !selectedFile || isLoading
                  ? 'bg-gray-400 cursor-not-allowed'
                  : 'bg-green-500 hover:bg-green-600 hover:shadow-lg transform hover:scale-105'
              } text-white`}
            >
              {isLoading ? 'Classifying...' : 'Classify'}
            </button>
          </div>
        </div>

        {/* Error Display */}
        {error && (
          <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded-xl mb-6">
            {error}
          </div>
        )}

        {/* Result Card */}
        {result && (
          <div className={`bg-white rounded-xl shadow-lg border-l-4 ${getBorderColor(result.label)} p-8`}>
            <div className="space-y-6">
              {/* Label */}
              <div className="text-center">
                <div className="text-6xl mb-4">{getLabelEmoji(result.label)}</div>
                <h2 className="text-3xl font-bold text-gray-800 mb-2">
                  {result.label}
                </h2>
                <div className="text-lg text-gray-600">
                  Confidence: {Math.round(result.confidence * 100)}%
                </div>
              </div>

              {/* Disposal Tips */}
              <div className="space-y-4">
                <div className="bg-gray-50 rounded-lg p-4">
                  <h3 className="font-semibold text-gray-800 mb-2">English Tip:</h3>
                  <p className="text-gray-700">{result.tip}</p>
                </div>
                <div className="bg-gray-50 rounded-lg p-4">
                  <h3 className="font-semibold text-gray-800 mb-2">Hindi Tip:</h3>
                  <p className="text-gray-700">{getDisposalTipHindi(result.label)}</p>
                </div>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default ImageUpload;
