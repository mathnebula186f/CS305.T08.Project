import React from 'react';
import {createStackNavigator} from '@react-navigation/stack';

import Login from '../screens/Auth/Login';
import Signup from '../screens/Auth/Signup';

const Stack = createStackNavigator();

function AuthStack (){
    return (
      <Stack.Navigator screenOptions={{headerShown: false}} initialRouteName="Login" >
        <Stack.Screen name="Login" component={Login} />
        <Stack.Screen name="Signup" component={Signup} />
      </Stack.Navigator>
    );
}

export default AuthStack;