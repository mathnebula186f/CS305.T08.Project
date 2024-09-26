import React from "react";
import { View, StyleSheet } from "react-native";
import * as Animatable from 'react-native-animatable';

export default function LoadingScreen() {
  return (
    <View style={styles.container}>
      <Animatable.Image
        animation="rotate" 
        easing="ease-out" 
        iterationCount="infinite" 
        style={styles.image} 
        source={require("../../assets/icon.png")}
      />

    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: "center",
    alignItems: "center",
  },
  image: {
    width: 200,
    height: 200,
  },
});
