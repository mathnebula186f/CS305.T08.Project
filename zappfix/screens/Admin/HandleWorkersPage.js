import React, { useState, useEffect } from 'react';
import { View, Text, FlatList, TouchableOpacity, StyleSheet, TextInput } from 'react-native';
import { useFocusEffect } from '@react-navigation/native'; // Import useFocusEffect

import { AuthContext } from '../../context/AuthContext';

const HandleWorkersPage = ({ navigation }) => {
  const [workers, setWorkers] = useState([]);
  const [searchQuery, setSearchQuery] = useState('');
  const { API } = React.useContext(AuthContext);

  const fetchWorkers = async () => {
    try {
      const response = await fetch(`${API}/get_workers`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json'
        },
      });

      if (!response.ok) {
        throw new Error('Error fetching workers');
      }
      
      const data = await response.json();
      setWorkers(data.workers);
    } catch (error) {
      console.error('There was a problem with the fetch operation:', error);
    }
  };

  // Refetch data every time the screen comes into focus
  useFocusEffect(
    React.useCallback(() => {
      fetchWorkers();
    }, [])
  );

  const filteredWorkers = workers.filter(worker =>
    worker.name.toLowerCase().includes(searchQuery.toLowerCase())
  );

  const handleWorkerClick = (worker) => {
    navigation.navigate('AdminWorkerDetail', { worker });
  };

  const renderItem = ({ item }) => (
    <TouchableOpacity
      style={styles.workerItem}
      onPress={() => handleWorkerClick(item)}
    >
      <Text>{item.name}</Text>
      <Text style={item.verified ? styles.verified : styles.actionRequired}>
        {item.verified ? 'verified' : 'not verified'}
      </Text>
    </TouchableOpacity>
  );

  return (
    <View style={styles.container}>
      <TextInput
        style={styles.searchInput}
        placeholder="Search workers..."
        onChangeText={text => setSearchQuery(text)}
        value={searchQuery}
      />
      <FlatList
        data={filteredWorkers}
        renderItem={renderItem}
        keyExtractor={(item) => item.email}
      />
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    padding: 20,
  },
  searchInput: {
    height: 40,
    borderColor: 'gray',
    borderWidth: 1,
    marginBottom: 10,
    paddingHorizontal: 10,
  },
  workerItem: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    paddingVertical: 10,
    borderBottomWidth: 1,
    borderBottomColor: '#ccc',
  },
  verified: {
    color: 'green',
  },
  actionRequired: {
    color: 'red',
  },
});

export default HandleWorkersPage;
