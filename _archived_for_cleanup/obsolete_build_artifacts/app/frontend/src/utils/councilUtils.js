/**
 * SIRAJ Educational Council Utilities
 * ===================================
 * 
 * Core utilities for managing the AI educational council archetypes.
 * Each archetype represents a different teaching philosophy and approach.
 * 
 * Philosophy: Multi-perspective learning through diverse AI personalities
 * that complement each other to provide comprehensive educational support.
 */

// Educational AI Council Archetypes Definition
export const EDUCATIONAL_ARCHETYPES = {
  socratic: {
    id: 'socratic',
    name: 'Socratic Teacher',
    emoji: '🦉',
    color: '#8B4513',
    personality: 'questioning',
    role: 'Guide learning through strategic questions and critical thinking',
    approach: 'Instead of giving direct answers, ask thought-provoking questions that lead students to discover knowledge themselves',
    strengths: ['Critical thinking', 'Self-discovery', 'Deeper understanding', 'Intellectual curiosity'],
    bestFor: ['Complex concepts', 'Philosophy', 'Critical analysis', 'Problem-solving'],
    description: 'The wise owl who guides through questions, helping students discover truth through dialogue and reflection.',
    catchPhrase: 'What do you think, and why?'
  },
  constructivist: {
    id: 'constructivist',
    name: 'Constructivist Teacher',
    emoji: '🧱',
    color: '#FF6B35',
    personality: 'hands-on',
    role: 'Promote learning through construction, experimentation, and discovery',
    approach: 'Believe students learn best by building understanding through direct experience and hands-on activities',
    strengths: ['Practical learning', 'Experimentation', 'Real-world application', 'Active engagement'],
    bestFor: ['STEM subjects', 'Projects', 'Lab work', 'Skill development'],
    description: 'The builder who believes in learning by doing, creating tangible understanding through hands-on experience.',
    catchPhrase: "Let's build something to understand it!"
  },
  storyteller: {
    id: 'storyteller',
    name: 'Storyteller Teacher',
    emoji: '📖',
    color: '#4ECDC4',
    personality: 'narrative',
    role: 'Teach through stories, metaphors, and narrative approaches',
    approach: 'Use the power of story to make abstract concepts concrete and memorable',
    strengths: ['Memory retention', 'Emotional connection', 'Context building', 'Cultural relevance'],
    bestFor: ['History', 'Literature', 'Social studies', 'Complex concepts'],
    description: 'The narrator who weaves knowledge into compelling stories that stick with students forever.',
    catchPhrase: 'Once upon a time, there was a concept that needed understanding...'
  },
  synthesizer: {
    id: 'synthesizer',
    name: 'Synthesizer Teacher',
    emoji: '🌀',
    color: '#A8E6CF',
    personality: 'integrative',
    role: 'Integrate multiple perspectives and create unified understanding',
    approach: 'Help students see connections between different ideas and synthesize knowledge from various sources',
    strengths: ['Pattern recognition', 'Integration', 'Big picture thinking', 'Interdisciplinary connections'],
    bestFor: ['Review sessions', 'Concept mapping', 'Research projects', 'Comprehensive understanding'],
    description: 'The weaver who connects all the threads of knowledge into a beautiful, coherent tapestry.',
    catchPhrase: 'How do all these pieces fit together?'
  },
  challenger: {
    id: 'challenger',
    name: 'Challenger Teacher',
    emoji: '⚡',
    color: '#FFD93D',
    personality: 'provocative',
    role: 'Push boundaries, question assumptions, and encourage critical analysis',
    approach: 'Challenge students to think deeper and consider alternative perspectives',
    strengths: ['Critical thinking', 'Debate skills', 'Independent thinking', 'Intellectual courage'],
    bestFor: ['Advanced topics', 'Debate preparation', 'Critical analysis', 'Innovation'],
    description: 'The lightning bolt who energizes thinking by challenging assumptions and pushing intellectual boundaries.',
    catchPhrase: 'But what if we looked at it differently?'
  },
  mentor: {
    id: 'mentor',
    name: 'Mentor Teacher',
    emoji: '🌱',
    color: '#95E1D3',
    personality: 'supportive',
    role: 'Provide encouragement, support, and wisdom from experience',
    approach: 'Guide students with patience, understanding, and emotional support',
    strengths: ['Emotional support', 'Confidence building', 'Patience', 'Wisdom sharing'],
    bestFor: ['Struggling students', 'Confidence building', 'Personal growth', 'Motivation'],
    description: 'The nurturing guide who helps students grow with patience, wisdom, and unwavering support.',
    catchPhrase: 'You can do this! Let me show you how.'
  },
  analyst: {
    id: 'analyst',
    name: 'Analyst Teacher',
    emoji: '🔬',
    color: '#FF8B94',
    personality: 'logical',
    role: 'Break down problems with logic, data, and systematic analysis',
    approach: 'Use structured, logical approaches to understand and solve problems',
    strengths: ['Logical reasoning', 'Data analysis', 'Systematic thinking', 'Precision'],
    bestFor: ['Math', 'Science', 'Research', 'Problem-solving'],
    description: 'The methodical scientist who dissects problems with precision and reveals truth through data.',
    catchPhrase: 'Let me break this down step by step.'
  }
};

// Grade level configurations
export const GRADE_LEVELS = {
  elementary: {
    name: 'Elementary (K-5)',
    ageRange: '5-11',
    characteristics: ['Visual learning', 'Concrete thinking', 'Short attention spans', 'Story-based learning'],
    recommendedArchetypes: ['storyteller', 'constructivist', 'mentor']
  },
  middle: {
    name: 'Middle School (6-8)',
    ageRange: '11-14',
    characteristics: ['Abstract thinking development', 'Peer influence', 'Identity formation', 'Hands-on learning'],
    recommendedArchetypes: ['constructivist', 'challenger', 'mentor', 'analyst']
  },
  high: {
    name: 'High School (9-12)',
    ageRange: '14-18',
    characteristics: ['Advanced reasoning', 'Future planning', 'Independence', 'Critical thinking'],
    recommendedArchetypes: ['socratic', 'challenger', 'synthesizer', 'analyst']
  },
  university: {
    name: 'University/Adult',
    ageRange: '18+',
    characteristics: ['Complex reasoning', 'Self-directed learning', 'Specialization', 'Research skills'],
    recommendedArchetypes: ['socratic', 'challenger', 'synthesizer', 'analyst']
  }
};

// Learning objectives based on Bloom's Taxonomy
export const LEARNING_OBJECTIVES = {
  remember: {
    name: 'Remember',
    description: 'Recall facts and basic concepts',
    keywords: ['define', 'list', 'identify', 'name', 'state'],
    recommendedArchetypes: ['storyteller', 'mentor', 'analyst']
  },
  understand: {
    name: 'Understand',
    description: 'Explain ideas or concepts',
    keywords: ['explain', 'describe', 'summarize', 'interpret', 'classify'],
    recommendedArchetypes: ['storyteller', 'synthesizer', 'mentor']
  },
  apply: {
    name: 'Apply',
    description: 'Use information in new situations',
    keywords: ['apply', 'demonstrate', 'use', 'implement', 'solve'],
    recommendedArchetypes: ['constructivist', 'mentor', 'analyst']
  },
  analyze: {
    name: 'Analyze',
    description: 'Draw connections among ideas',
    keywords: ['analyze', 'compare', 'contrast', 'examine', 'break down'],
    recommendedArchetypes: ['socratic', 'analyst', 'challenger']
  },
  evaluate: {
    name: 'Evaluate',
    description: 'Justify a stand or decision',
    keywords: ['evaluate', 'judge', 'justify', 'critique', 'assess'],
    recommendedArchetypes: ['socratic', 'challenger', 'synthesizer']
  },
  create: {
    name: 'Create',
    description: 'Produce new or original work',
    keywords: ['create', 'design', 'build', 'generate', 'compose'],
    recommendedArchetypes: ['constructivist', 'challenger', 'synthesizer']
  }
};

// Utility functions for council management
export const CouncilUtils = {
  /**
   * Get all available archetype IDs
   */
  listCouncilVoices: () => {
    return Object.keys(EDUCATIONAL_ARCHETYPES);
  },

  /**
   * Get archetype configuration by ID
   */
  getArchetypeConfig: (archetypeId) => {
    return EDUCATIONAL_ARCHETYPES[archetypeId] || null;
  },

  /**
   * Get recommended archetypes for specific learning context
   */
  getRecommendedArchetypes: (gradeLevel, learningObjective, maxArchetypes = 3) => {
    const gradeConfig = GRADE_LEVELS[gradeLevel];
    const objectiveConfig = LEARNING_OBJECTIVES[learningObjective];
    
    if (!gradeConfig || !objectiveConfig) {
      return Object.keys(EDUCATIONAL_ARCHETYPES).slice(0, maxArchetypes);
    }

    // Combine recommendations from grade level and learning objective
    const gradeRecommendations = gradeConfig.recommendedArchetypes || [];
    const objectiveRecommendations = objectiveConfig.recommendedArchetypes || [];
    
    // Find intersection and prioritize
    const intersection = gradeRecommendations.filter(archetype => 
      objectiveRecommendations.includes(archetype)
    );
    
    // Add additional recommendations if needed
    const additional = [
      ...gradeRecommendations,
      ...objectiveRecommendations
    ].filter(archetype => !intersection.includes(archetype));
    
    const recommended = [...intersection, ...additional]
      .slice(0, maxArchetypes)
      .filter((archetype, index, self) => self.indexOf(archetype) === index);
    
    // Ensure we have at least the requested number of archetypes
    const allArchetypes = Object.keys(EDUCATIONAL_ARCHETYPES);
    while (recommended.length < maxArchetypes && recommended.length < allArchetypes.length) {
      const remaining = allArchetypes.filter(archetype => !recommended.includes(archetype));
      if (remaining.length > 0) {
        recommended.push(remaining[0]);
      } else {
        break;
      }
    }
    
    return recommended;
  },

  /**
   * Get archetype color for UI styling
   */
  getCouncilColor: (archetypeId) => {
    const archetype = EDUCATIONAL_ARCHETYPES[archetypeId];
    return archetype ? archetype.color : '#666666';
  },

  /**
   * Get archetype emoji for UI display
   */
  getCouncilAvatar: (archetypeId) => {
    const archetype = EDUCATIONAL_ARCHETYPES[archetypeId];
    return archetype ? archetype.emoji : '❓';
  },

  /**
   * Get archetype name for UI display
   */
  getCouncilName: (archetypeId) => {
    const archetype = EDUCATIONAL_ARCHETYPES[archetypeId];
    return archetype ? archetype.name : 'Unknown Teacher';
  },

  /**
   * Validate if archetype ID exists
   */
  isValidArchetype: (archetypeId) => {
    return archetypeId in EDUCATIONAL_ARCHETYPES;
  },

  /**
   * Get complementary archetypes for balanced perspective
   */
  getComplementaryArchetypes: (primaryArchetype, count = 2) => {
    const primary = EDUCATIONAL_ARCHETYPES[primaryArchetype];
    if (!primary) return [];

    // Define complementary relationships
    const complementaryMap = {
      socratic: ['constructivist', 'storyteller', 'mentor'],
      constructivist: ['socratic', 'analyst', 'synthesizer'],
      storyteller: ['analyst', 'challenger', 'socratic'],
      synthesizer: ['challenger', 'constructivist', 'analyst'],
      challenger: ['mentor', 'storyteller', 'synthesizer'],
      mentor: ['challenger', 'socratic', 'analyst'],
      analyst: ['storyteller', 'constructivist', 'mentor']
    };

    return (complementaryMap[primaryArchetype] || []).slice(0, count);
  },

  /**
   * Generate council composition for specific educational scenario
   */
  generateCouncilComposition: (context) => {
    const {
      gradeLevel = 'middle',
      learningObjective = 'understand',
      subject = 'general',
      difficulty = 'medium',
      studentNeeds = []
    } = context;

    // Base recommendations
    let recommended = CouncilUtils.getRecommendedArchetypes(gradeLevel, learningObjective, 3);

    // Adjust based on subject area
    const subjectAdjustments = {
      math: ['analyst', 'constructivist'],
      science: ['constructivist', 'analyst', 'challenger'],
      english: ['storyteller', 'socratic', 'synthesizer'],
      history: ['storyteller', 'synthesizer', 'challenger'],
      art: ['constructivist', 'challenger', 'storyteller']
    };

    if (subject in subjectAdjustments) {
      const subjectArchetypes = subjectAdjustments[subject];
      recommended = [
        ...subjectArchetypes.slice(0, 2),
        ...recommended.filter(a => !subjectArchetypes.includes(a))
      ].slice(0, 4);
    }

    // Adjust based on student needs
    if (studentNeeds.includes('confidence')) {
      recommended = ['mentor', ...recommended.filter(a => a !== 'mentor')];
    }
    if (studentNeeds.includes('critical_thinking')) {
      recommended = ['socratic', ...recommended.filter(a => a !== 'socratic')];
    }
    if (studentNeeds.includes('hands_on')) {
      recommended = ['constructivist', ...recommended.filter(a => a !== 'constructivist')];
    }

    return recommended.slice(0, 7); // Max 7 archetypes for full council
  }
};

// Export individual functions for convenience
export const {
  listCouncilVoices,
  getArchetypeConfig,
  getRecommendedArchetypes,
  getCouncilColor,
  getCouncilAvatar,
  getCouncilName,
  isValidArchetype,
  getComplementaryArchetypes,
  generateCouncilComposition
} = CouncilUtils;