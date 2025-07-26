import React, { useState } from 'react';
import { Link, useLocation } from 'react-router-dom';
import { motion } from 'framer-motion';
import { 
  Menu, 
  X, 
  Brain, 
  Zap, 
  Settings, 
  User,
  Bell,
  Search,
  Sun,
  Moon,
  Activity
} from 'lucide-react';
import './Header.css';

/**
 * Header Component
 * ===============
 * 
 * Main navigation header for the SIRAJ Educational AI application.
 * Features responsive design, theme switching, and session status.
 */

const Header = ({ 
  sidebarOpen, 
  setSidebarOpen, 
  currentSession, 
  isConnected, 
  onNewSession,
  userPreferences,
  onUpdatePreferences 
}) => {
  const location = useLocation();
  const [searchQuery, setSearchQuery] = useState('');
  const [showSearch, setShowSearch] = useState(false);
  const [showNotifications, setShowNotifications] = useState(false);

  const toggleTheme = () => {
    const newTheme = userPreferences?.theme === 'light' ? 'dark' : 'light';
    onUpdatePreferences?.({ theme: newTheme });
  };

  const handleSearch = (e) => {
    e.preventDefault();
    if (searchQuery.trim()) {
      // Implement search functionality
      console.log('Searching for:', searchQuery);
      setSearchQuery('');
      setShowSearch(false);
    }
  };

  const getPageTitle = () => {
    switch (location.pathname) {
      case '/':
        return 'Dashboard';
      case '/session':
      case '/session/':
        return 'AI Council Session';
      case '/homework':
        return 'Homework Assistant';
      case '/analytics':
        return 'Learning Analytics';
      case '/settings':
        return 'Settings';
      default:
        if (location.pathname.startsWith('/session/')) {
          return `Session ${currentSession?.id?.slice(-8) || 'Active'}`;
        }
        return 'SIRAJ Educational AI';
    }
  };

  const notifications = [
    { id: 1, type: 'session', message: 'Council session completed successfully', time: '2 minutes ago' },
    { id: 2, type: 'homework', message: 'New homework feedback available', time: '1 hour ago' },
    { id: 3, type: 'system', message: 'AI models updated to latest version', time: '3 hours ago' }
  ];

  return (
    <header className="app-header">
      <div className="header-container">
        {/* Left section - Logo and Navigation */}
        <div className="header-left">
          {/* Sidebar toggle */}
          <button
            className="sidebar-toggle"
            onClick={() => setSidebarOpen(!sidebarOpen)}
            aria-label="Toggle sidebar"
          >
            <motion.div
              animate={{ rotate: sidebarOpen ? 90 : 0 }}
              transition={{ duration: 0.2 }}
            >
              {sidebarOpen ? <X size={20} /> : <Menu size={20} />}
            </motion.div>
          </button>

          {/* Logo */}
          <Link to="/" className="header-logo">
            <Brain className="logo-icon" size={32} />
            <div className="logo-text">
              <span className="logo-primary">SIRAJ</span>
              <span className="logo-secondary">AI</span>
            </div>
          </Link>

          {/* Page title */}
          <div className="page-title">
            <h1>{getPageTitle()}</h1>
            {currentSession && (
              <div className="session-indicator">
                <Activity size={14} />
                <span>Session Active</span>
              </div>
            )}
          </div>
        </div>

        {/* Center section - Search */}
        <div className="header-center">
          {showSearch ? (
            <motion.form
              className="search-form"
              onSubmit={handleSearch}
              initial={{ width: 0, opacity: 0 }}
              animate={{ width: 300, opacity: 1 }}
              exit={{ width: 0, opacity: 0 }}
              transition={{ duration: 0.3 }}
            >
              <Search size={16} className="search-icon" />
              <input
                type="text"
                placeholder="Search topics, sessions, homework..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                autoFocus
                className="search-input"
              />
              <button
                type="button"
                onClick={() => setShowSearch(false)}
                className="search-close"
              >
                <X size={16} />
              </button>
            </motion.form>
          ) : (
            <button
              className="search-trigger"
              onClick={() => setShowSearch(true)}
              aria-label="Open search"
            >
              <Search size={16} />
              <span>Search...</span>
            </button>
          )}
        </div>

        {/* Right section - Actions and Status */}
        <div className="header-right">
          {/* Connection status */}
          <div className={`connection-status ${isConnected ? 'connected' : 'disconnected'}`}>
            <div className="status-dot"></div>
            <span className="status-text">
              {isConnected ? 'Connected' : 'Disconnected'}
            </span>
          </div>

          {/* New session button */}
          <button
            className="new-session-btn"
            onClick={onNewSession}
            disabled={!isConnected}
            aria-label="Start new AI council session"
          >
            <Zap size={16} />
            <span>New Session</span>
          </button>

          {/* Notifications */}
          <div className="notifications-container">
            <button
              className={`notifications-btn ${showNotifications ? 'active' : ''}`}
              onClick={() => setShowNotifications(!showNotifications)}
              aria-label="View notifications"
            >
              <Bell size={18} />
              {notifications.length > 0 && (
                <span className="notification-badge">{notifications.length}</span>
              )}
            </button>

            {showNotifications && (
              <motion.div
                className="notifications-dropdown"
                initial={{ opacity: 0, y: -10, scale: 0.95 }}
                animate={{ opacity: 1, y: 0, scale: 1 }}
                exit={{ opacity: 0, y: -10, scale: 0.95 }}
                transition={{ duration: 0.2 }}
              >
                <div className="notifications-header">
                  <h3>Notifications</h3>
                  <button
                    onClick={() => setShowNotifications(false)}
                    className="close-notifications"
                  >
                    <X size={16} />
                  </button>
                </div>
                <div className="notifications-list">
                  {notifications.length > 0 ? (
                    notifications.map((notification) => (
                      <div key={notification.id} className="notification-item">
                        <div className={`notification-type ${notification.type}`}></div>
                        <div className="notification-content">
                          <p>{notification.message}</p>
                          <span className="notification-time">{notification.time}</span>
                        </div>
                      </div>
                    ))
                  ) : (
                    <div className="no-notifications">
                      <p>No notifications</p>
                    </div>
                  )}
                </div>
              </motion.div>
            )}
          </div>

          {/* Theme toggle */}
          <button
            className="theme-toggle"
            onClick={toggleTheme}
            aria-label="Toggle theme"
          >
            {userPreferences?.theme === 'light' ? (
              <Moon size={18} />
            ) : (
              <Sun size={18} />
            )}
          </button>

          {/* Settings */}
          <Link to="/settings" className="settings-link">
            <Settings size={18} />
          </Link>

          {/* User profile */}
          <div className="user-profile">
            <button className="profile-btn" aria-label="User profile">
              <User size={18} />
            </button>
          </div>
        </div>
      </div>

      {/* Mobile overlay for search */}
      {showSearch && (
        <div className="mobile-search-overlay" onClick={() => setShowSearch(false)}>
          <div className="mobile-search-container" onClick={(e) => e.stopPropagation()}>
            <form onSubmit={handleSearch} className="mobile-search-form">
              <Search size={20} className="search-icon" />
              <input
                type="text"
                placeholder="Search SIRAJ..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                autoFocus
                className="mobile-search-input"
              />
              <button type="button" onClick={() => setShowSearch(false)}>
                <X size={20} />
              </button>
            </form>
          </div>
        </div>
      )}
    </header>
  );
};

export default Header;