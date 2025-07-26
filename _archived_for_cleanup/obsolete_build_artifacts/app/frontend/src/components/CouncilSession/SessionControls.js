import React, { useState } from 'react';
import { motion } from 'framer-motion';
import {
  X,
  Settings,
  Users,
  Target,
  Zap,
  Eye,
  Clock,
  Globe,
  Volume2,
  Palette
} from 'lucide-react';
import { 
  EDUCATIONAL_ARCHETYPES,
  GRADE_LEVELS,
  LEARNING_OBJECTIVES,
  getCouncilColor,
  getCouncilAvatar,
  getCouncilName 
} from '../../utils/councilUtils';
import './SessionControls.css';

/**
 * SessionControls Component
 * ========================
 * 
 * Settings panel for customizing the AI council session.
 * Allows selection of archetypes, grade level, learning objectives, and other preferences.
 */

const SessionControls = ({
  settings,
  onSettingsChange,
  selectedArchetypes,
  onArchetypeToggle,
  onClose
}) => {
  const [activeTab, setActiveTab] = useState('archetypes');

  const handleSettingChange = (key, value) => {
    onSettingsChange(prev => ({
      ...prev,
      [key]: value
    }));
  };

  const tabs = [
    {
      id: 'archetypes',
      label: 'AI Teachers',
      icon: Users,
      description: 'Select your teaching council'
    },
    {
      id: 'learning',
      label: 'Learning',
      icon: Target,
      description: 'Set learning preferences'
    },
    {
      id: 'experience',
      label: 'Experience',
      icon: Palette,
      description: 'Customize your experience'
    }
  ];

  const renderArchetypesTab = () => (
    <div className="tab-content">
      <div className="section-header">
        <h3>Choose Your AI Teaching Council</h3>
        <p>Select the AI teachers you'd like to learn from. Each brings a unique teaching perspective.</p>
      </div>

      <div className="archetypes-grid">
        {Object.entries(EDUCATIONAL_ARCHETYPES).map(([id, config]) => {
          const isSelected = selectedArchetypes.includes(id);
          
          return (
            <motion.div
              key={id}
              className={`archetype-card ${isSelected ? 'selected' : ''}`}
              style={{ '--archetype-color': config.color }}
              onClick={() => onArchetypeToggle(id)}
              whileHover={{ scale: 1.02 }}
              whileTap={{ scale: 0.98 }}
            >
              <div className="archetype-header">
                <div className="archetype-avatar">
                  <span className="avatar-emoji">{config.emoji}</span>
                </div>
                <div className="archetype-info">
                  <h4>{config.name}</h4>
                  <p className="archetype-personality">{config.personality}</p>
                </div>
                <div className="selection-indicator">
                  {isSelected && <span className="checkmark">✓</span>}
                </div>
              </div>
              
              <div className="archetype-description">
                <p>{config.role}</p>
              </div>
              
              <div className="archetype-approach">
                <span className="approach-label">Approach:</span>
                <p>{config.approach}</p>
              </div>
              
              <div className="archetype-strengths">
                <span className="strengths-label">Strengths:</span>
                <div className="strengths-tags">
                  {config.strengths?.slice(0, 3).map((strength, index) => (
                    <span key={index} className="strength-tag">{strength}</span>
                  ))}
                </div>
              </div>
            </motion.div>
          );
        })}
      </div>

      <div className="selection-summary">
        <div className="selected-count">
          <Users className="count-icon" />
          <span>{selectedArchetypes.length} teachers selected</span>
        </div>
        <div className="selection-note">
          <p>💡 We recommend 3-5 teachers for a balanced learning experience.</p>
        </div>
      </div>
    </div>
  );

  const renderLearningTab = () => (
    <div className="tab-content">
      <div className="section-header">
        <h3>Learning Configuration</h3>
        <p>Customize the learning experience to match your needs and goals.</p>
      </div>

      <div className="settings-grid">
        {/* Grade Level */}
        <div className="setting-group">
          <label className="setting-label">
            <Globe className="setting-icon" />
            Grade Level
          </label>
          <select
            value={settings.gradeLevel}
            onChange={(e) => handleSettingChange('gradeLevel', e.target.value)}
            className="setting-select"
          >
            {Object.entries(GRADE_LEVELS).map(([key, level]) => (
              <option key={key} value={key}>{level.name}</option>
            ))}
          </select>
          <p className="setting-description">
            Adjusts language complexity and teaching approaches
          </p>
        </div>

        {/* Learning Objective */}
        <div className="setting-group">
          <label className="setting-label">
            <Target className="setting-icon" />
            Learning Objective
          </label>
          <select
            value={settings.learningObjective}
            onChange={(e) => handleSettingChange('learningObjective', e.target.value)}
            className="setting-select"
          >
            {Object.entries(LEARNING_OBJECTIVES).map(([key, objective]) => (
              <option key={key} value={key}>{objective.name}</option>
            ))}
          </select>
          <p className="setting-description">
            {LEARNING_OBJECTIVES[settings.learningObjective]?.description}
          </p>
        </div>

        {/* Session Preferences */}
        <div className="setting-group">
          <label className="setting-label">
            <Clock className="setting-icon" />
            Session Preferences
          </label>
          <div className="checkbox-group">
            <label className="checkbox-label">
              <input
                type="checkbox"
                checked={settings.streamingMode}
                onChange={(e) => handleSettingChange('streamingMode', e.target.checked)}
              />
              <span className="checkbox-text">Real-time streaming responses</span>
            </label>
            <label className="checkbox-label">
              <input
                type="checkbox"
                checked={settings.showThinking}
                onChange={(e) => handleSettingChange('showThinking', e.target.checked)}
              />
              <span className="checkbox-text">Show AI thinking process</span>
            </label>
            <label className="checkbox-label">
              <input
                type="checkbox"
                checked={settings.autoSpeak}
                onChange={(e) => handleSettingChange('autoSpeak', e.target.checked)}
              />
              <span className="checkbox-text">Auto-read responses aloud</span>
            </label>
          </div>
        </div>

        {/* Response Length */}
        <div className="setting-group">
          <label className="setting-label">
            <Eye className="setting-icon" />
            Response Style
          </label>
          <div className="radio-group">
            {[
              { value: 'concise', label: 'Concise', description: 'Brief, focused answers' },
              { value: 'detailed', label: 'Detailed', description: 'Comprehensive explanations' },
              { value: 'adaptive', label: 'Adaptive', description: 'Adjusts based on complexity' }
            ].map((option) => (
              <label key={option.value} className="radio-label">
                <input
                  type="radio"
                  name="responseStyle"
                  value={option.value}
                  checked={settings.responseStyle === option.value}
                  onChange={(e) => handleSettingChange('responseStyle', e.target.value)}
                />
                <span className="radio-text">
                  <strong>{option.label}</strong>
                  <span className="radio-description">{option.description}</span>
                </span>
              </label>
            ))}
          </div>
        </div>
      </div>
    </div>
  );

  const renderExperienceTab = () => (
    <div className="tab-content">
      <div className="section-header">
        <h3>Experience Preferences</h3>
        <p>Customize the interface and interaction style to suit your preferences.</p>
      </div>

      <div className="settings-grid">
        {/* Visual Preferences */}
        <div className="setting-group">
          <label className="setting-label">
            <Eye className="setting-icon" />
            Visual Preferences
          </label>
          <div className="checkbox-group">
            <label className="checkbox-label">
              <input
                type="checkbox"
                checked={settings.showAvatars}
                onChange={(e) => handleSettingChange('showAvatars', e.target.checked)}
              />
              <span className="checkbox-text">Show teacher avatars</span>
            </label>
            <label className="checkbox-label">
              <input
                type="checkbox"
                checked={settings.animationsEnabled}
                onChange={(e) => handleSettingChange('animationsEnabled', e.target.checked)}
              />
              <span className="checkbox-text">Enable animations</span>
            </label>
            <label className="checkbox-label">
              <input
                type="checkbox"
                checked={settings.compactMode}
                onChange={(e) => handleSettingChange('compactMode', e.target.checked)}
              />
              <span className="checkbox-text">Compact display mode</span>
            </label>
          </div>
        </div>

        {/* Audio Preferences */}
        <div className="setting-group">
          <label className="setting-label">
            <Volume2 className="setting-icon" />
            Audio Preferences
          </label>
          <div className="slider-group">
            <label className="slider-label">
              Speech Rate
              <input
                type="range"
                min="0.5"
                max="2"
                step="0.1"
                value={settings.speechRate || 1}
                onChange={(e) => handleSettingChange('speechRate', parseFloat(e.target.value))}
                className="setting-slider"
              />
              <span className="slider-value">{settings.speechRate || 1}x</span>
            </label>
          </div>
        </div>

        {/* Interaction Preferences */}
        <div className="setting-group">
          <label className="setting-label">
            <Zap className="setting-icon" />
            Interaction Style
          </label>
          <div className="radio-group">
            {[
              { value: 'formal', label: 'Formal', description: 'Professional, structured responses' },
              { value: 'casual', label: 'Casual', description: 'Friendly, conversational tone' },
              { value: 'encouraging', label: 'Encouraging', description: 'Supportive, motivational approach' }
            ].map((option) => (
              <label key={option.value} className="radio-label">
                <input
                  type="radio"
                  name="interactionStyle"
                  value={option.value}
                  checked={settings.interactionStyle === option.value}
                  onChange={(e) => handleSettingChange('interactionStyle', e.target.value)}
                />
                <span className="radio-text">
                  <strong>{option.label}</strong>
                  <span className="radio-description">{option.description}</span>
                </span>
              </label>
            ))}
          </div>
        </div>

        {/* Accessibility */}
        <div className="setting-group">
          <label className="setting-label">
            <Eye className="setting-icon" />
            Accessibility
          </label>
          <div className="checkbox-group">
            <label className="checkbox-label">
              <input
                type="checkbox"
                checked={settings.highContrast}
                onChange={(e) => handleSettingChange('highContrast', e.target.checked)}
              />
              <span className="checkbox-text">High contrast mode</span>
            </label>
            <label className="checkbox-label">
              <input
                type="checkbox"
                checked={settings.reduceMotion}
                onChange={(e) => handleSettingChange('reduceMotion', e.target.checked)}
              />
              <span className="checkbox-text">Reduce motion</span>
            </label>
            <label className="checkbox-label">
              <input
                type="checkbox"
                checked={settings.screenReaderOptimized}
                onChange={(e) => handleSettingChange('screenReaderOptimized', e.target.checked)}
              />
              <span className="checkbox-text">Screen reader optimized</span>
            </label>
          </div>
        </div>
      </div>
    </div>
  );

  return (
    <motion.div
      className="session-controls-overlay"
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      exit={{ opacity: 0 }}
      onClick={onClose}
    >
      <motion.div
        className="session-controls"
        initial={{ opacity: 0, scale: 0.95, y: 20 }}
        animate={{ opacity: 1, scale: 1, y: 0 }}
        exit={{ opacity: 0, scale: 0.95, y: 20 }}
        transition={{ duration: 0.3 }}
        onClick={(e) => e.stopPropagation()}
      >
        {/* Header */}
        <div className="controls-header">
          <div className="header-content">
            <Settings className="header-icon" />
            <div>
              <h2>Session Settings</h2>
              <p>Customize your AI learning experience</p>
            </div>
          </div>
          <button className="close-btn" onClick={onClose}>
            <X size={20} />
          </button>
        </div>

        {/* Tab Navigation */}
        <div className="tab-navigation">
          {tabs.map((tab) => {
            const Icon = tab.icon;
            return (
              <button
                key={tab.id}
                className={`tab-btn ${activeTab === tab.id ? 'active' : ''}`}
                onClick={() => setActiveTab(tab.id)}
              >
                <Icon size={18} />
                <span className="tab-label">{tab.label}</span>
              </button>
            );
          })}
        </div>

        {/* Tab Content */}
        <div className="tab-container">
          {activeTab === 'archetypes' && renderArchetypesTab()}
          {activeTab === 'learning' && renderLearningTab()}
          {activeTab === 'experience' && renderExperienceTab()}
        </div>

        {/* Footer */}
        <div className="controls-footer">
          <div className="footer-info">
            <p>Changes take effect immediately for new responses</p>
          </div>
          <div className="footer-actions">
            <button className="footer-btn secondary" onClick={onClose}>
              Done
            </button>
          </div>
        </div>
      </motion.div>
    </motion.div>
  );
};

export default SessionControls;