import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import Dashboard from './components/Dashboard';
import EducationalCouncilInterface from './components/EducationalCouncilInterface';
import AnalyticsDashboard from './components/AnalyticsDashboard';
import Header from './components/Header';
import Sidebar from './components/Sidebar';
import { useSirajAPI } from './hooks/useSirajAPI';
import './App.css';

function App() {
  const [currentPhase, setCurrentPhase] = useState('synthesis');
  const [qwanMetrics] = useState({
    wholeness: 0.89,
    freedom: 0.92,
    exactness: 0.87,
    egolessness: 0.94,
    eternity: 0.91
  });
  
  // Use the API hook with error handling
  const { systemStatus, initializeSystem } = useSirajAPI();
  const isConnected = systemStatus === 'healthy';

  // Initialize system with error handling
  useEffect(() => {
    const init = async () => {
      try {
        await initializeSystem();
      } catch (error) {
        console.log('API not available, running in offline mode');
      }
    };
    
    init();
  }, [initializeSystem]);

  // Simulate living spiral phase progression
  useEffect(() => {
    const phases = ['collapse', 'council', 'synthesis', 'rebirth'];
    const interval = setInterval(() => {
      setCurrentPhase(prev => {
        const currentIndex = phases.indexOf(prev);
        return phases[(currentIndex + 1) % phases.length];
      });
    }, 30000); // Change phase every 30 seconds
    
    return () => clearInterval(interval);
  }, []);

  return (
    <Router>
      <div className="App">
        <Header 
          systemStatus={systemStatus}
          currentPhase={currentPhase}
          isConnected={isConnected}
        />
        <div className="app-layout">
          <Sidebar 
            currentPhase={currentPhase}
            qwanMetrics={qwanMetrics}
            isConnected={isConnected}
          />
          <main className="main-content">
            <Routes>
              <Route 
                path="/" 
                element={
                  <Dashboard 
                    systemHealth={systemStatus}
                    qwanMetrics={qwanMetrics}
                    currentPhase={currentPhase}
                    isConnected={isConnected}
                  />
                } 
              />
              <Route path="/council" element={<EducationalCouncilInterface />} />
              <Route 
                path="/analytics" 
                element={
                  <AnalyticsDashboard 
                    qwanMetrics={qwanMetrics}
                    currentPhase={currentPhase}
                    systemHealth={systemStatus}
                    sessionHistory={[]}
                  />
                } 
              />
              <Route path="*" element={<Navigate to="/" replace />} />
            </Routes>
          </main>
        </div>
      </div>
    </Router>
  );
}

export default App;