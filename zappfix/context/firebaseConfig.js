// Import the functions you need from the SDKs you need
import { initializeApp } from "firebase/app";
import { getAnalytics } from "firebase/analytics";
import { getMessaging } from "firebase/messaging";
// TODO: Add SDKs for Firebase products that you want to use
// https://firebase.google.com/docs/web/setup#available-libraries

// Your web app's Firebase configuration
// For Firebase JS SDK v7.20.0 and later, measurementId is optional
const firebaseConfig = {
  apiKey: "AIzaSyDzFba7pnNer1QFmOPNFdcwZt1r6YsxaIs",
  authDomain: "handymanhive-ecf9c.firebaseapp.com",
  projectId: "handymanhive-ecf9c",
  storageBucket: "handymanhive-ecf9c.appspot.com",
  messagingSenderId: "1083876176600",
  appId: "1:1083876176600:web:ec51fb8f6c4364ca26ddad",
  measurementId: "G-3Y5KEC0BMD"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
const analytics = getAnalytics(app);
const messaging= getMessaging(app);