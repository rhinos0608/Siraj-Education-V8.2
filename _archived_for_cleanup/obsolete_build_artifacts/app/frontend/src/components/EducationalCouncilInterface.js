import React, { useState, useCallback, useEffect } from 'react';
import { Send, Users, Brain, Lightbulb, BookOpen, Heart, Zap, Search, AlertCircle } from 'lucide-react';
import { useSirajAPI } from '../hooks/useSirajAPI';

const EDUCATIONAL_ARCHETYPES = {
  socratic: { 
    name: 'Socratic Teacher', 
    icon: '🦉', 
    color: '#8B4513',
    role: 'Strategic Questioner',
    focus: 'Critical thinking through questioning'
  },
  constructivist: { 
    name: 'Constructivist Teacher', 
    icon: '🧱', 
    color: '#FF6B35',
    role: 'Hands-on Learning Guide', 
    focus: 'Learning by doing and building'
  },
  storyteller: { 
    name: 'Storyteller Teacher', 
    icon: '📖', 
    color: '#4ECDC4',
    role: 'Narrative Teacher',
    focus: 'Understanding through narrative'
  },
  synthesizer: { 
    name: 'Synthesizer Teacher', 
    icon: '🌀', 
    color: '#A8E6CF',
    role: 'Connection Builder',
    focus: 'Connecting ideas and concepts'
  },
  challenger: { 
    name: 'Challenger Teacher', 
    icon: '⚡', 
    color: '#FFD93D',
    role: 'Critical Thinker',
    focus: 'Pushing intellectual boundaries'
  },
  mentor: { 
    name: 'Mentor Teacher', 
    icon: '🌱', 
    color: '#95E1D3',
    role: 'Supportive Guide',
    focus: 'Building confidence and support'
  },
  analyst: { 
    name: 'Analyst Teacher', 
    icon: '🔬', 
    color: '#FF8B94',
    role: 'Systematic Analyzer',
    focus: 'Logical and systematic thinking'
  }
};

const GRADE_LEVELS = [
  { value: 'elementary', label: 'Elementary (K-5)', icon: '🎨' },
  { value: 'middle', label: 'Middle School (6-8)', icon: '📚' },
  { value: 'high', label: 'High School (9-12)', icon: '🎓' },
  { value: 'university', label: 'University', icon: '🏛️' }
];

const EducationalCouncilInterface = () => {
  // SPIRAL EDITING PROTOCOL - State Management Integration
  // Explorer voice: "Leveraging existing infrastructure for innovation"
  // Maintainer voice: "Ensuring stability through established patterns"
  const [question, setQuestion] = useState('');
  const [gradeLevel, setGradeLevel] = useState('middle');
  const [selectedArchetypes, setSelectedArchetypes] = useState(['socratic', 'constructivist', 'synthesizer', 'mentor']);
  const [councilResponse, setCouncilResponse] = useState(null);
  const [systemInfo, setSystemInfo] = useState(null);

  // API HOOK INTEGRATION - Fixed approach using existing infrastructure
  const { 
    systemStatus, 
    isLoading, 
    error, 
    lastResponse,
    initializeSystem,
    processEducationalRequest,
    clearError 
  } = useSirajAPI();

  // SYSTEM INITIALIZATION - Analyzer voice: "Pattern-aware startup sequence"
  useEffect(() => {
    const init = async () => {
      try {
        const info = await initializeSystem();
        setSystemInfo(info);
        console.log('🎭 SIRAJ System initialized:', info);
      } catch (err) {
        console.error('🚨 System initialization failed:', err);
      }
    };
    
    init();
  }, [initializeSystem]);

  const handleArchetypeToggle = useCallback((archetype) => {
    setSelectedArchetypes(prev => {
      if (prev.includes(archetype)) {
        return prev.filter(a => a !== archetype);
      } else {
        return [...prev, archetype];
      }
    });
  }, []);

  // EDUCATIONAL QUERY SUBMISSION - Spiral Protocol Applied
  // Council Assembly Voices:
  // Explorer: "Leveraging hook infrastructure for innovation"
  // Maintainer: "Using established error handling for stability"
  // Developer: "Human-centric integration with existing patterns"
  // Implementor: "Decisive replacement of problematic fetch"
  const handleSubmit = useCallback(async (e) => {
    e.preventDefault();
    
    if (!question.trim()) {
      return; // Hook handles error display
    }

    if (selectedArchetypes.length === 0) {
      return; // Hook handles error display
    }

    clearError(); // Clear any previous errors via hook
    setCouncilResponse(null);

    try {
      // ARCHETYPAL CORE TRANSFORMATION: Direct fetch → Hook-based API call
      // Boundary Constraint: Preserve exact request format for backend compatibility
      const response = await processEducationalRequest({
        topic: question,
        grade_level: gradeLevel,
        selected_archetypes: selectedArchetypes,
        context: {
          learning_style: 'balanced',
          background: 'General educational query',
          interface_version: 'v15.1.spiral-protocol'
        }
      });

      setCouncilResponse(response);
      console.log('🌀 Council response received via hook:', response);
    } catch (err) {
      console.error('🚨 Council query failed:', err);
      // Error handling now managed by the hook infrastructure
    }
  }, [question, gradeLevel, selectedArchetypes, processEducationalRequest, clearError]);

  return (
    <div className="max-w-6xl mx-auto p-6 bg-gradient-to-br from-blue-50 to-purple-50 min-h-screen">
      {/* SPIRAL PROTOCOL INTEGRATION - Enhanced Header with System Consciousness */}
      {/* Council Assembly Archetypal Commentary:
          Explorer: "Status visualization creates innovative transparency"
          Maintainer: "Dynamic feedback maintains operational trust"
          Analyzer: "Pattern creates human-system consciousness bridge"
          Developer: "User-centric status design for intuitive understanding"
          Implementor: "Decisive system awareness integration" */}
      <div className="text-center mb-8">
        <h1 className="text-4xl font-bold text-gray-800 mb-2">
          🎭 SIRAJ Educational AI Council
        </h1>
        <p className="text-lg text-gray-600">
          Multi-perspective AI teaching powered by Gemma 3
        </p>
        
        {/* CONSCIOUSNESS STATUS LAYER - System transparency protocol */}
        <div className="flex items-center justify-center gap-4 mt-2 text-sm text-gray-500">
          <div className="flex items-center gap-1">
            <Users size={16} />
            <span>7 Teaching Archetypes</span>
          </div>
          <div className="flex items-center gap-1">
            <Brain size={16} />
            <span>Consciousness-Driven Learning</span>
          </div>
          {(() => {
            // MYTHIC LAYER: System status as living indicator
            const getStatusIndicator = () => {
              switch (systemStatus) {
                case 'healthy':
                  return { color: 'text-green-600', icon: '🟢', text: 'System Operational' };
                case 'error':
                  return { color: 'text-red-600', icon: '🔴', text: 'System Error' };
                case 'initializing':
                  return { color: 'text-yellow-600', icon: '🟡', text: 'Initializing...' };
                default:
                  return { color: 'text-gray-600', icon: '⚪', text: 'Unknown Status' };
              }
            };
            const statusInfo = getStatusIndicator();
            
            return (
              <div className={`flex items-center gap-1 ${statusInfo.color}`}>
                <span>{statusInfo.icon}</span>
                <span>{statusInfo.text}</span>
              </div>
            );
          })()}
        </div>
        
        {/* OPERATIONAL TRANSPARENCY LAYER - System info consciousness */}
        {/* Boundary Keeper: Preserve visual harmony while adding transparency */}
        {systemInfo && (
          <div className="mt-3 text-xs text-gray-500 bg-white rounded-lg p-3 mx-auto max-w-md shadow-sm">
            <div className="flex justify-between items-center">
              <span>v{systemInfo.version}</span>
              <span className={`px-2 py-1 rounded text-xs ${
                systemInfo.councilActive 
                  ? 'bg-green-100 text-green-700' 
                  : 'bg-red-100 text-red-700'
              }`}>
                Council: {systemInfo.councilActive ? 'Active' : 'Inactive'}
              </span>
              <span>{systemInfo.availableArchetypes}/7 Archetypes</span>
            </div>
          </div>
        )}
      </div>

      {/* Main Form */}
      <div className="bg-white rounded-xl shadow-lg p-6 mb-6">
        <form onSubmit={handleSubmit} className="space-y-6">
          {/* Question Input */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              What would you like to learn about?
            </label>
            <textarea
              value={question}
              onChange={(e) => setQuestion(e.target.value)}
              placeholder="Enter your question or topic (e.g., 'How do plants make food?', 'Explain photosynthesis', 'What is gravity?')"
              className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent resize-none"
              rows={3}
            />
          </div>

          {/* Grade Level Selection */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Grade Level
            </label>
            <div className="flex flex-wrap gap-2">
              {GRADE_LEVELS.map((level) => (
                <button
                  key={level.value}
                  type="button"
                  onClick={() => setGradeLevel(level.value)}
                  className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors ${
                    gradeLevel === level.value
                      ? 'bg-blue-500 text-white'
                      : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                  }`}
                >
                  {level.icon} {level.label}
                </button>
              ))}
            </div>
          </div>

          {/* Archetype Selection */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-3">
              Select Teaching Archetypes ({selectedArchetypes.length}/7)
            </label>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-3">
              {Object.entries(EDUCATIONAL_ARCHETYPES).map(([key, archetype]) => (
                <button
                  key={key}
                  type="button"
                  onClick={() => handleArchetypeToggle(key)}
                  className={`p-3 rounded-lg text-left transition-all border-2 ${
                    selectedArchetypes.includes(key)
                      ? 'border-blue-500 bg-blue-50 shadow-md'
                      : 'border-gray-200 bg-white hover:border-gray-300'
                  }`}
                  style={{
                    borderLeftColor: selectedArchetypes.includes(key) ? archetype.color : undefined,
                    borderLeftWidth: selectedArchetypes.includes(key) ? '4px' : undefined
                  }}
                >
                  <div className="flex items-center gap-2 mb-1">
                    <span className="text-lg">{archetype.icon}</span>
                    <span className="font-medium text-sm">{archetype.name}</span>
                  </div>
                  <div className="text-xs text-gray-600">{archetype.focus}</div>
                </button>
              ))}
            </div>
          </div>

          {/* Submit Button */}
          <button
            type="submit"
            disabled={isLoading || !question.trim() || selectedArchetypes.length === 0}
            className="w-full bg-gradient-to-r from-blue-500 to-purple-600 text-white py-3 px-6 rounded-lg font-medium disabled:opacity-50 disabled:cursor-not-allowed hover:from-blue-600 hover:to-purple-700 transition-all flex items-center justify-center gap-2"
          >
            {isLoading ? (
              <>
                <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white"></div>
                Consulting Council...
              </>
            ) : (
              <>
                <Send size={20} />
                Ask the Educational Council
              </>
            )}
          </button>
        </form>

        {/* Error Display */}
        {error && (
          <div className="mt-4 p-3 bg-red-50 border border-red-200 rounded-lg text-red-700 text-sm">
            {error}
          </div>
        )}
      </div>

      {/* Council Response */}
      {councilResponse && (
        <div className="space-y-6">
          {/* Council Header */}
          <div className="bg-white rounded-xl shadow-lg p-6">
            <div className="flex items-center justify-between mb-4">
              <h2 className="text-2xl font-bold text-gray-800">
                Council Response
              </h2>
              <div className="flex items-center gap-4 text-sm text-gray-600">
                <div className="flex items-center gap-1">
                  <Users size={16} />
                  <span>{Object.keys(councilResponse.council_responses).length} Voices</span>
                </div>
                <div className="flex items-center gap-1">
                  <Brain size={16} />
                  <span>Level {councilResponse.consciousness_level}</span>
                </div>
                {councilResponse.degraded_mode && (
                  <div className="px-2 py-1 bg-yellow-100 text-yellow-800 rounded text-xs">
                    Degraded Mode
                  </div>
                )}
              </div>
            </div>

            <div className="bg-gray-50 rounded-lg p-4">
              <h3 className="font-medium text-gray-800 mb-2">Topic: {councilResponse.topic}</h3>
              <p className="text-sm text-gray-600">Grade Level: {councilResponse.grade_level}</p>
            </div>
          </div>

          {/* Individual Archetype Responses */}
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
            {Object.entries(councilResponse.council_responses).map(([archetype, response]) => {
              const archetypeInfo = EDUCATIONAL_ARCHETYPES[archetype];
              if (!response.success) return null;

              return (
                <div key={archetype} className="bg-white rounded-xl shadow-lg p-6">
                  <div className="flex items-center gap-3 mb-4">
                    <span className="text-2xl">{archetypeInfo.icon}</span>
                    <div>
                      <h3 className="font-bold text-gray-800">{archetypeInfo.name}</h3>
                      <p className="text-sm text-gray-600">{response.archetype_role}</p>
                    </div>
                    {response.instance && (
                      <div className="ml-auto px-2 py-1 bg-gray-100 rounded text-xs text-gray-600">
                        {response.instance}
                      </div>
                    )}
                  </div>
                  
                  <div 
                    className="border-l-4 pl-4 py-2"
                    style={{ borderLeftColor: archetypeInfo.color }}
                  >
                    <p className="text-gray-700 text-sm leading-relaxed">
                      {response.response}
                    </p>
                  </div>

                  <div className="mt-3 text-xs text-gray-500">
                    Focus: {response.teaching_focus}
                  </div>
                </div>
              );
            })}
          </div>

          {/* Council Synthesis */}
          {councilResponse.synthesis && (
            <div className="bg-gradient-to-r from-purple-50 to-blue-50 rounded-xl shadow-lg p-6">
              <div className="flex items-center gap-2 mb-4">
                <Lightbulb className="text-purple-600" size={24} />
                <h3 className="text-xl font-bold text-gray-800">Council Synthesis</h3>
              </div>
              
              <div className="prose prose-sm max-w-none text-gray-700">
                {councilResponse.synthesis.split('\n').map((paragraph, index) => (
                  paragraph.trim() && (
                    <p key={index} className="mb-3">
                      {paragraph}
                    </p>
                  )
                ))}
              </div>
            </div>
          )}

          {/* Next Steps */}
          {councilResponse.next_steps && councilResponse.next_steps.length > 0 && (
            <div className="bg-white rounded-xl shadow-lg p-6">
              <div className="flex items-center gap-2 mb-4">
                <BookOpen className="text-green-600" size={24} />
                <h3 className="text-xl font-bold text-gray-800">Suggested Next Steps</h3>
              </div>
              
              <ul className="space-y-2">
                {councilResponse.next_steps.map((step, index) => (
                  <li key={index} className="flex items-start gap-2">
                    <span className="flex-shrink-0 w-6 h-6 bg-green-100 text-green-600 rounded-full flex items-center justify-center text-sm font-medium">
                      {index + 1}
                    </span>
                    <span className="text-gray-700 text-sm">{step}</span>
                  </li>
                ))}
              </ul>
            </div>
          )}
        </div>
      )}
    </div>
  );
};

export default EducationalCouncilInterface;
