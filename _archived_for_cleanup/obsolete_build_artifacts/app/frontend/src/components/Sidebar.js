import React, { useState, useEffect } from 'react';
import { NavLink, useLocation } from 'react-router-dom';
import { motion, AnimatePresence } from 'framer-motion';

/**
 * SIRAJ Enhanced Sidebar - Notion x World Anvil Design
 * 
 * Combines Notion's clean navigation with World Anvil's rich information display
 * Embodies QWAN principles through conscious design choices
 * 
 * Features:
 * - Multi-layered information hierarchy
 * - Real-time system consciousness indicators
 * - Archetype status and effectiveness metrics
 * - Living Spiral phase visualization
 * - Council health monitoring
 * - Quick access to educational tools
 */

const Sidebar = ({ 
  isOpen, 
  onToggle, 
  currentPhase, 
  systemHealth, 
  qwanMetrics, 
  isConnected 
}) => {
  const location = useLocation();
  const [expandedSections, setExpandedSections] = useState({
    council: true,
    tools: true,
    analytics: false,
    system: false
  });

  // === ARCHETYPE SYSTEM CONFIGURATION ===
  const archetypes = [
    { 
      id: 'socratic', 
      name: 'Socratic Teacher', 
      emoji: '🦉', 
      color: 'var(--color-socratic)',
      status: 'active',
      effectiveness: 87,
      role: 'Questions & Critical Thinking'
    },
    { 
      id: 'constructivist', 
      name: 'Constructivist Teacher', 
      emoji: '🧱', 
      color: 'var(--color-constructivist)',
      status: 'active',
      effectiveness: 92,
      role: 'Hands-on Learning'
    },
    { 
      id: 'storyteller', 
      name: 'Storyteller Teacher', 
      emoji: '📖', 
      color: 'var(--color-storyteller)',
      status: 'active',
      effectiveness: 89,
      role: 'Narrative & Context'
    },
    { 
      id: 'synthesizer', 
      name: 'Synthesizer Teacher', 
      emoji: '🌀', 
      color: 'var(--color-synthesizer)',
      status: 'active',
      effectiveness: 94,
      role: 'Integration & Unity'
    },
    { 
      id: 'challenger', 
      name: 'Challenger Teacher', 
      emoji: '⚡', 
      color: 'var(--color-challenger)',
      status: 'active',
      effectiveness: 76,
      role: 'Push Boundaries'
    },
    { 
      id: 'mentor', 
      name: 'Mentor Teacher', 
      emoji: '🌱', 
      color: 'var(--color-mentor)',
      status: 'active',
      effectiveness: 91,
      role: 'Support & Guidance'
    },
    { 
      id: 'analyst', 
      name: 'Analyst Teacher', 
      emoji: '🔬', 
      color: 'var(--color-analyst)',
      status: 'active',
      effectiveness: 85,
      role: 'Data & Logic'
    }
  ];

  // === NAVIGATION STRUCTURE ===
  const navigationItems = [
    {
      path: '/',
      name: 'Dashboard',
      icon: '🏠',
      description: 'Educational overview & quick actions',
      phase: 'collapse'
    },
    {
      path: '/council',
      name: 'Council Session',
      icon: '🏛️',
      description: 'Multi-archetype learning conversations',
      phase: 'council'
    },
    {
      path: '/homework',
      name: 'Homework Feedback',
      icon: '📝',
      description: 'AI-powered assignment evaluation',
      phase: 'synthesis'
    },
    {
      path: '/analytics',
      name: 'Learning Analytics',
      icon: '📊',
      description: 'Progress insights & QWAN metrics',
      phase: 'synthesis'
    },
    {
      path: '/curriculum',
      name: 'Curriculum Alignment',
      icon: '🎯',
      description: 'Standards mapping & objectives',
      phase: 'rebirth'
    },
    {
      path: '/progress',
      name: 'Student Progress',
      icon: '📈',
      description: 'Growth tracking & mastery levels',
      phase: 'rebirth'
    }
  ];

  // === SECTION TOGGLE HANDLER ===
  const toggleSection = (section) => {
    setExpandedSections(prev => ({
      ...prev,
      [section]: !prev[section]
    }));
  };

  // === EFFECTIVENESS CALCULATION ===
  const averageEffectiveness = Math.round(
    archetypes.reduce((sum, arch) => sum + arch.effectiveness, 0) / archetypes.length
  );

  return (
    <>
      {/* Overlay for mobile */}
      {isOpen && (
        <div 
          className="sidebar-overlay"
          onClick={onToggle}
        />
      )}

      {/* Main Sidebar */}
      <motion.aside 
        className={`siraj-sidebar ${isOpen ? 'open' : 'collapsed'}`}
        initial={false}
        animate={{ 
          width: isOpen ? 280 : 60,
          opacity: isOpen ? 1 : 0.9
        }}
        transition={{ duration: 0.3, ease: 'easeInOut' }}
      >
        {/* Sidebar Header */}
        <div className="sidebar-header">
          <motion.div 
            className="sidebar-logo"
            animate={{ scale: isOpen ? 1 : 0.8 }}
          >
            <div className="logo-icon">🧠</div>
            <AnimatePresence>
              {isOpen && (
                <motion.div 
                  className="logo-text"
                  initial={{ opacity: 0, x: -10 }}
                  animate={{ opacity: 1, x: 0 }}
                  exit={{ opacity: 0, x: -10 }}
                  transition={{ delay: 0.1 }}
                >
                  <div className="logo-title">SIRAJ</div>
                  <div className="logo-subtitle">Educational AI</div>
                </motion.div>
              )}
            </AnimatePresence>
          </motion.div>

          {/* System Status Indicator */}
          <AnimatePresence>
            {isOpen && (
              <motion.div 
                className="system-status"
                initial={{ opacity: 0, y: -10 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: -10 }}
              >
                <div className={`status-indicator ${isConnected ? 'connected' : 'disconnected'}`}>
                  <div className="status-dot"></div>
                  <span className="status-text">
                    {isConnected ? 'Connected' : 'Offline'}
                  </span>
                </div>
                <div className="phase-indicator">
                  <span className="phase-label">Phase:</span>
                  <span className={`phase-value ${currentPhase}`}>
                    {currentPhase.charAt(0).toUpperCase() + currentPhase.slice(1)}
                  </span>
                </div>
              </motion.div>
            )}
          </AnimatePresence>
        </div>

        {/* Navigation Section */}
        <nav className="sidebar-nav">
          <AnimatePresence>
            {isOpen && (
              <motion.div 
                className="nav-section"
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                exit={{ opacity: 0 }}
                transition={{ delay: 0.2 }}
              >
                <div className="nav-section-header">
                  <span className="nav-section-title">Navigation</span>
                </div>
                <ul className="nav-list">
                  {navigationItems.map((item, index) => (
                    <motion.li 
                      key={item.path}
                      initial={{ opacity: 0, x: -20 }}
                      animate={{ opacity: 1, x: 0 }}
                      transition={{ delay: 0.1 * index }}
                    >
                      <NavLink 
                        to={item.path}
                        className={({ isActive }) => 
                          `nav-link ${isActive ? 'active' : ''} phase-${item.phase}`
                        }
                      >
                        <span className="nav-icon">{item.icon}</span>
                        <div className="nav-content">
                          <span className="nav-name">{item.name}</span>
                          <span className="nav-description">{item.description}</span>
                        </div>
                        <div className="nav-phase-indicator">
                          <div className={`phase-dot ${item.phase}`}></div>
                        </div>
                      </NavLink>
                    </motion.li>
                  ))}
                </ul>
              </motion.div>
            )}
          </AnimatePresence>
        </nav>

        {/* Council Archetypes Section */}
        <AnimatePresence>
          {isOpen && (
            <motion.div 
              className="sidebar-section"
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: 20 }}
              transition={{ delay: 0.3 }}
            >
              <button 
                className="section-toggle"
                onClick={() => toggleSection('council')}
              >
                <span className="section-title">AI Council</span>
                <div className="section-meta">
                  <span className="effectiveness-badge">
                    {averageEffectiveness}% Effective
                  </span>
                  <span className={`toggle-icon ${expandedSections.council ? 'expanded' : ''}`}>
                    ▼
                  </span>
                </div>
              </button>

              <AnimatePresence>
                {expandedSections.council && (
                  <motion.div 
                    className="archetype-grid"
                    initial={{ height: 0, opacity: 0 }}
                    animate={{ height: 'auto', opacity: 1 }}
                    exit={{ height: 0, opacity: 0 }}
                    transition={{ duration: 0.3 }}
                  >
                    {archetypes.map((archetype, index) => (
                      <motion.div 
                        key={archetype.id}
                        className="archetype-mini-card"
                        initial={{ opacity: 0, scale: 0.9 }}
                        animate={{ opacity: 1, scale: 1 }}
                        transition={{ delay: 0.05 * index }}
                        style={{ '--archetype-color': archetype.color }}
                      >
                        <div className="archetype-mini-header">
                          <span className="archetype-emoji">{archetype.emoji}</span>
                          <div className="archetype-info">
                            <div className="archetype-name">{archetype.name.split(' ')[0]}</div>
                            <div className="archetype-effectiveness">
                              {archetype.effectiveness}%
                            </div>
                          </div>
                        </div>
                        <div className="archetype-progress">
                          <div 
                            className="progress-fill"
                            style={{ width: `${archetype.effectiveness}%` }}
                          ></div>
                        </div>
                      </motion.div>
                    ))}
                  </motion.div>
                )}
              </AnimatePresence>
            </motion.div>
          )}
        </AnimatePresence>

        {/* QWAN Metrics Section */}
        <AnimatePresence>
          {isOpen && qwanMetrics && (
            <motion.div 
              className="sidebar-section"
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: 20 }}
              transition={{ delay: 0.4 }}
            >
              <button 
                className="section-toggle"
                onClick={() => toggleSection('analytics')}
              >
                <span className="section-title">QWAN Metrics</span>
                <span className={`toggle-icon ${expandedSections.analytics ? 'expanded' : ''}`}>
                  ▼
                </span>
              </button>

              <AnimatePresence>
                {expandedSections.analytics && (
                  <motion.div 
                    className="qwan-metrics"
                    initial={{ height: 0, opacity: 0 }}
                    animate={{ height: 'auto', opacity: 1 }}
                    exit={{ height: 0, opacity: 0 }}
                    transition={{ duration: 0.3 }}
                  >
                    {Object.entries(qwanMetrics).map(([key, value], index) => (
                      <div key={key} className="qwan-metric">
                        <div className="metric-header">
                          <span className="metric-name">
                            {key.charAt(0).toUpperCase() + key.slice(1)}
                          </span>
                          <span className="metric-value">{Math.round(value * 100)}%</span>
                        </div>
                        <div className="metric-bar">
                          <motion.div 
                            className="metric-fill"
                            initial={{ width: 0 }}
                            animate={{ width: `${value * 100}%` }}
                            transition={{ delay: 0.1 * index, duration: 0.8 }}
                          />
                        </div>
                      </div>
                    ))}
                  </motion.div>
                )}
              </AnimatePresence>
            </motion.div>
          )}
        </AnimatePresence>

        {/* Living Spiral Visualization */}
        <AnimatePresence>
          {isOpen && (
            <motion.div 
              className="sidebar-section spiral-section"
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: 20 }}
              transition={{ delay: 0.5 }}
            >
              <div className="section-title-static">Living Spiral</div>
              <div className="spiral-visualization">
                {['collapse', 'council', 'synthesis', 'rebirth'].map((phase, index) => (
                  <div 
                    key={phase}
                    className={`spiral-phase-mini ${currentPhase === phase ? 'active' : ''}`}
                  >
                    <div className="phase-dot"></div>
                    <span className="phase-name">{phase}</span>
                  </div>
                ))}
              </div>
            </motion.div>
          )}
        </AnimatePresence>

        {/* Footer */}
        <div className="sidebar-footer">
          <AnimatePresence>
            {isOpen && (
              <motion.div 
                className="footer-content"
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                exit={{ opacity: 0 }}
              >
                <div className="consciousness-quote">
                  "Education is the lighting of a fire, not the filling of a pail."
                </div>
                <div className="version-info">
                  SIRAJ v8.1.0 • Consciousness-Driven
                </div>
              </motion.div>
            )}
          </AnimatePresence>
        </div>
      </motion.aside>
    </>
  );
};

export default Sidebar;
