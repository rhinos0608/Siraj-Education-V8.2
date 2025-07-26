import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import {
  BookOpen,
  Calculator,
  Beaker,
  Globe,
  Palette,
  Music,
  Code,
  Heart,
  Lightbulb,
  Zap,
  ArrowRight
} from 'lucide-react';
import './TopicSuggestions.css';

/**
 * TopicSuggestions Component
 * =========================
 * 
 * Provides curated topic suggestions and example questions to help students
 * get started with their AI council sessions. Suggestions are tailored to
 * grade level and subject areas.
 */

const TopicSuggestions = ({ gradeLevel, onSuggestionSelect }) => {
  const [selectedCategory, setSelectedCategory] = useState('popular');
  const [suggestions, setSuggestions] = useState([]);

  // Subject categories with icons and colors
  const categories = {
    popular: {
      label: 'Popular Topics',
      icon: Zap,
      color: '#667eea',
      description: 'Most asked questions by students'
    },
    math: {
      label: 'Mathematics',
      icon: Calculator,
      color: '#f093fb',
      description: 'Numbers, equations, and problem solving'
    },
    science: {
      label: 'Science',
      icon: Beaker,
      color: '#4ecdc4',
      description: 'Explore the natural world'
    },
    english: {
      label: 'English & Literature',
      icon: BookOpen,
      color: '#ff6b6b',
      description: 'Language, writing, and stories'
    },
    history: {
      label: 'History & Social Studies',
      icon: Globe,
      color: '#a8e6cf',
      description: 'Past events and human societies'
    },
    arts: {
      label: 'Arts & Creativity',
      icon: Palette,
      color: '#ffd93d',
      description: 'Creative expression and design'
    },
    technology: {
      label: 'Technology & Coding',
      icon: Code,
      color: '#95e1d3',
      description: 'Digital world and programming'
    },
    life: {
      label: 'Life Skills',
      icon: Heart,
      color: '#ff8b94',
      description: 'Personal development and wellness'
    }
  };

  // Topic suggestions organized by category and grade level
  const topicData = {
    popular: {
      elementary: [
        {
          question: "Why do we need to sleep?",
          description: "Learn about the importance of sleep for your body and mind",
          archetypes: ['storyteller', 'mentor', 'analyst'],
          tags: ['health', 'science', 'daily life']
        },
        {
          question: "How do plants grow?",
          description: "Discover the amazing process of plant growth",
          archetypes: ['constructivist', 'storyteller', 'analyst'],
          tags: ['science', 'nature', 'biology']
        },
        {
          question: "What makes a good friend?",
          description: "Explore the qualities of friendship and relationships",
          archetypes: ['mentor', 'storyteller', 'socratic'],
          tags: ['social skills', 'emotions', 'relationships']
        }
      ],
      middle: [
        {
          question: "How does the internet work?",
          description: "Understand the technology that connects the world",
          archetypes: ['analyst', 'constructivist', 'storyteller'],
          tags: ['technology', 'communication', 'networks']
        },
        {
          question: "Why do we have different emotions?",
          description: "Explore the science and purpose of human emotions",
          archetypes: ['analyst', 'mentor', 'storyteller'],
          tags: ['psychology', 'emotions', 'human behavior']
        },
        {
          question: "What causes climate change?",
          description: "Learn about environmental changes and their impacts",
          archetypes: ['analyst', 'challenger', 'synthesizer'],
          tags: ['environment', 'science', 'current events']
        }
      ],
      high: [
        {
          question: "How can I choose the right career path?",
          description: "Get guidance on career exploration and decision-making",
          archetypes: ['mentor', 'socratic', 'synthesizer'],
          tags: ['career', 'planning', 'future']
        },
        {
          question: "What are the ethics of artificial intelligence?",
          description: "Explore the moral implications of AI technology",
          archetypes: ['socratic', 'challenger', 'synthesizer'],
          tags: ['ethics', 'technology', 'philosophy']
        },
        {
          question: "How do I write a compelling college essay?",
          description: "Master the art of persuasive and personal writing",
          archetypes: ['mentor', 'challenger', 'analyst'],
          tags: ['writing', 'college prep', 'communication']
        }
      ],
      university: [
        {
          question: "How can I develop critical thinking skills?",
          description: "Enhance your analytical and reasoning abilities",
          archetypes: ['socratic', 'challenger', 'analyst'],
          tags: ['critical thinking', 'analysis', 'skills']
        },
        {
          question: "What are the implications of quantum computing?",
          description: "Understand cutting-edge computing technology",
          archetypes: ['analyst', 'synthesizer', 'challenger'],
          tags: ['technology', 'computing', 'future']
        },
        {
          question: "How do I conduct effective research?",
          description: "Learn research methodologies and best practices",
          archetypes: ['analyst', 'mentor', 'synthesizer'],
          tags: ['research', 'methodology', 'academic skills']
        }
      ]
    },
    math: {
      elementary: [
        {
          question: "Why do we need to learn multiplication?",
          description: "Discover real-world uses of multiplication",
          archetypes: ['storyteller', 'constructivist', 'mentor'],
          tags: ['multiplication', 'practical math', 'everyday use']
        },
        {
          question: "What are fractions and how do I use them?",
          description: "Understand fractions through visual examples",
          archetypes: ['constructivist', 'analyst', 'storyteller'],
          tags: ['fractions', 'visual learning', 'practical math']
        }
      ],
      middle: [
        {
          question: "How is algebra used in real life?",
          description: "See algebra applications in everyday situations",
          archetypes: ['analyst', 'constructivist', 'storyteller'],
          tags: ['algebra', 'real-world applications', 'problem solving']
        },
        {
          question: "What is the Pythagorean theorem and why is it important?",
          description: "Explore this fundamental geometric principle",
          archetypes: ['analyst', 'constructivist', 'synthesizer'],
          tags: ['geometry', 'theorems', 'spatial reasoning']
        }
      ],
      high: [
        {
          question: "How does calculus help us understand change?",
          description: "Grasp the concepts and applications of calculus",
          archetypes: ['analyst', 'synthesizer', 'storyteller'],
          tags: ['calculus', 'change', 'advanced math']
        },
        {
          question: "What role does statistics play in decision making?",
          description: "Learn how data analysis guides important choices",
          archetypes: ['analyst', 'challenger', 'synthesizer'],
          tags: ['statistics', 'data analysis', 'decision making']
        }
      ],
      university: [
        {
          question: "How do mathematical proofs work?",
          description: "Master the art of mathematical reasoning",
          archetypes: ['socratic', 'analyst', 'challenger'],
          tags: ['proofs', 'logic', 'mathematical reasoning']
        }
      ]
    },
    science: {
      elementary: [
        {
          question: "What makes the sky blue?",
          description: "Learn about light and how we see colors",
          archetypes: ['storyteller', 'analyst', 'constructivist'],
          tags: ['physics', 'light', 'colors', 'atmosphere']
        },
        {
          question: "How do magnets work?",
          description: "Explore the invisible forces around us",
          archetypes: ['constructivist', 'analyst', 'storyteller'],
          tags: ['magnetism', 'forces', 'physics']
        }
      ],
      middle: [
        {
          question: "How do vaccines protect us from diseases?",
          description: "Understand the science of immunity and prevention",
          archetypes: ['analyst', 'storyteller', 'mentor'],
          tags: ['biology', 'health', 'immune system']
        },
        {
          question: "What happens when volcanoes erupt?",
          description: "Explore the powerful forces inside Earth",
          archetypes: ['storyteller', 'analyst', 'constructivist'],
          tags: ['geology', 'earth science', 'natural disasters']
        }
      ],
      high: [
        {
          question: "How does DNA determine our traits?",
          description: "Discover the blueprint of life",
          archetypes: ['analyst', 'synthesizer', 'storyteller'],
          tags: ['genetics', 'biology', 'heredity']
        },
        {
          question: "What is quantum mechanics and why does it matter?",
          description: "Explore the strange world of quantum physics",
          archetypes: ['analyst', 'challenger', 'synthesizer'],
          tags: ['physics', 'quantum mechanics', 'modern science']
        }
      ]
    }
    // Add more categories as needed
  };

  useEffect(() => {
    // Load suggestions based on selected category and grade level
    const categoryData = topicData[selectedCategory];
    if (categoryData && categoryData[gradeLevel]) {
      setSuggestions(categoryData[gradeLevel]);
    } else {
      // Fallback to popular topics for the grade level
      setSuggestions(topicData.popular[gradeLevel] || topicData.popular.middle);
    }
  }, [selectedCategory, gradeLevel]);

  const handleSuggestionClick = (suggestion) => {
    onSuggestionSelect({
      question: suggestion.question,
      archetypes: suggestion.archetypes,
      gradeLevel: gradeLevel
    });
  };

  return (
    <motion.div
      className="topic-suggestions"
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.6 }}
    >
      <div className="suggestions-header">
        <div className="header-content">
          <Lightbulb className="header-icon" />
          <div>
            <h2>Explore Topics</h2>
            <p>Get started with these curated questions and topics</p>
          </div>
        </div>
      </div>

      {/* Category Navigation */}
      <div className="category-nav">
        {Object.entries(categories).map(([key, category]) => {
          const Icon = category.icon;
          return (
            <button
              key={key}
              className={`category-btn ${selectedCategory === key ? 'active' : ''}`}
              onClick={() => setSelectedCategory(key)}
              style={{ '--category-color': category.color }}
            >
              <Icon size={18} />
              <span className="category-label">{category.label}</span>
            </button>
          );
        })}
      </div>

      {/* Category Description */}
      <div className="category-description">
        <p>{categories[selectedCategory]?.description}</p>
      </div>

      {/* Suggestions Grid */}
      <div className="suggestions-grid">
        {suggestions.map((suggestion, index) => (
          <motion.div
            key={index}
            className="suggestion-card"
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: index * 0.1 }}
            onClick={() => handleSuggestionClick(suggestion)}
            whileHover={{ y: -4, boxShadow: '0 8px 25px rgba(0,0,0,0.15)' }}
            whileTap={{ scale: 0.98 }}
          >
            <div className="suggestion-content">
              <h3 className="suggestion-question">{suggestion.question}</h3>
              <p className="suggestion-description">{suggestion.description}</p>
              
              <div className="suggestion-meta">
                <div className="suggestion-tags">
                  {suggestion.tags?.slice(0, 3).map((tag, tagIndex) => (
                    <span key={tagIndex} className="suggestion-tag">
                      {tag}
                    </span>
                  ))}
                </div>
                
                <div className="suggestion-teachers">
                  <span className="teachers-label">
                    {suggestion.archetypes?.length} teachers
                  </span>
                </div>
              </div>
            </div>
            
            <div className="suggestion-action">
              <ArrowRight size={16} />
            </div>
          </motion.div>
        ))}
      </div>

      {/* Custom Question Prompt */}
      <div className="custom-question-prompt">
        <div className="prompt-content">
          <h3>Have a different question?</h3>
          <p>Type your own question in the input below to get personalized help from your AI teaching council.</p>
        </div>
      </div>

      {/* Quick Tips */}
      <div className="quick-tips">
        <h4>💡 Tips for Better Responses</h4>
        <ul>
          <li>Be specific about what you want to learn</li>
          <li>Include context about your current understanding</li>
          <li>Ask follow-up questions to dive deeper</li>
          <li>Let the AI know if you prefer examples or explanations</li>
        </ul>
      </div>
    </motion.div>
  );
};

export default TopicSuggestions;