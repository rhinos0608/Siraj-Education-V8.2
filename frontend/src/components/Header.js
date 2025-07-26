import React from 'react';

/**
 * SIRAJ Header - Clean Notion-Inspired Design
 * 
 * Simple, readable header focused on:
 * - Clear navigation context
 * - System status visibility
 * - Clean typography
 * - High contrast design
 */

const Header = ({ 
  systemStatus = 'offline', 
  currentPhase = 'synthesis', 
  isConnected = false 
}) => {
  
  const getStatusColor = () => {
    switch (systemStatus) {
      case 'healthy': return '#0f7b6c';
      case 'error': return '#e03e3e';
      case 'initializing': return '#cb912f';
      default: return '#6f6f6f';
    }
  };

  const getStatusText = () => {
    switch (systemStatus) {
      case 'healthy': return 'AI Council Online';
      case 'error': return 'System Error';
      case 'initializing': return 'Initializing...';
      default: return 'Offline Mode';
    }
  };

  return (
    <header className="siraj-header">
      <div className="header-left">
        <div>
          <h1 className="page-title">SIRAJ Educational AI</h1>
          <p className="page-subtitle">Consciousness-driven learning platform</p>
        </div>
      </div>
      
      <div style={{ display: 'flex', alignItems: 'center', gap: 'var(--spacing-lg)' }}>
        {/* Phase Indicator */}
        <div style={{ display: 'flex', alignItems: 'center', gap: 'var(--spacing-sm)' }}>
          <div style={{ 
            width: '8px', 
            height: '8px', 
            borderRadius: '50%', 
            backgroundColor: 'var(--color-primary)' 
          }}></div>
          <span style={{ 
            fontSize: 'var(--font-size-sm)', 
            color: 'var(--color-text-secondary)',
            textTransform: 'capitalize'
          }}>
            Phase: {currentPhase}
          </span>
        </div>
        
        {/* System Status */}
        <div style={{ display: 'flex', alignItems: 'center', gap: 'var(--spacing-sm)' }}>
          <div style={{ 
            width: '8px', 
            height: '8px', 
            borderRadius: '50%', 
            backgroundColor: getStatusColor() 
          }}></div>
          <span style={{ 
            fontSize: 'var(--font-size-sm)', 
            color: 'var(--color-text-secondary)' 
          }}>
            {getStatusText()}
          </span>
        </div>
      </div>
    </header>
  );
};

export default Header;