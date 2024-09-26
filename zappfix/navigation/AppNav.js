import React, { useContext } from 'react';
import { NavigationContainer } from "@react-navigation/native";

import AuthStack from "./AuthStack";
import AppStack from "./AppStack";
import AdminAppStack from "./AdminAppStack";
import WorkerAppStack from './WorkerAppStack';
import { AuthContext } from '../context/AuthContext';
import LoadingScreen from '../screens/Loading/LoadingScreen';



const AppNav = () => {
  const { isLoading, userToken, isWorker,isAdmin } = useContext(AuthContext);
  if (isLoading) {
    return (
      <LoadingScreen/>
    );
  }
  return (
    <NavigationContainer>
      {/* {userToken != null && isWorker=="True" ? <WorkerAppStack /> : (userToken != null ? <AppStack /> : <AuthStack />)} */}
      {
        userToken != null ? (
          isAdmin=="True" ? <AdminAppStack /> : (
            isWorker=="True" ? <WorkerAppStack /> : <AppStack />
          )
        ) : <AuthStack />
      }
    </NavigationContainer>
  );
}

export default AppNav;
