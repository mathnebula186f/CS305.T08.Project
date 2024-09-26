import * as React from "react";
import { createBottomTabNavigator } from '@react-navigation/bottom-tabs';
import { createStackNavigator } from '@react-navigation/stack';
import Ionicons from 'react-native-vector-icons/Ionicons';

import AdminHome from "../screens/Admin/AdminHome";
import HandleWorkersPage from "../screens/Admin/HandleWorkersPage";
import LoadingScreen from "../screens/Loading/LoadingScreen";
import AdminWorkerDetailPage from "../screens/Admin/AdminWorkerDetailPage";

const Tab = createBottomTabNavigator();
const Stack = createStackNavigator();

function HandleWorkersStack() {
  return (
    <Stack.Navigator screenOptions={{ headerShown: false }}>
      <Stack.Screen name="HandleWorkers" component={HandleWorkersPage} options={{ title: 'Worker Details' }}/>
      <Stack.Screen name="AdminWorkerDetail" component={AdminWorkerDetailPage} options={{ title: 'Worker Details' }} />
    </Stack.Navigator>
  );
}

export default function AdminAppStack() {
  const data = {
    num_workers: 10,
    num_verified_workers: 0,
    num_users: 100,
    num_completed_tasks: 50
  }
  return (
    <Tab.Navigator initialRouteName="AdminHome"
      screenOptions={({ route }) => ({
        tabBarIcon: ({ focused, color, size }) => {
          let iconName;

          if (route.name === 'Admin DashBoard') {
            iconName = 'person';
          } else if (route.name === 'Handle Workers') {
            iconName = 'hammer';
          }
          return <Ionicons name={iconName} size={size} color={color} />;
        }
      })}
    >
      <Tab.Screen name="Admin DashBoard" component={AdminHome} initialParams={{adminDetails: data}} />
      <Tab.Screen name="Handle Workers" component={HandleWorkersStack} />
      <Tab.Screen name="Loading" component={LoadingScreen} options={{ tabBarButton:()=>null }}/>
    </Tab.Navigator>
  );
}
