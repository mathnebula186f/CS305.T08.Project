import React from 'react';
import AppNav from './navigation/AppNav';
import { AuthProvider } from './context/AuthContext';
// import { usePushNotifications } from './context/pushNotifications';


function App() {
  // const {expoPushToken, notification} = usePushNotifications();
  // const data=JSON.stringify(notification, undefined, 2);
  // console.log('data:',data, 'expoPushToken:',expoPushToken);
  return (
    <AuthProvider>
        <AppNav/>
    </AuthProvider>
    
  );
}


export default App;