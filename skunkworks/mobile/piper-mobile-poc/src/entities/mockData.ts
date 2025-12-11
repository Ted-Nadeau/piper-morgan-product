/**
 * Mock Entity Data
 */

import { Entity } from './types';

export const mockEntities: Entity[] = [
  {
    id: '1',
    type: 'task',
    title: 'Review Q1 roadmap draft',
    subtitle: 'From: Sarah Chen',
    heat: 'warm',
    lifecycle: 'active',
  },
  {
    id: '2',
    type: 'decision',
    title: 'Approve vendor contract',
    subtitle: 'Legal cleared, awaiting PM sign-off',
    heat: 'hot',
    lifecycle: 'blocked',
  },
  {
    id: '3',
    type: 'person',
    title: 'Sarah Chen',
    subtitle: 'Waiting for response (2 days)',
    heat: 'warm',
    lifecycle: 'active',
  },
  {
    id: '4',
    type: 'project',
    title: 'Mobile 2.0 Initiative',
    subtitle: '67% complete · 12 open tasks',
    heat: 'cold',
    lifecycle: 'active',
  },
  {
    id: '5',
    type: 'blocker',
    title: 'API rate limiting unresolved',
    subtitle: 'Blocking: 3 tasks, 1 milestone',
    heat: 'hot',
    lifecycle: 'blocked',
  },
  {
    id: '6',
    type: 'task',
    title: 'Prepare board presentation',
    subtitle: 'Due: Tomorrow 9am',
    heat: 'hot',
    lifecycle: 'active',
  },
];
