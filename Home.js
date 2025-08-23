import React from 'react';
import Lottie from 'lottie-react';
import ecoAnimation from './assets/Animation.json';

const Home = ({ onNavigate }) => {
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

      {/* Main Action Buttons */}
      <div className="space-y-5 w-full max-w-md">
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
      <div className="mt-6 text-center space-y-3 z-10">
        <button
          onClick={() => onNavigate('history')}
          className="text-white hover:text-blue-200 font-medium text-lg block w-full transition-colors"
        >
          View History & Stats 📊
        </button>
        <button
          onClick={() => onNavigate('futureVision')}
          className="text-white hover:text-green-200 font-medium text-lg block w-full transition-colors"
        >
          Future Vision 🌍
        </button>
      </div>

      {/* Footer */}
      <div className="mt-8 text-center z-10">
        <p className="text-sm text-white/70">
          EcoSort © 2025 – AI for Sustainable Cities (SDG 11)
        </p>
      </div>
    </div>
  );
};

export default Home;
