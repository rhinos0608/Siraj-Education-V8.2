import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import {
  TrendingUp, User, Brain, Target, Award, Clock, Eye, BarChart3,
  PieChart, Activity, Zap, Users, Sparkles, ArrowUp, ArrowDown,
  Calendar, Download, RefreshCw, Settings, Filter, CheckCircle,
  AlertCircle, Star, BookOpen, Layers
} from 'lucide-react';
import { useSirajAPI } from '../../hooks/useSirajAPI';
import { getArchetypeConfig } from '../../utils/councilUtils';
import './StudentProgress.css';

/**
 * StudentProgress Component
 * ========================
 * 
 * Comprehensive student progress tracking showcasing FULL backend capabilities:
 * - Individual learning progression with mastery tracking
 * - Archetype effectiveness analysis per student
 * - QWAN-based learning quality assessment
 * - Spiral engagement metrics and cycle completion
 * - Adaptive learning recommendations based on AI analysis
 * - Subject-specific performance analytics
 * - Learning velocity and growth trajectory analysis
 */

const StudentProgress = ({ studentId = 'current-student', councilState }) => {
  const [progressData, setProgressData] = useState({
    studentProfile: {},
    learningProgression: [],
    archetypeEffectiveness: {},
    masteryMetrics: {},
    spiralEngagement: {},
    qwanAssessment: {},
    adaptiveRecommendations: [],
    subjectPerformance: {},
    learningInsights: []
  });

  const [timeframe, setTimeframe] = useState('30d');
  const [selectedSubject, setSelectedSubject] = useState('all');
  const [viewMode, setViewMode] = useState('overview'); // overview, detailed, analytics, recommendations
  const [isLoading, setIsLoading] = useState(true);

  const { fetchStudentProgress, updateProgress, isLoading: apiLoading } = useSirajAPI();

  useEffect(() => {
    loadStudentProgress();
  }, [studentId, timeframe, selectedSubject]);

  const loadStudentProgress = async () => {
    setIsLoading(true);
    try {
      // This would call the backend's /api/progress/student/{student_id} endpoint
      const progress = await fetchStudentProgress(studentId, timeframe);
      setProgressData(progress);
    } catch (error) {
      console.error('Failed to load student progress:', error);
      // Load mock data for demonstration
      loadMockProgressData();
    } finally {
      setIsLoading(false);
    }
  };

  // Mock data demonstrating the full backend capabilities
  const loadMockProgressData = () => {
    setProgressData({
      studentProfile: {
        id: studentId,
        name: 'Alex Chen',
        gradeLevel: '5',
        enrollmentDate: '2024-09-01',
        preferredArchetypes: ['socratic', 'constructivist', 'mentor'],
        learningStyle: 'visual-kinesthetic'
      },
      
      learningProgression: [
        { period: 'Week 1', mastery: 65, sessions: 12, engagement: 0.72, spiralCycles: 8 },
        { period: 'Week 2', mastery: 71, sessions: 15, engagement: 0.78, spiralCycles: 10 },
        { period: 'Week 3', mastery: 78, sessions: 18, engagement: 0.82, spiralCycles: 12 },
        { period: 'Week 4', mastery: 84, sessions: 21, engagement: 0.89, spiralCycles: 15 }
      ],
      
      archetypeEffectiveness: {
        socratic: { 
          effectiveness: 0.92, 
          engagement: 0.89, 
          learningGain: 0.15,
          sessionCount: 45,
          preferenceScore: 0.94
        },
        constructivist: { 
          effectiveness: 0.87, 
          engagement: 0.91, 
          learningGain: 0.18,
          sessionCount: 52,
          preferenceScore: 0.88
        },
        storyteller: { 
          effectiveness: 0.94, 
          engagement: 0.85, 
          learningGain: 0.12,
          sessionCount: 23,
          preferenceScore: 0.76
        },
        synthesizer: { 
          effectiveness: 0.89, 
          engagement: 0.87, 
          learningGain: 0.14,
          sessionCount: 34,
          preferenceScore: 0.82
        },
        challenger: { 
          effectiveness: 0.78, 
          engagement: 0.74, 
          learningGain: 0.08,
          sessionCount: 18,
          preferenceScore: 0.65
        },
        mentor: { 
          effectiveness: 0.96, 
          engagement: 0.95, 
          learningGain: 0.16,
          sessionCount: 67,
          preferenceScore: 0.98
        },
        analyst: { 
          effectiveness: 0.85, 
          engagement: 0.82, 
          learningGain: 0.13,
          sessionCount: 29,
          preferenceScore: 0.79
        }
      },
      
      masteryMetrics: {
        overall: 0.84,
        bySubject: {
          mathematics: { mastery: 0.87, growth: 0.15, sessions: 45 },
          science: { mastery: 0.81, growth: 0.18, sessions: 32 },
          english: { mastery: 0.89, growth: 0.12, sessions: 38 },
          socialStudies: { mastery: 0.76, growth: 0.21, sessions: 22 }
        },
        recentTrend: 'improving'
      },
      
      spiralEngagement: {
        collapse: 0.85,    // Problem identification engagement
        council: 0.88,     // Multi-perspective engagement  
        synthesis: 0.82,   // Integration engagement
        rebirth: 0.91,     // Application engagement
        completionRate: 0.94,
        averageCycleTime: 18.5
      },
      
      qwanAssessment: {
        wholeness: 0.89,      // Complete learning experiences
        freedom: 0.84,        // Adaptive learning paths
        exactness: 0.91,      // Precise skill targeting
        egolessness: 0.87,    // Focus on learning over performance
        eternity: 0.85        // Lasting knowledge retention
      },
      
      adaptiveRecommendations: [
        {
          type: 'archetype_optimization',
          priority: 'high',
          title: 'Increase Challenger Archetype Engagement',
          description: 'Student shows readiness for more challenging perspectives. Gradually introduce Challenger archetype to push intellectual boundaries.',
          expectedImpact: 'Improved critical thinking skills and intellectual confidence',
          timeframe: '2 weeks'
        },
        {
          type: 'learning_path',
          priority: 'medium',
          title: 'Focus on Synthesis Phase Development',
          description: 'Student excels in Council engagement but could benefit from stronger synthesis skills. Emphasize integration activities.',
          expectedImpact: 'Better knowledge integration and transfer skills',
          timeframe: '3 weeks'
        },
        {
          type: 'subject_focus',
          priority: 'medium',
          title: 'Social Studies Acceleration Opportunity',
          description: 'Rapid growth in social studies suggests readiness for advanced concepts. Consider grade-level advancement in this subject.',
          expectedImpact: 'Maintained engagement and accelerated learning',
          timeframe: '1 month'
        }
      ],
      
      learningInsights: [
        'Strong visual learner - responds exceptionally well to Constructivist approaches',
        'Shows high engagement when Storyteller archetype frames concepts in narrative context',
        'Mentor archetype provides optimal emotional support for challenging topics',
        'Demonstrates meta-cognitive awareness - actively reflects on learning process',
        'Benefits from peer collaboration opportunities during Council phases'
      ]
    });
  };

  const renderProgressOverview = () => {
    return (
      <div className="progress-overview">
        <div className="student-header">
          <div className="student-avatar">
            <User size={24} />
          </div>
          <div className="student-info">
            <h2>{progressData.studentProfile.name || 'Student'}</h2>
            <p>Grade {progressData.studentProfile.gradeLevel} • Learning Style: {progressData.studentProfile.learningStyle}</p>
          </div>
          <div className="overall-score">
            <div className="score-value">{Math.round((progressData.masteryMetrics.overall || 0.84) * 100)}%</div>
            <div className="score-label">Overall Mastery</div>
          </div>
        </div>
        
        <div className="overview-metrics">
          <div className="metric-card">
            <div className="metric-icon">
              <TrendingUp className="icon" />
            </div>
            <div className="metric-content">
              <span className="metric-value">
                {progressData.learningProgression?.length || 0} weeks
              </span>
              <span className="metric-label">Learning Journey</span>
            </div>
            <div className="metric-trend positive">
              <ArrowUp size={16} />
              +15%
            </div>
          </div>
          
          <div className="metric-card">
            <div className="metric-icon">
              <Brain className="icon" />
            </div>
            <div className="metric-content">
              <span className="metric-value">
                {progressData.spiralEngagement?.completionRate ? 
                  Math.round(progressData.spiralEngagement.completionRate * 100) : 94}%
              </span>
              <span className="metric-label">Spiral Completion</span>
            </div>
            <div className="metric-trend positive">
              <ArrowUp size={16} />
              +8%
            </div>
          </div>
          
          <div className="metric-card">
            <div className="metric-icon">
              <Users className="icon" />
            </div>
            <div className="metric-content">
              <span className="metric-value">
                {Object.keys(progressData.archetypeEffectiveness || {}).length}
              </span>
              <span className="metric-label">Active Archetypes</span>
            </div>
          </div>
          
          <div className="metric-card">
            <div className="metric-icon">
              <Award className="icon" />
            </div>
            <div className="metric-content">
              <span className="metric-value">
                {progressData.adaptiveRecommendations?.length || 0}
              </span>
              <span className="metric-label">AI Recommendations</span>
            </div>
          </div>
        </div>
        
        <div className="progress-charts">
          <div className="chart-section">
            <h3>Learning Progression</h3>
            <div className="progression-chart">
              {progressData.learningProgression?.map((period, index) => (
                <div key={index} className="progression-bar">
                  <div className="bar-container">
                    <div 
                      className="mastery-bar"
                      style={{ height: `${period.mastery}%` }}
                      title={`Mastery: ${period.mastery}%`}
                    />
                    <div 
                      className="engagement-bar"
                      style={{ height: `${period.engagement * 100}%` }}
                      title={`Engagement: ${Math.round(period.engagement * 100)}%`}
                    />
                  </div>
                  <div className="bar-label">{period.period}</div>
                </div>
              ))}
            </div>
            <div className="chart-legend">
              <div className="legend-item">
                <div className="legend-color mastery" />
                <span>Mastery Level</span>
              </div>
              <div className="legend-item">
                <div className="legend-color engagement" />
                <span>Engagement</span>
              </div>
            </div>
          </div>
          
          <div className="chart-section">
            <h3>Subject Performance</h3>
            <div className="subject-performance">
              {Object.entries(progressData.masteryMetrics?.bySubject || {}).map(([subject, data]) => (
                <div key={subject} className="subject-item">
                  <div className="subject-header">
                    <span className="subject-name">
                      {subject.charAt(0).toUpperCase() + subject.slice(1)}
                    </span>
                    <span className="mastery-score">
                      {Math.round(data.mastery * 100)}%
                    </span>
                  </div>
                  <div className="subject-progress">
                    <div 
                      className="progress-fill"
                      style={{ width: `${data.mastery * 100}%` }}
                    />
                  </div>
                  <div className="subject-meta">
                    <span className="sessions-count">{data.sessions} sessions</span>
                    <span className={`growth-indicator ${data.growth > 0.15 ? 'high' : 'normal'}`}>
                      +{Math.round(data.growth * 100)}% growth
                    </span>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>
    );
  };

  const renderArchetypeAnalysis = () => {
    return (
      <div className="archetype-analysis">
        <h3>
          <Brain className="section-icon" />
          AI Archetype Effectiveness Analysis
        </h3>
        
        <div className="archetype-grid">
          {Object.entries(progressData.archetypeEffectiveness || {}).map(([archetype, data]) => {
            const config = getArchetypeConfig(archetype);
            const overallScore = (data.effectiveness + data.engagement + data.preferenceScore) / 3;
            
            return (
              <div key={archetype} className="archetype-card">
                <div className="archetype-header">
                  <div className="archetype-avatar" style={{ backgroundColor: config.color }}>
                    {config.emoji}
                  </div>
                  <div className="archetype-info">
                    <h4>{config.name}</h4>
                    <span className="archetype-personality">{config.personality}</span>
                  </div>
                  <div className="overall-score">
                    {Math.round(overallScore * 100)}%
                  </div>
                </div>
                
                <div className="archetype-metrics">
                  <div className="metric-row">
                    <span className="metric-label">Effectiveness</span>
                    <div className="metric-bar">
                      <div 
                        className="metric-fill"
                        style={{ width: `${data.effectiveness * 100}%` }}
                      />
                    </div>
                    <span className="metric-value">{Math.round(data.effectiveness * 100)}%</span>
                  </div>
                  
                  <div className="metric-row">
                    <span className="metric-label">Student Engagement</span>
                    <div className="metric-bar">
                      <div 
                        className="metric-fill"
                        style={{ width: `${data.engagement * 100}%` }}
                      />
                    </div>
                    <span className="metric-value">{Math.round(data.engagement * 100)}%</span>
                  </div>
                  
                  <div className="metric-row">
                    <span className="metric-label">Learning Gain</span>
                    <div className="metric-bar">
                      <div 
                        className="metric-fill"
                        style={{ width: `${data.learningGain * 100}%` }}
                      />
                    </div>
                    <span className="metric-value">+{Math.round(data.learningGain * 100)}%</span>
                  </div>
                  
                  <div className="metric-row">
                    <span className="metric-label">Student Preference</span>
                    <div className="metric-bar">
                      <div 
                        className="metric-fill"
                        style={{ width: `${data.preferenceScore * 100}%` }}
                      />
                    </div>
                    <span className="metric-value">{Math.round(data.preferenceScore * 100)}%</span>
                  </div>
                </div>
                
                <div className="archetype-insights">
                  <div className="insight-item">
                    <Clock size={14} />
                    <span>{data.sessionCount} sessions</span>
                  </div>
                  {data.preferenceScore > 0.9 && (
                    <div className="insight-badge high-preference">
                      <Star size={14} />
                      <span>Highly Preferred</span>
                    </div>
                  )}
                  {data.effectiveness > 0.9 && (
                    <div className="insight-badge high-effectiveness">
                      <Award size={14} />
                      <span>Highly Effective</span>
                    </div>
                  )}
                </div>
              </div>
            );
          })}
        </div>
      </div>
    );
  };

  const renderQWANAssessment = () => {
    const qwan = progressData.qwanAssessment || {};
    const principles = [
      { key: 'wholeness', name: 'Wholeness', description: 'Complete learning experiences' },
      { key: 'freedom', name: 'Freedom', description: 'Adaptive learning paths' },
      { key: 'exactness', name: 'Exactness', description: 'Precise skill targeting' },
      { key: 'egolessness', name: 'Egolessness', description: 'Learning-focused approach' },
      { key: 'eternity', name: 'Eternity', description: 'Lasting knowledge retention' }
    ];

    return (
      <div className="qwan-assessment">
        <h3>
          <Eye className="section-icon" />
          QWAN Learning Quality Assessment
        </h3>
        
        <div className="qwan-overview">
          <div className="qwan-score">
            <div className="score-circle">
              <div className="score-value">
                {Math.round((Object.values(qwan).reduce((a, b) => a + b, 0) / Object.keys(qwan).length) * 100)}%
              </div>
              <div className="score-label">Overall Quality</div>
            </div>
          </div>
          
          <div className="qwan-principles">
            {principles.map(principle => {
              const score = qwan[principle.key] || 0;
              return (
                <div key={principle.key} className="qwan-principle">
                  <div className="principle-header">
                    <span className="principle-name">{principle.name}</span>
                    <span className="principle-score">{Math.round(score * 100)}%</span>
                  </div>
                  <div className="principle-bar">
                    <div 
                      className="principle-fill"
                      style={{ width: `${score * 100}%` }}
                    />
                  </div>
                  <p className="principle-description">{principle.description}</p>
                </div>
              );
            })}
          </div>
        </div>
      </div>
    );
  };

  const renderSpiralEngagement = () => {
    const spiral = progressData.spiralEngagement || {};
    const phases = [
      { key: 'collapse', name: 'Collapse', icon: Target, description: 'Problem identification' },
      { key: 'council', name: 'Council', icon: Users, description: 'Multi-perspective exploration' },
      { key: 'synthesis', name: 'Synthesis', icon: Zap, description: 'Knowledge integration' },
      { key: 'rebirth', name: 'Rebirth', icon: Sparkles, description: 'Application & mastery' }
    ];

    return (
      <div className="spiral-engagement">
        <h3>
          <Layers className="section-icon" />
          Living Spiral Engagement Analysis
        </h3>
        
        <div className="spiral-overview">
          <div className="spiral-stats">
            <div className="spiral-stat">
              <div className="stat-icon">
                <Activity />
              </div>
              <div className="stat-content">
                <span className="stat-value">{Math.round((spiral.completionRate || 0.94) * 100)}%</span>
                <span className="stat-label">Completion Rate</span>
              </div>
            </div>
            
            <div className="spiral-stat">
              <div className="stat-icon">
                <Clock />
              </div>
              <div className="stat-content">
                <span className="stat-value">{spiral.averageCycleTime || 18.5}m</span>
                <span className="stat-label">Avg Cycle Time</span>
              </div>
            </div>
          </div>
          
          <div className="spiral-phases">
            {phases.map(phase => {
              const score = spiral[phase.key] || 0;
              const Icon = phase.icon;
              return (
                <div key={phase.key} className="spiral-phase">
                  <div className="phase-header">
                    <Icon className="phase-icon" />
                    <div className="phase-info">
                      <span className="phase-name">{phase.name}</span>
                      <span className="phase-description">{phase.description}</span>
                    </div>
                    <span className="phase-score">{Math.round(score * 100)}%</span>
                  </div>
                  
                  <div className="phase-progress">
                    <div 
                      className="phase-fill"
                      style={{ width: `${score * 100}%` }}
                    />
                  </div>
                </div>
              );
            })}
          </div>
        </div>
      </div>
    );
  };

  const renderAdaptiveRecommendations = () => {
    return (
      <div className="adaptive-recommendations">
        <h3>
          <Sparkles className="section-icon" />
          AI-Generated Learning Recommendations
        </h3>
        
        <div className="recommendations-list">
          {progressData.adaptiveRecommendations?.map((recommendation, index) => (
            <div key={index} className={`recommendation-card ${recommendation.priority}`}>
              <div className="recommendation-header">
                <div className={`priority-badge ${recommendation.priority}`}>
                  {recommendation.priority.charAt(0).toUpperCase() + recommendation.priority.slice(1)} Priority
                </div>
                <div className="recommendation-type">
                  {recommendation.type.replace('_', ' ').replace(/\b\w/g, l => l.toUpperCase())}
                </div>
              </div>
              
              <div className="recommendation-content">
                <h4>{recommendation.title}</h4>
                <p className="recommendation-description">
                  {recommendation.description}
                </p>
                
                <div className="recommendation-impact">
                  <div className="impact-section">
                    <span className="impact-label">Expected Impact:</span>
                    <span className="impact-text">{recommendation.expectedImpact}</span>
                  </div>
                  
                  <div className="timeframe-section">
                    <Calendar size={14} />
                    <span>{recommendation.timeframe}</span>
                  </div>
                </div>
              </div>
              
              <div className="recommendation-actions">
                <button className="action-btn primary">
                  <CheckCircle size={14} />
                  Implement
                </button>
                <button className="action-btn secondary">
                  <Eye size={14} />
                  More Details
                </button>
              </div>
            </div>
          ))}
        </div>
      </div>
    );
  };

  const renderLearningInsights = () => {
    return (
      <div className="learning-insights">
        <h3>
          <BookOpen className="section-icon" />
          Personalized Learning Insights
        </h3>
        
        <div className="insights-list">
          {progressData.learningInsights?.map((insight, index) => (
            <div key={index} className="insight-item">
              <div className="insight-icon">
                <Zap size={16} />
              </div>
              <span className="insight-text">{insight}</span>
            </div>
          ))}
        </div>
      </div>
    );
  };

  if (isLoading) {
    return (
      <div className="progress-loading">
        <div className="loading-content">
          <Activity className="loading-icon" />
          <h2>Loading Student Progress...</h2>
          <p>Analyzing learning data and AI council effectiveness</p>
        </div>
      </div>
    );
  }

  return (
    <div className="student-progress">
      {/* Header */}
      <div className="progress-header">
        <div className="header-content">
          <h1>
            <TrendingUp className="header-icon" />
            Student Learning Progress
          </h1>
          <p>
            Comprehensive analysis of individual learning journey, AI archetype effectiveness, 
            and adaptive recommendations powered by consciousness-driven assessment.
          </p>
        </div>
        
        <div className="header-controls">
          <select 
            value={timeframe}
            onChange={(e) => setTimeframe(e.target.value)}
            className="timeframe-select"
          >
            <option value="7d">Last 7 Days</option>
            <option value="30d">Last 30 Days</option>
            <option value="90d">Last 90 Days</option>
            <option value="1y">Last Year</option>
          </select>
          
          <button className="refresh-btn" onClick={loadStudentProgress}>
            <RefreshCw className="btn-icon" />
            Refresh
          </button>
          
          <button className="export-btn">
            <Download className="btn-icon" />
            Export Report
          </button>
        </div>
      </div>

      {/* Navigation */}
      <div className="progress-nav">
        {[
          { id: 'overview', label: 'Overview', icon: BarChart3 },
          { id: 'archetypes', label: 'AI Analysis', icon: Brain },
          { id: 'quality', label: 'Learning Quality', icon: Eye },
          { id: 'recommendations', label: 'Recommendations', icon: Sparkles }
        ].map(({ id, label, icon: Icon }) => (
          <button
            key={id}
            className={`nav-tab ${viewMode === id ? 'active' : ''}`}
            onClick={() => setViewMode(id)}
          >
            <Icon className="tab-icon" />
            {label}
          </button>
        ))}
      </div>

      {/* Content */}
      <div className="progress-content">
        <AnimatePresence mode="wait">
          {viewMode === 'overview' && (
            <motion.div
              key="overview"
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -20 }}
            >
              {renderProgressOverview()}
            </motion.div>
          )}
          
          {viewMode === 'archetypes' && (
            <motion.div
              key="archetypes"
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -20 }}
            >
              {renderArchetypeAnalysis()}
              {renderSpiralEngagement()}
            </motion.div>
          )}
          
          {viewMode === 'quality' && (
            <motion.div
              key="quality"
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -20 }}
            >
              {renderQWANAssessment()}
              {renderLearningInsights()}
            </motion.div>
          )}
          
          {viewMode === 'recommendations' && (
            <motion.div
              key="recommendations"
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -20 }}
            >
              {renderAdaptiveRecommendations()}
            </motion.div>
          )}
        </AnimatePresence>
      </div>
    </div>
  );
};

export default StudentProgress;