import React, { useState } from 'react';
import { Link, useLocation } from 'react-router-dom';
import { motion, AnimatePresence } from 'framer-motion';
import {
  Home,
  Brain,
  BookOpen,
  BarChart3,
  Settings,
  History,
  Users,
  Zap,
  HelpCircle,
  ChevronDown,
  ChevronRight,
  X
} from 'lucide-react';
import { getCouncilColor, getCouncilAvatar, listCouncilVoices } from '../../utils/councilUtils';
import './Sidebar.css';

/**
 * Sidebar Component
 * ================
 * 
 * Navigation sidebar for the SIRAJ Educational AI application.
 * Features collapsible sections, quick session access, and council overview.
 */

const Sidebar = ({ 
  currentSession, 
  userPreferences, 
  onUpdatePreferences, 
  onClose 
}) => {
  const location = useLocation();
  const [expandedSections, setExpandedSections] = useState({
    council: true,
    sessions: false,
    preferences: false
  });

  const navigationItems = [
    {
      id: 'dashboard',
      label: 'Dashboard',
      icon: Home,
      path: '/',
      description: 'Overview and quick access'
    },
    {
      id: 'session',
      label: 'AI Council Session',
      icon: Brain,
      path: '/session',
      description: 'Multi-perspective learning'
    },
    {
      id: 'homework',
      label: 'Homework Assistant',
      icon: BookOpen,
      path: '/homework',
      description: 'Submit work for feedback'
    },
    {
      id: 'analytics',
      label: 'Learning Analytics',
      icon: BarChart3,
      path: '/analytics',
      description: 'Progress and insights'
    },
    {
      id: 'settings',
      label: 'Settings',
      icon: Settings,
      path: '/settings',
      description: 'Customize your experience'
    }
  ];

  const councilArchetypes = listCouncilVoices();
  
  const recentSessions = [
    { id: 'session-1', topic: 'Photosynthesis Explained', timestamp: '2 hours ago', archetypes: 3 },
    { id: 'session-2', topic: 'Algebra Problem Solving', timestamp: '1 day ago', archetypes: 5 },
    { id: 'session-3', topic: 'Essay Writing Tips', timestamp: '2 days ago', archetypes: 4 }
  ];

  const toggleSection = (section) => {
    setExpandedSections(prev => ({
      ...prev,
      [section]: !prev[section]
    }));
  };

  const isActivePath = (path) => {
    if (path === '/') {
      return location.pathname === '/';
    }
    return location.pathname.startsWith(path);
  };

  const handleArchetypePreference = (archetype) => {
    const currentPreferred = userPreferences.preferredArchetypes || [];
    const isPreferred = currentPreferred.includes(archetype);
    
    let newPreferred;
    if (isPreferred) {
      newPreferred = currentPreferred.filter(a => a !== archetype);
    } else {
      newPreferred = [...currentPreferred, archetype];
    }
    
    onUpdatePreferences({ preferredArchetypes: newPreferred });
  };

  return (
    <>
      {/* Mobile backdrop */}
      <div className="sidebar-backdrop" onClick={onClose} />
      
      {/* Sidebar */}
      <motion.aside
        className="app-sidebar"
        initial={{ x: -280 }}
        animate={{ x: 0 }}
        exit={{ x: -280 }}
        transition={{ duration: 0.3, ease: "easeOut" }}
      >
        {/* Sidebar Header */}
        <div className="sidebar-header">
          <div className="sidebar-title">
            <Brain size={24} className="sidebar-title-icon" />
            <div>
              <h2>Navigation</h2>
              <p>AI-Powered Learning</p>
            </div>
          </div>
          <button 
            className="sidebar-close"
            onClick={onClose}
            aria-label="Close sidebar"
          >
            <X size={20} />
          </button>
        </div>

        <div className="sidebar-content">
          {/* Main Navigation */}
          <nav className="sidebar-nav">
            <div className="nav-section">
              <h3 className="nav-section-title">Main</h3>
              <ul className="nav-list">
                {navigationItems.map((item) => {
                  const Icon = item.icon;
                  const isActive = isActivePath(item.path);
                  
                  return (
                    <li key={item.id}>
                      <Link
                        to={item.path}
                        className={`nav-item ${isActive ? 'active' : ''}`}
                        onClick={onClose}
                      >
                        <Icon size={18} className="nav-icon" />
                        <div className="nav-content">
                          <span className="nav-label">{item.label}</span>
                          <span className="nav-description">{item.description}</span>
                        </div>
                      </Link>
                    </li>
                  );
                })}
              </ul>
            </div>

            {/* AI Council Section */}
            <div className="nav-section">
              <button
                className="nav-section-toggle"
                onClick={() => toggleSection('council')}
                aria-expanded={expandedSections.council}
              >
                <h3 className="nav-section-title">AI Teaching Council</h3>
                {expandedSections.council ? (
                  <ChevronDown size={16} />
                ) : (
                  <ChevronRight size={16} />
                )}
              </button>
              
              <AnimatePresence>
                {expandedSections.council && (
                  <motion.div
                    className="council-overview"
                    initial={{ height: 0, opacity: 0 }}
                    animate={{ height: 'auto', opacity: 1 }}
                    exit={{ height: 0, opacity: 0 }}
                    transition={{ duration: 0.3 }}
                  >
                    <div className="council-grid">
                      {councilArchetypes.map((archetype) => {
                        const isPreferred = userPreferences.preferredArchetypes?.includes(archetype);
                        
                        return (
                          <button
                            key={archetype}
                            className={`archetype-card ${isPreferred ? 'preferred' : ''}`}
                            onClick={() => handleArchetypePreference(archetype)}
                            style={{ '--archetype-color': getCouncilColor(archetype) }}
                          >
                            <span className="archetype-avatar">
                              {getCouncilAvatar(archetype)}
                            </span>
                            <span className="archetype-name">
                              {archetype.charAt(0).toUpperCase() + archetype.slice(1)}
                            </span>
                            {isPreferred && (
                              <div className="preferred-indicator">⭐</div>
                            )}
                          </button>
                        );
                      })}
                    </div>
                    <p className="council-help">
                      Click to set preferred teaching styles for new sessions
                    </p>
                  </motion.div>
                )}
              </AnimatePresence>
            </div>

            {/* Recent Sessions */}
            <div className="nav-section">
              <button
                className="nav-section-toggle"
                onClick={() => toggleSection('sessions')}
                aria-expanded={expandedSections.sessions}
              >
                <h3 className="nav-section-title">Recent Sessions</h3>
                {expandedSections.sessions ? (
                  <ChevronDown size={16} />
                ) : (
                  <ChevronRight size={16} />
                )}
              </button>
              
              <AnimatePresence>
                {expandedSections.sessions && (
                  <motion.div
                    className="sessions-list"
                    initial={{ height: 0, opacity: 0 }}
                    animate={{ height: 'auto', opacity: 1 }}
                    exit={{ height: 0, opacity: 0 }}
                    transition={{ duration: 0.3 }}
                  >
                    {recentSessions.length > 0 ? (
                      recentSessions.map((session) => (
                        <Link
                          key={session.id}
                          to={`/session/${session.id}`}
                          className="session-item"
                          onClick={onClose}
                        >
                          <div className="session-icon">
                            <History size={16} />
                          </div>
                          <div className="session-content">
                            <div className="session-topic">{session.topic}</div>
                            <div className="session-meta">
                              <span className="session-time">{session.timestamp}</span>
                              <span className="session-archetypes">
                                {session.archetypes} teachers
                              </span>
                            </div>
                          </div>
                        </Link>
                      ))
                    ) : (
                      <div className="no-sessions">
                        <p>No recent sessions</p>
                        <Link to="/session" onClick={onClose}>
                          Start your first session
                        </Link>
                      </div>
                    )}
                  </motion.div>
                )}
              </AnimatePresence>
            </div>
          </nav>

          {/* Current Session Status */}
          {currentSession && (
            <div className="current-session">
              <div className="session-header">
                <Zap size={16} className="session-status-icon" />
                <span>Active Session</span>
              </div>
              <div className="session-details">
                <div className="session-id">
                  {currentSession.id?.slice(-8) || 'Active'}
                </div>
                <div className="session-duration">
                  Started {new Date(currentSession.startTime).toLocaleTimeString()}
                </div>
                <div className="session-archetypes-count">
                  {currentSession.selectedArchetypes?.length || 0} AI teachers active
                </div>
              </div>
              <Link 
                to={`/session/${currentSession.id}`}
                className="session-continue-btn"
                onClick={onClose}
              >
                Continue Session
              </Link>
            </div>
          )}

          {/* Quick Preferences */}
          <div className="nav-section">
            <button
              className="nav-section-toggle"
              onClick={() => toggleSection('preferences')}
              aria-expanded={expandedSections.preferences}
            >
              <h3 className="nav-section-title">Quick Settings</h3>
              {expandedSections.preferences ? (
                <ChevronDown size={16} />
              ) : (
                <ChevronRight size={16} />
              )}
            </button>
            
            <AnimatePresence>
              {expandedSections.preferences && (
                <motion.div
                  className="quick-preferences"
                  initial={{ height: 0, opacity: 0 }}
                  animate={{ height: 'auto', opacity: 1 }}
                  exit={{ height: 0, opacity: 0 }}
                  transition={{ duration: 0.3 }}
                >
                  <div className="preference-item">
                    <label htmlFor="grade-level">Grade Level</label>
                    <select
                      id="grade-level"
                      value={userPreferences.gradeLevel || 'middle'}
                      onChange={(e) => onUpdatePreferences({ gradeLevel: e.target.value })}
                      className="preference-select"
                    >
                      <option value="elementary">Elementary (K-5)</option>
                      <option value="middle">Middle School (6-8)</option>
                      <option value="high">High School (9-12)</option>
                      <option value="university">University/Adult</option>
                    </select>
                  </div>
                  
                  <div className="preference-item">
                    <label>
                      <input
                        type="checkbox"
                        checked={userPreferences.animationsEnabled !== false}
                        onChange={(e) => onUpdatePreferences({ animationsEnabled: e.target.checked })}
                        className="preference-checkbox"
                      />
                      Enable animations
                    </label>
                  </div>
                </motion.div>
              )}
            </AnimatePresence>
          </div>
        </div>

        {/* Sidebar Footer */}
        <div className="sidebar-footer">
          <div className="help-section">
            <HelpCircle size={16} />
            <div>
              <div className="help-title">Need Help?</div>
              <div className="help-description">
                Learn how to use SIRAJ effectively
              </div>
            </div>
          </div>
          
          <div className="version-info">
            <div className="version-text">SIRAJ AI v8.1.0</div>
            <div className="model-info">Powered by Gemma 3n</div>
          </div>
        </div>
      </motion.aside>
    </>
  );
};

export default Sidebar;