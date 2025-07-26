import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { motion, AnimatePresence } from 'framer-motion';

/**
 * SIRAJ Educational Dashboard - Consciousness-Driven Overview
 * 
 * This component serves as the central hub for educational consciousness,
 * providing a comprehensive view of:
 * - System health and AI council status
 * - Learning progress and QWAN metrics
 * - Recent educational interactions
 * - Quick access to all major features
 * - Real-time system consciousness indicators
 * 
 * Embodies QWAN principles through visual design and information architecture
 */

const Dashboard = ({ 
  systemHealth, 
  qwanMetrics, 
  currentPhase, 
  sessionHistory, 
  isConnected 
}) => {
  const [activeInsight, setActiveInsight] = useState(0);
  const [timeOfDay, setTimeOfDay] = useState('');
  const [recentActivity, setRecentActivity] = useState([]);
  const [learningStats, setLearningStats] = useState({
    totalSessions: 0,
    totalQuestions: 0,
    averageEffectiveness: 0,
    preferredArchetypes: [],
    learningStreak: 0
  });

  // === ARCHETYPE SYSTEM CONFIGURATION ===
  const archetypes = [
    { 
      id: 'socratic', 
      name: 'Socratic', 
      emoji: '🦉', 
      color: '#8B4513',
      description: 'Questions & Critical Thinking',
      effectiveness: 87,
      recentUse: 12
    },
    { 
      id: 'constructivist', 
      name: 'Builder', 
      emoji: '🧱', 
      color: '#FF6B35',
      description: 'Hands-on Learning',
      effectiveness: 92,
      recentUse: 8
    },
    { 
      id: 'storyteller', 
      name: 'Storyteller', 
      emoji: '📖', 
      color: '#4ECDC4',
      description: 'Narrative Learning',
      effectiveness: 89,
      recentUse: 15
    },
    { 
      id: 'synthesizer', 
      name: 'Synthesizer', 
      emoji: '🌀', 
      color: '#A8E6CF',
      description: 'Integration & Unity',
      effectiveness: 94,
      recentUse: 6
    },
    { 
      id: 'challenger', 
      name: 'Challenger', 
      emoji: '⚡', 
      color: '#FFD93D',
      description: 'Critical Analysis',
      effectiveness: 76,
      recentUse: 4
    },
    { 
      id: 'mentor', 
      name: 'Mentor', 
      emoji: '🌱', 
      color: '#95E1D3',
      description: 'Support & Guidance',
      effectiveness: 91,
      recentUse: 10
    },
    { 
      id: 'analyst', 
      name: 'Analyst', 
      emoji: '🔬', 
      color: '#FF8B94',
      description: 'Data & Logic',
      effectiveness: 85,
      recentUse: 7
    }
  ];

  // === EDUCATIONAL INSIGHTS ===
  const insights = [
    {
      title: "Multi-Perspective Learning",
      description: "AI Council provides 7 distinct teaching approaches for comprehensive understanding",
      metric: "94% Synthesis Quality",
      icon: "🏛️",
      color: "var(--color-primary)"
    },
    {
      title: "Living Spiral Methodology",
      description: "Natural learning cycle: Collapse → Council → Synthesis → Rebirth",
      metric: `Current: ${currentPhase.charAt(0).toUpperCase() + currentPhase.slice(1)}`,
      icon: "🌀",
      color: "var(--color-secondary)"
    },
    {
      title: "QWAN-Aligned Education",
      description: "Quality Without A Name principles embedded in every interaction",
      metric: `${Math.round((Object.values(qwanMetrics || {}).reduce((a, b) => a + b, 0) / 5) * 100)}% Average`,
      icon: "⚖️",
      color: "var(--color-accent)"
    },
    {
      title: "Consciousness-Driven AI",
      description: "Ethical AI that prioritizes student growth over system metrics",
      metric: "Always Active",
      icon: "🧠",
      color: "var(--color-success)"
    }
  ];

  // === QUICK ACTIONS CONFIGURATION ===
  const quickActions = [
    {
      title: "Start Council Session",
      description: "Begin multi-archetype AI collaboration",
      icon: "🏛️",
      path: "/council",
      color: "var(--color-primary)",
      gradient: "linear-gradient(135deg, var(--color-primary), var(--color-secondary))"
    },
    {
      title: "Submit Homework",
      description: "Get AI feedback from multiple perspectives",
      icon: "📝",
      path: "/homework",
      color: "var(--color-accent)",
      gradient: "linear-gradient(135deg, var(--color-accent), var(--color-info))"
    },
    {
      title: "View Analytics",
      description: "Explore learning insights and progress",
      icon: "📊",
      path: "/analytics",
      color: "var(--color-info)",
      gradient: "linear-gradient(135deg, var(--color-info), var(--color-primary))"
    },
    {
      title: "Curriculum Alignment",
      description: "Map learning to educational standards",
      icon: "🎯",
      path: "/curriculum",
      color: "var(--color-warning)",
      gradient: "linear-gradient(135deg, var(--color-warning), var(--color-accent))"
    },
    {
      title: "Track Progress",
      description: "Monitor learning growth and mastery",
      icon: "📈",
      path: "/progress",
      color: "var(--color-success)",
      gradient: "linear-gradient(135deg, var(--color-success), var(--color-primary))"
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
    const interval = setInterval(updateTimeOfDay, 60000); // Update every minute
    return () => clearInterval(interval);
  }, []);

  // === INSIGHTS ROTATION ===
  useEffect(() => {
    const interval = setInterval(() => {
      setActiveInsight(prev => (prev + 1) % insights.length);
    }, 5000);
    return () => clearInterval(interval);
  }, [insights.length]);

  // === MOCK DATA GENERATION (In real app, this would come from API) ===
  useEffect(() => {
    // Simulate recent activity
    setRecentActivity([
      {
        id: 1,
        type: "council_session",
        title: "Discussed quantum mechanics with AI Council",
        timestamp: Date.now() - 1000 * 60 * 30, // 30 minutes ago
        archetypes: ["socratic", "analyst", "storyteller"],
        effectiveness: 92
      },
      {
        id: 2,
        type: "homework_feedback",
        title: "Received feedback on climate change essay",
        timestamp: Date.now() - 1000 * 60 * 60 * 2, // 2 hours ago
        archetypes: ["mentor", "challenger", "constructivist"],
        effectiveness: 87
      },
      {
        id: 3,
        type: "progress_update",
        title: "Mastery level increased in Physics",
        timestamp: Date.now() - 1000 * 60 * 60 * 24, // 1 day ago
        subject: "Physics",
        improvement: "+12%"
      }
    ]);

    // Simulate learning statistics
    setLearningStats({
      totalSessions: 147,
      totalQuestions: 523,
      averageEffectiveness: 89,
      preferredArchetypes: ["storyteller", "socratic", "mentor"],
      learningStreak: 12
    });
  }, []);

  // === UTILITY FUNCTIONS ===
  const formatTimeAgo = (timestamp) => {
    const diff = Date.now() - timestamp;
    const minutes = Math.floor(diff / (1000 * 60));
    const hours = Math.floor(diff / (1000 * 60 * 60));
    const days = Math.floor(diff / (1000 * 60 * 60 * 24));

    if (days > 0) return `${days} day${days > 1 ? 's' : ''} ago`;
    if (hours > 0) return `${hours} hour${hours > 1 ? 's' : ''} ago`;
    if (minutes > 0) return `${minutes} minute${minutes > 1 ? 's' : ''} ago`;
    return 'Just now';
  };

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

  return (
    <div className="dashboard">
      {/* Welcome Section */}
      <div className="dashboard-header">
        <div className="welcome-section">
          <motion.div 
            className="welcome-message"
            initial={{ opacity: 0, y: 30 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6 }}
          >
            <h1 className="welcome-title">
              <span className="welcome-icon">🧠</span>
              {getGreeting()}
            </h1>
            <p className="welcome-subtitle">
              Your consciousness-driven learning companion is ready. 
              The AI Council awaits your questions.
            </p>
          </motion.div>

          <motion.div 
            className="system-status-card"
            initial={{ opacity: 0, x: 30 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.6, delay: 0.2 }}
          >
            <div className="status-header">
              <span className="status-icon">⚡</span>
              <h3 className="status-title">System Consciousness</h3>
            </div>
            <div className="status-metrics">
              <div className="status-item">
                <span className={`status-indicator ${isConnected ? 'connected' : 'offline'}`}>
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
                  {archetypes.length} AI Teachers Active
                </span>
              </div>
            </div>
          </motion.div>
        </div>
      </div>

      {/* Quick Actions Grid */}
      <div className="quick-actions-section">
        <h2 className="section-title">
          <span className="title-icon">🚀</span>
          Quick Actions
        </h2>
        <div className="quick-actions-grid">
          {quickActions.map((action, index) => (
            <motion.div
              key={action.path}
              initial={{ opacity: 0, y: 20, scale: 0.95 }}
              animate={{ opacity: 1, y: 0, scale: 1 }}
              transition={{ duration: 0.4, delay: index * 0.1 }}
            >
              <Link to={action.path} className="quick-action-card">
                <div className="action-background" style={{ background: action.gradient }}>
                  <div className="action-icon">{action.icon}</div>
                </div>
                <div className="action-content">
                  <h3 className="action-title">{action.title}</h3>
                  <p className="action-description">{action.description}</p>
                </div>
                <div className="action-arrow">→</div>
              </Link>
            </motion.div>
          ))}
        </div>
      </div>

      {/* Main Dashboard Content */}
      <div className="dashboard-main">
        {/* Left Column */}
        <div className="dashboard-left">
          {/* AI Council Status */}
          <div className="dashboard-card council-status-card">
            <div className="card-header">
              <h3 className="card-title">
                <span className="card-icon">🏛️</span>
                AI Council Status
              </h3>
              <div className="council-effectiveness">
                {Math.round(archetypes.reduce((sum, arch) => sum + arch.effectiveness, 0) / archetypes.length)}% 
                <span className="effectiveness-label">Avg Effectiveness</span>
              </div>
            </div>
            <div className="council-grid">
              {archetypes.map((archetype, index) => (
                <motion.div
                  key={archetype.id}
                  className="archetype-status"
                  initial={{ opacity: 0, scale: 0.8 }}
                  animate={{ opacity: 1, scale: 1 }}
                  transition={{ duration: 0.3, delay: index * 0.05 }}
                  style={{ '--archetype-color': archetype.color }}
                >
                  <div className="archetype-avatar">
                    <span className="archetype-emoji">{archetype.emoji}</span>
                  </div>
                  <div className="archetype-info">
                    <span className="archetype-name">{archetype.name}</span>
                    <span className="archetype-description">{archetype.description}</span>
                  </div>
                  <div className="archetype-metrics">
                    <div className="effectiveness-bar">
                      <div 
                        className="effectiveness-fill"
                        style={{ width: `${archetype.effectiveness}%` }}
                      ></div>
                    </div>
                    <span className="recent-use">Used {archetype.recentUse}x</span>
                  </div>
                </motion.div>
              ))}
            </div>
          </div>

          {/* Learning Statistics */}
          <div className="dashboard-card learning-stats-card">
            <div className="card-header">
              <h3 className="card-title">
                <span className="card-icon">📊</span>
                Learning Statistics
              </h3>
              <div className="stats-period">This Month</div>
            </div>
            <div className="stats-grid">
              <div className="stat-item">
                <div className="stat-value">{learningStats.totalSessions}</div>
                <div className="stat-label">Council Sessions</div>
                <div className="stat-trend positive">+23%</div>
              </div>
              <div className="stat-item">
                <div className="stat-value">{learningStats.totalQuestions}</div>
                <div className="stat-label">Questions Asked</div>
                <div className="stat-trend positive">+18%</div>
              </div>
              <div className="stat-item">
                <div className="stat-value">{learningStats.averageEffectiveness}%</div>
                <div className="stat-label">Avg Effectiveness</div>
                <div className="stat-trend positive">+5%</div>
              </div>
              <div className="stat-item">
                <div className="stat-value">{learningStats.learningStreak}</div>
                <div className="stat-label">Day Streak</div>
                <div className="stat-trend positive">🔥</div>
              </div>
            </div>

            <div className="preferred-archetypes">
              <h4 className="subsection-title">Your Preferred AI Teachers</h4>
              <div className="preferred-list">
                {learningStats.preferredArchetypes.map((archetypeId, index) => {
                  const archetype = archetypes.find(a => a.id === archetypeId);
                  return (
                    <div key={archetypeId} className="preferred-item">
                      <span className="rank">#{index + 1}</span>
                      <span className="preferred-emoji">{archetype?.emoji}</span>
                      <span className="preferred-name">{archetype?.name}</span>
                    </div>
                  );
                })}
              </div>
            </div>
          </div>
        </div>

        {/* Right Column */}
        <div className="dashboard-right">
          {/* Educational Insights Carousel */}
          <div className="dashboard-card insights-card">
            <div className="card-header">
              <h3 className="card-title">
                <span className="card-icon">💡</span>
                Educational Insights
              </h3>
              <div className="insight-navigation">
                {insights.map((_, index) => (
                  <button
                    key={index}
                    className={`nav-dot ${index === activeInsight ? 'active' : ''}`}
                    onClick={() => setActiveInsight(index)}
                  />
                ))}
              </div>
            </div>
            <AnimatePresence mode="wait">
              <motion.div
                key={activeInsight}
                className="insight-content"
                initial={{ opacity: 0, x: 20 }}
                animate={{ opacity: 1, x: 0 }}
                exit={{ opacity: 0, x: -20 }}
                transition={{ duration: 0.4 }}
              >
                <div className="insight-icon" style={{ color: insights[activeInsight].color }}>
                  {insights[activeInsight].icon}
                </div>
                <h4 className="insight-title">{insights[activeInsight].title}</h4>
                <p className="insight-description">{insights[activeInsight].description}</p>
                <div className="insight-metric">
                  <span className="metric-label">Current Status:</span>
                  <span className="metric-value" style={{ color: insights[activeInsight].color }}>
                    {insights[activeInsight].metric}
                  </span>
                </div>
              </motion.div>
            </AnimatePresence>
          </div>

          {/* QWAN Metrics */}
          {qwanMetrics && (
            <div className="dashboard-card qwan-card">
              <div className="card-header">
                <h3 className="card-title">
                  <span className="card-icon">⚖️</span>
                  QWAN Alignment
                </h3>
                <div className="qwan-score">
                  {Math.round((Object.values(qwanMetrics).reduce((a, b) => a + b, 0) / 5) * 100)}%
                </div>
              </div>
              <div className="qwan-metrics">
                {Object.entries(qwanMetrics).map(([principle, score], index) => (
                  <motion.div
                    key={principle}
                    className="qwan-metric"
                    initial={{ opacity: 0, y: 10 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ duration: 0.3, delay: index * 0.1 }}
                  >
                    <div className="metric-header">
                      <span className="metric-name">
                        {principle.charAt(0).toUpperCase() + principle.slice(1)}
                      </span>
                      <span className="metric-value">{Math.round(score * 100)}%</span>
                    </div>
                    <div className="metric-bar">
                      <motion.div
                        className="metric-fill"
                        initial={{ width: 0 }}
                        animate={{ width: `${score * 100}%` }}
                        transition={{ duration: 1, delay: index * 0.1 }}
                      />
                    </div>
                  </motion.div>
                ))}
              </div>
            </div>
          )}

          {/* Recent Activity */}
          <div className="dashboard-card activity-card">
            <div className="card-header">
              <h3 className="card-title">
                <span className="card-icon">📅</span>
                Recent Activity
              </h3>
              <Link to="/analytics" className="view-all-link">View All</Link>
            </div>
            <div className="activity-list">
              {recentActivity.map((activity, index) => (
                <motion.div
                  key={activity.id}
                  className="activity-item"
                  initial={{ opacity: 0, x: 20 }}
                  animate={{ opacity: 1, x: 0 }}
                  transition={{ duration: 0.3, delay: index * 0.1 }}
                >
                  <div className="activity-icon">
                    {activity.type === 'council_session' && '🏛️'}
                    {activity.type === 'homework_feedback' && '📝'}
                    {activity.type === 'progress_update' && '📈'}
                  </div>
                  <div className="activity-content">
                    <h4 className="activity-title">{activity.title}</h4>
                    <div className="activity-meta">
                      <span className="activity-time">{formatTimeAgo(activity.timestamp)}</span>
                      {activity.archetypes && (
                        <div className="activity-archetypes">
                          {activity.archetypes.slice(0, 3).map(archetypeId => {
                            const archetype = archetypes.find(a => a.id === archetypeId);
                            return (
                              <span key={archetypeId} className="archetype-mini">
                                {archetype?.emoji}
                              </span>
                            );
                          })}
                        </div>
                      )}
                      {activity.effectiveness && (
                        <span className="activity-effectiveness">
                          {activity.effectiveness}% effective
                        </span>
                      )}
                      {activity.improvement && (
                        <span className="activity-improvement">
                          {activity.improvement}
                        </span>
                      )}
                    </div>
                  </div>
                </motion.div>
              ))}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
