import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { motion } from 'framer-motion';
import {
  Brain,
  BookOpen,
  BarChart3,
  Zap,
  Users,
  Clock,
  TrendingUp,
  Award,
  Target,
  PlayCircle,
  ChevronRight,
  Sparkles
} from 'lucide-react';
import { 
  getCouncilColor, 
  getCouncilAvatar, 
  listCouncilVoices,
  getRecommendedArchetypes 
} from '../../utils/councilUtils';
import { useSirajAPI } from '../../hooks/useSirajAPI';
import './Dashboard.css';

/**
 * Dashboard Component
 * ==================
 * 
 * Main dashboard for the SIRAJ Educational AI application.
 * Provides overview, quick actions, and personalized recommendations.
 */

const Dashboard = ({ 
  currentSession, 
  userPreferences, 
  onStartSession, 
  onUpdatePreferences 
}) => {
  const [councilStatus, setCouncilStatus] = useState(null);
  const [recentActivity, setRecentActivity] = useState([]);
  const [learningStats, setLearningStats] = useState({
    sessionsCompleted: 0,
    homeworkSubmitted: 0,
    conceptsLearned: 0,
    streakDays: 0
  });
  const [welcomeMessage, setWelcomeMessage] = useState('');

  const { getCouncilStatus, loading, error } = useSirajAPI();

  useEffect(() => {
    loadDashboardData();
    generateWelcomeMessage();
  }, []);

  const loadDashboardData = async () => {
    try {
      const status = await getCouncilStatus();
      setCouncilStatus(status);
      
      // Mock data - in real app, would come from API
      setRecentActivity([
        {
          id: 1,
          type: 'session',
          title: 'Photosynthesis Deep Dive',
          description: 'Explored plant biology with 5 AI teachers',
          timestamp: new Date(Date.now() - 2 * 60 * 60 * 1000), // 2 hours ago
          archetypes: ['constructivist', 'storyteller', 'analyst']
        },
        {
          id: 2,
          type: 'homework',
          title: 'Algebra Problem Set #3',
          description: 'Received detailed feedback from AI council',
          timestamp: new Date(Date.now() - 1 * 24 * 60 * 60 * 1000), // 1 day ago
          score: 92
        },
        {
          id: 3,
          type: 'achievement',
          title: 'Critical Thinker Badge',
          description: 'Earned for asking insightful questions',
          timestamp: new Date(Date.now() - 2 * 24 * 60 * 60 * 1000), // 2 days ago
        }
      ]);
      
      setLearningStats({
        sessionsCompleted: 23,
        homeworkSubmitted: 15,
        conceptsLearned: 47,
        streakDays: 7
      });
    } catch (err) {
      console.error('Failed to load dashboard data:', err);
    }
  };

  const generateWelcomeMessage = () => {
    const hour = new Date().getHours();
    let greeting;
    
    if (hour < 12) {
      greeting = 'Good morning';
    } else if (hour < 17) {
      greeting = 'Good afternoon';
    } else {
      greeting = 'Good evening';
    }
    
    const gradeLevel = userPreferences.gradeLevel || 'middle';
    const messages = [
      `${greeting}! Ready to learn with your AI council?`,
      `${greeting}! What would you like to explore today?`,
      `${greeting}! Your AI teachers are ready to help you grow.`,
      `${greeting}! Let's unlock new knowledge together.`
    ];
    
    setWelcomeMessage(messages[Math.floor(Math.random() * messages.length)]);
  };

  const getTimeBasedSuggestions = () => {
    const hour = new Date().getHours();
    const gradeLevel = userPreferences.gradeLevel || 'middle';
    
    if (hour < 12) {
      return {
        title: "Morning Learning Boost",
        suggestions: [
          { topic: "Math Problem Solving", reason: "Your brain is fresh for analytical thinking" },
          { topic: "Science Concepts", reason: "Perfect time for complex topics" },
          { topic: "Reading Comprehension", reason: "High focus helps with deep understanding" }
        ]
      };
    } else if (hour < 17) {
      return {
        title: "Afternoon Exploration",
        suggestions: [
          { topic: "Creative Writing", reason: "Imagination peaks in the afternoon" },
          { topic: "History Discussions", reason: "Great for storytelling and context" },
          { topic: "Language Learning", reason: "Social brain is most active" }
        ]
      };
    } else {
      return {
        title: "Evening Reflection",
        suggestions: [
          { topic: "Review Today's Learning", reason: "Reinforce what you've learned" },
          { topic: "Homework Help", reason: "Perfect time for guided practice" },
          { topic: "Tomorrow's Preview", reason: "Prepare for upcoming lessons" }
        ]
      };
    }
  };

  const quickActions = [
    {
      id: 'new-session',
      title: 'Start AI Council Session',
      description: 'Get help from 7 different teaching perspectives',
      icon: Brain,
      color: 'var(--color-primary)',
      action: onStartSession,
      buttonText: 'Start Learning'
    },
    {
      id: 'homework',
      title: 'Submit Homework',
      description: 'Get detailed feedback on your assignments',
      icon: BookOpen,
      color: 'var(--color-warning)',
      link: '/homework',
      buttonText: 'Upload Work'
    },
    {
      id: 'analytics',
      title: 'View Progress',
      description: 'See your learning analytics and insights',
      icon: BarChart3,
      color: 'var(--color-info)',
      link: '/analytics',
      buttonText: 'View Stats'
    }
  ];

  const councilArchetypes = listCouncilVoices();
  const recommendedArchetypes = getRecommendedArchetypes(
    userPreferences.gradeLevel || 'middle',
    'understand',
    3
  );

  const suggestions = getTimeBasedSuggestions();

  const formatTimeAgo = (timestamp) => {
    const now = new Date();
    const diff = now - timestamp;
    const minutes = Math.floor(diff / 60000);
    const hours = Math.floor(diff / 3600000);
    const days = Math.floor(diff / 86400000);
    
    if (days > 0) return `${days} day${days > 1 ? 's' : ''} ago`;
    if (hours > 0) return `${hours} hour${hours > 1 ? 's' : ''} ago`;
    if (minutes > 0) return `${minutes} minute${minutes > 1 ? 's' : ''} ago`;
    return 'Just now';
  };

  return (
    <div className="dashboard">
      {/* Welcome Section */}
      <motion.section
        className="welcome-section"
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.6 }}
      >
        <div className="welcome-content">
          <div className="welcome-text">
            <h1 className="welcome-title">
              <Sparkles className="welcome-icon" />
              {welcomeMessage}
            </h1>
            <p className="welcome-subtitle">
              Your personal AI teaching council is ready to help you learn, grow, and succeed.
            </p>
          </div>
          
          {currentSession && (
            <motion.div
              className="active-session-card"
              initial={{ scale: 0.9, opacity: 0 }}
              animate={{ scale: 1, opacity: 1 }}
              transition={{ delay: 0.3 }}
            >
              <div className="session-indicator">
                <Zap className="session-icon" />
                <span>Session Active</span>
              </div>
              <div className="session-details">
                <div className="session-id">
                  {currentSession.id?.slice(-8) || 'Active'}
                </div>
                <div className="session-time">
                  Started at {new Date(currentSession.startTime).toLocaleTimeString()}
                </div>
              </div>
              <Link to={`/session/${currentSession.id}`} className="continue-session-btn">
                Continue Session
                <ChevronRight size={16} />
              </Link>
            </motion.div>
          )}
        </div>
      </motion.section>

      {/* Quick Actions */}
      <motion.section
        className="quick-actions-section"
        initial={{ opacity: 0, y: 30 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.6, delay: 0.2 }}
      >
        <h2>Quick Actions</h2>
        <div className="quick-actions-grid">
          {quickActions.map((action, index) => {
            const Icon = action.icon;
            
            return (
              <motion.div
                key={action.id}
                className="quick-action-card"
                style={{ '--action-color': action.color }}
                initial={{ opacity: 0, scale: 0.9 }}
                animate={{ opacity: 1, scale: 1 }}
                transition={{ delay: 0.1 * index }}
                whileHover={{ y: -4 }}
              >
                <div className="action-icon">
                  <Icon size={24} />
                </div>
                <div className="action-content">
                  <h3>{action.title}</h3>
                  <p>{action.description}</p>
                </div>
                {action.link ? (
                  <Link to={action.link} className="action-button">
                    {action.buttonText}
                    <ChevronRight size={16} />
                  </Link>
                ) : (
                  <button onClick={action.action} className="action-button">
                    {action.buttonText}
                    <ChevronRight size={16} />
                  </button>
                )}
              </motion.div>
            );
          })}
        </div>
      </motion.section>

      {/* Dashboard Grid */}
      <div className="dashboard-grid">
        {/* Learning Stats */}
        <motion.section
          className="stats-section card"
          initial={{ opacity: 0, x: -30 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ duration: 0.6, delay: 0.4 }}
        >
          <h2>Your Learning Journey</h2>
          <div className="stats-grid">
            <div className="stat-item">
              <div className="stat-icon sessions">
                <Brain size={20} />
              </div>
              <div className="stat-content">
                <div className="stat-number">{learningStats.sessionsCompleted}</div>
                <div className="stat-label">Sessions Completed</div>
              </div>
            </div>
            
            <div className="stat-item">
              <div className="stat-icon homework">
                <BookOpen size={20} />
              </div>
              <div className="stat-content">
                <div className="stat-number">{learningStats.homeworkSubmitted}</div>
                <div className="stat-label">Homework Submitted</div>
              </div>
            </div>
            
            <div className="stat-item">
              <div className="stat-icon concepts">
                <Target size={20} />
              </div>
              <div className="stat-content">
                <div className="stat-number">{learningStats.conceptsLearned}</div>
                <div className="stat-label">Concepts Mastered</div>
              </div>
            </div>
            
            <div className="stat-item">
              <div className="stat-icon streak">
                <Award size={20} />
              </div>
              <div className="stat-content">
                <div className="stat-number">{learningStats.streakDays}</div>
                <div className="stat-label">Day Learning Streak</div>
              </div>
            </div>
          </div>
        </motion.section>

        {/* AI Council Overview */}
        <motion.section
          className="council-section card"
          initial={{ opacity: 0, x: 30 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ duration: 0.6, delay: 0.6 }}
        >
          <h2>Your AI Teaching Council</h2>
          <div className="council-status">
            {councilStatus ? (
              <div className="status-item">
                <TrendingUp className="status-icon" />
                <span>All {councilStatus.available_archetypes?.length || 7} teachers online</span>
              </div>
            ) : (
              <div className="status-item loading">
                <Clock className="status-icon" />
                <span>Connecting to AI council...</span>
              </div>
            )}
          </div>
          
          <div className="recommended-teachers">
            <h3>Recommended for You</h3>
            <div className="teacher-list">
              {recommendedArchetypes.map((archetype) => (
                <div 
                  key={archetype}
                  className="teacher-item"
                  style={{ '--teacher-color': getCouncilColor(archetype) }}
                >
                  <span className="teacher-avatar">
                    {getCouncilAvatar(archetype)}
                  </span>
                  <span className="teacher-name">
                    {archetype.charAt(0).toUpperCase() + archetype.slice(1)}
                  </span>
                </div>
              ))}
            </div>
          </div>
          
          <Link to="/session" className="council-action-btn">
            Start Session with Council
            <PlayCircle size={16} />
          </Link>
        </motion.section>

        {/* Time-based Suggestions */}
        <motion.section
          className="suggestions-section card"
          initial={{ opacity: 0, y: 30 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 0.8 }}
        >
          <h2>{suggestions.title}</h2>
          <div className="suggestions-list">
            {suggestions.suggestions.map((suggestion, index) => (
              <div key={index} className="suggestion-item">
                <div className="suggestion-content">
                  <h4>{suggestion.topic}</h4>
                  <p>{suggestion.reason}</p>
                </div>
                <button 
                  className="suggestion-btn"
                  onClick={() => {
                    // Start session with this topic
                    onStartSession();
                  }}
                >
                  <PlayCircle size={16} />
                </button>
              </div>
            ))}
          </div>
        </motion.section>

        {/* Recent Activity */}
        <motion.section
          className="activity-section card"
          initial={{ opacity: 0, y: 30 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 1.0 }}
        >
          <h2>Recent Activity</h2>
          <div className="activity-list">
            {recentActivity.length > 0 ? (
              recentActivity.map((activity) => (
                <div key={activity.id} className="activity-item">
                  <div className={`activity-icon ${activity.type}`}>
                    {activity.type === 'session' && <Brain size={16} />}
                    {activity.type === 'homework' && <BookOpen size={16} />}
                    {activity.type === 'achievement' && <Award size={16} />}
                  </div>
                  <div className="activity-content">
                    <h4>{activity.title}</h4>
                    <p>{activity.description}</p>
                    <div className="activity-meta">
                      <span className="activity-time">
                        {formatTimeAgo(activity.timestamp)}
                      </span>
                      {activity.score && (
                        <span className="activity-score">
                          Score: {activity.score}%
                        </span>
                      )}
                      {activity.archetypes && (
                        <span className="activity-archetypes">
                          {activity.archetypes.length} teachers involved
                        </span>
                      )}
                    </div>
                  </div>
                </div>
              ))
            ) : (
              <div className="no-activity">
                <p>No recent activity</p>
                <button onClick={onStartSession} className="start-learning-btn">
                  Start Learning Now
                </button>
              </div>
            )}
          </div>
        </motion.section>
      </div>

      {/* Footer Call-to-Action */}
      <motion.section
        className="cta-section"
        initial={{ opacity: 0, y: 40 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.6, delay: 1.2 }}
      >
        <div className="cta-content">
          <h2>Ready to Learn Something New?</h2>
          <p>
            Start a conversation with your AI teaching council and discover new perspectives on any topic.
          </p>
          <button onClick={onStartSession} className="cta-button">
            <Brain size={20} />
            Start AI Council Session
          </button>
        </div>
      </motion.section>
    </div>
  );
};

export default Dashboard;