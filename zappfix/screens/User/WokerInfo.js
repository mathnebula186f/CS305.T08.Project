import React, { useState, useEffect, useContext } from 'react';
import {
  View,
  StyleSheet,
  Text,
  Dimensions,
  FlatList,
  Image,
  TouchableOpacity,
  Animated,
} from 'react-native';
import MapView, { Marker } from 'react-native-maps';
import * as Location from 'expo-location';
import MaterialCommunityIcons from 'react-native-vector-icons/MaterialCommunityIcons';
import { useFocusEffect, useNavigation } from "@react-navigation/native";
import Icon from 'react-native-vector-icons/MaterialIcons';

import { AuthContext } from '../../context/AuthContext';
import LoadingScreen from '../Loading/LoadingScreen';

const WorkerInfo = (props) => {
  const [location, setLocation] = useState(null);
  const [scrollOffset, setScrollOffset] = useState(new Animated.Value(0));
  const [selectedRating, setSelectedRating] = useState(null);
  const [isDropdownOpen, setDropdownOpen] = useState(false);
  const [workersData, setWorkersData] = useState([]);
  const {service} = props.route.params;
  const [workers,setWorkers]=useState([]);
  const navigation = useNavigation();

  const {API} = useContext(AuthContext);
   


  const [progress,setProgress]=useState(false);

  // Function to fetch nearest workers
  const fetchNearestWorkers = async () => {
    console.log("here i am",service);
    try {
      if(!location) return;
      // console.log("location", location)
      setProgress(true);
      const response = await fetch(`${API}/get_nearest_workers`, {
        method: 'POST', 
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          service: service,
          coords: [location.coords.latitude, location.coords.longitude],
        }),
      });
      const data = await response.json();
      // console.log("Workers=",data.workers);
      if (response.ok) {
        setWorkersData(data.workers);
        setWorkers(data.workers);
      } else {
        alert("No Workers Exist for These service!!");
        setWorkers([])
        // console.error('Failed to fetch nearest workers:', data.error);
      }
    } catch (error) {
      alert(error)
      // console.error('Error fetching nearest workers:', error);
    }
    setProgress(false);
  };


  useEffect(() => {
    (async () => {
      let { status } = await Location.requestForegroundPermissionsAsync();
      if (status !== 'granted') {
        console.log('Permission to access location was denied');
        return;
      }

      let location = await Location.getCurrentPositionAsync({});
      setLocation(location);

      if(location){
        fetchNearestWorkers();
      }
      fetchNearestWorkers();

    })();
  }, []);

  useFocusEffect(
    React.useCallback(() => {
      fetchNearestWorkers();
    }, [service])
  );

  const handleScroll = (event) => {
    const offsetY = event.nativeEvent.contentOffset.y;
    Animated.spring(scrollOffset, {
      toValue: offsetY,
      useNativeDriver: false
    }).start();
  };
  
  const maxMapHeight = Dimensions.get('window').height / 2;
  
  const mapHeight = scrollOffset.interpolate({
    inputRange: [0, maxMapHeight],
    outputRange: [maxMapHeight, 0],
    extrapolate: 'clamp',
  });


  const filteredWorkers = selectedRating
    ? workers.filter(worker => worker.rating >= selectedRating)
    : workers;

    const renderWorkerCard = ({ item }) => (
      <TouchableOpacity
        onPress={() => {
          navigation.navigate("RequestPage", {
            email: item.email,
            service: service,
            rating: item.rating,
          });
        }}
      >
        <View style={styles.workerCard}>
          <Image
            source={require("../../assets/Profile.jpg")}
            style={styles.profileImage}
          />
          <View style={styles.workerInfo}>
            <Text style={styles.workerName}>
              {item.first_name} {item.last_name}
            </Text>
            <Text>{item.email}</Text>
            {/* <Text style={styles.ratingText}>Rating: </Text> */}
            <StarRating rating={item.rating} />
          </View>
        </View>
        
      </TouchableOpacity>
    );

  const renderDropdownButton = () => (
    <TouchableOpacity
      style={styles.filterDropdownButton}
      onPress={() => setDropdownOpen(!isDropdownOpen)}
    >
      <Text style={styles.dropdownButtonText}>
        {selectedRating ? `Rating >= ${selectedRating}` : 'Filter by Rating'}
      </Text>
      <MaterialCommunityIcons
        name={isDropdownOpen ? 'chevron-up' : 'chevron-down'}
        size={24}
        color="black"
      />
    </TouchableOpacity>
  );

  const renderDropdownOptions = () => (
    <View style={styles.dropdownOptions}>
      {['Clear Filter', 4.0, 3.5, 3.0, 2.5, 1.5 ].map((value) => (
        <TouchableOpacity
          key={value}
          style={styles.dropdownOption}
          onPress={() => handleDropdownSelect(value)}
        >
          <Text>{value}</Text>
        </TouchableOpacity>
      ))}
    </View>
  );

  const renderMarkers = () => {
    console.log(workers)
    return workers.map((worker, index) => (
      <Marker
        key={index}
        coordinate={{
          latitude: worker.liveLatitude,
          longitude: worker.liveLongitude,
        }}
        title={`${worker.first_name} ${worker.last_name}`}
      />
    ));
  };

  const handleDropdownSelect = (value) => {
    if (value === 'Clear Filter') {
      setSelectedRating(null);
    } else {
      setSelectedRating(value);
    }
    setDropdownOpen(false);
  };

  return (
    <View style={styles.container}>
      <Animated.View style={{ height: mapHeight }}>
        {location && (
          <MapView
            style={styles.map}
            initialRegion={{
              latitude: location.coords.latitude,
              longitude: location.coords.longitude,
              latitudeDelta: 0.0922,
              longitudeDelta: 0.0421,
            }}
          >
            {/* Current Location Marker */}
            <Marker
              coordinate={{
                latitude: location.coords.latitude,
                longitude: location.coords.longitude,
              }}
              title="Current Location"
            />
            {renderMarkers()}
          </MapView>
        )}
      </Animated.View>
      {progress ? (
        <LoadingScreen />
      ) : (
        <View style={styles.contentContainer}>
          <Text style={styles.serviceProvidersInfo}>
            Service Providers Info
          </Text>

          {/* Filter Dropdown Button */}
          {renderDropdownButton()}

          {/* Dropdown Options */}
          {isDropdownOpen && renderDropdownOptions()}

          {/* FlatList of Worker Cards */}

          <FlatList
            data={filteredWorkers}
            keyExtractor={(item) => item.id}
            renderItem={renderWorkerCard}
            onScroll={handleScroll}
            contentContainerStyle={{ paddingBottom: 200 }} // Adjust this value as needed
          />
        </View>
      )}
      <View style={styles.reloadButtonContainer}>
          <TouchableOpacity style={styles.reloadButton} onPress={fetchNearestWorkers}>
            <Icon name="refresh" size={20} color="#fff" />
          </TouchableOpacity>
        </View>
    </View>
  );
};

const StarRating = ({ rating }) => {
  const fullStars = Math.floor(rating);
  const decimalPart = rating - fullStars;

  const stars = [];
  for (let i = 0; i < fullStars; i++) {
    stars.push(<MaterialCommunityIcons key={i} name="star" size={20} color="gold" />);
  }

  if (decimalPart > 0) {
    stars.push(<MaterialCommunityIcons key={fullStars} name="star-half" size={20} color="gold" />);
  }

  return <View style={styles.starContainer}>{stars}</View>;
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    borderColor: "black",
    borderWidth: 1,
  },
  map: {
    ...StyleSheet.absoluteFillObject,
  },
  contentContainer: {
    flex: 1,
    justifyContent: "center",
    alignItems: "center",
    paddingHorizontal: 20,
  },
  serviceProvidersInfo: {
    fontSize: 20,
    fontWeight: "bold",
    marginBottom: 10,
  },
  filterDropdownButton: {
    height: 50,
    width: "100%",
    flexDirection: "row",
    alignItems: "center",
    justifyContent: "space-between",
    marginBottom: 10,
    borderBottomWidth: 1,
    borderBottomColor: "black",
    paddingHorizontal: 10,
  },
  dropdownButtonText: {
    fontSize: 16,
  },
  dropdownOptions: {
    position: "absolute",
    top: 60,
    right: 10,
    width: 120,
    backgroundColor: "white",
    borderRadius: 5,
    elevation: 5,
    zIndex: 1,
  },
  dropdownOption: {
    padding: 10,
    borderBottomWidth: 1,
    borderBottomColor: "black",
  },
  workerCard: {
    width: "100%",
    flexDirection: "row",
    padding: 20,
    marginBottom: 20,
    backgroundColor: "#fff",
    borderRadius: 10,
    elevation: 5,
    alignItems: "center",
    justifyContent: "space-between",
  },
  profileImage: {
    width: 80,
    height: 80,
    borderRadius: 40,
    marginRight: 20,
  },
  workerInfo: {
    flex: 1,
    marginLeft: 10,
  },
  workerName: {
    fontSize: 16,
    fontWeight: "bold",
    marginBottom: 5,
  },
  starContainer: {
    flexDirection: "row",
  },
  ratingText: {
    fontSize: 16,
    color: "#333",
  },
  reloadButtonContainer: {
    position: "absolute",
    bottom: 20,
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

export default WorkerInfo;
