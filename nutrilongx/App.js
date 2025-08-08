import React from 'react';
import { NavigationContainer } from '@react-navigation/native';
import { createBottomTabNavigator } from '@react-navigation/bottom-tabs';
import { Ionicons } from '@expo/vector-icons';

import DashboardScreen from './screens/DashboardScreen';
import RoutinesScreen from './screens/RoutinesScreen';
import ChallengesScreen from './screens/ChallengesScreen';
import StatsScreen from './screens/StatsScreen';
import VideosScreen from './screens/VideosScreen';

const Tab = createBottomTabNavigator();

export default function App() {
  return (
    <NavigationContainer>
      <Tab.Navigator
        screenOptions={({ route }) => ({
          tabBarIcon: ({ color, size }) => {
            const icons = {
              Dashboard: 'home',
              Rutinas: 'barbell',
              Retos: 'flag',
              Estadísticas: 'stats-chart',
              Videos: 'videocam',
            };
            return <Ionicons name={icons[route.name]} size={size} color={color} />;
          },
          tabBarActiveTintColor: '#007AFF',
          tabBarInactiveTintColor: 'gray',
        })}
      >
        <Tab.Screen name="Dashboard" component={DashboardScreen} />
        <Tab.Screen name="Rutinas" component={RoutinesScreen} />
        <Tab.Screen name="Retos" component={ChallengesScreen} />
        <Tab.Screen name="Estadísticas" component={StatsScreen} />
        <Tab.Screen name="Videos" component={VideosScreen} />
      </Tab.Navigator>
    </NavigationContainer>
  );
}
