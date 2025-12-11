/**
 * IntentToast Component
 * Shows which intent was triggered
 */

import React, { useEffect } from 'react';
import { StyleSheet, Text, View } from 'react-native';
import Animated, {
  useSharedValue,
  useAnimatedStyle,
  withTiming,
  withDelay,
  runOnJS,
  Easing,
} from 'react-native-reanimated';

import { Entity, entityTypeConfig } from '../entities/types';
import { GestureType, IntentAction } from '../gestures/gestureConfig';
import { colors, spacing, borderRadius, typography } from '../theme';

interface IntentToastProps {
  entity: Entity;
  intent: IntentAction;
  gesture: GestureType;
  onDismiss: () => void;
}

const gestureLabels: Record<GestureType, string> = {
  swipeRight: '→',
  swipeLeft: '←',
  swipeUp: '↑',
  swipeDown: '↓',
  longPress: '⏸',
  doubleTap: '⏺⏺',
};

export function IntentToast({ entity, intent, gesture, onDismiss }: IntentToastProps) {
  const opacity = useSharedValue(0);
  const translateY = useSharedValue(50);

  useEffect(() => {
    opacity.value = withTiming(1, { duration: 200, easing: Easing.out(Easing.cubic) });
    translateY.value = withTiming(0, { duration: 200, easing: Easing.out(Easing.cubic) });

    opacity.value = withDelay(
      2000,
      withTiming(0, { duration: 200 }, (finished) => {
        if (finished) {
          runOnJS(onDismiss)();
        }
      })
    );
    translateY.value = withDelay(2000, withTiming(50, { duration: 200 }));
  }, []);

  const animatedStyle = useAnimatedStyle(() => ({
    opacity: opacity.value,
    transform: [{ translateY: translateY.value }],
  }));

  const typeConfig = entityTypeConfig[entity.type];

  return (
    <Animated.View style={[styles.container, animatedStyle]}>
      <View style={[styles.toast, { borderLeftColor: intent.confirmColor }]}>
        <View style={styles.entityInfo}>
          <Text style={styles.entityIcon}>{typeConfig.icon}</Text>
          <Text style={styles.entityTitle} numberOfLines={1}>
            {entity.title}
          </Text>
        </View>
        <View style={styles.intentInfo}>
          <Text style={styles.gestureIndicator}>{gestureLabels[gesture]}</Text>
          <Text style={[styles.intentLabel, { color: intent.confirmColor }]}>
            {intent.label}
          </Text>
        </View>
        <Text style={styles.intentCode}>intent: {intent.intent}</Text>
      </View>
    </Animated.View>
  );
}

const styles = StyleSheet.create({
  container: {
    position: 'absolute',
    bottom: 100,
    left: spacing.lg,
    right: spacing.lg,
    alignItems: 'center',
  },
  toast: {
    backgroundColor: colors.surfaceElevated,
    borderRadius: borderRadius.lg,
    padding: spacing.md,
    borderLeftWidth: 4,
    width: '100%',
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 4 },
    shadowOpacity: 0.4,
    shadowRadius: 8,
    elevation: 8,
  },
  entityInfo: {
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: spacing.sm,
  },
  entityIcon: {
    fontSize: 18,
    marginRight: spacing.sm,
  },
  entityTitle: {
    ...typography.body,
    flex: 1,
    color: colors.textSecondary,
  },
  intentInfo: {
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: spacing.xs,
  },
  gestureIndicator: {
    fontSize: 20,
    marginRight: spacing.sm,
    color: colors.textMuted,
  },
  intentLabel: {
    ...typography.title,
  },
  intentCode: {
    ...typography.caption,
    color: colors.textMuted,
    fontFamily: 'monospace',
  },
});
