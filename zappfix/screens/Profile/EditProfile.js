import React, { useContext, useState, useEffect } from "react";
import {
  View,
  TextInput,
  Alert,
  StyleSheet,
  TouchableOpacity,
  Text,
  KeyboardAvoidingView,
  FlatList,
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
import { AuthContext } from "../../context/AuthContext";
import LoadingScreen from "../Loading/LoadingScreen";

const EditProfile = () => {
  const [firstName, setFirstName] = useState("");
  const [lastName, setLastName] = useState("");
  const [age, setAge] = useState("");
  const [gender, setGender] = useState("");
  const [address, setAddress] = useState("");
  const [city, setCity] = useState("");
  const [state, setState] = useState("");
  const [zipCode, setZipCode] = useState("");
  const [phoneNumber, setPhoneNumber] = useState("");
  const { API, isWorker, email, userToken } = useContext(AuthContext);
  const [progress, SetProgress] = useState(false);

  useEffect(() => {
    fetchUserData();
  }, []);

  const fetchUserData = async () => {
    try {
      SetProgress(true);
      const response = await fetch(`${API}/get_user_data`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        credentials: "include",
        body: JSON.stringify({
          isWorker: isWorker,
          email: email,
          token: userToken,
        }),
      });
      const data = await response.json();
      if (response.ok) {
        const user = data.worker_details;
        setFirstName(user.first_name);
        setLastName(user.last_name);
        setAge(user.age);
        setAddress(user.address);
        setCity(user.city);
        setGender(user.gender);
        setPhoneNumber(user.phone_number);
        setState(user.state);
        setZipCode(user.zip_code);
      } else {
        console.error("Failed to fetch user data:", data.error);
      }
    } catch (error) {
      console.error("Error fetching user data:", error);
    } finally {
    }
    SetProgress(false);
  };

  const handleSubmit = async () => {
    try {
      const response = await fetch(`${API}/edit_personal_profile`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          email: email,
          first_name: firstName,
          last_name: lastName,
          age: age,
          gender: gender,
          address: address,
          city: city,
          state: state,
          zip_code: zipCode,
          phone_number: phoneNumber,
          isWorker: isWorker,
          token: userToken,
        }),
      });

      const data = await response.json();
      if (response.ok) {
        Alert.alert("Success", data.message);
        // Handle successful profile update
      } else {
        Alert.alert("Error", data.error);
        // Handle error from backend
      }
    } catch (error) {
      console.error("Error:", error);
      Alert.alert("Error", "An unexpected error occurred.");
      // Handle unexpected errors
    }
  };

  return (
      <NativeBaseProvider>
        <KeyboardAvoidingView style={{ flex: 1 }} behavior="padding">
      <FlatList contentContainerStyle={styles.scrollContainer} ListHeaderComponent=
      {progress ? (
        <LoadingScreen />
      ) : (
          <View style={styles.container}>
        <View style={styles.buttonContainer}>
          {/* First Name  Input Field */}
          <View style={styles.Middle}>
              <Text style={styles.LoginText}>Edit Profile</Text>
            </View>
          <View style={styles.buttonStyleX}>
            <View style={styles.emailInput} >
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
                value={firstName}
                _light={{
                  placeholderTextColor: "blueGray.400",
                }}
                _dark={{
                  placeholderTextColor: "blueGray.50",
                }}
                onChangeText={(text) => setFirstName(text)}
                placeholder="First Name"
              />
            </View>
          </View>
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
                        value={lastName}
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
                        value={age}
                        placeholder="Age"
                        keyboardType="numeric"
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
          <View style={styles.buttonStyleX}>
          <View style={styles.emailInput}>
                      <Input
                        InputLeftElement={
                          <Icon
                            as={<MaterialCommunityIcons name="gender-male-female" />}
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
                        value={gender}
                        placeholder="Gender"
                        _light={{
                          placeholderTextColor: "blueGray.400",
                        }}
                        _dark={{
                          placeholderTextColor: "blueGray.50",
                        }}
                        onChangeText={(text) => {
                          setGender(text);
                        }}
                      />
                    </View>
                  </View>
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
                        value={address}
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
                        value={city}
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
                        value={state}
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
                        value={zipCode}
                        placeholder="Zip Code"
                        keyboardType="numeric"
                        _light={{
                          placeholderTextColor: "blueGray.400",
                        }}
                        _dark={{
                          placeholderTextColor: "blueGray.50",
                        }}
                        onChangeText={(text) => {
                          setZipCode(text);
                        }}
                      />
                    </View>
                  </View>
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
                        value={phoneNumber}
                        placeholder="Phone Number"
                        keyboardType="phone-pad"
                        _light={{
                          placeholderTextColor: "blueGray.400",
                        }}
                        _dark={{
                          placeholderTextColor: "blueGray.50",
                        }}
                        onChangeText={(text) => {
                          setPhoneNumber(text);
                        }}
                      />
                    </View>
                  </View>
          <View style={styles.buttonStyle}>
                  <Button style={styles.buttonDesign} onPress={handleSubmit}>
                    Submit
                  </Button>
                </View>
        </View>
    </View>
      )}
      />
      </KeyboardAvoidingView>
      <View style={styles.reloadButtonContainer}>
        <TouchableOpacity style={styles.reloadButton} onPress={fetchUserData}>
          {/* <Icon name="refresh" size={20} color="#fff" /> */}
          <Icon
                            as={<MaterialCommunityIcons name="reload" />}
                            size={10}
                            _light={{
                              color: "#fff",
                            }}
                            _dark={{
                              color: "gray.300",
                            }}
                          />
        </TouchableOpacity>
      </View>
      </NativeBaseProvider>
  );
};

const styles = StyleSheet.create({
  scrollContainer: {
    flexGrow: 1,
  },
  container: {
    flex: 1,
    // padding: 10,
    // justifyContent: "center",
  },
  LoginText: {
    marginTop: 25,
    fontSize: 30,
    fontWeight: "bold",
  },
  Middle: {
    alignItems: "center",
    justifyContent: "center",
  },
  signupText: {
    fontWeight: "bold",
  },
  text2: {
    flexDirection: "row",
    justifyContent: "center",
    paddingTop: 5,
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
    marginLeft: 105,
    marginRight: 105,
    marginBottom: 15,
    
  },
  buttonStyleX: {
    marginTop: 12,
    marginLeft: 15,
    marginRight: 15,
  },
  buttonDesign: {
    backgroundColor: "#3498db",
  },
  reloadButtonContainer: {
    position: "absolute",
    bottom: 10,
    right: 20,
  },
  reloadButton: {
    backgroundColor: "#3498db",
    borderRadius: 50,
    width: 50,
    height: 50,
    alignItems: "center",
    justifyContent: "center",
  },
});

export default EditProfile;
