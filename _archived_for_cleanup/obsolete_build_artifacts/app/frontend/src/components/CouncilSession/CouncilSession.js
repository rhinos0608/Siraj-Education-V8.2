import React, { useState, useEffect, useRef } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { motion, AnimatePresence } from 'framer-motion';
import {
  Send, Mic, MicOff, Settings, Download, Share2, RotateCcw, Zap, Users, Brain,
  MessageSquare, Clock, CheckCircle, AlertCircle, Loader, Eye, Target, Layers,
  Activity, Award, Volume2, VolumeX, Maximize2, Minimize2
} from 'lucide-react';
import { useSirajAPI, useSirajWebSocket } from '../../hooks/useSirajAPI';
import { getArchetypeConfig } from '../../utils/councilUtils';
import CouncilMember from './CouncilMember';
import SessionControls from './SessionControls';
import TopicSuggestions from './TopicSuggestions';
import './CouncilSession.css';

/**
 * Enhanced CouncilSession Component
 * =================================
 * 
 * Now showcases the FULL backend real-time capabilities:
 * - Live multi-archetype streaming with rich visualization
 * - Real-time council deliberation display
 * - Living spiral phase transitions with animations
 * - Advanced WebSocket message handling
 * - Synthesis generation with step-by-step breakdown
 * - Session analytics and effectiveness tracking
 */

const CouncilSession = ({ 
  currentSession, 
  onSessionEnd, 
  councilState 
}) => {
  const { sessionId } = useParams();
  const navigate = useNavigate();
  
  // Enhanced Session state
  const [sessionActive, setSessionActive] = useState(false);
  const [question, setQuestion] = useState('');
  const [sessionHistory, setSessionHistory] = useState([]);
  const [selectedArchetypes, setSelectedArchetypes] = useState(['socratic', 'constructivist', 'mentor']);
  const [sessionSettings, setSessionSettings] = useState({
    gradeLevel: 'middle',
    learningObjective: 'understand',
    streamingMode: true,
    showThinking: true,
    showSynthesis: true,
    enableAudio: false,
    visualMode: 'council' // council, spiral, focus
  });
  
  // Real-time streaming state
  const [councilPhase, setCouncilPhase] = useState('waiting'); // waiting, deliberating, synthesizing, complete
  const [deliberationStages, setDeliberationStages] = useState([]);
  const [synthesisStages, setSynthesisStages] = useState([]);
  const [archetypeResponses, setArchetypeResponses] = useState({});
  const [currentSpeaker, setCurrentSpeaker] = useState(null);
  const [spiralProgress, setSpiralProgress] = useState({
    collapse: false,
    council: false,
    synthesis: false,
    rebirth: false
  });
  
  // UI state
  const [isRecording, setIsRecording] = useState(false);
  const [showSettings, setShowSettings] = useState(false);
  const [showSuggestions, setShowSuggestions] = useState(true);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [isFullscreen, setIsFullscreen] = useState(false);
  const [sessionStats, setSessionStats] = useState({
    startTime: null,
    messageCount: 0,
    archetypeParticipation: {},
    spiralCycles: 0
  });
  
  // Refs
  const messagesEndRef = useRef(null);
  const inputRef = useRef(null);
  const mediaRecorderRef = useRef(null);
  const councilContainerRef = useRef(null);
  
  // Enhanced API hooks
  const { processEducationalRequest } = useSirajAPI();
  const {
    connected,
    streaming,
    stages,
    currentStage,
    finalResult,
    error: wsError,
    connect,
    disconnect,
    sendEducationalRequest
  } = useSirajWebSocket(sessionId || currentSession?.id);

  // Initialize enhanced session
  useEffect(() => {
    initializeEnhancedSession();
    return () => {
      disconnect();
    };
  }, [sessionId]);

  // Process real-time WebSocket stages
  useEffect(() => {
    processWebSocketStages();
  }, [stages, currentStage]);

  // Auto-scroll to bottom
  useEffect(() => {
    scrollToBottom();
  }, [sessionHistory, archetypeResponses, synthesisStages]);

  const initializeEnhancedSession = async () => {
    if (sessionId && sessionId !== 'new') {
      try {
        setSessionActive(true);
        setSessionStats(prev => ({ ...prev, startTime: new Date() }));
      } catch (error) {
        console.error('Failed to load session:', error);
        navigate('/council/new');
      }
    } else {
      const newSessionId = `session-${Date.now()}`;
      const newSession = {
        id: newSessionId,
        startTime: new Date(),
        topic: '',
        gradeLevel: sessionSettings.gradeLevel,
        selectedArchetypes: selectedArchetypes,
        spiralPhase: 'collapse'
      };
      
      if (sessionSettings.streamingMode) {
        connect();
      }
    }
  };

  const processWebSocketStages = () => {
    stages.forEach(stage => {
      switch (stage.type) {
        case 'session_start':
          setCouncilPhase('deliberating');
          setSpiralProgress(prev => ({ ...prev, collapse: true, council: true }));
          setSessionStats(prev => ({ ...prev, spiralCycles: prev.spiralCycles + 1 }));
          break;
          
        case 'archetype_start':
          setCurrentSpeaker(stage.archetype);
          setDeliberationStages(prev => [...prev, {
            type: 'start',
            archetype: stage.archetype,
            timestamp: new Date(),
            emoji: stage.emoji,
            name: stage.name
          }]);
          break;
          
        case 'archetype_chunk':
          // Real-time archetype response building
          setArchetypeResponses(prev => ({
            ...prev,
            [stage.archetype]: {
              ...prev[stage.archetype],
              content: (prev[stage.archetype]?.content || '') + stage.chunk,
              isStreaming: true,
              lastUpdate: new Date()
            }
          }));
          break;
          
        case 'archetype_complete':
          setArchetypeResponses(prev => ({
            ...prev,
            [stage.archetype]: {
              ...prev[stage.archetype],
              content: stage.full_response,
              isStreaming: false,
              completed: true,
              timestamp: new Date()
            }
          }));
          
          setSessionStats(prev => ({
            ...prev,
            archetypeParticipation: {
              ...prev.archetypeParticipation,
              [stage.archetype]: (prev.archetypeParticipation[stage.archetype] || 0) + 1
            }
          }));
          break;
          
        case 'synthesis_start':
          setCouncilPhase('synthesizing');
          setSpiralProgress(prev => ({ ...prev, synthesis: true }));
          setSynthesisStages([{ type: 'start', timestamp: new Date() }]);
          break;
          
        case 'synthesis_chunk':
          setSynthesisStages(prev => [...prev, {
            type: 'chunk',
            content: stage.chunk,
            timestamp: new Date()
          }]);
          break;
          
        case 'synthesis_complete':
          setCouncilPhase('complete');
          setSpiralProgress(prev => ({ ...prev, rebirth: true }));
          setSynthesisStages(prev => [...prev, {
            type: 'complete',
            content: stage.synthesis,
            timestamp: new Date()
          }]);
          
          // Add to session history
          const responseEntry = {
            id: Date.now(),
            type: 'council_response',
            archetypeResponses: { ...archetypeResponses },
            synthesis: stage.synthesis,
            timestamp: new Date(),
            sessionStats: { ...sessionStats }
          };
          setSessionHistory(prev => [...prev, responseEntry]);
          break;
          
        case 'session_complete':
          setCurrentSpeaker(null);
          setSessionStats(prev => ({ ...prev, messageCount: prev.messageCount + 1 }));
          
          // Reset for next question
          setTimeout(() => {
            setCouncilPhase('waiting');
            setArchetypeResponses({});
            setDeliberationStages([]);
            setSynthesisStages([]);
            setSpiralProgress({
              collapse: false,
              council: false,
              synthesis: false,
              rebirth: false
            });
          }, 3000);
          break;
      }
    });
  };

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  const handleSubmitQuestion = async (e) => {
    e.preventDefault();
    
    if (!question.trim() || selectedArchetypes.length === 0) return;
    
    setIsSubmitting(true);
    setShowSuggestions(false);
    
    // Reset spiral progress
    setSpiralProgress({ collapse: true, council: false, synthesis: false, rebirth: false });
    
    const requestData = {
      topic: question,
      grade_level: sessionSettings.gradeLevel,
      learning_objective: sessionSettings.learningObjective,
      context: `Session settings: ${JSON.stringify(sessionSettings)}`,
      session_id: currentSession?.id,
      selected_archetypes: selectedArchetypes,
      streaming: sessionSettings.streamingMode
    };

    try {
      // Add question to history with enhanced metadata
      const questionEntry = {
        id: Date.now(),
        type: 'question',
        content: question,
        timestamp: new Date(),
        user: 'student',
        selectedArchetypes: [...selectedArchetypes],
        gradeLevel: sessionSettings.gradeLevel,
        learningObjective: sessionSettings.learningObjective
      };
      
      setSessionHistory(prev => [...prev, questionEntry]);
      setQuestion('');

      if (sessionSettings.streamingMode && connected) {
        // Use enhanced WebSocket streaming
        sendEducationalRequest(requestData);
      } else {
        // Fallback to direct API
        const response = await processEducationalRequest(requestData);
        
        const responseEntry = {
          id: Date.now() + 1,
          type: 'response',
          content: response,
          timestamp: new Date(),
          archetypes: selectedArchetypes
        };
        
        setSessionHistory(prev => [...prev, responseEntry]);
      }
      
      setSessionActive(true);
    } catch (error) {
      console.error('Failed to submit question:', error);
      const errorEntry = {
        id: Date.now() + 2,
        type: 'error',
        content: 'Sorry, I encountered an error processing your question. Please try again.',
        timestamp: new Date()
      };
      setSessionHistory(prev => [...prev, errorEntry]);
    } finally {
      setIsSubmitting(false);
    }
  };

  // Enhanced archetype response rendering
  const renderArchetypeResponses = () => {
    return (
      <div className="archetype-responses">
        <div className="responses-header">
          <Users className="responses-icon" />
          <h3>Council Deliberation</h3>
          <div className="deliberation-status">
            {councilPhase === 'deliberating' && <span className="status-badge deliberating">Active Discussion</span>}
            {councilPhase === 'synthesizing' && <span className="status-badge synthesizing">Creating Synthesis</span>}
            {councilPhase === 'complete' && <span className="status-badge complete">Complete</span>}
          </div>
        </div>
        
        <div className="archetype-grid">
          {selectedArchetypes.map(archetype => {
            const config = getArchetypeConfig(archetype);
            const response = archetypeResponses[archetype];
            const isActive = currentSpeaker === archetype;
            
            return (
              <motion.div
                key={archetype}
                className={`archetype-response-card ${isActive ? 'active' : ''} ${response?.completed ? 'completed' : ''}`}
                initial={{ opacity: 0, scale: 0.9 }}
                animate={{ opacity: 1, scale: 1 }}
                transition={{ duration: 0.3 }}
                style={{ borderColor: config.color }}
              >
                <div className="archetype-header">
                  <div className="archetype-avatar" style={{ backgroundColor: config.color }}>
                    {config.emoji}
                  </div>
                  <div className="archetype-info">
                    <h4>{config.name}</h4>
                    <span className="archetype-role">{config.personality}</span>
                  </div>
                  <div className="response-status">
                    {response?.isStreaming && <Loader className="streaming-icon" size={16} />}
                    {response?.completed && <CheckCircle className="completed-icon" size={16} />}
                    {isActive && !response && <Activity className="active-icon" size={16} />}
                  </div>
                </div>
                
                <div className="response-content">
                  {response?.content ? (
                    <div className="response-text">
                      {response.content}
                      {response.isStreaming && <span className="cursor">|</span>}
                    </div>
                  ) : isActive ? (
                    <div className="thinking-indicator">
                      <div className="thinking-dots">
                        <span></span>
                        <span></span>
                        <span></span>
                      </div>
                      <span>Thinking...</span>
                    </div>
                  ) : (
                    <div className="waiting-indicator">
                      Waiting to contribute...
                    </div>
                  )}
                </div>
                
                {response?.completed && (
                  <div className="response-footer">
                    <div className="response-meta">
                      <Clock size={12} />
                      <span>{new Date(response.timestamp).toLocaleTimeString()}</span>
                    </div>
                  </div>
                )}
              </motion.div>
            );
          })}
        </div>
      </div>
    );
  };

  // Enhanced synthesis rendering
  const renderSynthesis = () => {
    if (synthesisStages.length === 0) return null;
    
    const completeSynthesis = synthesisStages.find(stage => stage.type === 'complete');
    
    return (
      <motion.div
        className="synthesis-container"
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
      >
        <div className="synthesis-header">
          <Brain className="synthesis-icon" />
          <h3>Council Synthesis</h3>
          <div className="synthesis-meta">
            <span>Integrating {selectedArchetypes.length} perspectives</span>
          </div>
        </div>
        
        <div className="synthesis-content">
          {councilPhase === 'synthesizing' && !completeSynthesis && (
            <div className="synthesis-building">
              <div className="synthesis-progress">
                <div className="progress-bar">
                  <div className="progress-fill" style={{ width: '60%' }} />
                </div>
                <span>Building unified response...</span>
              </div>
              
              <div className="synthesis-steps">
                {synthesisStages.filter(s => s.type === 'chunk').map((stage, index) => (
                  <div key={index} className="synthesis-step">
                    {stage.content}
                  </div>
                ))}
                <div className="building-indicator">
                  <Loader className="building-icon" size={16} />
                  <span>Synthesizing insights...</span>
                </div>
              </div>
            </div>
          )}
          
          {completeSynthesis && (
            <div className="synthesis-result">
              <div className="synthesis-text">
                {completeSynthesis.content}
              </div>
              
              <div className="synthesis-footer">
                <div className="synthesis-stats">
                  <div className="stat">
                    <Users size={14} />
                    <span>{selectedArchetypes.length} voices</span>
                  </div>
                  <div className="stat">
                    <Clock size={14} />
                    <span>{new Date(completeSynthesis.timestamp).toLocaleTimeString()}</span>
                  </div>
                  <div className="stat">
                    <Award size={14} />
                    <span>Unified wisdom</span>
                  </div>
                </div>
                
                <div className="synthesis-actions">
                  <button className="action-btn">
                    <Download size={14} />
                    Save Response
                  </button>
                  <button className="action-btn">
                    <Share2 size={14} />
                    Share
                  </button>
                </div>
              </div>
            </div>
          )}
        </div>
      </motion.div>
    );
  };

  // Living spiral progress indicator
  const renderSpiralProgress = () => {
    return (
      <div className="spiral-progress">
        <div className="spiral-phases">
          {Object.entries(spiralProgress).map(([phase, completed]) => (
            <div key={phase} className={`spiral-phase ${completed ? 'completed' : ''}`}>
              <div className="phase-icon">
                {phase === 'collapse' && <Target size={16} />}
                {phase === 'council' && <Users size={16} />}
                {phase === 'synthesis' && <Brain size={16} />}
                {phase === 'rebirth' && <Zap size={16} />}
              </div>
              <span className="phase-name">{phase}</span>
              {completed && <CheckCircle className="completed-indicator" size={12} />}
            </div>
          ))}
        </div>
        
        <div className="spiral-connector">
          <svg viewBox="0 0 400 50">
            <path
              d="M 50 25 Q 150 5 250 25 Q 350 45 350 25"
              stroke="#3b82f6"
              strokeWidth="2"
              fill="none"
              strokeDasharray="5,5"
              className="spiral-path"
            />
          </svg>
        </div>
      </div>
    );
  };

  // Enhanced session statistics
  const renderSessionStats = () => {
    if (!sessionActive) return null;
    
    return (
      <div className="session-stats">
        <div className="stats-grid">
          <div className="stat-item">
            <Clock className="stat-icon" />
            <div className="stat-content">
              <span className="stat-value">
                {sessionStats.startTime ? 
                  Math.round((new Date() - sessionStats.startTime) / 60000) : 0}m
              </span>
              <span className="stat-label">Session Time</span>
            </div>
          </div>
          
          <div className="stat-item">
            <MessageSquare className="stat-icon" />
            <div className="stat-content">
              <span className="stat-value">{sessionStats.messageCount}</span>
              <span className="stat-label">Questions</span>
            </div>
          </div>
          
          <div className="stat-item">
            <RotateCcw className="stat-icon" />
            <div className="stat-content">
              <span className="stat-value">{sessionStats.spiralCycles}</span>
              <span className="stat-label">Spiral Cycles</span>
            </div>
          </div>
          
          <div className="stat-item">
            <Users className="stat-icon" />
            <div className="stat-content">
              <span className="stat-value">{selectedArchetypes.length}</span>
              <span className="stat-label">Active Council</span>
            </div>
          </div>
        </div>
      </div>
    );
  };

  return (
    <div className={`enhanced-council-session ${isFullscreen ? 'fullscreen' : ''}`}>
      {/* Enhanced Session Header */}
      <div className="session-header">
        <div className="session-info">
          <h1>
            <Brain className="header-icon" />
            AI Council Session
          </h1>
          <div className="session-meta">
            {currentSession && (
              <>
                <span className="session-id">ID: {currentSession.id?.slice(-8)}</span>
                <span className="session-time">
                  Started: {new Date(currentSession.startTime).toLocaleTimeString()}
                </span>
              </>
            )}
            <div className="connection-status">
              <div className={`status-dot ${connected ? 'connected' : 'disconnected'}`} />
              <span>{connected ? 'Real-time Active' : 'Offline Mode'}</span>
            </div>
            <div className="council-phase">
              <span className={`phase-indicator ${councilPhase}`}>
                {councilPhase.charAt(0).toUpperCase() + councilPhase.slice(1)}
              </span>
            </div>
          </div>
        </div>
        
        <div className="session-actions">
          <button
            className="session-action-btn"
            onClick={() => setIsFullscreen(!isFullscreen)}
            title={isFullscreen ? 'Exit Fullscreen' : 'Enter Fullscreen'}
          >
            {isFullscreen ? <Minimize2 size={18} /> : <Maximize2 size={18} />}
          </button>
          
          <button
            className="session-action-btn"
            onClick={() => setShowSettings(!showSettings)}
            title="Session Settings"
          >
            <Settings size={18} />
          </button>
          
          <button
            className="session-action-btn"
            title="Export Session"
            disabled={sessionHistory.length === 0}
          >
            <Download size={18} />
          </button>
          
          <button
            className="session-action-btn new-session"
            title="New Session"
          >
            <RotateCcw size={18} />
            New Session
          </button>
        </div>
      </div>

      {/* Living Spiral Progress */}
      {sessionActive && renderSpiralProgress()}

      {/* Session Statistics */}
      {renderSessionStats()}

      {/* Enhanced Session Settings Panel */}
      <AnimatePresence>
        {showSettings && (
          <SessionControls
            settings={sessionSettings}
            onSettingsChange={setSessionSettings}
            selectedArchetypes={selectedArchetypes}
            onArchetypeToggle={(archetype) => {
              setSelectedArchetypes(prev => 
                prev.includes(archetype) 
                  ? prev.filter(a => a !== archetype)
                  : [...prev, archetype]
              );
            }}
            onClose={() => setShowSettings(false)}
          />
        )}
      </AnimatePresence>

      {/* Main Session Area */}
      <div className="session-main" ref={councilContainerRef}>
        <div className="messages-container">
          
          {/* Welcome Message */}
          {!sessionActive && sessionHistory.length === 0 && (
            <motion.div
              className="welcome-message"
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6 }}
            >
              <div className="welcome-content">
                <Brain className="welcome-icon" />
                <h2>Welcome to Your Enhanced AI Teaching Council</h2>
                <p>
                  Experience real-time collaboration between {selectedArchetypes.length} AI teaching personalities. 
                  Watch the living spiral methodology unfold as your council deliberates and synthesizes wisdom.
                </p>
                
                <div className="selected-teachers">
                  <span className="teachers-label">Your Council:</span>
                  <div className="teacher-avatars">
                    {selectedArchetypes.map((archetype) => {
                      const config = getArchetypeConfig(archetype);
                      return (
                        <div
                          key={archetype}
                          className="teacher-avatar"
                          style={{ backgroundColor: config.color }}
                          title={`${config.name} - ${config.role}`}
                        >
                          {config.emoji}
                        </div>
                      );
                    })}
                  </div>
                </div>
              </div>
            </motion.div>
          )}

          {/* Topic Suggestions */}
          {showSuggestions && sessionHistory.length === 0 && (
            <TopicSuggestions
              gradeLevel={sessionSettings.gradeLevel}
              onSuggestionSelect={(suggestion) => {
                setQuestion(suggestion.question);
                inputRef.current?.focus();
              }}
            />
          )}

          {/* Session History */}
          <div className="messages-list">
            {sessionHistory.map((entry) => (
              <motion.div
                key={entry.id}
                className={`message ${entry.type}`}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.4 }}
              >
                {entry.type === 'question' && (
                  <div className="question-message">
                    <div className="message-header">
                      <MessageSquare className="message-icon" />
                      <span className="message-author">You asked:</span>
                      <span className="message-meta">
                        {entry.selectedArchetypes?.length} council members • {entry.gradeLevel} level
                      </span>
                      <span className="message-time">
                        {entry.timestamp.toLocaleTimeString()}
                      </span>
                    </div>
                    <div className="message-content">
                      {entry.content}
                    </div>
                  </div>
                )}

                {entry.type === 'council_response' && (
                  <div className="council-response-message">
                    <div className="message-header">
                      <Brain className="message-icon" />
                      <span className="message-author">AI Council Complete Response</span>
                      <span className="message-time">
                        {entry.timestamp.toLocaleTimeString()}
                      </span>
                    </div>
                    
                    {/* Individual archetype responses */}
                    <div className="archetype-responses-summary">
                      {Object.entries(entry.archetypeResponses).map(([archetype, response]) => {
                        const config = getArchetypeConfig(archetype);
                        return (
                          <div key={archetype} className="archetype-summary">
                            <div className="archetype-header">
                              <span className="archetype-emoji" style={{ color: config.color }}>
                                {config.emoji}
                              </span>
                              <span className="archetype-name">{config.name}</span>
                            </div>
                            <div className="archetype-content">
                              {response.content}
                            </div>
                          </div>
                        );
                      })}
                    </div>
                    
                    {/* Synthesis */}
                    <div className="synthesis-summary">
                      <div className="synthesis-header">
                        <Zap className="synthesis-icon" />
                        <span>Council Synthesis</span>
                      </div>
                      <div className="synthesis-content">
                        {entry.synthesis}
                      </div>
                    </div>
                  </div>
                )}

                {entry.type === 'error' && (
                  <div className="error-message">
                    <AlertCircle className="message-icon" />
                    <span>{entry.content}</span>
                  </div>
                )}
              </motion.div>
            ))}
          </div>

          {/* Real-time Council Deliberation */}
          {councilPhase !== 'waiting' && renderArchetypeResponses()}
          
          {/* Real-time Synthesis */}
          {renderSynthesis()}

          {/* WebSocket Error */}
          {wsError && (
            <div className="error-message">
              <AlertCircle className="message-icon" />
              <span>Connection error: {wsError}</span>
            </div>
          )}

          <div ref={messagesEndRef} />
        </div>

        {/* Enhanced Input Area */}
        <div className="input-area">
          {selectedArchetypes.length === 0 && (
            <div className="no-teachers-warning">
              <AlertCircle size={16} />
              <span>Please select at least one AI teacher to continue</span>
            </div>
          )}

          <form onSubmit={handleSubmitQuestion} className="question-form">
            <div className="input-container">
              <textarea
                ref={inputRef}
                value={question}
                onChange={(e) => setQuestion(e.target.value)}
                placeholder="Ask your AI teaching council anything... Watch them deliberate in real-time!"
                className="question-input"
                rows={2}
                disabled={isSubmitting || selectedArchetypes.length === 0 || councilPhase === 'deliberating'}
                onKeyDown={(e) => {
                  if (e.key === 'Enter' && !e.shiftKey) {
                    e.preventDefault();
                    handleSubmitQuestion(e);
                  }
                }}
              />
              
              <div className="input-actions">
                <button
                  type="button"
                  className={`voice-btn ${isRecording ? 'recording' : ''}`}
                  title={isRecording ? 'Stop Recording' : 'Voice Input'}
                >
                  {isRecording ? <MicOff size={18} /> : <Mic size={18} />}
                </button>
                
                <button
                  type="submit"
                  className="submit-btn"
                  disabled={!question.trim() || isSubmitting || selectedArchetypes.length === 0 || councilPhase === 'deliberating'}
                  title="Send Question to Council"
                >
                  {isSubmitting || councilPhase === 'deliberating' ? (
                    <Loader className="spinning" size={18} />
                  ) : (
                    <Send size={18} />
                  )}
                </button>
              </div>
            </div>
            
            <div className="input-footer">
              <div className="character-count">
                {question.length}/1000
              </div>
              
              <div className="council-status">
                {councilPhase === 'waiting' && (
                  <span className="status-text">💡 Ready for your question</span>
                )}
                {councilPhase === 'deliberating' && (
                  <span className="status-text">🧠 Council is deliberating...</span>
                )}
                {councilPhase === 'synthesizing' && (
                  <span className="status-text">⚡ Creating synthesis...</span>
                )}
                {councilPhase === 'complete' && (
                  <span className="status-text">✨ Council response complete</span>
                )}
              </div>
              
              <div className="streaming-indicator">
                {connected && <div className="streaming-dot" />}
                <span>{connected ? 'Live streaming active' : 'Offline mode'}</span>
              </div>
            </div>
          </form>
        </div>
      </div>
    </div>
  );
};

export default CouncilSession;