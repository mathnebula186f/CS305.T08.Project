import React, { useState, useEffect } from 'react';
import { View, Text, Image, ScrollView, StyleSheet, Linking, TouchableOpacity, Button } from 'react-native';
import { useNavigation } from '@react-navigation/native';

import { AuthContext } from '../../context/AuthContext';

import adminPhoto from '../../assets/icon.png';
const AdminWorkerDetailPage = ({ route }) => {
  const { worker } = route.params;
  const navigation = useNavigation();
  const { API } = React.useContext(AuthContext);
  const [certificates, setCertificates] = useState([]);
  const [isApproved, setIsApproved] = useState(worker.verified);
  const [rating, setRating] = useState("");

  useEffect(() => {
    // Fetch certificates when the component mounts
    fetchCertificates(worker.email);
  }, []);

  const fetchCertificates = async (email) => {
    try {
      const response = await fetch(`${API}/get_certificates`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ email: email }),
      });
      const data = await response.json();
      setCertificates(data.certificates);
      console.log("here is the rating=",data.rating)
      setRating(data.rating);
    } catch (error) {
      console.error('Error fetching certificates:', error);
    }
  };

  const openPdfUrl = (pdfUrl) => {
    Linking.openURL(pdfUrl);
  };

  const changeVerificationStatus = async () => {
    try {
      const response = await fetch(`${API}/change_verification_status`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ email: worker.email }),
      });
      const data = await response.json();
      setIsApproved(!isApproved); // Toggle verification status
    } catch (error) {
      console.error('Error changing verification status:', error);
    }
  };

  return (
    <ScrollView contentContainerStyle={styles.container}>
      <View style={styles.header}>
        <Image source={adminPhoto} style={styles.workerImage} />
        <Text style={styles.workerName}>{worker.name}</Text>
        <Text>Status: {isApproved ? 'Approved' : 'Action Required'}</Text>
        {/* Add more worker details */}
        <Text>Rating: {rating}</Text>
      </View>
      {/* <View style={styles.history}>
        <Text style={styles.sectionTitle}>Task History</Text>
        {worker.history.map((item) => (
          <View key={item.id} style={styles.historyItem}>
            <Text>{item.task}</Text>
            <Text>{item.date}</Text>
          </View>
        ))}
      </View> */}
      {/* Certificates Section */}
      <View style={styles.pdfSection}>
        <Text style={styles.sectionTitle}>Certificates</Text>
        {certificates.length > 0 ? (
          certificates.map((certificate, index) => (
            <TouchableOpacity key={index} onPress={() => openPdfUrl(certificate.certificate_data)}>
              <Text style={styles.downloadLink}>{certificate.certificate_name}</Text>
            </TouchableOpacity>
          ))
        ) : (
          <Text>No certificates uploaded yet</Text>
        )}
      </View>
      {/* Approve/Disapprove Button */}
      <View style={styles.buttonContainer}>
        <Button title={isApproved ? 'Disapprove' : 'Approve'} onPress={changeVerificationStatus} />
      </View>
    </ScrollView>
  );
};

const styles = StyleSheet.create({
  container: {
    padding: 20,
  },
  header: {
    alignItems: 'center',
    marginBottom: 20,
  },
  workerImage: {
    width: 150,
    height: 150,
    borderRadius: 75,
    marginBottom: 10,
  },
  workerName: {
    fontSize: 20,
    fontWeight: 'bold',
    marginBottom: 5,
  },
  history: {
    marginBottom: 20,
  },
  sectionTitle: {
    fontSize: 18,
    fontWeight: 'bold',
    marginBottom: 10,
  },
  historyItem: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    marginBottom: 5,
  },
  pdfSection: {
    marginBottom: 20,
  },
  downloadLink: {
    color: 'blue',
    textDecorationLine: 'underline',
    marginBottom: 10,
  },
  buttonContainer: {
    flexDirection: 'row',
    justifyContent: 'center',
    marginTop: 20,
  },
});

export default AdminWorkerDetailPage;
