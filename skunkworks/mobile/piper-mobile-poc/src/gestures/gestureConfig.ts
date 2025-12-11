/**
 * Gesture Configuration
 * Maps gesture types to intents based on entity type
 */

import { EntityType } from '../entities/types';

export type GestureType =
  | 'swipeRight'
  | 'swipeLeft'
  | 'swipeUp'
  | 'swipeDown'
  | 'longPress'
  | 'doubleTap';

export type IntentAction = {
  intent: string;
  label: string;
  confirmColor: string;
};

export type GestureIntentMap = {
  [G in GestureType]?: IntentAction;
};

export type EntityGestureConfig = {
  [K in EntityType]: GestureIntentMap;
};

export const gestureIntents: EntityGestureConfig = {
  task: {
    swipeRight: { intent: 'complete', label: 'Complete', confirmColor: '#27AE60' },
    swipeLeft: { intent: 'defer', label: 'Defer', confirmColor: '#95A5A6' },
    swipeUp: { intent: 'escalate', label: 'Escalate', confirmColor: '#E67E22' },
    swipeDown: { intent: 'delegate', label: 'Delegate', confirmColor: '#9B59B6' },
    longPress: { intent: 'showActions', label: 'Actions', confirmColor: '#3498DB' },
    doubleTap: { intent: 'quickView', label: 'Quick View', confirmColor: '#3498DB' },
  },
  decision: {
    swipeRight: { intent: 'approve', label: 'Approve', confirmColor: '#27AE60' },
    swipeLeft: { intent: 'decline', label: 'Decline', confirmColor: '#E74C3C' },
    swipeUp: { intent: 'needsMoreInfo', label: 'Need Info', confirmColor: '#F39C12' },
    longPress: { intent: 'showContext', label: 'Context', confirmColor: '#3498DB' },
  },
  person: {
    swipeRight: { intent: 'sendMessage', label: 'Message', confirmColor: '#3498DB' },
    swipeLeft: { intent: 'snooze', label: 'Snooze', confirmColor: '#95A5A6' },
    longPress: { intent: 'showRelationships', label: 'Relationships', confirmColor: '#9B59B6' },
    doubleTap: { intent: 'quickCall', label: 'Call', confirmColor: '#27AE60' },
  },
  project: {
    swipeRight: { intent: 'openDashboard', label: 'Dashboard', confirmColor: '#3498DB' },
    swipeLeft: { intent: 'archive', label: 'Archive', confirmColor: '#95A5A6' },
    swipeUp: { intent: 'addMilestone', label: 'Add Milestone', confirmColor: '#27AE60' },
    longPress: { intent: 'showTimeline', label: 'Timeline', confirmColor: '#9B59B6' },
  },
  blocker: {
    swipeRight: { intent: 'markResolved', label: 'Resolved', confirmColor: '#27AE60' },
    swipeLeft: { intent: 'escalate', label: 'Escalate', confirmColor: '#E74C3C' },
    longPress: { intent: 'showBlockedItems', label: 'Blocked Items', confirmColor: '#E67E22' },
  },
};

export const gestureThresholds = {
  swipe: {
    commitThreshold: 100,
    warningThreshold: 60,
    velocityThreshold: 500,
  },
  longPress: {
    duration: 500,
  },
  doubleTap: {
    maxDelay: 300,
  },
};

export function getIntentForGesture(
  entityType: EntityType,
  gesture: GestureType
): IntentAction | undefined {
  return gestureIntents[entityType][gesture];
}
