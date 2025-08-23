import React, { useState, useEffect } from 'react';
import { PieChart, Pie, Cell, ResponsiveContainer, Legend, Tooltip } from 'recharts';

const History = ({ onNavigate }) => {
  const [historyData, setHistoryData] = useState([]);
  const [isLoading, setIsLoading] = useState(true);

  // Mock data for demonstration - replace with actual API call
  useEffect(() => {
    // Simulate API call to fetch history data
    const fetchHistoryData = async () => {
      try {
        // Mock data - replace with actual API endpoint
        const mockData = [
          {
            id: 1,
            label: 'recyclable',
            confidence: 0.95,
            imageUrl: 'https://via.placeholder.com/80x80/2ECC71/FFFFFF?text=♻️',
            timestamp: '2025-01-15T10:30:00Z'
          },
          {
            id: 2,
            label: 'biodegradable',
            confidence: 0.87,
            imageUrl: 'https://via.placeholder.com/80x80/F1C40F/FFFFFF?text=🌱',
            timestamp: '2025-01-15T09:15:00Z'
          },
          {
            id: 3,
            label: 'hazardous',
            confidence: 0.92,
            imageUrl: 'https://via.placeholder.com/80x80/E74C3C/FFFFFF?text=☣️',
            timestamp: '2025-01-15T08:45:00Z'
          },
          {
            id: 4,
            label: 'recyclable',
            confidence: 0.78,
            imageUrl: 'https://via.placeholder.com/80x80/2ECC71/FFFFFF?text=♻️',
            timestamp: '2025-01-15T07:20:00Z'
          },
          {
            id: 5,
            label: 'biodegradable',
            confidence: 0.91,
            imageUrl: 'https://via.placeholder.com/80x80/F1C40F/FFFFFF?text=🌱',
            timestamp: '2025-01-15T06:30:00Z'
          }
        ];
        
        setHistoryData(mockData);
      } catch (error) {
        console.error('Failed to fetch history data:', error);
      } finally {
        setIsLoading(false);
      }
    };

    fetchHistoryData();
  }, []);

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

  const getLabelColor = (label) => {
    switch (label.toLowerCase()) {
      case 'recyclable':
        return '#2ECC71';
      case 'biodegradable':
        return '#F1C40F';
      case 'hazardous':
        return '#E74C3C';
      default:
        return '#95A5A6';
    }
  };

  const formatTimestamp = (timestamp) => {
    const date = new Date(timestamp);
    return date.toLocaleDateString('en-US', {
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    });
  };

  // Prepare data for pie chart
  const pieChartData = historyData.reduce((acc, item) => {
    const existing = acc.find(d => d.name === item.label);
    if (existing) {
      existing.value += 1;
    } else {
      acc.push({ name: item.label, value: 1 });
    }
    return acc;
  }, []);

  const COLORS = ['#2ECC71', '#F1C40F', '#E74C3C'];

  if (isLoading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500 mx-auto mb-4"></div>
          <p className="text-gray-600">Loading history...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-green-500 via-green-400 to-blue-500 p-6 relative overflow-hidden">
      <div className="max-w-4xl mx-auto">
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
            History & Stats 📊
          </h1>
        </div>

        {/* Pie Chart Section */}
        <div className="bg-white rounded-xl border border-gray-200 shadow-lg p-8 mb-8">
          <h2 className="text-2xl font-semibold text-gray-800 mb-6 text-center">
            Last 5 Scans Summary
          </h2>
          <div className="h-80">
            <ResponsiveContainer width="100%" height="100%">
              <PieChart>
                <Pie
                  data={pieChartData}
                  cx="50%"
                  cy="50%"
                  labelLine={false}
                  label={({ name, percent }) => `${name} ${(percent * 100).toFixed(0)}%`}
                  outerRadius={80}
                  fill="#8884d8"
                  dataKey="value"
                >
                  {pieChartData.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                  ))}
                </Pie>
                <Tooltip />
                <Legend />
              </PieChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* History List Section */}
        <div className="bg-white rounded-xl border border-gray-200 shadow-lg p-8 mb-8">
          <h2 className="text-2xl font-semibold text-gray-800 mb-6">
            Recent Classifications
          </h2>
          <div className="space-y-4">
            {historyData.map((item) => (
              <div
                key={item.id}
                className="flex items-center space-x-4 p-4 border border-gray-200 rounded-lg hover:shadow-md transition-shadow"
              >
                {/* Thumbnail */}
                <div className="flex-shrink-0">
                  <img
                    src={item.imageUrl}
                    alt={`${item.label} item`}
                    className="w-16 h-16 rounded-lg object-cover border border-gray-200"
                  />
                </div>

                {/* Content */}
                <div className="flex-1 min-w-0">
                  <div className="flex items-center space-x-3 mb-2">
                    <span className="text-2xl">{getLabelEmoji(item.label)}</span>
                    <h3 className="text-lg font-semibold text-gray-800 capitalize">
                      {item.label}
                    </h3>
                  </div>
                  <div className="flex items-center justify-between">
                    <div className="flex items-center space-x-2">
                      <div className="w-20 bg-gray-200 rounded-full h-2">
                        <div
                          className="bg-blue-500 h-2 rounded-full"
                          style={{ width: `${item.confidence * 100}%` }}
                        ></div>
                      </div>
                      <span className="text-sm text-gray-600">
                        {Math.round(item.confidence * 100)}%
                      </span>
                    </div>
                    <span className="text-sm text-gray-500">
                      {formatTimestamp(item.timestamp)}
                    </span>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Footer */}
        <div className="text-center">
          <p className="text-lg text-gray-600 italic">
            Your past scans help build a cleaner future ✨
          </p>
        </div>
      </div>
    </div>
  );
};

export default History;
