import React, { useState, useEffect, useContext } from 'react';
import { View, Text, Image, StyleSheet, TouchableOpacity, ScrollView } from 'react-native';
import Icon from 'react-native-vector-icons/MaterialIcons';
import * as DocumentPicker from 'expo-document-picker';
import * as FileSystem from 'expo-file-system';
import { useNavigation } from '@react-navigation/native';
import MaterialCommunityIcons from "react-native-vector-icons/MaterialCommunityIcons";

import { AuthContext } from '../../context/AuthContext';
import LoadingScreen from '../Loading/LoadingScreen';


const Profile = () => {
  const [user, setUser] = useState(null);
  const { logout, isWorker, setIsLoading, API,email ,userToken,setImageUri} = useContext(AuthContext);
  const [progress,SetProgress]=useState(false);
  const navigation = useNavigation();

  useEffect(() => {
    fetchUserData();
  }, []);

  const fetchUserData = async () => {
    try {
      SetProgress(true);
      const response = await fetch(`${API}/get_user_data`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        credentials: 'include',
        body: JSON.stringify({ isWorker: isWorker,email:email,token:userToken }),
      });
      const data = await response.json();
      if (response.ok) {
        setUser(data.worker_details);
      } else {
        console.error('Failed to fetch user data:', data.error);
        if(data.error == "Token expired"){
          alert(data.error);
          logout();
        }
      }
    } catch (error) {
      console.error('Error fetching user data:', error);
    } finally {
      
    }
    SetProgress(false);
  };

  const handleEditProfile = () => {
    console.log('Reload Profile button pressed');
    navigation.navigate("EditProfile")
  };

  const handleLogout = () => {
    console.log('Logout button pressed');
  };
  const handleImgUpload = async () => {
    try {
      const result = await DocumentPicker.getDocumentAsync({
        type: 'image/*', // Allow only image files
        copyToCacheDirectory: true, // Set to true if you want to copy the file to the app's cache directory
      });
  
      if (!result.canceled ) {
        // Do something with the selected image
        const { uri, name, type } = result.assets[0];
        console.log('Selected image:', { uri, name, type });
        const image=await FileSystem.readAsStringAsync(uri,{encoding:FileSystem.EncodingType.Base64});
        // console.log(image);
        console.log("isWorker==",isWorker)
        const resp=await fetch(`${API}/upload_profile_pic`,{
          method:'POST',
          headers:{
            'Content-Type':'application/json',
          },
          body:JSON.stringify({email:email,token:userToken, isWorker:isWorker, image:image})
        })
        const data=await resp.json();
        if(resp.ok){
          setUser(prevUser => ({ ...prevUser, profile_pic: data.url }));
          setImageUri(data.url);
        }
        if(!resp.ok){
          alert(data.error);
        }
      } else {
        console.log('Image selection canceled');
      }
    } catch (error) {
      console.error('Error selecting image:', error);
    }
  }

  const StarRating = ({ rating }) => {
    const fullStars = Math.floor(rating);
    const decimalPart = rating - fullStars;

    const stars = [];
    for (let i = 0; i < fullStars; i++) {
      stars.push(
        <MaterialCommunityIcons key={i} name="star" size={20} color="gold" />
      );
    }

    if (decimalPart > 0) {
      stars.push(
        <MaterialCommunityIcons
          key={fullStars}
          name="star-half"
          size={20}
          color="gold"
        />
      );
    }

    return <View style={{ flexDirection: "row" }}>{stars}</View>;
  };
  return (
    <View>
      <ScrollView>
        <View style={styles.container}>
          {progress ? (
            <LoadingScreen />
          ) : (
            user && (
              <View>
                <View style={styles.profileInfo}>
                  <>
                    <TouchableOpacity onPress={handleImgUpload}>
                      {user.profile_pic ? (
                        <>
                          <Image
                            source={{ uri: user.profile_pic }}
                            style={styles.profileImage}
                          />
                        </>
                      ) : (
                        <>
                          <Image
                            source={require("../../assets/Profile.jpg")}
                            style={styles.profileImage}
                          />
                        </>
                      )}
                      {/* <Image source={require('../assets/Profile.jpg')} style={styles.profileImage}/> */}
                    </TouchableOpacity>
                    <View style={styles.profileDetails}>
                      <Text style={styles.profileName}>{user.first_name}</Text>
                      <Text style={styles.profileId}>{user.last_name}</Text>
                    </View>
                  </>
                </View>

                <View style={styles.card}>
                  <Text style={styles.cardTitle}>Contact Information</Text>
                  <View style={styles.infoContainer}>
                    <View style={styles.infoItem}>
                      <Icon name="phone" size={20} color="#555" />
                      <Text>{` ${user.phone_number}`}</Text>
                    </View>
                    <View style={styles.infoItem}>
                      <Icon name="email" size={20} color="#555" />
                      <Text>{` ${user.email}`}</Text>
                    </View>
                  </View>
                </View>

                <View style={styles.card}>
                  <Text style={styles.cardTitle}>Personal Information</Text>
                  <View style={styles.infoContainer}>
                    <View style={styles.infoItem}>
                      <Icon name="person" size={20} color="#555" />
                      <Text>{` ${user.age} years old`}</Text>
                    </View>
                    <View style={styles.infoItem}>
                      <Icon name="wc" size={20} color="#555" />
                      <Text>{` ${user.gender}`}</Text>
                    </View>
                  </View>
                </View>

                <View style={styles.card}>
                  <Text style={styles.cardTitle}>Address</Text>
                  <View style={styles.infoContainer}>
                    <View style={styles.infoItem}>
                      <Icon name="location-on" size={20} color="#555" />
                      <Text>{` ${user.address}, ${user.city}, ${user.state} ${user.zip_code}`}</Text>
                    </View>
                  </View>
                </View>

                {isWorker == "True" && (
                  <View style={styles.card}>
                    <Text style={styles.cardTitle}>
                      <View style={styles.rating}>
                        <Text style={styles.ratingText}>Rating : </Text>
                        <StarRating rating={user.rating} />
                      </View>
                    </Text>
                    {/* <View style={styles.infoContainer}> */}
                      {/* <View style={styles.infoItem}> */}
                        {/* Display rating stars */}
                        {/* Include displayRatingStars function here */}
                        {/* You can use user.rating instead of profile.rating */}
                      </View>
                    // </View>
                  // </View>
                )}

                <View style={styles.bottomButtons}>
                  <TouchableOpacity
                    style={styles.button}
                    onPress={handleEditProfile}
                  >
                    <Icon name="edit" size={20} color="#fff" />
                    <Text style={styles.buttonText}>Edit Profile</Text>
                  </TouchableOpacity>
                  <TouchableOpacity
                    style={[styles.button, { backgroundColor: "#FF5733" }]}
                    onPress={logout}
                  >
                    <Icon name="exit-to-app" size={20} color="#fff" />
                    <Text style={styles.buttonText}>Logout</Text>
                  </TouchableOpacity>
                </View>
              </View>
            )
          )}
        </View>
      </ScrollView>
      <View style={styles.reloadButtonContainer}>
        <TouchableOpacity style={styles.reloadButton} onPress={fetchUserData}>
          <Icon name="refresh" size={20} color="#fff" />
        </TouchableOpacity>
      </View>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    padding: 20,
  },
  profileInfo: {
    flexDirection: "row",
    alignItems: "flex-start",
    marginBottom: 16,
  },
  profileImage: {
    width: 80,
    height: 80,
    borderRadius: 40,
    marginRight: 16,
  },
  profileDetails: {
    justifyContent: "space-between",
  },
  profileName: {
    fontSize: 20,
    fontWeight: "bold",
    color: "#333",
    writingDirection: "rtl",
  },
  profileId: {
    fontSize: 16,
    color: "#666",
  },
  card: {
    backgroundColor: "#fff",
    borderRadius: 10,
    padding: 15,
    marginBottom: 20,
    elevation: 3,
  },
  cardTitle: {
    fontSize: 18,
    fontWeight: "bold",
    marginBottom: 10,
  },
  infoContainer: {
    flexDirection: "column",
  },
  infoItem: {
    flexDirection: "row",
    alignItems: "center",
    marginBottom: 5,
  },
  bottomButtons: {
    flexDirection: "row",
    justifyContent: "space-between",
  },
  button: {
    flex: 1,
    flexDirection: "row",
    alignItems: "center",
    justifyContent: "center",
    backgroundColor: "#3498db",
    borderRadius: 5,
    padding: 10,
    marginHorizontal: 5,
    marginBottom: 50,
  },
  buttonText: {
    color: "#fff",
    marginLeft: 5,
  },
  reloadButtonContainer: {
    position: "absolute",
    bottom: 10,
    right: 10,
  },
  reloadButton: {
    backgroundColor: "#3498db",
    borderRadius: 50,
    width: 50,
    height: 50,
    alignItems: "center",
    justifyContent: "center",
  },
  rating: {
    flexDirection: "row",
    alignItems: "center",
    justifyContent:"center",
  },
  ratingText: {
    fontSize: 18,
    fontWeight: "bold",
    marginRight: 5,
  },
});

export default Profile;
