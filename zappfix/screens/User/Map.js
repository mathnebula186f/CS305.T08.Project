import React, { useState, useEffect } from 'react';
import { View, StyleSheet ,Text} from 'react-native';
import MapView, { Marker, Polyline } from 'react-native-maps';
import * as Location from 'expo-location';

const Map = () => {
  const [location, setLocation] = useState(null);

  useEffect(() => {
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

  return (
    <View style={styles.container}>
    <Text>Hello</Text>
      {location ? (
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
          {/* <Marker
            coordinate={{
              latitude: location.coords.latitude+0.01,
              longitude: location.coords.longitude,
            }}
            title="Anup Kumarm Plumber"
            pinColor="yellow"
          />
          <Marker
            coordinate={{
              latitude: location.coords.latitude+0.01,
              longitude: location.coords.longitude+0.01,
            }}
            title="Ramu Electrician"
            pinColor="blue"
          />
          <Marker
            coordinate={{
              latitude: location.coords.latitude,
              longitude: location.coords.longitude+0.01,
            }}
            title="Ram Bulb"
            pinColor="yellow"
          />
          <Marker
            coordinate={{
              latitude: location.coords.latitude,
              longitude: location.coords.longitude-0.01,
            }}
            title="Pammi salon"
            pinColor="yellow"
          />
          <Marker */}
            {/* coordinate={{
              latitude: location.coords.latitude-0.01,
              longitude: location.coords.longitude-0.01,
            }}
            title="Yadav hair & care"
            pinColor="yellow"
          /> */}
          {/* Add more markers if needed */}
          
          {/* Example Polyline */}
          {/* <Polyline
            coordinates={[
              { latitude: location.coords.latitude, longitude: location.coords.longitude },
              { latitude: 37.78825, longitude: -122.4324 }
            ]}
            strokeWidth={2}
            strokeColor="red"
          /> */}
          {/* Add more Polylines if needed */}
        </MapView>
      ) : null}
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    ...StyleSheet.absoluteFillObject,
    justifyContent: 'flex-end',
    alignItems: 'center',
  },
  map: {
    ...StyleSheet.absoluteFillObject,
  },
});

export default Map;
