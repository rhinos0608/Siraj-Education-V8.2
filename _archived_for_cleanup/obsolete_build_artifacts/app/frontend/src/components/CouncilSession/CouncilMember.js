import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import {
  MessageSquare,
  ThumbsUp,
  ThumbsDown,
  Copy,
  MoreHorizontal,
  Eye,
  EyeOff,
  Volume2,
  VolumeX
} from 'lucide-react';
import { 
  getCouncilColor, 
  getCouncilAvatar, 
  getCouncilName,
  getArchetypeConfig 
} from '../../utils/councilUtils';
import './CouncilMember.css';

/**
 * CouncilMember Component
 * ======================
 * 
 * Represents an individual AI archetype in the council session.
 * Shows streaming responses, personality indicators, and interaction controls.
 */

const CouncilMember = ({ 
  archetype, 
  stages, 
  isActive, 
  showThinking,
  onFeedback 
}) => {
  const [isExpanded, setIsExpanded] = useState(true);
  const [isSpeaking, setIsSpeaking] = useState(false);
  const [showActions, setShowActions] = useState(false);
  const [currentResponse, setCurrentResponse] = useState('');
  const [responseComplete, setResponseComplete] = useState(false);

  const archetypeConfig = getArchetypeConfig(archetype);
  
  useEffect(() => {
    // Build current response from stages
    let response = '';
    let complete = false;
    
    stages.forEach(stage => {
      if (stage.type === 'archetype_response') {
        response += stage.message || '';
        complete = stage.complete || false;
      }
    });
    
    setCurrentResponse(response);
    setResponseComplete(complete);
  }, [stages]);

  const handleCopyResponse = async () => {
    try {
      await navigator.clipboard.writeText(currentResponse);
      // Show success feedback
    } catch (error) {
      console.error('Failed to copy response:', error);
    }
  };

  const handleTextToSpeech = () => {
    if (isSpeaking) {
      speechSynthesis.cancel();
      setIsSpeaking(false);
    } else {
      const utterance = new SpeechSynthesisUtterance(currentResponse);
      utterance.rate = 0.9;
      utterance.pitch = 1;
      
      // Try to set a voice that matches the archetype personality
      const voices = speechSynthesis.getVoices();
      if (voices.length > 0) {
        // Simple voice selection based on archetype
        const voiceIndex = Math.abs(archetype.charCodeAt(0)) % voices.length;
        utterance.voice = voices[voiceIndex];
      }
      
      utterance.onstart = () => setIsSpeaking(true);
      utterance.onend = () => setIsSpeaking(false);
      utterance.onerror = () => setIsSpeaking(false);
      
      speechSynthesis.speak(utterance);
    }
  };

  const handleFeedbackClick = (type) => {
    if (onFeedback) {
      onFeedback({
        archetype,
        feedbackType: type,
        response: currentResponse,
        timestamp: new Date()
      });
    }
  };

  if (!archetypeConfig) {
    return null;
  }

  return (
    <motion.div
      className={`council-member ${isActive ? 'active' : ''} ${responseComplete ? 'complete' : ''}`}
      style={{ '--archetype-color': archetypeConfig.color }}
      initial={{ opacity: 0, scale: 0.95 }}
      animate={{ opacity: 1, scale: 1 }}
      transition={{ duration: 0.3 }}
    >
      {/* Member Header */}
      <div className="member-header">
        <div className="member-info">
          <div className="member-avatar">
            <span className="avatar-emoji">{archetypeConfig.emoji}</span>
            {isActive && (
              <div className="activity-indicator">
                <div className="activity-pulse" />
              </div>
            )}
          </div>
          
          <div className="member-details">
            <h3 className="member-name">{archetypeConfig.name}</h3>
            <p className="member-role">{archetypeConfig.role}</p>
            <div className="member-personality">
              <span className="personality-tag">{archetypeConfig.personality}</span>
            </div>
          </div>
        </div>
        
        <div className="member-controls">
          <button
            className="control-btn"
            onClick={() => setIsExpanded(!isExpanded)}
            title={isExpanded ? 'Collapse' : 'Expand'}
          >
            {isExpanded ? <EyeOff size={16} /> : <Eye size={16} />}
          </button>
          
          <button
            className="control-btn"
            onClick={() => setShowActions(!showActions)}
            title="More Actions"
          >
            <MoreHorizontal size={16} />
          </button>
        </div>
      </div>

      {/* Member Content */}
      <AnimatePresence>
        {isExpanded && (
          <motion.div
            className="member-content"
            initial={{ height: 0, opacity: 0 }}
            animate={{ height: 'auto', opacity: 1 }}
            exit={{ height: 0, opacity: 0 }}
            transition={{ duration: 0.3 }}
          >
            {/* Thinking Process (if enabled) */}
            {showThinking && isActive && !responseComplete && (
              <div className="thinking-process">
                <div className="thinking-header">
                  <span>🤔 Thinking...</span>
                </div>
                <div className="thinking-content">
                  <div className="thinking-dots">
                    <span></span>
                    <span></span>
                    <span></span>
                  </div>
                  <p>Considering the question from a {archetypeConfig.personality} perspective...</p>
                </div>
              </div>
            )}

            {/* Response Content */}
            {currentResponse && (
              <div className="response-content">
                <div className="response-text">
                  {currentResponse}
                  {!responseComplete && isActive && (
                    <span className="typing-cursor">|</span>
                  )}
                </div>
                
                {responseComplete && (
                  <motion.div
                    className="response-footer"
                    initial={{ opacity: 0 }}
                    animate={{ opacity: 1 }}
                    transition={{ delay: 0.5 }}
                  >
                    <div className="response-actions">
                      <button
                        className="action-btn"
                        onClick={handleCopyResponse}
                        title="Copy Response"
                      >
                        <Copy size={14} />
                      </button>
                      
                      <button
                        className={`action-btn ${isSpeaking ? 'active' : ''}`}
                        onClick={handleTextToSpeech}
                        title={isSpeaking ? 'Stop Speaking' : 'Read Aloud'}
                      >
                        {isSpeaking ? <VolumeX size={14} /> : <Volume2 size={14} />}
                      </button>
                      
                      <div className="feedback-buttons">
                        <button
                          className="action-btn feedback-btn helpful"
                          onClick={() => handleFeedbackClick('helpful')}
                          title="This was helpful"
                        >
                          <ThumbsUp size={14} />
                        </button>
                        
                        <button
                          className="action-btn feedback-btn not-helpful"
                          onClick={() => handleFeedbackClick('not-helpful')}
                          title="This wasn't helpful"
                        >
                          <ThumbsDown size={14} />
                        </button>
                      </div>
                    </div>
                    
                    <div className="response-meta">
                      <span className="response-time">
                        {new Date().toLocaleTimeString()}
                      </span>
                      <span className="response-length">
                        {currentResponse.length} characters
                      </span>
                    </div>
                  </motion.div>
                )}
              </div>
            )}

            {/* No Response Yet */}
            {!currentResponse && !isActive && (
              <div className="waiting-response">
                <MessageSquare className="waiting-icon" />
                <span>Waiting for question...</span>
              </div>
            )}

            {/* Teaching Approach Info */}
            {showActions && (
              <motion.div
                className="archetype-info"
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: 10 }}
                transition={{ duration: 0.2 }}
              >
                <h4>Teaching Approach</h4>
                <p>{archetypeConfig.approach}</p>
                
                <div className="strengths-list">
                  <h5>Strengths:</h5>
                  <ul>
                    {archetypeConfig.strengths?.map((strength, index) => (
                      <li key={index}>{strength}</li>
                    ))}
                  </ul>
                </div>
                
                <div className="best-for">
                  <h5>Best for:</h5>
                  <div className="tags">
                    {archetypeConfig.bestFor?.map((item, index) => (
                      <span key={index} className="tag">{item}</span>
                    ))}
                  </div>
                </div>
              </motion.div>
            )}
          </motion.div>
        )}
      </AnimatePresence>

      {/* Processing Indicator */}
      {isActive && !responseComplete && (
        <div className="processing-indicator">
          <div className="processing-bar">
            <div className="processing-fill" />
          </div>
          <span className="processing-text">
            {archetypeConfig.name} is formulating a response...
          </span>
        </div>
      )}
    </motion.div>
  );
};

export default CouncilMember;