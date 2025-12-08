/**
 * Theme Configuration
 */

export const colors = {
  background: '#1A1A2E',
  surface: '#16213E',
  surfaceElevated: '#1F2B4B',
  textPrimary: '#FFFFFF',
  textSecondary: '#A0AEC0',
  textMuted: '#718096',
  primary: '#4A90D9',
  success: '#27AE60',
  warning: '#F39C12',
  danger: '#E74C3C',
  info: '#3498DB',
  task: '#4A90D9',
  person: '#9B59B6',
  project: '#27AE60',
  decision: '#E67E22',
  blocker: '#E74C3C',
  heatCold: '#3498DB',
  heatWarm: '#F39C12',
  heatHot: '#E74C3C',
};

export const spacing = {
  xs: 4,
  sm: 8,
  md: 16,
  lg: 24,
  xl: 32,
  xxl: 48,
};

export const borderRadius = {
  sm: 4,
  md: 8,
  lg: 16,
  xl: 24,
  full: 9999,
};

export const typography = {
  title: {
    fontSize: 24,
    fontWeight: '700' as const,
    color: colors.textPrimary,
  },
  subtitle: {
    fontSize: 18,
    fontWeight: '600' as const,
    color: colors.textPrimary,
  },
  body: {
    fontSize: 16,
    fontWeight: '400' as const,
    color: colors.textPrimary,
  },
  caption: {
    fontSize: 14,
    fontWeight: '400' as const,
    color: colors.textSecondary,
  },
  label: {
    fontSize: 12,
    fontWeight: '600' as const,
    color: colors.textMuted,
    textTransform: 'uppercase' as const,
    letterSpacing: 1,
  },
};
