import React from 'react';
import { NavLink } from 'react-router-dom';

/**
 * SIRAJ Sidebar - Clean Notion-Inspired Navigation
 * 
 * Simple, focused sidebar with:
 * - Clear navigation structure
 * - High contrast text
 * - Minimal visual noise
 * - Essential information only
 */

const Sidebar = ({ 
  currentPhase = 'synthesis', 
  qwanMetrics, 
  isConnected = false 
}) => {

  // === NAVIGATION STRUCTURE ===
  const navigationItems = [
    {
      path: '/',
      name: 'Dashboard',
      icon: '🏠',
      description: 'Educational overview'
    },
    {
      path: '/council',
      name: 'Council Session',
      icon: '🏛️',
      description: 'Multi-archetype learning'
    },
    {
      path: '/analytics',
      name: 'Analytics',
      icon: '📊',
      description: 'Progress insights'
    }
  ];

  const archetypes = [
    { id: 'socratic', name: 'Socratic', emoji: '🦉', effectiveness: 87 },
    { id: 'constructivist', name: 'Builder', emoji: '🧱', effectiveness: 92 },
    { id: 'storyteller', name: 'Storyteller', emoji: '📖', effectiveness: 89 },
    { id: 'synthesizer', name: 'Synthesizer', emoji: '🌀', effectiveness: 94 },
    { id: 'mentor', name: 'Mentor', emoji: '🌱', effectiveness: 91 },
    { id: 'analyst', name: 'Analyst', emoji: '🔬', effectiveness: 85 },
    { id: 'challenger', name: 'Challenger', emoji: '⚡', effectiveness: 76 }
  ];

  const averageEffectiveness = Math.round(
    archetypes.reduce((sum, arch) => sum + arch.effectiveness, 0) / archetypes.length
  );

  return (
    <aside className="siraj-sidebar">
      {/* Sidebar Header */}
      <div className="sidebar-header">
        <div style={{ textAlign: 'center', marginBottom: 'var(--spacing-lg)' }}>
          <div className="logo-title">SIRAJ</div>
          <div className="logo-subtitle">Educational AI</div>
        </div>

        {/* System Status */}
        <div style={{ 
          backgroundColor: 'var(--color-bg-secondary)', 
          padding: 'var(--spacing-md)', 
          borderRadius: 'var(--radius-md)',
          marginBottom: 'var(--spacing-lg)'
        }}>
          <div style={{ 
            display: 'flex', 
            alignItems: 'center', 
            gap: 'var(--spacing-sm)',
            marginBottom: 'var(--spacing-sm)'
          }}>
            <span>{isConnected ? '🟢' : '🔴'}</span>
            <span style={{ fontSize: 'var(--font-size-sm)', color: 'var(--color-text-secondary)' }}>
              {isConnected ? 'Connected' : 'Offline'}
            </span>
          </div>
          <div style={{ 
            display: 'flex', 
            alignItems: 'center', 
            gap: 'var(--spacing-sm)'
          }}>
            <span>🌀</span>
            <span style={{ fontSize: 'var(--font-size-sm)', color: 'var(--color-text-secondary)' }}>
              Phase: {currentPhase.charAt(0).toUpperCase() + currentPhase.slice(1)}
            </span>
          </div>
        </div>
      </div>

      {/* Navigation Section */}
      <nav style={{ marginBottom: 'var(--spacing-xl)' }}>
        <div style={{ 
          fontSize: 'var(--font-size-xs)', 
          fontWeight: '600',
          color: 'var(--color-text-secondary)',
          textTransform: 'uppercase',
          letterSpacing: '0.5px',
          marginBottom: 'var(--spacing-md)'
        }}>
          Navigation
        </div>
        <ul className="nav-list">
          {navigationItems.map((item) => (
            <li key={item.path}>
              <NavLink 
                to={item.path}
                className={({ isActive }) => 
                  `nav-link ${isActive ? 'active' : ''}`
                }
              >
                <span className="nav-icon">{item.icon}</span>
                <div>
                  <div style={{ fontWeight: '500' }}>{item.name}</div>
                  <div style={{ 
                    fontSize: 'var(--font-size-xs)', 
                    color: 'var(--color-text-tertiary)' 
                  }}>
                    {item.description}
                  </div>
                </div>
              </NavLink>
            </li>
          ))}
        </ul>
      </nav>

      {/* AI Council Section */}
      <div style={{ marginBottom: 'var(--spacing-xl)' }}>
        <div style={{ 
          fontSize: 'var(--font-size-xs)', 
          fontWeight: '600',
          color: 'var(--color-text-secondary)',
          textTransform: 'uppercase',
          letterSpacing: '0.5px',
          marginBottom: 'var(--spacing-md)',
          display: 'flex',
          justifyContent: 'space-between',
          alignItems: 'center'
        }}>
          <span>AI Council</span>
          <span style={{ 
            backgroundColor: 'var(--color-success)', 
            color: 'white',
            padding: '2px 6px',
            borderRadius: '4px',
            fontSize: '10px'
          }}>
            {averageEffectiveness}%
          </span>
        </div>
        
        <div style={{ display: 'grid', gap: 'var(--spacing-sm)' }}>
          {archetypes.map((archetype) => (
            <div 
              key={archetype.id}
              style={{
                display: 'flex',
                alignItems: 'center',
                gap: 'var(--spacing-sm)',
                padding: 'var(--spacing-sm)',
                backgroundColor: 'var(--color-bg-secondary)',
                borderRadius: 'var(--radius-sm)',
                borderLeft: `3px solid var(--color-${archetype.id})`
              }}
            >
              <span style={{ fontSize: 'var(--font-size-md)' }}>{archetype.emoji}</span>
              <div style={{ flex: 1, minWidth: 0 }}>
                <div style={{ 
                  fontSize: 'var(--font-size-xs)', 
                  fontWeight: '500',
                  color: 'var(--color-text-primary)',
                  whiteSpace: 'nowrap',
                  overflow: 'hidden',
                  textOverflow: 'ellipsis'
                }}>
                  {archetype.name}
                </div>
                <div style={{ 
                  fontSize: '10px', 
                  color: 'var(--color-text-tertiary)' 
                }}>
                  {archetype.effectiveness}%
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* QWAN Metrics */}
      {qwanMetrics && (
        <div>
          <div style={{ 
            fontSize: 'var(--font-size-xs)', 
            fontWeight: '600',
            color: 'var(--color-text-secondary)',
            textTransform: 'uppercase',
            letterSpacing: '0.5px',
            marginBottom: 'var(--spacing-md)'
          }}>
            QWAN Metrics
          </div>
          
          <div style={{ display: 'grid', gap: 'var(--spacing-sm)' }}>
            {Object.entries(qwanMetrics).map(([key, value]) => (
              <div key={key} style={{ padding: 'var(--spacing-sm)' }}>
                <div style={{ 
                  display: 'flex', 
                  justifyContent: 'space-between', 
                  alignItems: 'center',
                  marginBottom: 'var(--spacing-xs)'
                }}>
                  <span style={{ 
                    fontSize: 'var(--font-size-xs)',
                    color: 'var(--color-text-primary)',
                    textTransform: 'capitalize'
                  }}>
                    {key}
                  </span>
                  <span style={{ 
                    fontSize: 'var(--font-size-xs)',
                    color: 'var(--color-text-secondary)'
                  }}>
                    {Math.round(value * 100)}%
                  </span>
                </div>
                <div style={{ 
                  height: '3px', 
                  backgroundColor: 'var(--color-bg-tertiary)', 
                  borderRadius: '2px',
                  overflow: 'hidden'
                }}>
                  <div 
                    style={{ 
                      height: '100%', 
                      backgroundColor: 'var(--color-primary)',
                      width: `${value * 100}%`,
                      transition: 'width 0.3s ease'
                    }}
                  />
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Footer */}
      <div style={{ 
        marginTop: 'auto',
        paddingTop: 'var(--spacing-lg)',
        textAlign: 'center'
      }}>
        <div style={{ 
          fontSize: '10px', 
          color: 'var(--color-text-tertiary)',
          fontStyle: 'italic',
          lineHeight: 1.4,
          marginBottom: 'var(--spacing-sm)'
        }}>
          "Education is the lighting of a fire, not the filling of a pail."
        </div>
        <div style={{ 
          fontSize: '10px', 
          color: 'var(--color-text-tertiary)' 
        }}>
          SIRAJ v8.1.0
        </div>
      </div>
    </aside>
  );
};

export default Sidebar;