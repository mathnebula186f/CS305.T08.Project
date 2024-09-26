import React from 'react';
import { View, Text, FlatList, TouchableOpacity, StyleSheet } from 'react-native';
import Icon from 'react-native-vector-icons/Feather'; // Assuming you have imported the search icon from a suitable library

const SearchResults = ({ route, navigation }) => {
  const { searchResults } = route.params;

  const handleResultPress = (serviceName) => {
    // Navigate to a detail screen or perform any other action when a result is clicked
    // For now, let's just log the selected service name
    console.log("Service clicked:", serviceName);
    navigation.navigate("WorkerInfo", {service:serviceName} );
  };

  return (
    <View style={styles.container}>
      <FlatList
        data={searchResults.services} // Assuming services are provided in the "services" array
        renderItem={({ item }) => (
          <TouchableOpacity onPress={() => handleResultPress(item)} style={styles.itemContainer}>
            <Text style={styles.itemText}>{item}</Text>
            <Icon name="search" size={20} color="#000000" style={styles.searchIcon} />
          </TouchableOpacity>
        )}
        keyExtractor={(item) => item.name}
      />
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#FFFFFF',
  },
  itemContainer: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
    paddingVertical: 15,
    paddingHorizontal: 20,
    borderBottomWidth: 1,
    borderBottomColor: '#EAEAEA',
  },
  itemText: {
    fontSize: 16,
    flex: 1,
  },
  searchIcon: {
    marginLeft: 10,
  },
});

export default SearchResults;
