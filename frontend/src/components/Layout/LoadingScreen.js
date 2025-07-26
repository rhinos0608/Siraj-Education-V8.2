import React, { useEffect, useState } from 'react';
import { motion } from 'framer-motion';
import './LoadingScreen.css';

/**
 * LoadingScreen Component
 * =====================
 * 
 * Beautiful loading screen that displays while the SIRAJ Educational AI
 * system initializes. Features animated council archetypes and loading states.
 */

const LoadingScreen = () => {
  const [loadingStage, setLoadingStage] = useState(0);
  const [loadingText, setLoadingText] = useState('Initializing SIRAJ Educational AI...');

  const loadingStages = [
    { text: 'Initializing SIRAJ Educational AI...', duration: 1000 },
    { text: 'Connecting to Ollama AI service...', duration: 800 },
    { text: 'Loading Gemma 3n models...', duration: 1200 },
    { text: 'Assembling AI teaching council...', duration: 900 },
    { text: 'Preparing multi-perspective learning...', duration: 700 },
    { text: 'Ready for educational excellence!', duration: 500 }
  ];

  const councilArchetypes = [
    { emoji: '🦉', name: 'Socratic', color: '#8B4513', delay: 0 },
    { emoji: '🧱', name: 'Constructivist', color: '#FF6B35', delay: 0.2 },
    { emoji: '📖', name: 'Storyteller', color: '#4ECDC4', delay: 0.4 },
    { emoji: '🌀', name: 'Synthesizer', color: '#A8E6CF', delay: 0.6 },
    { emoji: '⚡', name: 'Challenger', color: '#FFD93D', delay: 0.8 },
    { emoji: '🌱', name: 'Mentor', color: '#95E1D3', delay: 1.0 },
    { emoji: '🔬', name: 'Analyst', color: '#FF8B94', delay: 1.2 }
  ];

  useEffect(() => {
    const timer = setTimeout(() => {
      if (loadingStage < loadingStages.length - 1) {
        setLoadingStage(prev => prev + 1);
        setLoadingText(loadingStages[loadingStage + 1].text);
      }
    }, loadingStages[loadingStage].duration);

    return () => clearTimeout(timer);
  }, [loadingStage, loadingStages]);

  return (
    <div className="loading-screen">
      {/* Background gradient */}
      <div className="loading-background">
        <div className="gradient-orb orb-1"></div>
        <div className="gradient-orb orb-2"></div>
        <div className="gradient-orb orb-3"></div>
      </div>

      {/* Main loading content */}
      <div className="loading-content">
        {/* SIRAJ Logo/Title */}
        <motion.div
          className="loading-logo"
          initial={{ opacity: 0, scale: 0.8 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ duration: 0.8, ease: "easeOut" }}
        >
          <h1 className="logo-text">
            <span className="logo-letter">S</span>
            <span className="logo-letter">I</span>
            <span className="logo-letter">R</span>
            <span className="logo-letter">A</span>
            <span className="logo-letter">J</span>
          </h1>
          <p className="logo-subtitle">Educational AI Council</p>
        </motion.div>

        {/* Council Archetypes Circle */}
        <motion.div
          className="council-circle"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.5, duration: 1 }}
        >
          {councilArchetypes.map((archetype, index) => (
            <motion.div
              key={archetype.name}
              className="archetype-avatar"
              style={{
                '--archetype-color': archetype.color,
                '--archetype-index': index,
                '--total-archetypes': councilArchetypes.length
              }}
              initial={{ 
                scale: 0, 
                rotate: 0,
                opacity: 0
              }}
              animate={{ 
                scale: 1, 
                rotate: 360,
                opacity: 1
              }}
              transition={{
                delay: 1 + archetype.delay,
                duration: 0.8,
                ease: "easeOut"
              }}
              whileHover={{ scale: 1.2 }}
            >
              <span className="archetype-emoji">{archetype.emoji}</span>
              <span className="archetype-name">{archetype.name}</span>
            </motion.div>
          ))}
        </motion.div>

        {/* Loading Text */}
        <motion.div
          className="loading-text-container"
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 1.5, duration: 0.6 }}
        >
          <motion.p
            key={loadingText}
            className="loading-text"
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -10 }}
            transition={{ duration: 0.4 }}
          >
            {loadingText}
          </motion.p>
        </motion.div>

        {/* Progress Bar */}
        <motion.div
          className="loading-progress"
          initial={{ opacity: 0, width: 0 }}
          animate={{ opacity: 1, width: "100%" }}
          transition={{ delay: 2, duration: 0.8 }}
        >
          <motion.div
            className="progress-bar"
            initial={{ width: "0%" }}
            animate={{ width: `${((loadingStage + 1) / loadingStages.length) * 100}%` }}
            transition={{ duration: 0.5, ease: "easeOut" }}
          />
        </motion.div>

        {/* Loading Spinner */}
        <motion.div
          className="loading-spinner"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 2.5, duration: 0.5 }}
        >
          <div className="spinner-ring"></div>
          <div className="spinner-ring"></div>
          <div className="spinner-ring"></div>
        </motion.div>

        {/* Version Info */}
        <motion.div
          className="version-info"
          initial={{ opacity: 0 }}
          animate={{ opacity: 0.7 }}
          transition={{ delay: 3, duration: 0.5 }}
        >
          <p>SIRAJ Educational AI v8.1.0</p>
          <p>Powered by Gemma 3n via Ollama</p>
        </motion.div>
      </div>
    </div>
  );
};

export default LoadingScreen;