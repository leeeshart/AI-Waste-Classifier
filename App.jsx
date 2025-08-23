import React, { useState } from 'react';
import Home from './Home';
import ImageUpload from './ImageUpload';
import TextClassify from './TextClassify';
import History from './History';
import FutureVision from './FutureVision';

function App() {
  const [currentPage, setCurrentPage] = useState('home');

  const renderPage = () => {
    switch (currentPage) {
      case 'home':
        return <Home onNavigate={setCurrentPage} />;
      case 'imageUpload':
        return <ImageUpload onNavigate={setCurrentPage} />;
      case 'textClassify':
        return <TextClassify onNavigate={setCurrentPage} />;
      case 'history':
        return <History onNavigate={setCurrentPage} />;
      case 'futureVision':
        return <FutureVision onNavigate={setCurrentPage} />;
      default:
        return <Home onNavigate={setCurrentPage} />;
    }
  };

  return (
    <div className="App">
      {renderPage()}
    </div>
  );
}

export default App;
