import React from 'react';

const FutureVision = ({ onNavigate }) => {
  const features = [
    {
      icon: '🌐',
      title: 'Multi-language Support',
      description: 'Breaking language barriers to make waste management accessible to everyone, everywhere.'
    },
    {
      icon: '🎮',
      title: 'Gamification & Eco-points',
      description: 'Earn points, unlock achievements, and compete with friends while saving the planet.'
    },
    {
      icon: '🗺️',
      title: 'Municipal Bin Locator',
      description: 'Find the nearest recycling bins, composting centers, and hazardous waste drop-offs in your area.'
    }
  ];

  return (
    <div className="min-h-screen bg-gradient-to-br from-green-500 via-green-400 to-blue-500 flex flex-col items-center justify-center px-6 py-8 relative overflow-hidden">
      {/* Background Pattern */}
      <div className="absolute inset-0 opacity-10">
        <div className="absolute top-20 left-20 w-32 h-32 bg-white rounded-full"></div>
        <div className="absolute bottom-20 right-20 w-24 h-24 bg-white rounded-full"></div>
        <div className="absolute top-1/2 left-10 w-16 h-16 bg-white rounded-full"></div>
        <div className="absolute top-1/3 right-10 w-20 h-20 bg-white rounded-full"></div>
      </div>

              {/* Navigation */}
        <div className="absolute top-6 left-6 z-20">
          <button
            onClick={() => onNavigate('home')}
            className="text-white hover:text-gray-200 font-medium flex items-center space-x-2 transition-colors bg-black/20 hover:bg-black/30 px-3 py-2 rounded-lg"
          >
            <span>←</span>
            <span>Back to Home</span>
          </button>
        </div>

      {/* Main Content */}
      <div className="text-center z-10 max-w-6xl mx-auto">
        {/* Title */}
        <div className="mb-16">
          <h1 className="text-5xl md:text-6xl font-bold text-white mb-6 drop-shadow-lg">
            EcoSort – Towards Cleaner Cities 🌍
          </h1>
          <p className="text-xl md:text-2xl text-white/90 font-medium max-w-3xl mx-auto leading-relaxed">
            Empowering communities with AI-driven waste management solutions for a sustainable tomorrow
          </p>
        </div>

        {/* Feature Cards */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8 mb-16">
          {features.map((feature, index) => (
            <div
              key={index}
              className="bg-white/10 backdrop-blur-sm rounded-2xl p-8 border border-white/20 hover:bg-white/20 transition-all duration-300 transform hover:scale-105 hover:shadow-2xl"
            >
              {/* Icon */}
              <div className="text-6xl mb-6 drop-shadow-lg animate-pulse">
                {feature.icon}
              </div>
              
              {/* Title */}
              <h3 className="text-2xl font-bold text-white mb-4 drop-shadow-md">
                {feature.title}
              </h3>
              
              {/* Description */}
              <p className="text-white/90 leading-relaxed">
                {feature.description}
              </p>
            </div>
          ))}
        </div>

        {/* Call to Action */}
        <div className="bg-white/20 backdrop-blur-sm rounded-2xl p-8 border border-white/30 max-w-2xl mx-auto">
          <h2 className="text-3xl font-bold text-white mb-4">
            Join the Revolution 🚀
          </h2>
          <p className="text-white/90 mb-6 text-lg">
            Be part of the movement that's transforming how cities handle waste. 
            Every scan, every classification, every action brings us closer to a cleaner world.
          </p>
          <button
            onClick={() => onNavigate('home')}
            className="bg-white text-green-600 hover:bg-gray-100 font-bold py-4 px-8 rounded-xl transition-all duration-300 transform hover:scale-105 shadow-lg"
          >
            Start Making a Difference
          </button>
        </div>

        {/* Footer */}
        <div className="mt-16 text-center">
          <p className="text-white/70 text-lg">
            Together, we can build cities that thrive in harmony with nature ✨
          </p>
        </div>
      </div>
    </div>
  );
};

export default FutureVision;
