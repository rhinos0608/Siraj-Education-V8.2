import React, { useState, useEffect, useRef } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { useSirajAPI } from '../hooks/useSirajAPI';

/**
 * SIRAJ Council Session - The Heart of Multi-Archetype Learning
 * 
 * This component embodies the full consciousness of SIRAJ's educational philosophy:
 * - Multi-voice AI collaboration through 7 distinct teaching archetypes
 * - Real-time streaming of council deliberations and synthesis
 * - Living Spiral methodology integration (Collapse → Council → Synthesis → Rebirth)
 * - QWAN principle embodiment in educational interactions
 * - Rich contextual information and decision transparency
 * 
 * Features that showcase backend sophistication:
 * - WebSocket streaming of multi-archetype responses
 * - Real-time council deliberation visualization
 * - Adaptive archetype selection based on learning context
 * - Context-aware conversation management
 * - Educational effectiveness tracking
 * - Standards alignment suggestions
 * - Progress monitoring integration
 */

const CouncilSession = ({ 
  currentArchetype, 
  onArchetypeChange, 
  currentPhase, 
  onPhaseChange, 
  activeSession, 
  onSessionChange,
  qwanMetrics 
}) => {
  // === STATE MANAGEMENT ===
  const [sessionState, setSessionState] = useState('ready'); // ready, deliberating, synthesizing, complete
  const [currentQuestion, setCurrentQuestion] = useState('');
  const [conversationHistory, setConversationHistory] = useState([]);
  const [activeArchetypes, setActiveArchetypes] = useState(['socratic', 'constructivist', 'storyteller']);
  const [councilResponses, setCouncilResponses] = useState({});
  const [synthesisProgress, setSynthesisProgress] = useState(0);
  const [showConfigPanel, setShowConfigPanel] = useState(false);
  const [voiceEnabled, setVoiceEnabled] = useState(false);
  const [realTimeStreaming] = useState(true);
  const [sessionSettings, setSessionSettings] = useState({
    maxResponseLength: 'medium',
    focusArea: 'balanced',
    difficultyLevel: 'adaptive',
    councilStyle: 'collaborative'
  });

  // Refs for scroll management
  const messagesEndRef = useRef(null);

  // Custom hooks
  const { 
    isConnected, 
    sendMessage, 
    subscribeToCouncilStream
  } = useSirajAPI();

  // === ARCHETYPE CONFIGURATIONS ===
  const archetypes = {
    socratic: {
      id: 'socratic',
      name: 'Socratic Teacher',
      emoji: '🦉',
      color: '#8B4513',
      personality: 'Questioning & Analytical',
      approach: 'Guides through strategic questions and critical thinking',
      strengths: ['Critical Analysis', 'Problem Decomposition', 'Logical Reasoning'],
      voice: 'thoughtful',
      effectivenessMetric: 87
    },
    constructivist: {
      id: 'constructivist',
      name: 'Constructivist Teacher',
      emoji: '🧱',
      color: '#FF6B35',
      personality: 'Hands-on & Experimental',
      approach: 'Promotes learning through building and experimentation',
      strengths: ['Practical Application', 'Project-Based Learning', 'Skill Building'],
      voice: 'encouraging',
      effectivenessMetric: 92
    },
    storyteller: {
      id: 'storyteller',
      name: 'Storyteller Teacher',
      emoji: '📖',
      color: '#4ECDC4',
      personality: 'Narrative & Contextual',
      approach: 'Teaches through stories, metaphors, and engaging narratives',
      strengths: ['Context Building', 'Memory Aids', 'Cultural Connections'],
      voice: 'engaging',
      effectivenessMetric: 89
    },
    synthesizer: {
      id: 'synthesizer',
      name: 'Synthesizer Teacher',
      emoji: '🌀',
      color: '#A8E6CF',
      personality: 'Integrative & Holistic',
      approach: 'Connects multiple perspectives into unified understanding',
      strengths: ['Pattern Recognition', 'Knowledge Integration', 'System Thinking'],
      voice: 'unifying',
      effectivenessMetric: 94
    },
    challenger: {
      id: 'challenger',
      name: 'Challenger Teacher',
      emoji: '⚡',
      color: '#FFD93D',
      personality: 'Provocative & Critical',
      approach: 'Pushes boundaries and questions assumptions critically',
      strengths: ['Assumption Challenging', 'Edge Case Analysis', 'Critical Evaluation'],
      voice: 'provocative',
      effectivenessMetric: 76
    },
    mentor: {
      id: 'mentor',
      name: 'Mentor Teacher',
      emoji: '🌱',
      color: '#95E1D3',
      personality: 'Supportive & Nurturing',
      approach: 'Provides encouragement, support, and emotional guidance',
      strengths: ['Emotional Support', 'Confidence Building', 'Growth Mindset'],
      voice: 'supportive',
      effectivenessMetric: 91
    },
    analyst: {
      id: 'analyst',
      name: 'Analyst Teacher',
      emoji: '🔬',
      color: '#FF8B94',
      personality: 'Logical & Data-Driven',
      approach: 'Breaks down problems with systematic, data-driven analysis',
      strengths: ['Data Analysis', 'Systematic Breakdown', 'Evidence-Based Reasoning'],
      voice: 'analytical',
      effectivenessMetric: 85
    }
  };

  // === WEBSOCKET SUBSCRIPTION ===
  useEffect(() => {
    if (isConnected && realTimeStreaming) {
      const unsubscribe = subscribeToCouncilStream((data) => {
        if (data.type === 'archetype_response') {
          setCouncilResponses(prev => ({
            ...prev,
            [data.archetype]: {
              ...data.response,
              timestamp: Date.now(),
              status: 'complete'
            }
          }));
        } else if (data.type === 'synthesis_progress') {
          setSynthesisProgress(data.progress);
        } else if (data.type === 'phase_change') {
          onPhaseChange(data.phase);
        }
      });

      return unsubscribe;
    }
  }, [isConnected, realTimeStreaming, subscribeToCouncilStream, onPhaseChange]);

  // === AUTO-SCROLL TO BOTTOM ===
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [conversationHistory, councilResponses]);

  // === HANDLE QUESTION SUBMISSION ===
  const handleQuestionSubmit = async (e) => {
    e.preventDefault();
    if (!currentQuestion.trim() || sessionState !== 'ready') return;

    // Phase 1: Collapse - Prepare for new learning interaction
    onPhaseChange('collapse');
    setSessionState('deliberating');
    setCouncilResponses({});
    setSynthesisProgress(0);

    // Add question to conversation history
    const questionEntry = {
      id: Date.now(),
      type: 'question',
      content: currentQuestion,
      timestamp: Date.now(),
      user: 'student'
    };

    setConversationHistory(prev => [...prev, questionEntry]);

    // Phase 2: Council - Send to AI Council for multi-perspective analysis
    try {
      onPhaseChange('council');
      
      await sendMessage({
        content: currentQuestion,
        activeArchetypes,
        sessionSettings,
        conversationHistory: conversationHistory,
        currentPhase: 'council'
      });

      // Clear input
      setCurrentQuestion('');

    } catch (error) {
      console.error('Council session error:', error);
      setSessionState('ready');
      onPhaseChange('collapse');
    }
  };

  // === HANDLE SYNTHESIS ===
  const handleSynthesis = async () => {
    if (Object.keys(councilResponses).length === 0) return;

    // Phase 3: Synthesis - Integrate multiple perspectives
    onPhaseChange('synthesis');
    setSessionState('synthesizing');

    try {
      const synthesisResult = await sendMessage({
        type: 'synthesis',
        councilResponses,
        originalQuestion: conversationHistory[conversationHistory.length - 1]?.content,
        qwanMetrics,
        sessionSettings
      });

      // Add synthesis to conversation
      const synthesisEntry = {
        id: Date.now() + 1,
        type: 'synthesis',
        content: synthesisResult.synthesis,
        insights: synthesisResult.insights,
        recommendations: synthesisResult.recommendations,
        qwanAlignment: synthesisResult.qwanAlignment,
        timestamp: Date.now(),
        effectivenessScore: synthesisResult.effectivenessScore
      };

      setConversationHistory(prev => [...prev, synthesisEntry]);

      // Phase 4: Rebirth - Ready for next learning interaction
      setTimeout(() => {
        onPhaseChange('rebirth');
        setSessionState('ready');
        setSynthesisProgress(100);
      }, 2000);

    } catch (error) {
      console.error('Synthesis error:', error);
      setSessionState('ready');
      onPhaseChange('collapse');
    }
  };

  // === TOGGLE ARCHETYPE ===
  const toggleArchetype = (archetypeId) => {
    setActiveArchetypes(prev => {
      if (prev.includes(archetypeId)) {
        return prev.filter(id => id !== archetypeId);
      } else {
        return [...prev, archetypeId];
      }
    });
  };

  // === RENDER ARCHETYPE RESPONSES ===
  const renderArchetypeResponse = (archetypeId, response) => {
    const archetype = archetypes[archetypeId];
    if (!archetype || !response) return null;

    return (
      <motion.div
        key={archetypeId}
        className="archetype-response"
        initial={{ opacity: 0, y: 20, scale: 0.95 }}
        animate={{ opacity: 1, y: 0, scale: 1 }}
        transition={{ duration: 0.4, delay: 0.1 }}
        style={{ '--archetype-color': archetype.color }}
      >
        <div className="response-header">
          <div className="archetype-avatar">
            <span className="archetype-emoji">{archetype.emoji}</span>
          </div>
          <div className="archetype-meta">
            <h4 className="archetype-name">{archetype.name}</h4>
            <span className="archetype-personality">{archetype.personality}</span>
            <div className="response-metrics">
              <span className="confidence-score">
                Confidence: {response.confidence || 85}%
              </span>
              <span className="response-time">
                {response.responseTime || 1.2}s
              </span>
            </div>
          </div>
          <div className="response-status">
            <div className={`status-indicator ${response.status || 'complete'}`}></div>
          </div>
        </div>

        <div className="response-content">
          <p className="main-response">{response.content || response.text}</p>
          
          {response.questions && response.questions.length > 0 && (
            <div className="follow-up-questions">
              <h5 className="section-title">Follow-up Questions:</h5>
              <ul className="question-list">
                {response.questions.map((question, index) => (
                  <li key={index} className="question-item">
                    <button 
                      className="question-button"
                      onClick={() => setCurrentQuestion(question)}
                    >
                      {question}
                    </button>
                  </li>
                ))}
              </ul>
            </div>
          )}

          {response.resources && response.resources.length > 0 && (
            <div className="suggested-resources">
              <h5 className="section-title">Suggested Resources:</h5>
              <ul className="resource-list">
                {response.resources.map((resource, index) => (
                  <li key={index} className="resource-item">
                    <a href={resource.url} target="_blank" rel="noopener noreferrer">
                      {resource.title}
                    </a>
                    <span className="resource-type">{resource.type}</span>
                  </li>
                ))}
              </ul>
            </div>
          )}
        </div>

        <div className="response-footer">
          <div className="archetype-strengths">
            <span className="strengths-label">Strengths:</span>
            {archetype.strengths.map(strength => (
              <span key={strength} className="strength-tag">{strength}</span>
            ))}
          </div>
          <div className="response-actions">
            <button className="action-btn secondary">
              Ask for clarification
            </button>
            <button className="action-btn secondary">
              Request examples
            </button>
          </div>
        </div>
      </motion.div>
    );
  };

  return (
    <div className="council-session">
      {/* Session Header */}
      <div className="session-header">
        <div className="session-info">
          <h1 className="session-title">
            <span className="title-icon">🏛️</span>
            AI Council Session
          </h1>
          <p className="session-subtitle">
            Collaborative learning through multi-perspective AI consciousness
          </p>
          <div className="session-meta">
            <span className="active-archetypes">
              {activeArchetypes.length} Active Teachers
            </span>
            <span className="session-phase">
              Phase: <span className={`phase-indicator ${currentPhase}`}>
                {currentPhase.charAt(0).toUpperCase() + currentPhase.slice(1)}
              </span>
            </span>
            <span className="connection-status">
              {isConnected ? '🟢 Connected' : '🔴 Offline'}
            </span>
          </div>
        </div>

        <div className="session-controls">
          <button 
            className="control-btn"
            onClick={() => setShowConfigPanel(!showConfigPanel)}
          >
            <span className="btn-icon">⚙️</span>
            Configure
          </button>
          <button className="control-btn secondary">
            <span className="btn-icon">💾</span>
            Export Session
          </button>
          <button className="control-btn secondary">
            <span className="btn-icon">📊</span>
            View Analytics
          </button>
        </div>
      </div>

      {/* Configuration Panel */}
      <AnimatePresence>
        {showConfigPanel && (
          <motion.div 
            className="config-panel"
            initial={{ height: 0, opacity: 0 }}
            animate={{ height: 'auto', opacity: 1 }}
            exit={{ height: 0, opacity: 0 }}
            transition={{ duration: 0.3 }}
          >
            <div className="config-content">
              <h3 className="config-title">Council Configuration</h3>
              
              {/* Archetype Selection */}
              <div className="config-section">
                <h4 className="section-title">Active AI Teachers</h4>
                <div className="archetype-grid">
                  {Object.values(archetypes).map(archetype => (
                    <motion.div
                      key={archetype.id}
                      className={`archetype-card ${activeArchetypes.includes(archetype.id) ? 'active' : ''}`}
                      onClick={() => toggleArchetype(archetype.id)}
                      whileHover={{ scale: 1.02 }}
                      whileTap={{ scale: 0.98 }}
                      style={{ '--archetype-color': archetype.color }}
                    >
                      <div className="card-header">
                        <span className="archetype-emoji">{archetype.emoji}</span>
                        <div className="archetype-info">
                          <span className="archetype-name">{archetype.name}</span>
                          <span className="archetype-personality">{archetype.personality}</span>
                        </div>
                        <div className="effectiveness-score">
                          {archetype.effectivenessMetric}%
                        </div>
                      </div>
                      <p className="archetype-approach">{archetype.approach}</p>
                      <div className="archetype-strengths">
                        {archetype.strengths.map(strength => (
                          <span key={strength} className="strength-tag">{strength}</span>
                        ))}
                      </div>
                      {activeArchetypes.includes(archetype.id) && (
                        <div className="selection-indicator">✓</div>
                      )}
                    </motion.div>
                  ))}
                </div>
              </div>

              {/* Session Settings */}
              <div className="config-section">
                <h4 className="section-title">Session Settings</h4>
                <div className="settings-grid">
                  <div className="setting-item">
                    <label htmlFor="maxResponseLength">Response Length</label>
                    <select 
                      id="maxResponseLength"
                      value={sessionSettings.maxResponseLength}
                      onChange={(e) => setSessionSettings(prev => ({
                        ...prev,
                        maxResponseLength: e.target.value
                      }))}
                    >
                      <option value="brief">Brief</option>
                      <option value="medium">Medium</option>
                      <option value="detailed">Detailed</option>
                    </select>
                  </div>
                  
                  <div className="setting-item">
                    <label htmlFor="focusArea">Focus Area</label>
                    <select 
                      id="focusArea"
                      value={sessionSettings.focusArea}
                      onChange={(e) => setSessionSettings(prev => ({
                        ...prev,
                        focusArea: e.target.value
                      }))}
                    >
                      <option value="balanced">Balanced</option>
                      <option value="analytical">Analytical</option>
                      <option value="creative">Creative</option>
                      <option value="practical">Practical</option>
                    </select>
                  </div>

                  <div className="setting-item">
                    <label htmlFor="councilStyle">Council Style</label>
                    <select 
                      id="councilStyle"
                      value={sessionSettings.councilStyle}
                      onChange={(e) => setSessionSettings(prev => ({
                        ...prev,
                        councilStyle: e.target.value
                      }))}
                    >
                      <option value="collaborative">Collaborative</option>
                      <option value="debate">Debate</option>
                      <option value="supportive">Supportive</option>
                      <option value="challenging">Challenging</option>
                    </select>
                  </div>
                </div>
              </div>
            </div>
          </motion.div>
        )}
      </AnimatePresence>

      {/* Main Session Area */}
      <div className="session-main">
        {/* Conversation History */}
        <div className="conversation-area">
          <div className="conversation-history">
            {conversationHistory.map(entry => (
              <div key={entry.id} className={`conversation-entry ${entry.type}`}>
                {entry.type === 'question' && (
                  <div className="question-entry">
                    <div className="entry-header">
                      <span className="entry-icon">👤</span>
                      <span className="entry-label">Student Question</span>
                      <span className="entry-timestamp">
                        {new Date(entry.timestamp).toLocaleTimeString()}
                      </span>
                    </div>
                    <div className="entry-content">
                      <p>{entry.content}</p>
                    </div>
                  </div>
                )}

                {entry.type === 'synthesis' && (
                  <div className="synthesis-entry">
                    <div className="entry-header">
                      <span className="entry-icon">🌀</span>
                      <span className="entry-label">Council Synthesis</span>
                      <span className="effectiveness-badge">
                        {entry.effectivenessScore}% Effective
                      </span>
                    </div>
                    <div className="entry-content">
                      <div className="synthesis-content">
                        <h4>Integrated Response</h4>
                        <p>{entry.content}</p>
                      </div>
                      
                      {entry.insights && (
                        <div className="synthesis-insights">
                          <h4>Key Insights</h4>
                          <ul>
                            {entry.insights.map((insight, index) => (
                              <li key={index}>{insight}</li>
                            ))}
                          </ul>
                        </div>
                      )}

                      {entry.recommendations && (
                        <div className="synthesis-recommendations">
                          <h4>Next Steps</h4>
                          <ul>
                            {entry.recommendations.map((rec, index) => (
                              <li key={index}>{rec}</li>
                            ))}
                          </ul>
                        </div>
                      )}

                      {entry.qwanAlignment && (
                        <div className="qwan-alignment">
                          <h4>QWAN Alignment</h4>
                          <div className="qwan-metrics">
                            {Object.entries(entry.qwanAlignment).map(([principle, score]) => (
                              <div key={principle} className="qwan-metric">
                                <span className="metric-name">
                                  {principle.charAt(0).toUpperCase() + principle.slice(1)}
                                </span>
                                <div className="metric-bar">
                                  <div 
                                    className="metric-fill"
                                    style={{ width: `${score * 100}%` }}
                                  ></div>
                                </div>
                                <span className="metric-value">{Math.round(score * 100)}%</span>
                              </div>
                            ))}
                          </div>
                        </div>
                      )}
                    </div>
                  </div>
                )}
              </div>
            ))}

            {/* Active Council Responses */}
            {sessionState === 'deliberating' && (
              <div className="council-responses">
                <div className="responses-header">
                  <h3 className="responses-title">
                    <span className="title-icon">🏛️</span>
                    Council Deliberation
                  </h3>
                  <div className="deliberation-progress">
                    <span className="progress-text">
                      {Object.keys(councilResponses).length} of {activeArchetypes.length} responses
                    </span>
                    <div className="progress-bar">
                      <div 
                        className="progress-fill"
                        style={{ 
                          width: `${(Object.keys(councilResponses).length / activeArchetypes.length) * 100}%` 
                        }}
                      ></div>
                    </div>
                  </div>
                </div>

                <div className="responses-grid">
                  {activeArchetypes.map(archetypeId => 
                    renderArchetypeResponse(archetypeId, councilResponses[archetypeId])
                  )}
                </div>

                {Object.keys(councilResponses).length === activeArchetypes.length && (
                  <motion.div 
                    className="synthesis-trigger"
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: 0.5 }}
                  >
                    <button 
                      className="synthesis-btn"
                      onClick={handleSynthesis}
                      disabled={sessionState !== 'deliberating'}
                    >
                      <span className="btn-icon">🌀</span>
                      Synthesize Council Responses
                      <span className="btn-description">
                        Integrate all perspectives into unified understanding
                      </span>
                    </button>
                  </motion.div>
                )}
              </div>
            )}

            {/* Synthesis Progress */}
            {sessionState === 'synthesizing' && (
              <motion.div 
                className="synthesis-progress"
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
              >
                <div className="synthesis-header">
                  <span className="synthesis-icon">🌀</span>
                  <h3>Synthesizing Council Wisdom...</h3>
                </div>
                <div className="synthesis-steps">
                  <div className={`synthesis-step ${synthesisProgress > 25 ? 'complete' : 'active'}`}>
                    Analyzing perspectives
                  </div>
                  <div className={`synthesis-step ${synthesisProgress > 50 ? 'complete' : synthesisProgress > 25 ? 'active' : ''}`}>
                    Finding connections
                  </div>
                  <div className={`synthesis-step ${synthesisProgress > 75 ? 'complete' : synthesisProgress > 50 ? 'active' : ''}`}>
                    Integrating insights
                  </div>
                  <div className={`synthesis-step ${synthesisProgress > 90 ? 'complete' : synthesisProgress > 75 ? 'active' : ''}`}>
                    Generating response
                  </div>
                </div>
                <div className="synthesis-progress-bar">
                  <div 
                    className="progress-fill"
                    style={{ width: `${synthesisProgress}%` }}
                  ></div>
                </div>
              </motion.div>
            )}

            <div ref={messagesEndRef} />
          </div>
        </div>

        {/* Question Input */}
        <div className="question-input-area">
          <form onSubmit={handleQuestionSubmit} className="question-form">
            <div className="input-container">
              <textarea
                value={currentQuestion}
                onChange={(e) => setCurrentQuestion(e.target.value)}
                placeholder="Ask your question to the AI Council... They'll collaborate to provide multiple perspectives and synthesized wisdom."
                className="question-input"
                rows={3}
                disabled={sessionState !== 'ready'}
                onKeyDown={(e) => {
                  if (e.key === 'Enter' && !e.shiftKey) {
                    e.preventDefault();
                    handleQuestionSubmit(e);
                  }
                }}
              />
              <div className="input-actions">
                <button 
                  type="button"
                  className={`voice-btn ${voiceEnabled ? 'active' : ''}`}
                  onClick={() => setVoiceEnabled(!voiceEnabled)}
                >
                  🎤
                </button>
                <button 
                  type="submit"
                  className="submit-btn"
                  disabled={!currentQuestion.trim() || sessionState !== 'ready'}
                >
                  <span className="btn-text">
                    {sessionState === 'ready' ? 'Ask Council' : 'Processing...'}
                  </span>
                  <span className="btn-icon">→</span>
                </button>
              </div>
            </div>
            <div className="input-footer">
              <div className="character-count">
                {currentQuestion.length} / 2000 characters
              </div>
              <div className="input-hints">
                <span className="hint">💡 Try: "Explain quantum physics in simple terms"</span>
                <span className="hint">💡 Try: "Help me write a persuasive essay about climate change"</span>
              </div>
            </div>
          </form>
        </div>
      </div>
    </div>
  );
};

export default CouncilSession;
