/**
 * Piper Morgan Mobile PoC
 */

import React from 'react';
import { StatusBar } from 'expo-status-bar';
import { SafeAreaProvider } from 'react-native-safe-area-context';

import { GestureLabScreen } from './src/screens/GestureLabScreen';

export default function App() {
  return (
    <SafeAreaProvider>
      <StatusBar style="light" />
      <GestureLabScreen />
    </SafeAreaProvider>
  );
}
