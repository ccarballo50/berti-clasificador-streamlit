import React from 'react';
import { View, Text, StyleSheet, ProgressBarAndroid, TouchableOpacity } from 'react-native';

export default function DashboardScreen() {
  return (
    <View style={styles.container}>
      <Text style={styles.title}>¡Hola, César! 👋</Text>
      <Text style={styles.level}>🏆 Nivel 1 - Principiante</Text>

      <Text style={styles.progressText}>Días de vida ganados: 5</Text>
      <ProgressBarAndroid styleAttr="Horizontal" indeterminate={false} progress={0.25} />

      <TouchableOpacity style={styles.quickAction}>
        <Text style={styles.quickActionText}>➕ Registrar Progreso</Text>
      </TouchableOpacity>
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, padding: 24, backgroundColor: '#fff' },
  title: { fontSize: 24, fontWeight: 'bold', marginBottom: 10 },
  level: { fontSize: 18, marginBottom: 20 },
  progressText: { fontSize: 16, marginBottom: 10 },
  quickAction: { marginTop: 20, backgroundColor: '#007AFF', padding: 15, borderRadius: 10 },
  quickActionText: { color: '#fff', textAlign: 'center', fontWeight: 'bold' },
});
