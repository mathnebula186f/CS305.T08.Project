import { useState, useRef, useEffect } from "react";
import * as Device from 'expo-device';
import * as Notifications from 'expo-notifications';
import Constants from "expo-constants";
import { Platform } from "react-native";

export const usePushNotifications = () => {
    Notifications.setNotificationHandler({
        handleNotification: async () => ({
            shouldShowAlert: true,
            shouldPlaySound: true,
            shouldSetBadge: true,
        }),
    });

    const [expoPushToken, setExpoPushToken] = useState("");
    const [notification, setNotification] = useState(false);
    const notificationListener = useRef();
    const responseListener = useRef();
    const registerForPushNotificationsAsync = async () => {
        let token;
        if (Device.isDevice) {
            const { status: existingStatus } = await Notifications.getPermissionsAsync();
            let finalStatus = existingStatus;
            if (existingStatus !== "granted") {
                const { status } = await Notifications.requestPermissionsAsync();
                finalStatus = status;
            }
            if (finalStatus !== "granted") {
                alert("Failed to get push token for push notification!");
                return;
            }
            token = (await Notifications.getExpoPushTokenAsync({
                projectId: Constants.expoConfig?.extra?.eas.projectId,
            })).data;
            console.log('here:',token);
            if(Platform.OS === 'android') {
                Notifications.setNotificationChannelAsync('default', {
                    name: 'default',
                    importance: Notifications.AndroidImportance.MAX,
                    vibrationPattern: [0, 250, 250, 250],
                    lightColor: '#FF231F7C',
                });
            }
            return token;
        } else {
            alert("Must use physical device for Push Notifications");
        }
    }
    useEffect(()=>{
        registerForPushNotificationsAsync().then(token => setExpoPushToken(token));
        notificationListener.current = Notifications.addNotificationReceivedListener(notification => {
            setNotification(notification);
        });
        responseListener.current = Notifications.addNotificationResponseReceivedListener(response => {
            console.log(response);
        });
        return () => {

            Notifications.removeNotificationSubscription(notificationListener.current);
            Notifications.removeNotificationSubscription(responseListener.current);
        };
    
    })

    return {
        expoPushToken,
        notification,
    }
}