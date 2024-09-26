import React, { useState, useEffect, useContext } from 'react';
import Timeline from 'react-native-timeline-flatlist'
import {
  View,
  StyleSheet,
  Text,
  TouchableOpacity,
  Linking,
  Image,
  Modal,
  Pressable,
  TextInput,
  SafeAreaView,
} from "react-native";
import MapView, { Marker, Polyline } from 'react-native-maps';
import * as Location from 'expo-location';
import Icon from 'react-native-vector-icons/MaterialIcons';
import AsyncStorage from '@react-native-async-storage/async-storage';
import { Rating } from "react-native-ratings";
import { AuthContext } from '../../context/AuthContext';
import { useNavigation } from '@react-navigation/native';

const User_InteractionPage = (props) => {
  const [location, setLocation] = useState(null);
  const { API } = useContext(AuthContext);
  const [distance, setDistance] = useState(0);
  const { email, service,status } = props.route.params;
  const [workerProfile, setWorkerProfile] = useState([]);
  const [routeCoordinates, setRouteCoordinates] = useState([]);
  const [modalVisible, setModalVisible] = useState(false);
  const [review, setReview] = useState("");
  const [rating, setRating] = useState(0);
  const navigation=useNavigation();

  
  useEffect(() => {
    fetchWorkerProfile();
    (async () => {
      let { status } = await Location.requestForegroundPermissionsAsync();
      if (status !== 'granted') {
        console.log('Permission to access location was denied');
        return;
      }

      let location = await Location.getCurrentPositionAsync({});
      setLocation(location);
    })();
  }, []);

  const fetchWorkerProfile = async () => {
    try {
      const user_email = await AsyncStorage.getItem("email");
      const response = await fetch(`${API}/get_worker_profile`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ email: user_email, worker_email: email }),
      });

      const data = await response.json();
      data.latitude += 0.1;
      data.longitude += 0.1;
      if (response.ok) {
        setWorkerProfile(data);

        if (location && data.latitude && data.longitude) {
          const userCoords = {
            latitude: location.coords.latitude,
            longitude: location.coords.longitude,
          };
          const workerCoords = {
            latitude: data.latitude,
            longitude: data.longitude,
          };
          const calculatedDistance = calculateDistance(userCoords, workerCoords);
          setDistance(calculatedDistance);
          fetchRoute(userCoords, workerCoords);
        }
      } else {
        console.error('Failed to fetch worker profile:', data.message);
      }
    } catch (error) {
      console.error('Error fetching worker profile:', error);
    }
  };

  useEffect(() => {
    fetchWorkerProfile();
  }, [API, email]);

  const calculateDistance = (startCoords, endCoords) => {
    const earthRadius = 6371;
    const dLat = toRadians(endCoords.latitude - startCoords.latitude);
    const dLon = toRadians(endCoords.longitude - startCoords.longitude);

    const a =
      Math.sin(dLat / 2) * Math.sin(dLat / 2) +
      Math.cos(toRadians(startCoords.latitude)) *
      Math.cos(toRadians(endCoords.latitude)) *
      Math.sin(dLon / 2) *
      Math.sin(dLon / 2);

    const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));

    const distance = earthRadius * c;
    return distance.toFixed(2);
  };

  const toRadians = (degrees) => {
    return degrees * (Math.PI / 180);
  };

  const openWhatsApp = () => {
    const phoneNumber = workerProfile.phone_number;
    const message = `Hello, I am interested in your ${service} service. Could you please provide me with more details about the service, including what it includes, any pricing information, and how I can avail of it? Additionally, I would like to inquire about your availability. Looking forward to your response. Thank you.`;

    Linking.openURL(`whatsapp://send?phone=+91${phoneNumber}&text=${encodeURIComponent(message)}`);
  };

  const fetchRoute = async (origin, destination) => {
    try {
      const url = `https://router.project-osrm.org/route/v1/driving/${origin.longitude},${origin.latitude};${destination.longitude},${destination.latitude}?overview=full&geometries=geojson`;

      const response = await fetch(url);
      const data = await response.json();

      if (response.ok && data.routes.length > 0) {
        const routeCoordinates = data.routes[0].geometry.coordinates.map(coord => ({
          latitude: coord[1],
          longitude: coord[0],
        }));
        setRouteCoordinates(routeCoordinates);
      }
    } catch (error) {
      console.error('Error fetching route:', error);
    }
  };
  const submitWorkdone = async () => {
    // console.log("Hi")
    try {
      if (!review.trim()) {
        console.error("Review cannot be empty");
        return;
      }
      if (rating === 0) {
        console.error("Rating cannot be zero");
        return;
      }
      const user_email=await AsyncStorage.getItem("email");
      const data = {
        user_email: user_email,
        worker_email: email,
        service: service,
        status:"Done",
        user_rating: rating,
        user_review: review,
      };
      const response = await fetch(`${API}/update_user_works`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(data),
      });
      if (response.ok) {
        console.log("Review submitted successfully");
        setModalVisible(false);
        alert("Review submitted successfully");
        navigation.navigate("User History")
      } else {
        console.error("Failed to submit review");
      }
    } catch (error) {
      console.error("Error submitting review:", error);
    }
  };

  const handleReject= async () =>{
    console.log("Hi")
    try {
      
      const user_email=await AsyncStorage.getItem("email");
      const data = {
        user_email: user_email,
        worker_email: email,
        service: service,
        status:"Reject",
        user_rating: rating,
        user_review: review,
      };
      const response = await fetch(`${API}/update_user_works`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(data),
      });
      if (response.ok) {
        console.log("Rejected successfully");
        setModalVisible(false);
        alert("Rejected successfully");
        navigation.navigate("User History")
      } else {
        console.error("Failed to submit ");
      }
    } catch (error) {
      console.error("Error submitting :", error);
    }
  }
  return (
    <View style={styles.container}>
      <View style={styles.mapContainer}>
        {location && workerProfile.latitude && workerProfile.longitude && status==="In Progress" && (
          <MapView
            style={styles.map}
            initialRegion={{
              latitude: location.coords.latitude,
              longitude: location.coords.longitude,
              latitudeDelta: 0.0922,
              longitudeDelta: 0.0421,
            }}
          >
            <Marker
              coordinate={{
                latitude: workerProfile.latitude,
                longitude: workerProfile.longitude,
              }}
              title="Worker Location"
            >
              <Image
                source={require("../../assets/scooter_icon.png")}
                style={{ width: 40, height: 40 }}
              />
            </Marker>
            <Marker
              coordinate={{
                latitude: location.coords.latitude,
                longitude: location.coords.longitude,
              }}
              title="Current Location"
            >
              <Image
                source={require("../../assets/user_icon.png")}
                style={{ width: 40, height: 40 }}
              />
            </Marker>
            <Polyline
              coordinates={routeCoordinates}
              strokeWidth={2}
              strokeColor="#FF0000"
            />
          </MapView>
        )}
      </View>
      <View style={styles.infoContainer}>
        <View style={styles.infoRow}>
          <TouchableOpacity style={styles.infoItem} onPress={openWhatsApp}>
            <Icon name="chat" size={42} color="#3498db" />
          </TouchableOpacity>
          <Text style={styles.infoItem}>{distance} KM Away</Text>
        </View>

        <View style={styles.infoRow}>
          <TouchableOpacity
            style={styles.button}
            onPress={() => setModalVisible(true)}
          >
            <Icon name="done" size={20} color="#fff" />
          </TouchableOpacity>
          <TouchableOpacity
            style={styles.button}
            onPress={handleReject}
          >
            <Icon name="close" size={20} color="#fff"/>
          </TouchableOpacity>
        </View>
      </View>

      <Modal
        animationType="slide"
        transparent={true}
        visible={modalVisible}
        onRequestClose={() => {
          setModalVisible(!modalVisible);
        }}
      >
        <View style={styles.modalContainer}>
          <View style={styles.modalContent}>
            <SafeAreaView style={styles.reviewContainer}>
              <TextInput
                style={styles.inputContainer}
                onChangeText={(text) => setReview(text)}
                value={review}
                placeholder="Write your review..."
                multiline={true}
              />
            </SafeAreaView>
            <Rating startingValue={0} onFinishRating={setRating} fractions={1} jumpValue={0.5} />

            <View style={styles.modalButtons}>
              <Pressable
                style={[styles.button, styles.buttonSubmit]}
                onPress={() => setModalVisible(!modalVisible)}
              >
                <Text style={styles.buttonText}>Close</Text>
              </Pressable>
              <Pressable
                style={[styles.button, styles.buttonSubmit]}
                onPress={() => {submitWorkdone()}}
              >
                <Text style={styles.buttonText}>Submit</Text>
              </Pressable>
            </View>
          </View>
        </View>
      </Modal>

      <View styles={styles.whatsappContainer}></View>
      <View style={styles.reloadButtonContainer}>
        <TouchableOpacity
          style={styles.reloadButton}
          onPress={fetchWorkerProfile}
        >
          <Icon name="refresh" size={20} color="#fff" />
        </TouchableOpacity>
      </View>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    flexDirection: "column",
  },
  mapContainer: {
    flex: 6,
  },
  map: {
    ...StyleSheet.absoluteFillObject,
  },
  whatsappContainer: {
    flex: 1,
    backgroundColor: "#FFFFFF",
    justifyContent: "center",
    alignItems: "center",
  },
  whatsappText: {
    fontSize: 16,
    fontWeight: "bold",
  },
  infoContainer: {
    flex: 1,
    flexDirection: "row",
    justifyContent: "space-around",
    alignItems: "center",
    backgroundColor: "#FFFFFF",
  },
  infoRow: {
    flexDirection: "row",
    alignItems: "center",
  },
  infoItem: {
    marginHorizontal: 10,
    fontSize: 16,
    fontWeight: "bold",
  },
  button: {
    flexDirection: "row",
    alignItems: "center",
    justifyContent: "center",
    backgroundColor: "#3498db",
    borderRadius: 5,
    padding: 10,
    marginHorizontal: 5,
  },
  buttonText: {
    color: "#fff",
    marginLeft: 5,
  },
  reloadButtonContainer: {
    position: "absolute",
    bottom: 120,
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
  reviewContainer: {
    borderWidth: 1,
    borderRadius: 5,
    marginHorizontal: 20,
    marginBottom: 20,
    padding: 5,
    height: 150,
    width: 200,
  },
  inputContainer: {
    textAlignVertical: "top",
    maxHeight: 150,
  },
  modalContainer: {
    flex: 1,
    justifyContent: "center",
    alignItems: "center",
    backgroundColor: "rgba(0, 0, 0, 0.5)",
  },
  modalContent: {
    backgroundColor: "#fff",
    borderRadius: 10,
    padding: 20,
    alignItems: "center",
    width: "80%",
  },
  modalButtons: {
    flexDirection: "row",
    justifyContent: "space-between",
    width: "100%",
    marginTop: 20,
  },

  buttonSubmit: {
    paddingHorizontal: 26,
  },
});


export default User_InteractionPage;