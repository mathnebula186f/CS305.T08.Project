import React, { useState, useEffect, useContext } from 'react';
import { View, StyleSheet, Text, TouchableOpacity, Linking, Image } from 'react-native';
import MapView, { Marker, Polyline } from 'react-native-maps';
import * as Location from 'expo-location';
import Icon from 'react-native-vector-icons/MaterialIcons';

import { AuthContext } from '../../context/AuthContext';
import AsyncStorage from '@react-native-async-storage/async-storage';
import { useNavigation } from '@react-navigation/native';
import Worker_TimeLine from './Worker_TimeLine';


const InteractionPage = (props) => {
  const [location, setLocation] = useState(null);
  const { API } = useContext(AuthContext);
  const [distance, setDistance] = useState(0);
  const [routeCoordinates, setRouteCoordinates] = useState([]);
  const { email , service ,status} = props.route.params;
  const [ latitutepoint, setlatitutepoint ] = useState(-1);
  const [ longitutepoint, setlongitutepoint ] = useState(-1);
  const [workerEmail,setWorkerEmail]=useState("");
  const navigation=useNavigation();
  

  useEffect(() => {
    // fetchUserProfile();
    (async () => {
      let { status } = await Location.requestForegroundPermissionsAsync();
      if (status !== 'granted') {
        console.log('Permission to access location was denied');
        return;
      }

      let location = await Location.getCurrentPositionAsync({});
      setLocation(location);
      const email1=await AsyncStorage.getItem("email");
      setWorkerEmail(email1)

      // Fetch the route between user's location and a fixed point
      const userLocation = { latitude: 30.9, longitude: 75.9 }; // as hardcoded in line 94&95
      const fixedPoint = { latitude: location.coords.latitude, longitude: location.coords.longitude }; // Worker loccation
      fetchRoute(userLocation, fixedPoint);
    })();
  }, []);

  

  const UpdateLocation = async () => {
    try {
      const worker_email=await AsyncStorage.getItem('email');
      setWorkerEmail(worker_email)
      const response = await fetch(`${API}/update_worker_location`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          email: worker_email,
          liveLatitude: location.coords.latitude,
          liveLongitude: location.coords.longitude,
        }),
      });
      const data = await response.json();
      if (response.ok) {
        alert(data.message);
      } else {
        console.error('Failed to Update Location:', data.error);
      }
    } catch (error) {
      console.error('Error Updating Location:', error);
    }
  };

  
  const openWhatsApp = () => {
    Linking.openURL('whatsapp://send?phone=+1234567890'); // Replace +1234567890 with your WhatsApp number
  };

  // Function to fetch route between origin and destination
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
  const handleReject= async () =>{
    alert("Reject is pressed");
    try {
      
      const worker_email=await AsyncStorage.getItem("email");
      const data = {
        user_email: email,
        worker_email: worker_email,
        service: service,
        status:"Reject",
      };
      const response = await fetch(`${API}/update_worker_works`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(data),
      });
      if (response.ok) {
        console.log("Rejected successfully");
        alert("Rejected successfully");
        navigation.navigate("Worker History");
      } else {
        alert("Failed to Reject ",data.error);
      }
    } catch (error) {
      alert("Error Rejecting :", error);
    }
  }
  const submitWorkdone = async () => {
    // console.log("Hi")
    alert("Accept Pressed!!");
    try {
      const worker_email=await AsyncStorage.getItem("email");
      console.log("Worker email=",worker_email,"user email=",email,"service=",service)
      const data = {
        user_email: email,
        worker_email: worker_email,
        service: service,
        status:"Done",
      };
      const response = await fetch(`${API}/update_worker_works`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(data),
      });
      if (response.ok) {
        console.log("Work Done successfully");
        alert("Work Done successfully");
        navigation.navigate("Worker History");
      } else {
        alert("Failed To send work done!!",data.error)
        // console.error();
      }
    } catch (error) {
      alert("Error submitting review:", error)
    }
  };
  return (
    <View style={styles.container}>
      <View style={styles.mapContainer}>
        <Worker_TimeLine
          route={{ params: { email: email, service: service, status: status } }}
        />
      </View>
      <View style={styles.infoContainer}>
        <View style={styles.infoRow}>
          {/* <TouchableOpacity style={styles.infoItem} onPress={openWhatsApp}>
            <Icon name="chat" size={42} color="#3498db" />
          </TouchableOpacity> */}
          {/* <Text style={styles.infoItem}>{distance} KM Away</Text> */}
        </View>

        <View style={styles.infoRow}>
          <TouchableOpacity
            style={[styles.button, styles.button2]}
            onPress={() => submitWorkdone()}
          >
            <Text style={styles.infoItem}> Mark as done</Text>
          </TouchableOpacity>
          <TouchableOpacity
            style={[styles.button, styles.button1]}
            onPress={handleReject}
          >
            <Text style={styles.infoItem}>Decline</Text>
          </TouchableOpacity>
        </View>
      </View>
      <View style={styles.reloadButtonContainer}>
        <TouchableOpacity style={styles.reloadButton} onPress={UpdateLocation}>
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
  button: {
    flexDirection: "row",
    alignItems: "center",
    justifyContent: "center",
    // backgroundColor: "#3498db",
    borderRadius: 5,
    padding: 10,
    marginHorizontal: 5,
  },
  infoContainer: {
    flex: 1,
    flexDirection: "row",
    justifyContent: "center",
    alignItems: "center",
    backgroundColor: "#FFFFFF",
  },
  infoRow: {
    flexDirection: "row",
    alignItems: "center",
    justifyContent: "center",
    textColor: "white",
  },
  infoItem: {
    marginHorizontal: 10,
    fontSize: 16,
    fontWeight: "bold",
    color:"white"
  },
  button1: {
    backgroundColor:"red",
  },
  button2: {
    backgroundColor:"green",
  },
});

export default InteractionPage;