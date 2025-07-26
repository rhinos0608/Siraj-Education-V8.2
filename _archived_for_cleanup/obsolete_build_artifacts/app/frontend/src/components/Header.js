import React, { useState, useEffect } from 'react';
import { useLocation } from 'react-router-dom';
import { motion, AnimatePresence } from 'framer-motion';

/**
 * SIRAJ Enhanced Header - Notion x World Anvil Design
 * 
 * Consciousness-driven header that provides:
 * - Contextual information based on current route
 * - Real-time system status and archetype management
 * - Quick access to core educational functions
 * - Living Spiral phase awareness
 * - QWAN principle embodiment in interface design
 */

const Header = ({ 
  sidebarOpen, 
  onSidebarToggle, 
  isDarkMode, 
  onDarkModeToggle, 
  currentArchetype, 
  onArchetypeChange, 
  isConnected, 
  currentPhase 
}) => {
  const location = useLocation();
  const [showArchetypeSelector, setShowArchetypeSelector] = useState(false);
  const [activeNotifications, setActiveNotifications] = useState([]);
  const [breadcrumbs, setBreadcrumbs] = useState([]);

  // === ARCHETYPE CONFIGURATIONS ===
  const archetypes = [
    { 
      id: 'socratic', 
      name: 'Socratic Teacher', 
      emoji: '🦉', 
      color: '#8B4513',
      approach: 'Questioning & Critical Thinking',
      active: true
    },
    { 
      id: 'constructivist', 
      name: 'Constructivist Teacher', 
      emoji: '🧱', 
      color: '#FF6B35',
      approach: 'Hands-on Learning & Building',
      active: true
    },
    { 
      id: 'storyteller', 
      name: 'Storyteller Teacher', 
      emoji: '📖', 
      color: '#4ECDC4',
      approach: 'Narrative & Contextual Learning',
      active: true
    },
    { 
      id: 'synthesizer', 
      name: 'Synthesizer Teacher', 
      emoji: '🌀', 
      color: '#A8E6CF',
      approach: 'Integration & Unified Understanding',
      active: true
    },
    { 
      id: 'challenger', 
      name: 'Challenger Teacher', 
      emoji: '⚡', 
      color: '#FFD93D',
      approach: 'Boundary Pushing & Critical Analysis',
      active: true
    },
    { 
      id: 'mentor', 
      name: 'Mentor Teacher', 
      emoji: '🌱', 
      color: '#95E1D3',
      approach: 'Support & Emotional Guidance',
      active: true
    },
    { 
      id: 'analyst', 
      name: 'Analyst Teacher', 
      emoji: '🔬', 
      color: '#FF8B94',
      approach: 'Data-driven & Logical Analysis',
      active: true
    }
  ];

  // === ROUTE CONFIGURATIONS ===
  const routeConfigs = {
    '/': {
      title: 'Educational Dashboard',
      subtitle: 'Overview of learning progress and system status',
      icon: '🏠',
      actions: ['Quick Start Council', 'View Analytics', 'Submit Homework'],
      color: 'var(--color-primary)'
    },
    '/council': {
      title: 'AI Council Session',
      subtitle: 'Multi-perspective learning through collaborative AI',
      icon: '🏛️',
      actions: ['Start New Session', 'Select Archetypes', 'View History'],
      color: 'var(--color-secondary)'
    },
    '/homework': {
      title: 'Homework Feedback',
      subtitle: 'AI-powered assignment evaluation and improvement',
      icon: '📝',
      actions: ['Submit Assignment', 'View Feedback', 'Get Suggestions'],
      color: 'var(--color-accent)'
    },
    '/analytics': {
      title: 'Learning Analytics',
      subtitle: 'Deep insights into learning patterns and progress',
      icon: '📊',
      actions: ['Generate Report', 'Export Data', 'View Trends'],
      color: 'var(--color-info)'
    },
    '/curriculum': {
      title: 'Curriculum Alignment',
      subtitle: 'Standards mapping and learning objective tracking',
      icon: '🎯',
      actions: ['Map Standards', 'Create Objectives', 'Track Progress'],
      color: 'var(--color-warning)'
    },
    '/progress': {
      title: 'Student Progress',
      subtitle: 'Comprehensive growth tracking and mastery monitoring',
      icon: '📈',
      actions: ['View Progress', 'Set Goals', 'Generate Report'],
      color: 'var(--color-success)'
    }
  };

  // === CURRENT ROUTE CONFIGURATION ===
  const currentRoute = routeConfigs[location.pathname] || routeConfigs['/'];

  // === BREADCRUMB GENERATION ===
  useEffect(() => {
    const generateBreadcrumbs = () => {
      const pathSegments = location.pathname.split('/').filter(Boolean);
      const crumbs = [{ name: 'SIRAJ', path: '/', icon: '🧠' }];
      
      if (pathSegments.length > 0) {
        crumbs.push({
          name: currentRoute.title,
          path: location.pathname,
          icon: currentRoute.icon
        });
      }
      
      setBreadcrumbs(crumbs);
    };

    generateBreadcrumbs();
  }, [location.pathname, currentRoute]);

  // === NOTIFICATION SYSTEM ===
  useEffect(() => {
    const notifications = [];
    
    if (!isConnected) {
      notifications.push({
        id: 'connection',
        type: 'warning',
        message: 'Offline mode - Limited functionality available',
        icon: '⚠️'
      });
    }
    
    if (currentPhase === 'collapse') {
      notifications.push({
        id: 'phase',
        type: 'info',
        message: 'System is analyzing current learning state',
        icon: '🔍'
      });
    }
    
    setActiveNotifications(notifications);
  }, [isConnected, currentPhase]);

  // === CURRENT ARCHETYPE ===
  const selectedArchetype = archetypes.find(arch => arch.id === currentArchetype) || archetypes[0];

  return (
    <header className="siraj-header">
      {/* Left Section - Navigation & Context */}
      <div className="header-left">
        {/* Sidebar Toggle */}
        <button 
          className="sidebar-toggle"
          onClick={onSidebarToggle}
          aria-label="Toggle sidebar"
        >
          <span className={`hamburger ${sidebarOpen ? 'open' : ''}`}>
            <span></span>
            <span></span>
            <span></span>
          </span>
        </button>

        {/* Breadcrumb Navigation */}
        <nav className="breadcrumb-nav">
          {breadcrumbs.map((crumb, index) => (
            <div key={crumb.path} className="breadcrumb-item">
              {index > 0 && <span className="breadcrumb-separator">→</span>}
              <a href={crumb.path} className="breadcrumb-link">
                <span className="breadcrumb-icon">{crumb.icon}</span>
                <span className="breadcrumb-name">{crumb.name}</span>
              </a>
            </div>
          ))}
        </nav>

        {/* Page Context */}
        <div className="page-context">
          <div className="page-title-section">
            <h1 className="page-title" style={{ color: currentRoute.color }}>
              {currentRoute.title}
            </h1>
            <p className="page-subtitle">{currentRoute.subtitle}</p>
          </div>
        </div>
      </div>

      {/* Center Section - Current Status */}
      <div className="header-center">
        {/* Phase Indicator */}
        <div className="phase-indicator">
          <div className={`phase-icon ${currentPhase}`}>
            <motion.div
              animate={{ rotate: currentPhase === 'synthesis' ? 360 : 0 }}
              transition={{ duration: 2, repeat: currentPhase === 'synthesis' ? Infinity : 0 }}
            >
              {currentPhase === 'collapse' && '🔍'}
              {currentPhase === 'council' && '🏛️'}
              {currentPhase === 'synthesis' && '🌀'}
              {currentPhase === 'rebirth' && '🌟'}
            </motion.div>
          </div>
          <div className="phase-info">
            <span className="phase-name">{currentPhase.charAt(0).toUpperCase() + currentPhase.slice(1)}</span>
            <span className="phase-description">
              {currentPhase === 'collapse' && 'Analyzing learning needs'}
              {currentPhase === 'council' && 'AI collaboration active'}
              {currentPhase === 'synthesis' && 'Integrating perspectives'}
              {currentPhase === 'rebirth' && 'Ready for growth'}
            </span>
          </div>
        </div>

        {/* Active Notifications */}
        <AnimatePresence>
          {activeNotifications.map(notification => (
            <motion.div
              key={notification.id}
              className={`notification ${notification.type}`}
              initial={{ opacity: 0, y: -10 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -10 }}
            >
              <span className="notification-icon">{notification.icon}</span>
              <span className="notification-message">{notification.message}</span>
            </motion.div>
          ))}
        </AnimatePresence>
      </div>

      {/* Right Section - Controls & Settings */}
      <div className="header-right">
        {/* Archetype Selector */}
        <div className="archetype-selector">
          <button 
            className="archetype-current"
            onClick={() => setShowArchetypeSelector(!showArchetypeSelector)}
            style={{ borderLeftColor: selectedArchetype.color }}
          >
            <span className="archetype-emoji">{selectedArchetype.emoji}</span>
            <div className="archetype-info">
              <span className="archetype-name">{selectedArchetype.name}</span>
              <span className="archetype-approach">{selectedArchetype.approach}</span>
            </div>
            <span className={`dropdown-arrow ${showArchetypeSelector ? 'expanded' : ''}`}>▼</span>
          </button>

          <AnimatePresence>
            {showArchetypeSelector && (
              <motion.div 
                className="archetype-dropdown"
                initial={{ opacity: 0, y: -10, scale: 0.95 }}
                animate={{ opacity: 1, y: 0, scale: 1 }}
                exit={{ opacity: 0, y: -10, scale: 0.95 }}
                transition={{ duration: 0.2 }}
              >
                <div className="dropdown-header">
                  <span className="dropdown-title">Select AI Teacher</span>
                  <span className="dropdown-subtitle">Choose your learning companion</span>
                </div>
                <div className="archetype-list">
                  {archetypes.map((archetype, index) => (
                    <motion.button
                      key={archetype.id}
                      className={`archetype-option ${currentArchetype === archetype.id ? 'active' : ''}`}
                      onClick={() => {
                        onArchetypeChange(archetype.id);
                        setShowArchetypeSelector(false);
                      }}
                      initial={{ opacity: 0, x: -10 }}
                      animate={{ opacity: 1, x: 0 }}
                      transition={{ delay: index * 0.05 }}
                      style={{ '--archetype-color': archetype.color }}
                    >
                      <span className="option-emoji">{archetype.emoji}</span>
                      <div className="option-info">
                        <span className="option-name">{archetype.name}</span>
                        <span className="option-approach">{archetype.approach}</span>
                      </div>
                      {currentArchetype === archetype.id && (
                        <span className="option-selected">✓</span>
                      )}
                    </motion.button>
                  ))}
                </div>
              </motion.div>
            )}
          </AnimatePresence>
        </div>

        {/* Quick Actions */}
        <div className="quick-actions">
          {currentRoute.actions.slice(0, 2).map((action, index) => (
            <button key={action} className="quick-action-btn">
              {action}
            </button>
          ))}
        </div>

        {/* System Controls */}
        <div className="system-controls">
          {/* Connection Status */}
          <div className={`connection-status ${isConnected ? 'connected' : 'disconnected'}`}>
            <div className="connection-dot"></div>
            <span className="connection-text">{isConnected ? 'Online' : 'Offline'}</span>
          </div>

          {/* Dark Mode Toggle */}
          <button 
            className="dark-mode-toggle"
            onClick={onDarkModeToggle}
            aria-label="Toggle dark mode"
          >
            <motion.div
              animate={{ rotate: isDarkMode ? 180 : 0 }}
              transition={{ duration: 0.3 }}
            >
              {isDarkMode ? '☀️' : '🌙'}
            </motion.div>
          </button>

          {/* Settings Access */}
          <button className="settings-btn" aria-label="Open settings">
            <motion.div
              whileHover={{ rotate: 90 }}
              transition={{ duration: 0.2 }}
            >
              ⚙️
            </motion.div>
          </button>
        </div>
      </div>

      {/* Click outside to close archetype selector */}
      {showArchetypeSelector && (
        <div 
          className="dropdown-overlay"
          onClick={() => setShowArchetypeSelector(false)}
        />
      )}
    </header>
  );
};

export default Header;
