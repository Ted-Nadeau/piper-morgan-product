/**
 * EntityCard Component
 * Touchable card with gesture handling
 */

import React, { useCallback } from 'react';
import { StyleSheet, Text, View, Dimensions } from 'react-native';
import { Gesture, GestureDetector } from 'react-native-gesture-handler';
import Animated, {
  useSharedValue,
  useAnimatedStyle,
  withSpring,
  interpolate,
  interpolateColor,
  runOnJS,
  Extrapolation,
} from 'react-native-reanimated';
import * as Haptics from 'expo-haptics';

import { Entity, entityTypeConfig, heatColors } from '../entities/types';
import {
  GestureType,
  gestureIntents,
  gestureThresholds,
  IntentAction,
} from '../gestures/gestureConfig';
import { colors, spacing, borderRadius, typography } from '../theme';

const { width: SCREEN_WIDTH } = Dimensions.get('window');
const CARD_WIDTH = SCREEN_WIDTH - spacing.lg * 2;

interface EntityCardProps {
  entity: Entity;
  onIntent: (entity: Entity, intent: IntentAction, gesture: GestureType) => void;
}

export function EntityCard({ entity, onIntent }: EntityCardProps) {
  const translateX = useSharedValue(0);
  const translateY = useSharedValue(0);
  const isPressed = useSharedValue(false);
  const hasHapticFired = useSharedValue(false);

  const typeConfig = entityTypeConfig[entity.type];
  const entityGestures = gestureIntents[entity.type];
  const { commitThreshold, warningThreshold } = gestureThresholds.swipe;

  const fireIntent = useCallback(
    (gestureType: GestureType) => {
      const intentAction = entityGestures[gestureType];
      if (intentAction) {
        Haptics.impactAsync(Haptics.ImpactFeedbackStyle.Medium);
        onIntent(entity, intentAction, gestureType);
      }
    },
    [entity, entityGestures, onIntent]
  );

  const fireWarningHaptic = useCallback(() => {
    Haptics.impactAsync(Haptics.ImpactFeedbackStyle.Light);
  }, []);

  const panGesture = Gesture.Pan()
    .onStart(() => {
      isPressed.value = true;
      hasHapticFired.value = false;
    })
    .onUpdate((event) => {
      translateX.value = event.translationX;
      translateY.value = event.translationY;

      const maxTranslation = Math.max(
        Math.abs(event.translationX),
        Math.abs(event.translationY)
      );
      if (maxTranslation > warningThreshold && !hasHapticFired.value) {
        hasHapticFired.value = true;
        runOnJS(fireWarningHaptic)();
      }
    })
    .onEnd((event) => {
      isPressed.value = false;
      const { translationX, translationY, velocityX, velocityY } = event;

      const absX = Math.abs(translationX);
      const absY = Math.abs(translationY);

      const velocityCommit =
        Math.abs(velocityX) > gestureThresholds.swipe.velocityThreshold ||
        Math.abs(velocityY) > gestureThresholds.swipe.velocityThreshold;

      if (absX > absY) {
        if (translationX > commitThreshold || (velocityCommit && velocityX > 0)) {
          runOnJS(fireIntent)('swipeRight');
        } else if (translationX < -commitThreshold || (velocityCommit && velocityX < 0)) {
          runOnJS(fireIntent)('swipeLeft');
        }
      } else {
        if (translationY < -commitThreshold || (velocityCommit && velocityY < 0)) {
          runOnJS(fireIntent)('swipeUp');
        } else if (translationY > commitThreshold || (velocityCommit && velocityY > 0)) {
          runOnJS(fireIntent)('swipeDown');
        }
      }

      translateX.value = withSpring(0, { damping: 15, stiffness: 150 });
      translateY.value = withSpring(0, { damping: 15, stiffness: 150 });
    });

  const longPressGesture = Gesture.LongPress()
    .minDuration(gestureThresholds.longPress.duration)
    .onStart(() => {
      runOnJS(Haptics.impactAsync)(Haptics.ImpactFeedbackStyle.Heavy);
      runOnJS(fireIntent)('longPress');
    });

  const composedGesture = Gesture.Simultaneous(panGesture, longPressGesture);

  const animatedCardStyle = useAnimatedStyle(() => {
    const rightProgress = interpolate(
      translateX.value,
      [0, commitThreshold],
      [0, 1],
      Extrapolation.CLAMP
    );
    const leftProgress = interpolate(
      translateX.value,
      [0, -commitThreshold],
      [0, 1],
      Extrapolation.CLAMP
    );
    const upProgress = interpolate(
      translateY.value,
      [0, -commitThreshold],
      [0, 1],
      Extrapolation.CLAMP
    );
    const downProgress = interpolate(
      translateY.value,
      [0, commitThreshold],
      [0, 1],
      Extrapolation.CLAMP
    );

    let intentProgress = Math.max(rightProgress, leftProgress, upProgress, downProgress);
    let intentColor = colors.surface;

    if (rightProgress === intentProgress && rightProgress > 0.3) {
      const action = entityGestures.swipeRight;
      intentColor = action?.confirmColor || colors.success;
    } else if (leftProgress === intentProgress && leftProgress > 0.3) {
      const action = entityGestures.swipeLeft;
      intentColor = action?.confirmColor || colors.danger;
    } else if (upProgress === intentProgress && upProgress > 0.3) {
      const action = entityGestures.swipeUp;
      intentColor = action?.confirmColor || colors.warning;
    } else if (downProgress === intentProgress && downProgress > 0.3) {
      const action = entityGestures.swipeDown;
      intentColor = action?.confirmColor || colors.info;
    }

    const backgroundColor = interpolateColor(
      intentProgress,
      [0, 0.3, 1],
      [colors.surface, colors.surface, intentColor]
    );

    return {
      transform: [
        { translateX: translateX.value },
        { translateY: translateY.value },
        { scale: isPressed.value ? 0.98 : 1 },
        { rotate: `${translateX.value / 20}deg` },
      ],
      backgroundColor,
      opacity: interpolate(intentProgress, [0, 1], [1, 0.9]),
    };
  });

  return (
    <GestureDetector gesture={composedGesture}>
      <Animated.View style={[styles.card, animatedCardStyle]}>
        <View style={[styles.heatBar, { backgroundColor: heatColors[entity.heat] }]} />
        <View style={styles.cardContent}>
          <View style={styles.headerRow}>
            <Text style={styles.typeIcon}>{typeConfig.icon}</Text>
            <Text style={[styles.typeLabel, { color: typeConfig.color }]}>
              {typeConfig.label}
            </Text>
            <View style={[styles.heatBadge, { backgroundColor: heatColors[entity.heat] }]}>
              <Text style={styles.heatText}>{entity.heat.toUpperCase()}</Text>
            </View>
          </View>
          <Text style={styles.title} numberOfLines={2}>
            {entity.title}
          </Text>
          {entity.subtitle && (
            <Text style={styles.subtitle} numberOfLines={1}>
              {entity.subtitle}
            </Text>
          )}
        </View>
      </Animated.View>
    </GestureDetector>
  );
}

const styles = StyleSheet.create({
  card: {
    width: CARD_WIDTH,
    backgroundColor: colors.surface,
    borderRadius: borderRadius.lg,
    marginVertical: spacing.sm,
    overflow: 'hidden',
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 4 },
    shadowOpacity: 0.3,
    shadowRadius: 8,
    elevation: 8,
  },
  heatBar: {
    height: 4,
    width: '100%',
  },
  cardContent: {
    padding: spacing.md,
  },
  headerRow: {
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: spacing.sm,
  },
  typeIcon: {
    fontSize: 20,
    marginRight: spacing.xs,
  },
  typeLabel: {
    ...typography.label,
    flex: 1,
  },
  heatBadge: {
    paddingHorizontal: spacing.sm,
    paddingVertical: spacing.xs / 2,
    borderRadius: borderRadius.sm,
  },
  heatText: {
    ...typography.label,
    color: colors.textPrimary,
    fontSize: 10,
  },
  title: {
    ...typography.subtitle,
    marginBottom: spacing.xs,
  },
  subtitle: {
    ...typography.caption,
  },
});
