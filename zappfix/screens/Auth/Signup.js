import { StatusBar } from "expo-status-bar";
import React, { useContext } from "react";
import {
  SectionList,
  StyleSheet,
  Text,
  View,
  TouchableOpacity,
  KeyboardAvoidingView,
  FlatList
} from "react-native";
import {
  Input,
  NativeBaseProvider,
  Button,
  Icon,
  Box,
  Image,
  AspectRatio,
  Select,
} from "native-base";
import { FontAwesome5, MaterialCommunityIcons } from "@expo/vector-icons";
import { useNavigation } from "@react-navigation/native";
import { AuthContext } from "../../context/AuthContext";
import axios from "axios";
import Login from "./Login";
import LoadingScreen from "../Loading/LoadingScreen";
import { usePushNotifications } from "../../context/pushNotifications";
function Signup() {
  const {expoPushToken, notification} = usePushNotifications();
  const [firstName, setFirstName] = React.useState("");
  const [lastName, setLastName] = React.useState("");
  const [email, setEmail] = React.useState("");
  const [phoneNumber, setPhoneNumber] = React.useState("");
  const [selectedGender, setSelectedGender] = React.useState("");
  const [selectedRole, setSelectedRole] = React.useState("User");
  const [phoneNumberError, setPhoneNumberError] = React.useState("");
  const [emailError, setEmailError] = React.useState("");
  const [city, setCity] = React.useState("");
  const [state, setState] = React.useState("");
  const [zipcode, setZipCode] = React.useState("");
  const [age, setAge] = React.useState("");
  const [address, setAddress] = React.useState("");
  const [isOtpSent, setIsOtpSent] = React.useState(0);
  const [otp, setOtp] = React.useState("");
  const [progress, setProgress] = React.useState(false);
  // const [isWorker, setIsWorker]=React.useState(false);
  const { setIsLoading, API, isWorker, setIsWorker } = useContext(AuthContext);

  const navigation = useNavigation();

  const isPhoneNumberValid = (number) => {
    // You can implement your phone number validation logic here
    const phoneNumberPattern = /^\d{10}$/; // Assuming a valid phone number is a 10-digit number
    return phoneNumberPattern.test(number);
  };
  const isEmailValid = (email) => {
    // You can implement your email validation logic here
    const emailPattern = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
    return emailPattern.test(email);
  };

  const verifyOtp = async () => {
    // setIsLoading(true);
    if (selectedRole === "worker") {
      setIsWorker("True");
    } else if (selectedRole === "user") {
      console.log("selectedRole=", selectedRole);
      setIsWorker("False");
    }
    try {
      setProgress(true);
      const response = await fetch(`${API}/verify_otp`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          email: email,
          otp: otp,
          isWorker: isWorker,
          notification_id: expoPushToken,
        }),
      });

      const result = await response.json();
      console.log("result of verifying otp=", result);
      if (response.ok) {
        alert("Otp Verified Successfully you may proceed to login page!!");
        // navigator.navigate("Login");
      } else {
        alert(result.message);
      }
    } catch (error) {
      alert(error);
    }
    setProgress(false);
    // setIsLoading(false);
  };

  const handleSelectedRole = (itemValue) => {
    console.log("handleSelectedRole Called with itemValue", itemValue);
    if (itemValue == "worker") {
      setSelectedRole(itemValue);
      setIsWorker("True");
    } else if (itemValue == "user") {
      setSelectedRole(itemValue);
      setIsWorker("False");
    }
  };
  const handleSignUp = async () => {
    // Perform your signup logic here
    if (selectedRole === "worker") {
      setIsWorker("True");
    } else if (selectedRole === "user") {
      setIsWorker("False");
    }

    if (!isEmailValid(email)) {
      setEmailError("Please enter a valid email address");
      alert("Please enter a valid email address");
      return; // Stop the signup process if the email is not valid
    }
    // Phone number validation
    if (!isPhoneNumberValid(phoneNumber)) {
      setPhoneNumberError("Please enter a valid phone number");
      alert("Please enter a valid phone number");
      return; // Stop the signup process if the phone number is not valid
    }

    try {
      // Send a POST request to the backend with the user's information
      setProgress(true);
      const response = await fetch(`${API}/user_signup`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          first_name: firstName,
          last_name: lastName,
          phone_number: phoneNumber,
          email: email,
          age: age,
          gender: selectedGender,
          address: address,
          city: city,
          state: state,
          zip_code: zipcode,
          isWorker: isWorker,
        }),
      });

      const result = await response.json();
      console.log(result);

      // Handle the response from the backend
      console.log("Response:", response.data);

      // Check if the OTP needs to be sent
      if (response.ok) {
        setIsOtpSent(1);
        console.log("OTP sent successfully");
        alert("OTP sent successfully");
      } else {
        console.log("Failed to send OTP");
        alert("Failed to send OTP");
        // Handle the case where OTP sending fails
      }
    } catch (error) {
      console.error("Error signing up:", error);
      alert("Error sending otp");
      // Handle errors from the backend
    }
    setProgress(false);
  };
  return (
      <KeyboardAvoidingView style={{ flex: 1 }} behavior="padding">
      <FlatList contentContainerStyle={styles.scrollContainer} ListHeaderComponent=
        {progress ? (
          <LoadingScreen />
        ) : (
          <View style={styles.container}>
            <View style={styles.Middle}>
              <Text style={styles.LoginText}>Signup</Text>
            </View>
            <View style={styles.text2}>
              <Text>Already have account? </Text>
              <TouchableOpacity onPress={() => navigation.navigate("Login")}>
                <Text style={styles.signupText}> Login </Text>
              </TouchableOpacity>
            </View>

            {isOtpSent ? (
              <View>
                <View style={styles.buttonStyleX}>
                  <View style={styles.emailInput}>
                    <Input
                      variant="outline"
                      placeholder="Enter OTP"
                      _light={{
                        placeholderTextColor: "blueGray.400",
                      }}
                      _dark={{
                        placeholderTextColor: "blueGray.50",
                      }}
                      onChangeText={(text) => {
                        // Handle OTP input
                        setOtp(text);
                      }}
                    />
                  </View>
                </View>
                <View style={styles.buttonStyle}>
                  <Button style={styles.buttonDesign} onPress={verifyOtp}>
                    VERIFY OTP
                  </Button>
                </View>
              </View>
            ) : (
              <View>
                <View style={styles.buttonContainer}>
                  {/* First Name  Input Field */}
                  <View style={styles.buttonStyle}>
                    <View style={styles.emailInput}  className="-mb-4">
                      <Input
                        InputLeftElement={
                          <Icon
                            as={<FontAwesome5 name="user" />}
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
                        placeholder="First Name"
                        _light={{
                          placeholderTextColor: "blueGray.400",
                        }}
                        _dark={{
                          placeholderTextColor: "blueGray.50",
                        }}
                        onChangeText={(text) => setFirstName(text)}
                      />
                    </View>
                  </View>

                  {/* Last Name  Input Field */}
                  <View style={styles.buttonStyleX}>
                    <View style={styles.emailInput}>
                      <Input
                        InputLeftElement={
                          <Icon
                            as={<FontAwesome5 name="user" />}
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
                        placeholder="Last Name"
                        _light={{
                          placeholderTextColor: "blueGray.400",
                        }}
                        _dark={{
                          placeholderTextColor: "blueGray.50",
                        }}
                        onChangeText={(text) => {
                          setLastName(text);
                        }}
                      />
                    </View>
                  </View>

                  {/* Email Input Field */}
                  <View style={styles.buttonStyleX}>
                    <View style={styles.emailInput}>
                      <Input
                        InputLeftElement={
                          <Icon
                            as={<FontAwesome5 name="envelope" />}
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

                  {/* Phone Input Field */}
                  <View style={styles.buttonStyleX}>
                    <View style={styles.emailInput}>
                      <Input
                        InputLeftElement={
                          <Icon
                            as={<MaterialCommunityIcons name="phone-outline" />}
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
                        placeholder="Phone Number"
                        _light={{
                          placeholderTextColor: "blueGray.400",
                        }}
                        _dark={{
                          placeholderTextColor: "blueGray.50",
                        }}
                        onChangeText={(text) => {
                          setPhoneNumber(text);
                          setPhoneNumberError(""); // Clear the validation error when the user starts typing
                        }}
                      />
                    </View>
                  </View>
                  {phoneNumberError !== "" && (
                    <Text style={styles.errorText}>{phoneNumberError}</Text>
                  )}

                  {/* Age Input Field */}
                  <View style={styles.buttonStyleX}>
                    <View style={styles.emailInput}>
                      <Input
                        InputLeftElement={
                          <Icon
                            as={<MaterialCommunityIcons name="numeric" />}
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
                        placeholder="Age"
                        _light={{
                          placeholderTextColor: "blueGray.400",
                        }}
                        _dark={{
                          placeholderTextColor: "blueGray.50",
                        }}
                        onChangeText={(text) => {
                          setAge(text);
                        }}
                      />
                    </View>
                  </View>

                  {/* Gender Input Field */}
                  <View style={styles.buttonStyleX}>
                    <View style={styles.emailInput}>
                      <Select
                        InputLeftElement={
                          <Icon
                            as={<FontAwesome5 name="venus-mars" />}
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
                        selectedValue={selectedGender}
                        onValueChange={(itemValue) =>
                          setSelectedGender(itemValue)
                        }
                        variant="outline"
                        placeholder="Select Gender"
                      >
                        <Select.Item label="Male" value="male" />
                        <Select.Item label="Female" value="female" />
                        <Select.Item label="Other" value="other" />
                      </Select>
                    </View>
                  </View>

                  {/* Address Input Field */}
                  <View style={styles.buttonStyleX}>
                    <View style={styles.emailInput}>
                      <Input
                        InputLeftElement={
                          <Icon
                            as={<MaterialCommunityIcons name="home-outline" />}
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
                        placeholder="Address"
                        _light={{
                          placeholderTextColor: "blueGray.400",
                        }}
                        _dark={{
                          placeholderTextColor: "blueGray.50",
                        }}
                        onChangeText={(text) => {
                          setAddress(text);
                        }}
                      />
                    </View>
                  </View>

                  {/* City Input Field */}
                  <View style={styles.buttonStyleX}>
                    <View style={styles.emailInput}>
                      <Input
                        InputLeftElement={
                          <Icon
                            as={<MaterialCommunityIcons name="city-variant-outline" />}
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
                        placeholder="City"
                        _light={{
                          placeholderTextColor: "blueGray.400",
                        }}
                        _dark={{
                          placeholderTextColor: "blueGray.50",
                        }}
                        onChangeText={(text) => {
                          setCity(text);
                        }}
                      />
                    </View>
                  </View>

                  {/* State Input Field */}
                  <View style={styles.buttonStyleX}>
                    <View style={styles.emailInput}>
                      <Input
                        InputLeftElement={
                          <Icon
                            as={<MaterialCommunityIcons name="map-marker-check-outline" />}
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
                        placeholder="State"
                        _light={{
                          placeholderTextColor: "blueGray.400",
                        }}
                        _dark={{
                          placeholderTextColor: "blueGray.50",
                        }}
                        onChangeText={(text) => {
                          setState(text);
                        }}
                      />
                    </View>
                  </View>

                  {/*  Input Field */}
                  <View style={styles.buttonStyleX}>
                    <View style={styles.emailInput}>
                      <Select
                        InputLeftElement={
                          <Icon
                            as={<FontAwesome5 name="briefcase" />}
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
                        selectedValue={selectedRole}
                        onValueChange={(itemValue) =>
                          handleSelectedRole(itemValue)
                        }
                        variant="outline"
                        placeholder="Select Role"
                      >
                        <Select.Item label="Worker" value="worker" />
                        <Select.Item label="User" value="user" />
                      </Select>
                    </View>
                  </View>
                </View>
                <View style={styles.buttonStyle}>
                  <Button style={styles.buttonDesign} onPress={handleSignUp}>
                    REGISTER NOW
                  </Button>
                </View>
              </View>
            )}

            <StatusBar style="auto" />
          </View>
        )}
      />
      </KeyboardAvoidingView>
  );
}

export default () => {
  return (
    <NativeBaseProvider>
      <Signup />
    </NativeBaseProvider>
  );
};

const styles = StyleSheet.create({
  scrollContainer: {
    flexGrow: 1,
  },
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
    marginBottom: 15,
  },
  buttonStyleX: {
    marginTop: 12,
    marginLeft: 15,
    marginRight: 15,
  },
  buttonDesign: {
    backgroundColor: "#026efd",
  },
  buttonContainer: {
    //   marginTop:30
  },
  errorText: {
    color: "red",
    marginLeft: 15,
  },
});
