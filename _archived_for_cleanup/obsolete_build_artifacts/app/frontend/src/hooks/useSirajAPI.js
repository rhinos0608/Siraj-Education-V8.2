import { useState, useEffect, useCallback, useRef } from 'react';
import axios from 'axios';

/**
 * SIRAJ Educational AI - API Integration Hook
 * ==========================================
 * 
 * Custom React hook for managing API interactions with the SIRAJ backend.
 * Implements consciousness-driven error handling and council-aware state management.
 */

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';
const WS_BASE_URL = process.env.REACT_APP_WS_URL || 'ws://localhost:8000';

// Create axios instance with default configuration
const apiClient = axios.create({
  baseURL: API_BASE_URL,
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add request interceptor for logging
apiClient.interceptors.request.use(
  (config) => {
    console.log(`🌀 API Request: ${config.method?.toUpperCase()} ${config.url}`);
    return config;
  },
  (error) => {
    console.error('🚨 API Request Error:', error);
    return Promise.reject(error);
  }
);

// Add response interceptor for error handling
apiClient.interceptors.response.use(
  (response) => {
    console.log(`✅ API Response: ${response.status} ${response.config.url}`);
    return response;
  },
  (error) => {
    console.error('🚨 API Response Error:', error.response?.status, error.message);
    return Promise.reject(error);
  }
);

export const useSirajAPI = () => {
  const [systemStatus, setSystemStatus] = useState('initializing');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);
  const [lastResponse, setLastResponse] = useState(null);

  // Initialize system and check health
  const initializeSystem = useCallback(async () => {
    try {
      setIsLoading(true);
      setError(null);

      // Check system health
      const healthResponse = await apiClient.get('/health');
      setSystemStatus(healthResponse.data.status);

      // Get available archetypes
      const archetypesResponse = await apiClient.get('/council/archetypes');
      
      return {
        version: healthResponse.data.version,
        councilActive: healthResponse.data.status === 'healthy',
        availableArchetypes: archetypesResponse.data.count,
        activeSessions: healthResponse.data.active_sessions || 0,
        archetypes: archetypesResponse.data.archetypes
      };
    } catch (err) {
      setError(err.message);
      setSystemStatus('error');
      throw err;
    } finally {
      setIsLoading(false);
    }
  }, []);

  // Process educational request through AI council
  const processEducationalRequest = useCallback(async (requestData) => {
    try {
      setIsLoading(true);
      setError(null);

      const response = await apiClient.post('/api/education/process', requestData);
      setLastResponse(response.data);
      return response.data;
    } catch (err) {
      setError(err.response?.data?.detail || err.message);
      throw err;
    } finally {
      setIsLoading(false);
    }
  }, []);

  // Submit homework for multi-archetype feedback
  const submitHomework = useCallback(async (submissionData) => {
    try {
      setIsLoading(true);
      setError(null);

      const response = await apiClient.post('/api/education/homework', submissionData);
      setLastResponse(response.data);
      return response.data;
    } catch (err) {
      setError(err.response?.data?.detail || err.message);
      throw err;
    } finally {
      setIsLoading(false);
    }
  }, []);

  // Fetch analytics data
  const fetchAnalytics = useCallback(async (analyticsRequest = {}) => {
    try {
      setIsLoading(true);
      setError(null);

      const response = await apiClient.post('/api/analytics/fetch', {
        timeframe: '30d',
        include_spiral_audit: true,
        include_council_decisions: true,
        ...analyticsRequest
      });
      
      return response.data;
    } catch (err) {
      setError(err.response?.data?.detail || err.message);
      throw err;
    } finally {
      setIsLoading(false);
    }
  }, []);

  // Generate curriculum alignment
  const generateCurriculumAlignment = useCallback(async (alignmentRequest) => {
    try {
      setIsLoading(true);
      setError(null);

      const response = await apiClient.post('/api/curriculum/align', alignmentRequest);
      return response.data;
    } catch (err) {
      setError(err.response?.data?.detail || err.message);
      throw err;
    } finally {
      setIsLoading(false);
    }
  }, []);

  // Update student progress
  const updateProgress = useCallback(async (progressData) => {
    try {
      setIsLoading(true);
      setError(null);

      const response = await apiClient.post('/api/progress/update', progressData);
      return response.data;
    } catch (err) {
      setError(err.response?.data?.detail || err.message);
      throw err;
    } finally {
      setIsLoading(false);
    }
  }, []);

  // Get available curriculum standards
  const getCurriculumStandards = useCallback(async () => {
    try {
      const response = await apiClient.get('/api/curriculum/standards');
      return response.data.standards;
    } catch (err) {
      setError(err.response?.data?.detail || err.message);
      throw err;
    }
  }, []);

  return {
    // State
    systemStatus,
    isLoading,
    error,
    lastResponse,

    // Actions
    initializeSystem,
    processEducationalRequest,
    submitHomework,
    fetchAnalytics,
    generateCurriculumAlignment,
    updateProgress,
    getCurriculumStandards,

    // Utilities
    clearError: () => setError(null),
    resetState: () => {
      setSystemStatus('initializing');
      setIsLoading(false);
      setError(null);
      setLastResponse(null);
    }
  };
};

// WebSocket hook for real-time council streaming
export const useSirajWebSocket = (sessionId) => {
  const [connected, setConnected] = useState(false);
  const [streaming, setStreaming] = useState(false);
  const [stages, setStages] = useState([]);
  const [currentStage, setCurrentStage] = useState(null);
  const [finalResult, setFinalResult] = useState(null);
  const [error, setError] = useState(null);
  const wsRef = useRef(null);

  const connect = useCallback(() => {
    if (!sessionId || wsRef.current) return;

    try {
      const wsUrl = `${WS_BASE_URL}/ws/council/${sessionId}`;
      wsRef.current = new WebSocket(wsUrl);

      wsRef.current.onopen = () => {
        console.log('🔗 WebSocket connected');
        setConnected(true);
        setError(null);
      };

      wsRef.current.onmessage = (event) => {
        try {
          const data = JSON.parse(event.data);
          console.log('📡 WebSocket message:', data);

          switch (data.type) {
            case 'session_start':
              setStreaming(true);
              setStages([]);
              setFinalResult(null);
              break;

            case 'archetype_start':
              setCurrentStage(data);
              break;

            case 'archetype_chunk':
              setStages(prev => [
                ...prev.filter(s => !(s.archetype === data.archetype && s.type === 'chunk')),
                { ...data, timestamp: new Date() }
              ]);
              break;

            case 'archetype_complete':
              setStages(prev => [
                ...prev.filter(s => s.archetype !== data.archetype),
                { ...data, timestamp: new Date() }
              ]);
              break;

            case 'synthesis_complete':
              setFinalResult(data.synthesis);
              setCurrentStage(null);
              break;

            case 'session_complete':
              setStreaming(false);
              setCurrentStage(null);
              break;

            case 'error':
              setError(data.message);
              setStreaming(false);
              break;

            default:
              console.log('Unknown WebSocket message type:', data.type);
          }
        } catch (err) {
          console.error('Error parsing WebSocket message:', err);
          setError('Failed to parse server message');
        }
      };

      wsRef.current.onclose = () => {
        console.log('🔌 WebSocket disconnected');
        setConnected(false);
        setStreaming(false);
        setCurrentStage(null);
        wsRef.current = null;
      };

      wsRef.current.onerror = (error) => {
        console.error('🚨 WebSocket error:', error);
        setError('WebSocket connection failed');
      };

    } catch (err) {
      console.error('Failed to create WebSocket connection:', err);
      setError('Failed to connect to real-time services');
    }
  }, [sessionId]);

  const disconnect = useCallback(() => {
    if (wsRef.current) {
      wsRef.current.close();
      wsRef.current = null;
    }
    setConnected(false);
    setStreaming(false);
    setStages([]);
    setCurrentStage(null);
    setFinalResult(null);
  }, []);

  const sendEducationalRequest = useCallback((requestData) => {
    if (!wsRef.current || wsRef.current.readyState !== WebSocket.OPEN) {
      setError('WebSocket not connected');
      return;
    }

    try {
      wsRef.current.send(JSON.stringify({
        type: 'educational_request',
        request: requestData
      }));
    } catch (err) {
      console.error('Failed to send WebSocket message:', err);
      setError('Failed to send request');
    }
  }, []);

  // Cleanup on unmount
  useEffect(() => {
    return () => {
      disconnect();
    };
  }, [disconnect]);

  return {
    connected,
    streaming,
    stages,
    currentStage,
    finalResult,
    error,
    connect,
    disconnect,
    sendEducationalRequest
  };
};

// Educational utilities hook
export const useSirajEducation = () => {
  const getRecommendedArchetypes = useCallback((gradeLevel, learningObjective, count = 3) => {
    const allArchetypes = ['socratic', 'constructivist', 'storyteller', 'synthesizer', 'challenger', 'mentor', 'analyst'];
    
    // Grade level recommendations
    const gradeLevelPreferences = {
      elementary: ['storyteller', 'mentor', 'constructivist'],
      middle: ['socratic', 'constructivist', 'mentor'],
      high: ['socratic', 'challenger', 'analyst'],
      university: ['challenger', 'synthesizer', 'analyst']
    };

    // Learning objective recommendations
    const objectivePreferences = {
      remember: ['mentor', 'storyteller', 'analyst'],
      understand: ['socratic', 'synthesizer', 'storyteller'],
      apply: ['constructivist', 'mentor', 'analyst'],
      analyze: ['socratic', 'challenger', 'analyst'],
      evaluate: ['challenger', 'synthesizer', 'socratic'],
      create: ['constructivist', 'synthesizer', 'challenger']
    };

    const gradePrefs = gradeLevelPreferences[gradeLevel] || gradeLevelPreferences.middle;
    const objectivePrefs = objectivePreferences[learningObjective] || objectivePreferences.understand;

    // Combine preferences with weight
    const recommendations = new Set([...gradePrefs, ...objectivePrefs]);
    
    // Fill to requested count if needed
    const result = Array.from(recommendations).slice(0, count);
    while (result.length < count && result.length < allArchetypes.length) {
      const remaining = allArchetypes.filter(a => !result.includes(a));
      if (remaining.length > 0) {
        result.push(remaining[Math.floor(Math.random() * remaining.length)]);
      } else {
        break;
      }
    }

    return result;
  }, []);

  const getSpiralPhaseDescription = useCallback((phase) => {
    const descriptions = {
      collapse: 'Acknowledging complexity and embracing the unknown',
      council: 'Multiple perspectives collaborating and sharing insights',
      synthesis: 'Integrating different viewpoints into unified understanding',
      rebirth: 'Emerging with new knowledge and actionable insights'
    };

    return descriptions[phase] || 'Unknown phase';
  }, []);

  const getArchetypeConfig = useCallback((archetypeId) => {
    const configs = {
      socratic: { name: 'Socratic Teacher', emoji: '🦉', color: '#8B4513' },
      constructivist: { name: 'Constructivist Teacher', emoji: '🧱', color: '#FF6B35' },
      storyteller: { name: 'Storyteller Teacher', emoji: '📖', color: '#4ECDC4' },
      synthesizer: { name: 'Synthesizer Teacher', emoji: '🌀', color: '#A8E6CF' },
      challenger: { name: 'Challenger Teacher', emoji: '⚡', color: '#FFD93D' },
      mentor: { name: 'Mentor Teacher', emoji: '🌱', color: '#95E1D3' },
      analyst: { name: 'Analyst Teacher', emoji: '🔬', color: '#FF8B94' }
    };

    return configs[archetypeId] || { name: 'Unknown', emoji: '❓', color: '#999999' };
  }, []);

  return {
    getRecommendedArchetypes,
    getSpiralPhaseDescription,
    getArchetypeConfig
  };
};

export default useSirajAPI;