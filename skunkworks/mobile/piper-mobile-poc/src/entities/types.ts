/**
 * Entity Type Definitions
 * Core domain model for Piper Morgan entities
 */

export type EntityType = 'task' | 'person' | 'project' | 'decision' | 'blocker';

export type HeatLevel = 'cold' | 'warm' | 'hot';

export type LifecycleState = 'nascent' | 'active' | 'blocked' | 'resolved';

export interface Entity {
  id: string;
  type: EntityType;
  title: string;
  subtitle?: string;
  heat: HeatLevel;
  lifecycle: LifecycleState;
  relatedEntityIds?: string[];
}

/**
 * Visual configuration for entity types
 */
export const entityTypeConfig: Record<EntityType, {
  icon: string;
  color: string;
  label: string;
}> = {
  task: { icon: '☑️', color: '#4A90D9', label: 'Task' },
  person: { icon: '👤', color: '#9B59B6', label: 'Person' },
  project: { icon: '📁', color: '#27AE60', label: 'Project' },
  decision: { icon: '⚖️', color: '#E67E22', label: 'Decision' },
  blocker: { icon: '🚫', color: '#E74C3C', label: 'Blocker' },
};

/**
 * Heat level colors for visual feedback
 */
export const heatColors: Record<HeatLevel, string> = {
  cold: '#3498DB',
  warm: '#F39C12',
  hot: '#E74C3C',
};
