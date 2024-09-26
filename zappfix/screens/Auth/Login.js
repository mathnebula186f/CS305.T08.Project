import { StatusBar } from "expo-status-bar";
import React, { useContext, useState } from "react";
import { StyleSheet, Text, TextInput, View, TouchableOpacity } from "react-native";
import {
  Input,
  NativeBaseProvider,
  Button,
  Icon,
  Box,
  Image,
  AspectRatio,
} from "native-base";
import { FontAwesome5 } from "@expo/vector-icons";
import { useNavigation } from "@react-navigation/native";

import { AuthContext } from "../../context/AuthContext";
import LoadingScreen from "../Loading/LoadingScreen";

function ToggleButton({ label, active, onPress }) {
  return (
    <TouchableOpacity
      onPress={onPress}
      style={[styles.toggleButton, active && styles.activeButton]}
    >
      <Text
        style={[styles.toggleButtonText, active && styles.activeButtonText]}
      >
        {label}
      </Text>
    </TouchableOpacity>
  );
}

function Login() {
  const navigation = useNavigation();
  const { API, verifyLoginOtp, setIsLoading, isWorker, setIsWorker } =
    useContext(AuthContext);
  const [email, setEmail] = React.useState("");
  const [emailError, setEmailError] = React.useState("");
  const [isOtpSent, setIsOtpSent] = React.useState(0);
  // const [otp, setOtp] = React.useState("");
  const [otp, setOtp] = useState(["", "", "", "", "", ""]);
  const [isAdmin1, setIsAdmin1] = React.useState(false); // Default to user
  const [progress, setProgress] = React.useState(false);
  const inputsarray = [];
  const [indexbutton,setindexbutton] = React.useState(0) ;
  const isEmailValid = (email) => {
    // You can implement your email validation logic here
    const emailPattern = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
    return emailPattern.test(email);
  };

  const handleUserToggle = () => {
    setIsAdmin1(false);
    setIsWorker("False");
  };
  const handleWorkerToggle = () => {
    setIsAdmin1(true);
    setIsWorker("True");
  };
  const sendOtp = async () => {
    try {
      // Send a POST request to the backend with the user's information
      setProgress(true);
      if (isAdmin1) {
        await setIsWorker("True");
      } else {
        await setIsWorker("False");
      }
      console.log(email, isAdmin1);
      const response = await fetch(`${API}/user_login`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ email: email, isWorker: isWorker }),
      });

      const result = await response.json();

      // Handle the response from the backend
      console.log("Response:", response.data);

      // Check if the OTP needs to be sent
      if (response.ok) {
        setIsOtpSent(1);
        console.log("OTP sent successfully");
        alert("OTP sent successfully");
      } else {
        alert("Failed to send OTP user not found");
        // Handle the case where OTP sending fails
      }
    } catch (error) {
      console.error("Error signing up:", error);
      alert(error);
      // Handle errors from the backend
    }
    setProgress(false);
  };

    // Function to get the masked email
    const getMaskedEmail = () => {
      // Check if email has at least 3 characters
      if (email.length >= 6) {
        // Extract first 3 characters of email and add stars for the rest
        return email.substring(0, 6) + '*'.repeat(email.length - 6);
      } else {
        // If email has less than 3 characters, return the original email
        return email;
      }
    };

  const handleVerifyOTP = async () => {
    const otpString = otp.join('');
    try {
      setProgress(true);
      await verifyLoginOtp(email, otpString, isAdmin1);
    } catch (error) {
      console.error("Error verifying OTP:", error);
      // Handle error if needed
    }
    setProgress(false);
  };

  // Handle the 6 box otp menu
  const handleOtpChange = (value, index) => {
    const newOtp = [...otp];
    newOtp[index] = value;
    setindexbutton(index);
    console.log("indexbutton",indexbutton);
    setOtp(newOtp);
    // Move focus to the next box if the current one has a value
    if (value && index < newOtp.length - 1) {
      inputsarray[index + 1]?.focus(); // Using optional chaining to avoid errors if inputs[index + 1] is undefined
    }
  };
  const handleKeyPress = (event, index) => {
    // If backspace is pressed and the current box is empty,
    // move focus to the previous box
    setindexbutton(index);
    if (event.nativeEvent.key === "Backspace" && index > 0 && !otp[index]) {
      inputsarray[index - 1]?.focus();
    }
  };

  return (
    <View style={styles.container}>
      {progress ? (
        <LoadingScreen />
      ) : isOtpSent ? (
        <View>
          <View style={styles.Middle}>
            <Text style={styles.LoginText}>VERIFY OTP</Text>
          </View>
          <View style={styles.text2}>
            <Text> Current Email : {getMaskedEmail()}</Text>
            <TouchableOpacity onPress={() => navigation.navigate("Signup")}>
              <Text style={styles.signupText}> Login Page</Text>
            </TouchableOpacity>
          </View>
          <View style={styles.buttonStyleX}>
            <View style={styles.containerbox}>
              {otp.map((digit, index) => (
                <TextInput
                  key={index}
                  style={styles.box}
                  maxLength={1}
                  keyboardType="numeric"
                  onChangeText={(value) => handleOtpChange(value, index)}
                  onKeyPress={(event) => handleKeyPress(event, index)}
                  value={digit}
                  ref={(input) => {
                    inputsarray[index] = input;
                    console.log("input: ", otp);
                  }}
                />
              ))}
            </View>
          </View>
          <View style={styles.buttonStyle}>
            <Button
              style={styles.buttonDesign}
              onPress={handleVerifyOTP}
              disabled={indexbutton < 5}
            >
              VERIFY OTP
            </Button>
          </View>
          <View style={styles.text2}>
            <Text> Want to change the email? </Text>
            <TouchableOpacity onPress={() => setIsOtpSent(false)}>
              <Text style={styles.signupText}> Login Page</Text>
            </TouchableOpacity>
          </View>
        </View>
      ) : (
        <View>
          <View style={styles.login}>
            <Image
              style={styles.image}
              source={require("../../assets/icon.png")}
            />
          </View>
          <View style={styles.Middle}>
            <Text style={styles.LoginText}>Login as</Text>
          </View>
          {/* Toggle button for user type */}
          <View style={styles.toggleContainer}>
            <ToggleButton
              label="User"
              active={!isAdmin1}
              onPress={handleUserToggle}
            />
            <Text style={styles.orText}> OR </Text>
            <ToggleButton
              label="Worker"
              active={isAdmin1}
              onPress={handleWorkerToggle}
            />
          </View>

          {/* Username or Email Input Field */}
          <View style={styles.buttonStyle}>
            <View style={styles.emailInput}>
              <Input
                InputLeftElement={
                  <Icon
                    as={<FontAwesome5 name="user-secret" />}
                    size="sm"
                    m={2}
                    _light={{
                      color: "black",
                    }}
                    _dark={{
                      color: "gray.300",
                    }}
                  />
                }
                variant="outline"
                placeholder="Email"
                _light={{
                  placeholderTextColor: "blueGray.400",
                }}
                _dark={{
                  placeholderTextColor: "blueGray.50",
                }}
                onChangeText={(text) => {
                  setEmail(text);
                  setEmailError(""); // Clear the validation error when the user starts typing
                }}
              />
            </View>
          </View>
          {emailError !== "" && (
            <Text style={styles.errorText}>{emailError}</Text>
          )}

          {/* Button */}
          <View style={styles.buttonStyle}>
            <Button style={styles.buttonDesign} onPress={sendOtp}>
              Send OTP
            </Button>
          </View>
          <View style={styles.text2}>
            <Text>Don't have an account? </Text>
            <TouchableOpacity onPress={() => navigation.navigate("Signup")}>
              <Text style={styles.signupText}> Sign up</Text>
            </TouchableOpacity>
          </View>

          <StatusBar style="auto" />
        </View>
      )}
    </View>
  );
}

export default () => {
  return (
    <NativeBaseProvider>
      <Login />
    </NativeBaseProvider>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: "#fff",
  },
  LoginText: {
    marginTop: 100,
    fontSize: 30,
    fontWeight: "bold",
  },
  Middle: {
    alignItems: "center",
    justifyContent: "center",
  },
  text2: {
    flexDirection: "row",
    justifyContent: "center",
    paddingTop: 5,
  },
  containerbox: {
    flexDirection: "row",
    justifyContent: "center",
    alignItems: "center",
  },
  box: {
    borderWidth: 1,
    borderColor: "black",
    width: 40,
    height: 40,
    margin: 10,
    textAlign: "center",
    fontSize: 20,
  },
  signupText: {
    fontWeight: "bold",
  },
  emailField: {
    marginTop: 30,
    marginLeft: 15,
  },
  emailInput: {
    marginTop: 10,
    marginRight: 5,
  },
  buttonStyle: {
    marginTop: 30,
    marginLeft: 15,
    marginRight: 15,
  },
  buttonStyleX: {
    marginTop: 12,
    marginLeft: 15,
    marginRight: 15,
  },
  buttonDesign: {
    backgroundColor: "#026efd",
  },
  toggleContainer: {
    flexDirection: "row",
    justifyContent: "center",
    alignItems: "center", // Add this line to center items vertically
    marginVertical: 10,
  },
  toggleButton: {
    paddingHorizontal: 20,
    paddingVertical: 10,
    marginHorizontal: 5,
    backgroundColor: "#eee",
    borderRadius: 5,
  },
  orText: {
    marginHorizontal: 10,
    fontSize: 16,
    fontWeight: "bold",
    color: "#333", // Adjust the color if needed
  },
  activeButton: {
    backgroundColor: "#026efd",
  },
  toggleButtonText: {
    fontWeight: "bold",
  },
  activeButtonText: {
    color: "#fff",
  },
  errorText: {
    color: "red",
    marginLeft: 15,
  },
  login: {
    flex: 1,
    justifyContent: 'center', 
    marginTop:120,
    alignItems: 'center', 
  },
  image: {
    width: 150,
    height: 150,
  },
});
