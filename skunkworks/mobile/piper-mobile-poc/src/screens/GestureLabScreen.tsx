/**
 * GestureLabScreen
 * Main playground for gesture exploration
 */

import React, { useState, useCallback } from 'react';
import { StyleSheet, Text, View, ScrollView } from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';
import { GestureHandlerRootView } from 'react-native-gesture-handler';

import { Entity } from '../entities/types';
import { mockEntities } from '../entities/mockData';
import { GestureType, IntentAction } from '../gestures/gestureConfig';
import { EntityCard } from '../components/EntityCard';
import { IntentToast } from '../components/IntentToast';
import { colors, spacing, typography } from '../theme';

interface ToastData {
  id: string;
  entity: Entity;
  intent: IntentAction;
  gesture: GestureType;
}

export function GestureLabScreen() {
  const [toasts, setToasts] = useState<ToastData[]>([]);

  const handleIntent = useCallback(
    (entity: Entity, intent: IntentAction, gesture: GestureType) => {
      const toastId = `${entity.id}-${Date.now()}`;
      const newToast: ToastData = {
        id: toastId,
        entity,
        intent,
        gesture,
      };

      setToasts((prev) => [...prev, newToast]);
      console.log(
        `[Intent] ${entity.type}:${entity.title} → ${gesture} → ${intent.intent}`
      );
    },
    []
  );

  const dismissToast = useCallback((toastId: string) => {
    setToasts((prev) => prev.filter((t) => t.id !== toastId));
  }, []);

  return (
    <GestureHandlerRootView style={styles.gestureRoot}>
      <SafeAreaView style={styles.container} edges={['top']}>
        <View style={styles.header}>
          <Text style={styles.title}>Gesture Lab</Text>
          <Text style={styles.subtitle}>
            Swipe, hold, or double-tap cards to trigger intents
          </Text>
        </View>

        <View style={styles.legend}>
          <Text style={styles.legendItem}>→ Primary action</Text>
          <Text style={styles.legendItem}>← Secondary</Text>
          <Text style={styles.legendItem}>↑↓ Contextual</Text>
          <Text style={styles.legendItem}>Hold: Menu</Text>
        </View>

        <ScrollView
          style={styles.scrollView}
          contentContainerStyle={styles.scrollContent}
          showsVerticalScrollIndicator={false}
        >
          {mockEntities.map((entity) => (
            <EntityCard
              key={entity.id}
              entity={entity}
              onIntent={handleIntent}
            />
          ))}
          <View style={styles.bottomSpacer} />
        </ScrollView>

        {toasts.map((toast) => (
          <IntentToast
            key={toast.id}
            entity={toast.entity}
            intent={toast.intent}
            gesture={toast.gesture}
            onDismiss={() => dismissToast(toast.id)}
          />
        ))}
      </SafeAreaView>
    </GestureHandlerRootView>
  );
}

const styles = StyleSheet.create({
  gestureRoot: {
    flex: 1,
  },
  container: {
    flex: 1,
    backgroundColor: colors.background,
  },
  header: {
    paddingHorizontal: spacing.lg,
    paddingTop: spacing.md,
    paddingBottom: spacing.sm,
  },
  title: {
    ...typography.title,
    marginBottom: spacing.xs,
  },
  subtitle: {
    ...typography.caption,
  },
  legend: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    paddingHorizontal: spacing.lg,
    paddingBottom: spacing.md,
    gap: spacing.md,
  },
  legendItem: {
    ...typography.label,
    fontSize: 10,
    color: colors.textMuted,
  },
  scrollView: {
    flex: 1,
  },
  scrollContent: {
    paddingHorizontal: spacing.lg,
    alignItems: 'center',
  },
  bottomSpacer: {
    height: 120,
  },
});
