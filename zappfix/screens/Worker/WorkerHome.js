import React, { useContext, useEffect,useState } from 'react';
import { View, Text, StyleSheet, TouchableOpacity, ScrollView, Alert } from 'react-native';
import { Svg, Path, Text as SvgText, SvgXml } from 'react-native-svg'; // Import SvgXml for SVG support
import AsyncStorage from '@react-native-async-storage/async-storage';
import Icon from 'react-native-vector-icons/MaterialIcons';
import { useNavigation } from '@react-navigation/native';

import { AuthContext } from '../../context/AuthContext';
import LoadingScreen from '../Loading/LoadingScreen';

const pinSvg = `
<svg xmlns="http://www.w3.org/2000/svg" fill="#FF0000" width="20" height="20" viewBox="0 0 24 24">
  <path d="M12 2c-3.313 0-6 2.687-6 6 0 2.232 1.223 4.18 3 5.226v8.774h6v-8.774c1.777-1.046 3-2.994 3-5.226 0-3.313-2.687-6-6-6zm0 2c2.206 0 4 1.794 4 4s-1.794 4-4 4-4-1.794-4-4 1.794-4 4-4z"/>
</svg>
`;
const circumference = 2 * Math.PI * 40;
const percentage = 34;                          // change this value to update progress of profile.
const greenLength = (percentage / 100) * circumference;


const WorkerHome = () => {
    // Sample data for user requests

    const  {logout,API} = useContext(AuthContext);
    const [userRequests,setUserRequests]=useState([]);
    const [progress,setProgress]=useState(false);
    const navigation =useNavigation();


    // Function to handle accept button press
    const handleAccept = async (id) => {
      
        Alert.alert(
            'Confirm Acceptance',
            'Are you sure you want to accept this request?',
            [
                {
                    text: 'Cancel',
                    style: 'cancel'
                },
                {
                    text: 'Accept',
                    onPress: async () => {
                      const email= await AsyncStorage.getItem("email");
                      console.log("Service=",id.service)
                        try {
                            const response = await fetch(`${API}/update_request`, {
                              method: 'POST',
                              headers: {
                                'Content-Type': 'application/json',
                              },
                              body: JSON.stringify({
                                user_email: id.email,
                                worker_email: email,
                                service: id.service,
                                status: "Accept",
                              }),
                            });
                      
                            const data = await response.json();
                            console.log("data=",data);
                            if (response.ok) {
                              Alert.alert('Success', data.message);
                              fetchUserRequests();
                              // Handle successful profile update
                            } else {
                              Alert.alert('Error', data.error);
                              // Handle error from backend
                            }
                          } catch (error) {
                            console.error('Error:', error);
                            Alert.alert('Error', 'An unexpected error occurred.');
                            // Handle unexpected errors
                          }
                    }
                }
            ]
        );
    };

    // Function to handle reject button press
    const handleReject =async  (id) => {
      
        Alert.alert(
            'Confirm Rejection',
            'Are you sure you want to reject this request?',
            [
                {
                    text: 'Cancel',
                    style: 'cancel'
                },
                {
                    text: 'Reject',
                    onPress: async () => {
                      const email= await AsyncStorage.getItem("email");
                        try {
                            const response = await fetch(`${API}/update_request`, {
                              method: 'POST',
                              headers: {
                                'Content-Type': 'application/json',
                              },
                              body: JSON.stringify({
                                user_email: id.email,
                                worker_email: email,
                                service: id.service,
                                status: "Rejected",
                              }),
                            });
                      
                            const data = await response.json();
                            console.log("data=",data);
                            if (response.ok) {
                              Alert.alert('Success', data.message);
                              fetchUserRequests();
                              // Handle successful profile update
                            } else {
                              Alert.alert('Error', data.error);
                              // Handle error from backend
                            }
                          } catch (error) {
                            console.error('Error:', error);
                            Alert.alert('Error', 'An unexpected error occurred.');
                            // Handle unexpected errors
                          }
                    }
                }
            ]
        );
    };

    const fetchUserRequests = async () => {
        const email= await AsyncStorage.getItem("email");
        console.log("email=",email);
        try {
            // setProgress
            setProgress(true);
            const response = await fetch(`${API}/get_user_requests`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    email:email,
                  }),
            });
            const data = await response.json();

            if (response.ok) {
                console.log("Requests=",data.requests);
                setUserRequests(data.requests);
            } else {
                console.error('Failed to fetch user requests:', data.error);
            }
        } catch (error) {
            console.error('Error fetching user requests:', error);
        }
        setProgress(false);
    };

  useEffect(() => {
      fetchUserRequests();
  }, []);

  
    return (
      <View style={styles.container}>
        <Text style={[styles.title, { marginTop: 10 }]}>
          Worker Home Screen
        </Text>
        <View style={styles.card1}>
          <View style={styles.progressContainer}>
            <Svg height="100" width="100">
              <Path
                d="M50 10
                            a 40 40 0 0 1 0 80
                            a 40 40 0 0 1 0 -80"
                fill="none"
                stroke="#CCCCCC"
                strokeWidth="10"
              />
              <Path
                d="M50 10
                            a 40 40 0 0 1 0 80
                            a 40 40 0 0 1 0 -80"
                fill="none"
                stroke="green"
                strokeWidth="10"
                strokeDasharray={`${greenLength} ${circumference}`}
              />
              <SvgText
                x="40%"
                y="60%"
                dominantBaseline="middle"
                textAnchor="middle"
                fontSize="24"
                fill="green"
                fontFamily="Arial"
              >
                {percentage}%
              </SvgText>
            </Svg>
            <Text
              style={[styles.progressText, styles.infoItem, { marginLeft: 10 }]}
            >
              {percentage}% of your profile is completed
            </Text>
          </View>
        </View>

        <Text className="my-1 font-semibold text-xl">
          Pending User Requests
        </Text>
        <View
          style={styles.scrollContainer}
          className="border-4 border-gray-400 rounded-lg p-3 "
        >
          {progress ? (
            <LoadingScreen />
          ) : (
            <ScrollView style={styles.scrollView}>
              {userRequests ? (
                userRequests.map((request) => (
                  <View
                    key={request.id}
                    style={styles.card}
                    className="border border-gray-300"
                  >
                    <Text style={styles.name}>{request.first_name}</Text>
                    <Text style={styles.problem}>{request.service}</Text>
                    <View style={styles.distanceContainer}>
                      <SvgXml xml={pinSvg} />
                      <Text style={styles.distance}>{request.status}</Text>
                    </View>
                    <View style={styles.buttonsContainer}>
                      <TouchableOpacity
                        style={[styles.button, styles.acceptButton]}
                        onPress={() => handleAccept(request)}
                      >
                        <Text style={styles.buttonText}>Accept</Text>
                      </TouchableOpacity>
                      <TouchableOpacity
                        style={[styles.button, styles.rejectButton]}
                        onPress={() => handleReject(request)}
                      >
                        <Text style={styles.buttonText}>Reject</Text>
                      </TouchableOpacity>
                    </View>
                  </View>
                ))
              ) : (
                <View style={styles.centered}>
                  <Text>No current requests</Text>
                </View>
              )}
            </ScrollView>
          )}
          <View style={styles.reloadButtonContainer}>
            <TouchableOpacity
              style={styles.reloadButton}
              onPress={fetchUserRequests}
            >
              <Icon name="refresh" size={20} color="#fff" />
            </TouchableOpacity>
          </View>
        </View>

        {/* <Text className="my-1 mt-4 font-semibold text-xl">Worker History of Works</Text>
            <ScrollView style={styles.scrollContainer} className="border border-gray-400 -p-2 my-1 rounded-lg">
            <WorkerHistory/>
            </ScrollView> */}
      </View>
    );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    alignItems: "center",
    justifyContent: "center",
    paddingHorizontal: 20,
  },
  title: {
    fontSize: 24,
    fontWeight: "bold",
    marginBottom: 20,
  },
  subtitle: {
    fontSize: 20,
    fontWeight: "bold",
    marginTop: 20,
    marginBottom: 10,
  },
  scrollContainer: {
    flex: 1,
    marginBottom: 20,
    width: "100%",
  },
  card1: {
    backgroundColor: "#fff",
    borderRadius: 8,
    padding: 20,
    marginBottom: 10,
    width: "100%",
    shadowColor: "#000",
    shadowOffset: {
      width: 0,
      height: 2,
    },
    shadowOpacity: 0.25,
    shadowRadius: 3.84,
    elevation: 5,
  },
  card: {
    backgroundColor: "#fff",
    borderRadius: 8,
    padding: 20,
    marginBottom: 10,
    width: "100%",
    
  },
  name: {
    fontSize: 16,
    fontWeight: "bold",
    marginBottom: 5,
  },
  problem: {
    fontSize: 14,
    marginBottom: 5,
  },
  distanceContainer: {
    flexDirection: "row",
    alignItems: "center",
    marginBottom: 10,
  },
  distance: {
    fontSize: 12,
    color: "#666",
    marginLeft: 5,
  },
  buttonsContainer: {
    flexDirection: "row",
    justifyContent: "space-between",
  },
  button: {
    paddingVertical: 8,
    paddingHorizontal: 15,
    borderRadius: 5,
  },
  acceptButton: {
    backgroundColor: "green",
  },
  rejectButton: {
    backgroundColor: "red",
  },
  buttonText: {
    color: "#fff",
    fontWeight: "bold",
  },
  progressContainer: {
    flexDirection: "row",
    alignItems: "center",
    marginBottom: 10,
  },
  fullWidthSeparator: {
    fontWeight: "bold",
    width: "100%",
    textAlign: "center",
    color: "gray",
    marginBottom: 15,
    marginTop: -15,
  },
  progressText: {
    fontSize: 18,
    fontWeight: "bold",
    color: "green",
    fontFamily: "Arial",
    flexWrap: "wrap",
  },
  centered: {
    flex: 1,
    justifyContent: "center",
    alignItems: "center",
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

  infoItem: {
    flexDirection: "row",
    alignItems: "center",
    marginBottom: 5,
    paddingHorizontal: 10,
    paddingVertical: 5,
    borderRadius: 5,
    maxWidth: "90%",
    textAlign: "center",
  },
});

export default WorkerHome;
