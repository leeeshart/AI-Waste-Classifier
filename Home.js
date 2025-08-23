import React from 'react';

const Home = ({ onNavigate }) => {
  return (
    <div className="min-h-screen bg-gray-50 flex flex-col items-center justify-center px-6 py-8">
      {/* Header Section */}
      <div className="text-center mb-16">
        <h1 className="text-5xl font-bold text-gray-800 mb-4">
          EcoSort ♻️
        </h1>
        <p className="text-xl text-gray-600 font-medium">
          Snap. Classify. Dispose Right.
        </p>
      </div>

      {/* Main Action Buttons */}
      <div className="space-y-6 w-full max-w-md">
        {/* Upload/Capture Button */}
        <button 
          onClick={() => onNavigate('imageUpload')}
          className="w-full bg-green-500 hover:bg-green-600 text-white font-semibold py-6 px-8 rounded-xl shadow-lg hover:shadow-xl transition-all duration-300 transform hover:scale-105 flex items-center justify-center space-x-3"
        >
          <span className="text-2xl">📸</span>
          <span className="text-lg">Upload / Capture Waste Image</span>
        </button>

        {/* Describe Object Button */}
        <button 
          onClick={() => onNavigate('textClassify')}
          className="w-full bg-blue-500 hover:bg-blue-600 text-white font-semibold py-6 px-8 rounded-xl shadow-lg hover:shadow-xl transition-all duration-300 transform hover:scale-105 flex items-center justify-center space-x-3"
        >
          <span className="text-2xl">⌨️</span>
          <span className="text-lg">Describe an Object</span>
        </button>
      </div>

      {/* Navigation Menu */}
      <div className="mt-8 text-center space-y-4">
        <button
          onClick={() => onNavigate('history')}
          className="text-blue-600 hover:text-blue-800 font-medium text-lg block w-full"
        >
          View History & Stats 📊
        </button>
        <button
          onClick={() => onNavigate('futureVision')}
          className="text-green-600 hover:text-green-800 font-medium text-lg block w-full"
        >
          Future Vision 🌍
        </button>
      </div>

      {/* Footer */}
      <div className="mt-8 text-center">
        <p className="text-sm text-gray-500">
          EcoSort © 2025 – AI for Sustainable Cities (SDG 11)
        </p>
      </div>
    </div>
  );
};

export default Home;
