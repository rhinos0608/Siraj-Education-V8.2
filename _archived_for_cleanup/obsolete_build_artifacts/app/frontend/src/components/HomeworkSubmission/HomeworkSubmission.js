import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import {
  Upload,
  FileText,
  Brain,
  CheckCircle,
  AlertCircle,
  Clock,
  Users,
  Sparkles,
  Eye,
  Download,
  RotateCcw,
  Send
} from 'lucide-react';
import { useSirajAPI } from '../../hooks/useSirajAPI';
import { getArchetypeConfig } from '../../utils/councilUtils';
import CouncilMember from '../CouncilSession/CouncilMember';
import './HomeworkSubmission.css';

/**
 * HomeworkSubmission Component
 * ===========================
 * 
 * Council-driven homework feedback system following SIRAJ philosophy:
 * - Multi-perspective analysis through educational archetypes
 * - Living spiral methodology: Submit → Council Analysis → Synthesis → Rebirth
 * - QWAN principles: Wholeness, freedom, exactness, egolessness, eternity
 * - Consciousness-driven feedback that helps students learn recursively
 */

const HomeworkSubmission = () => {
  // Living Spiral State Management
  const [spiralPhase, setSpiralPhase] = useState('collapse'); // collapse, council, synthesis, rebirth
  const [submissionData, setSubmissionData] = useState({
    assignment: '',
    studentResponse: '',
    subject: 'general',
    gradeLevel: 'middle',
    rubric: null,
    attachments: []
  });

  // Council Assembly State
  const [activeArchetypes, setActiveArchetypes] = useState(['mentor', 'analyst', 'constructivist']);
  const [councilFeedback, setCouncilFeedback] = useState({});
  const [synthesizedFeedback, setSynthesizedFeedback] = useState('');
  const [improvementPlan, setImprovementPlan] = useState([]);

  // UI State
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [showCouncilProcess, setShowCouncilProcess] = useState(false);
  const [feedbackComplete, setFeedbackComplete] = useState(false);
  const [validationErrors, setValidationErrors] = useState({});

  const { submitHomework, isLoading, error } = useSirajAPI();

  // Input Validation Schema (following AI_INSTRUCTIONS security requirements)
  const validateSubmission = (data) => {
    const errors = {};
    
    if (!data.assignment.trim()) {
      errors.assignment = 'Assignment description is required';
    } else if (data.assignment.length > 5000) {
      errors.assignment = 'Assignment description must be under 5000 characters';
    }
    
    if (!data.studentResponse.trim()) {
      errors.studentResponse = 'Student response is required';
    } else if (data.studentResponse.length > 10000) {
      errors.studentResponse = 'Student response must be under 10000 characters';
    }
    
    if (!['elementary', 'middle', 'high', 'university'].includes(data.gradeLevel)) {
      errors.gradeLevel = 'Invalid grade level';
    }
    
    return errors;
  };

  // Council Assembly for Homework Feedback
  const assembleHomeworkCouncil = async () => {
    setSpiralPhase('council');
    setShowCouncilProcess(true);
    
    try {
      const response = await submitHomework({
        ...submissionData,
        selectedArchetypes: activeArchetypes,
        requestStream: true
      });

      // Stream council responses in real-time
      for await (const chunk of response) {
        if (chunk.type === 'archetype_response') {
          setCouncilFeedback(prev => ({
            ...prev,
            [chunk.archetype]: [...(prev[chunk.archetype] || []), chunk]
          }));
        } else if (chunk.type === 'synthesis') {
          setSpiralPhase('synthesis');
          setSynthesizedFeedback(chunk.content);
        } else if (chunk.type === 'improvement_plan') {
          setSpiralPhase('rebirth');
          setImprovementPlan(chunk.steps);
          setFeedbackComplete(true);
        }
      }
    } catch (error) {
      console.error('Council assembly failed:', error);
      setSpiralPhase('collapse');
    }
  };

  // Handle form submission with spiral methodology
  const handleSubmit = async (e) => {
    e.preventDefault();
    
    // Phase 1: Collapse - Validate and acknowledge complexity
    setSpiralPhase('collapse');
    const errors = validateSubmission(submissionData);
    setValidationErrors(errors);
    
    if (Object.keys(errors).length > 0) {
      return; // Stay in collapse phase until issues resolved
    }

    setIsSubmitting(true);
    
    // Phase 2: Council - Assemble multi-voice feedback
    await assembleHomeworkCouncil();
    
    setIsSubmitting(false);
  };

  // Reset to begin new submission cycle
  const resetSubmission = () => {
    setSpiralPhase('collapse');
    setSubmissionData({
      assignment: '',
      studentResponse: '',
      subject: 'general',
      gradeLevel: 'middle',
      rubric: null,
      attachments: []
    });
    setCouncilFeedback({});
    setSynthesizedFeedback('');
    setImprovementPlan([]);
    setFeedbackComplete(false);
    setShowCouncilProcess(false);
    setValidationErrors({});
  };

  return (
    <div className="homework-submission">
      {/* Spiral Phase Indicator */}
      <div className="spiral-indicator">
        <div className="phase-steps">
          {['collapse', 'council', 'synthesis', 'rebirth'].map((phase, index) => (
            <div 
              key={phase}
              className={`phase-step ${spiralPhase === phase ? 'active' : ''} ${
                ['collapse', 'council', 'synthesis', 'rebirth'].indexOf(spiralPhase) > index ? 'completed' : ''
              }`}
            >
              <div className="phase-icon">
                {phase === 'collapse' && <AlertCircle size={20} />}
                {phase === 'council' && <Users size={20} />}
                {phase === 'synthesis' && <Brain size={20} />}
                {phase === 'rebirth' && <Sparkles size={20} />}
              </div>
              <span className="phase-name">{phase}</span>
            </div>
          ))}
        </div>
        <div className="spiral-visualization">
          <motion.div 
            className="spiral-line"
            initial={{ pathLength: 0 }}
            animate={{ pathLength: spiralPhase === 'rebirth' ? 1 : 0.7 }}
            transition={{ duration: 2, ease: "easeInOut" }}
          />
        </div>
      </div>

      {/* Main Content */}
      <div className="submission-content">
        
        {/* Phase 1: Collapse - Submission Form */}
        <AnimatePresence mode="wait">
          {(spiralPhase === 'collapse' || !feedbackComplete) && (
            <motion.div
              className="submission-form-container"
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -20 }}
              transition={{ duration: 0.5 }}
            >
              <div className="form-header">
                <h2>
                  <FileText className="header-icon" />
                  Submit Your Work for Council Review
                </h2>
                <p>Our AI Educational Council will provide multi-perspective feedback to help you learn and grow.</p>
              </div>

              <form onSubmit={handleSubmit} className="submission-form">
                {/* Assignment Description */}
                <div className="form-group">
                  <label htmlFor="assignment">Assignment Description</label>
                  <textarea
                    id="assignment"
                    value={submissionData.assignment}
                    onChange={(e) => setSubmissionData(prev => ({
                      ...prev,
                      assignment: e.target.value
                    }))}
                    placeholder="Describe the assignment, question, or task you were working on..."
                    className={validationErrors.assignment ? 'error' : ''}
                    rows={4}
                  />
                  {validationErrors.assignment && (
                    <span className="error-message">{validationErrors.assignment}</span>
                  )}
                </div>

                {/* Student Response */}
                <div className="form-group">
                  <label htmlFor="studentResponse">Your Work/Response</label>
                  <textarea
                    id="studentResponse"
                    value={submissionData.studentResponse}
                    onChange={(e) => setSubmissionData(prev => ({
                      ...prev,
                      studentResponse: e.target.value
                    }))}
                    placeholder="Paste your work, solution, essay, or response here..."
                    className={validationErrors.studentResponse ? 'error' : ''}
                    rows={8}
                  />
                  {validationErrors.studentResponse && (
                    <span className="error-message">{validationErrors.studentResponse}</span>
                  )}
                </div>

                {/* Metadata */}
                <div className="form-metadata">
                  <div className="form-group">
                    <label htmlFor="subject">Subject</label>
                    <select
                      id="subject"
                      value={submissionData.subject}
                      onChange={(e) => setSubmissionData(prev => ({
                        ...prev,
                        subject: e.target.value
                      }))}
                    >
                      <option value="general">General</option>
                      <option value="math">Mathematics</option>
                      <option value="science">Science</option>
                      <option value="english">English/Language Arts</option>
                      <option value="history">History/Social Studies</option>
                      <option value="coding">Programming/Computer Science</option>
                      <option value="art">Art/Creative</option>
                      <option value="other">Other</option>
                    </select>
                  </div>

                  <div className="form-group">
                    <label htmlFor="gradeLevel">Grade Level</label>
                    <select
                      id="gradeLevel"
                      value={submissionData.gradeLevel}
                      onChange={(e) => setSubmissionData(prev => ({
                        ...prev,
                        gradeLevel: e.target.value
                      }))}
                    >
                      <option value="elementary">Elementary (K-5)</option>
                      <option value="middle">Middle School (6-8)</option>
                      <option value="high">High School (9-12)</option>
                      <option value="university">University/College</option>
                    </select>
                  </div>
                </div>

                {/* Council Selection */}
                <div className="council-selection">
                  <h3>Select Your Advisory Council</h3>
                  <p>Choose which teaching archetypes will review your work:</p>
                  
                  <div className="archetype-grid">
                    {Object.entries({
                      mentor: 'Mentor Teacher',
                      analyst: 'Analyst Teacher', 
                      constructivist: 'Constructivist Teacher',
                      socratic: 'Socratic Teacher',
                      storyteller: 'Storyteller Teacher',
                      challenger: 'Challenger Teacher',
                      synthesizer: 'Synthesizer Teacher'
                    }).map(([key, name]) => {
                      const config = getArchetypeConfig(key);
                      return (
                        <label 
                          key={key}
                          className={`archetype-option ${activeArchetypes.includes(key) ? 'selected' : ''}`}
                        >
                          <input
                            type="checkbox"
                            checked={activeArchetypes.includes(key)}
                            onChange={(e) => {
                              if (e.target.checked) {
                                setActiveArchetypes(prev => [...prev, key]);
                              } else {
                                setActiveArchetypes(prev => prev.filter(a => a !== key));
                              }
                            }}
                          />
                          <div className="archetype-card">
                            <span className="archetype-emoji">{config?.emoji}</span>
                            <span className="archetype-name">{name}</span>
                          </div>
                        </label>
                      );
                    })}
                  </div>
                </div>

                {/* Submit Button */}
                <button 
                  type="submit" 
                  className="submit-btn"
                  disabled={isSubmitting || activeArchetypes.length === 0}
                >
                  {isSubmitting ? (
                    <>
                      <Clock className="btn-icon spinning" />
                      Assembling Council...
                    </>
                  ) : (
                    <>
                      <Send className="btn-icon" />
                      Submit for Council Review
                    </>
                  )}
                </button>
              </form>
            </motion.div>
          )}
        </AnimatePresence>

        {/* Phase 2 & 3: Council & Synthesis */}
        <AnimatePresence>
          {showCouncilProcess && (
            <motion.div
              className="council-process"
              initial={{ opacity: 0, y: 30 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -30 }}
              transition={{ duration: 0.6 }}
            >
              <div className="council-header">
                <h2>
                  <Users className="header-icon" />
                  Educational Council in Session
                </h2>
                <p>Your selected teaching archetypes are analyzing your work from multiple perspectives.</p>
              </div>

              {/* Council Members */}
              <div className="council-members">
                {activeArchetypes.map(archetype => (
                  <CouncilMember
                    key={archetype}
                    archetype={archetype}
                    stages={councilFeedback[archetype] || []}
                    isActive={spiralPhase === 'council'}
                    showThinking={true}
                    onFeedback={(feedback) => {
                      console.log('Council feedback received:', feedback);
                    }}
                  />
                ))}
              </div>

              {/* Synthesis */}
              {spiralPhase === 'synthesis' && synthesizedFeedback && (
                <motion.div
                  className="synthesis-section"
                  initial={{ opacity: 0, scale: 0.95 }}
                  animate={{ opacity: 1, scale: 1 }}
                  transition={{ duration: 0.5 }}
                >
                  <h3>
                    <Brain className="section-icon" />
                    Council Synthesis
                  </h3>
                  <div className="synthesis-content">
                    {synthesizedFeedback}
                  </div>
                </motion.div>
              )}
            </motion.div>
          )}
        </AnimatePresence>

        {/* Phase 4: Rebirth - Results & Improvement Plan */}
        <AnimatePresence>
          {feedbackComplete && (
            <motion.div
              className="feedback-results"
              initial={{ opacity: 0, y: 30 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.7 }}
            >
              <div className="results-header">
                <h2>
                  <Sparkles className="header-icon" />
                  Your Learning Journey Forward
                </h2>
                <p>Based on the council's analysis, here's your personalized improvement plan.</p>
              </div>

              {/* Improvement Plan */}
              {improvementPlan.length > 0 && (
                <div className="improvement-plan">
                  <h3>Next Steps for Growth</h3>
                  <div className="improvement-steps">
                    {improvementPlan.map((step, index) => (
                      <motion.div
                        key={index}
                        className="improvement-step"
                        initial={{ opacity: 0, x: -20 }}
                        animate={{ opacity: 1, x: 0 }}
                        transition={{ delay: index * 0.1 }}
                      >
                        <div className="step-number">{index + 1}</div>
                        <div className="step-content">{step}</div>
                      </motion.div>
                    ))}
                  </div>
                </div>
              )}

              {/* Action Buttons */}
              <div className="result-actions">
                <button 
                  className="action-btn secondary"
                  onClick={() => setShowCouncilProcess(!showCouncilProcess)}
                >
                  <Eye className="btn-icon" />
                  {showCouncilProcess ? 'Hide' : 'Review'} Council Process
                </button>
                
                <button 
                  className="action-btn secondary"
                  onClick={() => {
                    // Export feedback as PDF or text
                    console.log('Export feedback');
                  }}
                >
                  <Download className="btn-icon" />
                  Export Feedback
                </button>
                
                <button 
                  className="action-btn primary"
                  onClick={resetSubmission}
                >
                  <RotateCcw className="btn-icon" />
                  Submit New Work
                </button>
              </div>
            </motion.div>
          )}
        </AnimatePresence>
      </div>
    </div>
  );
};

export default HomeworkSubmission;