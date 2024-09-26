import AsyncStorage from "@react-native-async-storage/async-storage";
import { createContext, useEffect, useState } from "react";
import axios from "axios";
import { usePushNotifications } from "./pushNotifications";
export const AuthContext =createContext();

export const AuthProvider =({children}) => {
  const {expoPushToken, notification} = usePushNotifications();
    const [test,setTest]=useState('Test Value');
    const [isLoading,setIsLoading]=useState(false);
    const [userToken,setUserToken]=useState(null);
    const [isWorker,setIsWorker]=useState("");
    const [email,setEmail]=useState("");
    const [isAdmin,setIsAdmin]=useState("False");
    const [imageUri,setImageUri]=useState(null);
    const [user, setUser] = useState(null);
    const API = "http://192.168.218.130:8000";

    const logout= async ()=>{
        setIsLoading(true);
        await AsyncStorage.removeItem('userToken');
        await AsyncStorage.removeItem('isWorker');
      await AsyncStorage.removeItem('email');
      await AsyncStorage.removeItem('isAdmin');
      setIsAdmin("False");
        setUserToken(null);
        setIsWorker("");
        setIsLoading(false);
        setEmail("");
    }

    const verifyLoginOtp = async (email,otp,isAdmin1) =>{
        setIsLoading(true);
        try {
          if(isAdmin1){
            setIsWorker("True");
          }
          else{
            setIsWorker("False");
          }
            const response = await fetch(`${API}/verify_login_otp`, {
                method: 'POST',
                headers: {
                  'Content-Type': 'application/json',
                },
                credentials:"include",
                body: JSON.stringify({ 
                  email: email,
                  otp:otp,
                  isWorker:isWorker,
                  notification_id: expoPushToken
                 }),
              });
      
            const result = await response.json();
            console.log("here is the result",result);
          if (response.ok) {
            alert(result.message)
            setUserToken(result.token);
            setEmail(email);
            AsyncStorage.setItem('userToken', result.token);
            AsyncStorage.setItem('isWorker', isWorker);
            AsyncStorage.setItem('email', email);
            AsyncStorage.setItem("isAdmin", result.isAdmin);
            if (result.isAdmin == "True") {
              setIsAdmin("True");
            } 
              else { 
              setIsAdmin("False");
              } 
            }
            else{
              alert(result.error);
            }
          } catch (error) {
            alert(error);
          }
        
        setIsLoading(false);
    }
    const isLoggedIn = async ()=>{
        try{
            setIsLoading(true);
            const token=await AsyncStorage.getItem('userToken');
            const workerBool = await AsyncStorage.getItem('isWorker');
          const tempEmail = await AsyncStorage.getItem('email');
          const adminBool = await AsyncStorage.getItem('isAdmin');
          setIsAdmin(adminBool);
            setUserToken(token);
            setIsWorker(workerBool);
            setEmail(tempEmail);
            setIsLoading(false);
        }
        catch(e){
            alert("error",e);
        }
    }
    useEffect(()=>{
        isLoggedIn();
    },[]);


    const fetchUserData = async () => {
      try {
        // SetProgress(true);
        console.log("HELLO 1")
        const response = await fetch(`${API}/get_user_data`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          credentials: 'include',
          body: JSON.stringify({ isWorker: isWorker,email:email,token:userToken }),
        });
        const data = await response.json();
        console.log("HELLO 2")
        if (response.ok) {
          // data.worker_details.profile_pic = 'https://res.cloudinary.com/demo/image/upload/ar_1.0,c_thumb,g_face,w_0.6,z_0.7/r_max/co_black,e_outline/co_dimgrey,e_shadow,x_30,y_40/actor.png'
          setUser(data.worker_details);
          setImageUri(data.worker_details.profile_pic)
          console.log("data", data)
        } else {
          console.log("HELLO 3")
          console.error('Failed to fetch user data:', data.error);
          if(data.error == "Token expired"){
            alert(data.error);
            logout();
          }
        }
      } catch (error) {
        console.log("HELLO 4")
        console.error('Error fetching user data:', error);
      } finally {
        console.log("HELLO 5")
        
      }
      // SetProgress(false);
    };

    useEffect(()=>{
      if(isWorker && email && userToken){
        fetchUserData();
      }
    }
    ,[isWorker,email,userToken]);

    return (
        <AuthContext.Provider value={{logout,verifyLoginOtp,API,userToken,isLoading,test,setIsLoading,isWorker,setIsWorker,email,imageUri,setImageUri, user,isAdmin}}>
            {children}
        </AuthContext.Provider>
    );
}