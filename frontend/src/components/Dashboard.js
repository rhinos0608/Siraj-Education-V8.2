import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { motion } from 'framer-motion';

/**
 * SIRAJ Educational Dashboard - Notion-Inspired Clean Design
 * 
 * Simplified, readable interface focusing on:
 * - Clear information hierarchy
 * - High contrast text for readability
 * - Notion-style card layouts
 * - Graceful offline/error handling
 * - Clean visual design with proper spacing
 */

const Dashboard = ({ 
  systemHealth, 
  qwanMetrics, 
  currentPhase = 'synthesis', 
  isConnected = false 
}) => {
  const [timeOfDay, setTimeOfDay] = useState('');
  
  // System statistics - can be made dynamic in future
  const systemStats = {
    totalSessions: 147,
    averageEffectiveness: 89,
    learningStreak: 12,
    activeArchetypes: 7
  };

  // === ARCHETYPE SYSTEM CONFIGURATION ===
  const archetypes = [
    { 
      id: 'socratic', 
      name: 'Socratic Teacher', 
      emoji: '🦉', 
      effectiveness: 87,
      description: 'Questions & Critical Thinking'
    },
    { 
      id: 'constructivist', 
      name: 'Builder Teacher', 
      emoji: '🧱', 
      effectiveness: 92,
      description: 'Hands-on Learning'
    },
    { 
      id: 'storyteller', 
      name: 'Storyteller Teacher', 
      emoji: '📖', 
      effectiveness: 89,
      description: 'Narrative Learning'
    },
    { 
      id: 'synthesizer', 
      name: 'Synthesizer Teacher', 
      emoji: '🌀', 
      effectiveness: 94,
      description: 'Integration & Unity'
    },
    { 
      id: 'mentor', 
      name: 'Mentor Teacher', 
      emoji: '🌱', 
      effectiveness: 91,
      description: 'Support & Guidance'
    },
    { 
      id: 'analyst', 
      name: 'Analyst Teacher', 
      emoji: '🔬', 
      effectiveness: 85,
      description: 'Data & Logic'
    },
    { 
      id: 'challenger', 
      name: 'Challenger Teacher', 
      emoji: '⚡', 
      effectiveness: 76,
      description: 'Critical Analysis'
    }
  ];

  // === QUICK ACTIONS CONFIGURATION ===
  const quickActions = [
    {
      title: "Start Council Session",
      description: "Begin multi-archetype AI collaboration",
      icon: "🏛️",
      path: "/council",
      color: "var(--color-primary)"
    },
    {
      title: "Submit Homework",
      description: "Get AI feedback from multiple perspectives",
      icon: "📝",
      path: "/homework",
      color: "var(--color-accent)"
    },
    {
      title: "View Analytics",
      description: "Explore learning insights and progress",
      icon: "📊",
      path: "/analytics",
      color: "var(--color-success)"
    },
    {
      title: "Curriculum Alignment",
      description: "Map learning to educational standards",
      icon: "🎯",
      path: "/curriculum",
      color: "var(--color-warning)"
    }
  ];

  // === TIME-AWARE GREETING ===
  useEffect(() => {
    const updateTimeOfDay = () => {
      const hour = new Date().getHours();
      if (hour < 6) setTimeOfDay('late night');
      else if (hour < 12) setTimeOfDay('morning');
      else if (hour < 17) setTimeOfDay('afternoon');
      else if (hour < 21) setTimeOfDay('evening');
      else setTimeOfDay('night');
    };

    updateTimeOfDay();
    const interval = setInterval(updateTimeOfDay, 60000);
    return () => clearInterval(interval);
  }, []);

  const getGreeting = () => {
    const greetings = {
      'morning': 'Good morning! Ready to explore new ideas?',
      'afternoon': 'Good afternoon! Let\'s continue your learning journey.',
      'evening': 'Good evening! Time for deeper reflection and synthesis.',
      'night': 'Working late? The AI Council is always here to help.',
      'late night': 'Burning the midnight oil? Let\'s make it productive!'
    };
    return greetings[timeOfDay] || 'Welcome back to your learning journey!';
  };

  const getPhaseDescription = () => {
    const descriptions = {
      'collapse': 'Analyzing learning needs and preparing for growth',
      'council': 'AI teachers are collaborating on your questions',
      'synthesis': 'Integrating multiple perspectives into unified understanding',
      'rebirth': 'Ready for new learning adventures and discoveries'
    };
    return descriptions[currentPhase] || 'System ready for learning';
  };

  const averageEffectiveness = Math.round(
    archetypes.reduce((sum, arch) => sum + arch.effectiveness, 0) / archetypes.length
  );

  return (
    <div className="dashboard">
      {/* Offline Banner */}
      {!isConnected && (
        <div className="offline-banner">
          <strong>Offline Mode:</strong> Limited functionality available. Some features require internet connection.
        </div>
      )}

      {/* Welcome Section */}
      <div className="dashboard-header">
        <motion.div 
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6 }}
        >
          <h1 className="welcome-title">
            <span>🧠</span>
            {getGreeting()}
          </h1>
          <p className="welcome-subtitle">
            Your consciousness-driven learning companion is ready. The AI Council awaits your questions.
          </p>
        </motion.div>
      </div>

      {/* System Status */}
      <div className="dashboard-card">
        <div className="card-header">
          <h3 className="card-title">
            <span className="card-icon">⚡</span>
            System Status
          </h3>
        </div>
        
        <div className="system-status">
          <div className="status-item">
            <span className="status-indicator">
              {isConnected ? '🟢' : '🔴'}
            </span>
            <span className="status-label">
              {isConnected ? 'AI Council Online' : 'Offline Mode'}
            </span>
          </div>
          
          <div className="status-item">
            <span className="status-indicator">🌀</span>
            <span className="status-label">
              Phase: {currentPhase.charAt(0).toUpperCase() + currentPhase.slice(1)}
            </span>
          </div>
          
          <div className="status-item">
            <span className="status-indicator">👥</span>
            <span className="status-label">
              {systemStats.activeArchetypes} AI Teachers Active
            </span>
          </div>
          
          <div className="status-item">
            <span className="status-indicator">📊</span>
            <span className="status-label">
              {averageEffectiveness}% Average Effectiveness
            </span>
          </div>
        </div>
        
        <p className="text-secondary" style={{ marginTop: 'var(--spacing-md)', marginBottom: 0 }}>
          {getPhaseDescription()}
        </p>
      </div>

      {/* Quick Actions */}
      <div className="dashboard-card">
        <div className="card-header">
          <h3 className="card-title">
            <span className="card-icon">🚀</span>
            Quick Actions
          </h3>
        </div>
        
        <div className="quick-actions-grid">
          {quickActions.map((action, index) => (
            <motion.div
              key={action.path}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.4, delay: index * 0.1 }}
            >
              <Link to={action.path} className="quick-action-card">
                <div className="action-title">
                  <span>{action.icon}</span>
                  {action.title}
                </div>
                <p className="action-description">{action.description}</p>
              </Link>
            </motion.div>
          ))}
        </div>
      </div>

      {/* AI Council Overview */}
      <div className="dashboard-card">
        <div className="card-header">
          <h3 className="card-title">
            <span className="card-icon">🏛️</span>
            AI Council Overview
          </h3>
          <span className="text-secondary">
            {averageEffectiveness}% Avg Effectiveness
          </span>
        </div>
        
        <div className="archetype-grid">
          {archetypes.map((archetype, index) => (
            <motion.div
              key={archetype.id}
              className="archetype-mini-card"
              initial={{ opacity: 0, scale: 0.9 }}
              animate={{ opacity: 1, scale: 1 }}
              transition={{ duration: 0.3, delay: index * 0.05 }}
              style={{ '--archetype-color': `var(--color-${archetype.id})` }}
            >
              <div className="archetype-mini-header">
                <span className="archetype-emoji">{archetype.emoji}</span>
                <div>
                  <div className="archetype-name">{archetype.name}</div>
                  <div className="archetype-effectiveness">{archetype.effectiveness}% effective</div>
                </div>
              </div>
              <div className="archetype-progress">
                <div 
                  className="progress-fill"
                  style={{ width: `${archetype.effectiveness}%` }}
                ></div>
              </div>
              <p className="text-secondary" style={{ fontSize: 'var(--font-size-xs)', marginTop: 'var(--spacing-sm)', marginBottom: 0 }}>
                {archetype.description}
              </p>
            </motion.div>
          ))}
        </div>
      </div>

      {/* Learning Stats */}
      <div className="dashboard-card">
        <div className="card-header">
          <h3 className="card-title">
            <span className="card-icon">📈</span>
            Learning Progress
          </h3>
        </div>
        
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: 'var(--spacing-lg)' }}>
          <div>
            <div style={{ fontSize: 'var(--font-size-xl)', fontWeight: '600', color: 'var(--color-text-primary)' }}>
              {systemStats.totalSessions}
            </div>
            <div className="text-secondary">Total Sessions</div>
          </div>
          
          <div>
            <div style={{ fontSize: 'var(--font-size-xl)', fontWeight: '600', color: 'var(--color-text-primary)' }}>
              {systemStats.averageEffectiveness}%
            </div>
            <div className="text-secondary">Avg Effectiveness</div>
          </div>
          
          <div>
            <div style={{ fontSize: 'var(--font-size-xl)', fontWeight: '600', color: 'var(--color-text-primary)' }}>
              {systemStats.learningStreak}
            </div>
            <div className="text-secondary">Day Streak 🔥</div>
          </div>
          
          <div>
            <div style={{ fontSize: 'var(--font-size-xl)', fontWeight: '600', color: 'var(--color-text-primary)' }}>
              {systemStats.activeArchetypes}
            </div>
            <div className="text-secondary">AI Teachers</div>
          </div>
        </div>
      </div>

      {/* QWAN Metrics */}
      {qwanMetrics && (
        <div className="dashboard-card">
          <div className="card-header">
            <h3 className="card-title">
              <span className="card-icon">⚖️</span>
              QWAN Alignment
            </h3>
            <span className="text-secondary">
              {Math.round((Object.values(qwanMetrics).reduce((a, b) => a + b, 0) / 5) * 100)}% Overall
            </span>
          </div>
          
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: 'var(--spacing-lg)' }}>
            {Object.entries(qwanMetrics).map(([principle, score]) => (
              <div key={principle}>
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 'var(--spacing-sm)' }}>
                  <span style={{ fontWeight: '500', color: 'var(--color-text-primary)' }}>
                    {principle.charAt(0).toUpperCase() + principle.slice(1)}
                  </span>
                  <span className="text-secondary">{Math.round(score * 100)}%</span>
                </div>
                <div style={{ height: '6px', backgroundColor: 'var(--color-bg-tertiary)', borderRadius: '3px', overflow: 'hidden' }}>
                  <motion.div
                    style={{ 
                      height: '100%', 
                      backgroundColor: 'var(--color-primary)',
                      width: `${score * 100}%`
                    }}
                    initial={{ width: 0 }}
                    animate={{ width: `${score * 100}%` }}
                    transition={{ duration: 1, delay: 0.2 }}
                  />
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Getting Started */}
      <div className="dashboard-card">
        <div className="card-header">
          <h3 className="card-title">
            <span className="card-icon">💡</span>
            Getting Started
          </h3>
        </div>
        
        <div style={{ color: 'var(--color-text-secondary)' }}>
          <p>Ready to begin your learning journey? Here are some suggestions:</p>
          <ul style={{ listStyle: 'none', padding: 0 }}>
            <li style={{ padding: 'var(--spacing-sm) 0', borderBottom: '1px solid var(--color-bg-tertiary)' }}>
              <strong style={{ color: 'var(--color-text-primary)' }}>Ask a Question:</strong> Start a council session with any topic you're curious about
            </li>
            <li style={{ padding: 'var(--spacing-sm) 0', borderBottom: '1px solid var(--color-bg-tertiary)' }}>
              <strong style={{ color: 'var(--color-text-primary)' }}>Submit Homework:</strong> Get detailed feedback from multiple AI teachers
            </li>
            <li style={{ padding: 'var(--spacing-sm) 0', borderBottom: '1px solid var(--color-bg-tertiary)' }}>
              <strong style={{ color: 'var(--color-text-primary)' }}>View Analytics:</strong> Track your learning progress and insights
            </li>
            <li style={{ padding: 'var(--spacing-sm) 0' }}>
              <strong style={{ color: 'var(--color-text-primary)' }}>Explore Features:</strong> Discover curriculum alignment and progress tracking
            </li>
          </ul>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;