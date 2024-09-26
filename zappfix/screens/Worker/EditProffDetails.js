import React, { useState,useEffect,useContext } from 'react';
import { ScrollView, StyleSheet, View, Text, TouchableOpacity, Image } from 'react-native';
import * as DocumentPicker from 'expo-document-picker';
import * as FileSystem from 'expo-file-system';
import { WebView } from 'react-native-webview';
import {
    Dropdown,
    GroupDropdown,
    MultiselectDropdown,
} from 'sharingan-rn-modal-dropdown';
import Icon from 'react-native-vector-icons/MaterialIcons';

import { AuthContext } from '../../context/AuthContext';
import LoadingScreen from '../Loading/LoadingScreen';





const UserProfile = () => { 
    // Sample user data (replace with actual data)
    const [user, setUser] = useState(null);
    const { logout, isWorker, setIsLoading, API,email ,userToken} = useContext(AuthContext);
    useEffect(() => {
        fetchUserData();
      }, []);
    
      
      const fetchUserData = async () => {
        try {
          
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
          }
        } catch (error) {
          console.error('Error fetching user data:', error);
        } finally {
          
        }
      };

    return (
        <View style={styles.userProfileContainer}>
        {user && (<View><Image source={require('../../assets/Profile.jpg')} style={styles.avatar} />
        {/* <Image source={require('../assets/Profile.jpg')} style={styles.profileImage} /> */}
        <View style={styles.userInfo}>
            <Text style={styles.name}>{user.first_name}{user.last_name}</Text>
            <Text style={styles.details}>{user.age} years old</Text>
            <Text style={styles.details}>{user.address}</Text>
            
        </View>
</View>)}
        <View style={styles.reloadButtonContainer}>
              <TouchableOpacity style={styles.reloadButton} onPress={fetchUserData}>
                <Icon name="refresh" size={20} color="#fff" />
              </TouchableOpacity>
            </View>
            
        </View>
    );
};

const EditProffDetails = ({ navigation }) => {
    const [valueMS, setValueMS] = useState([]);
    const [pdfUri, setPdfUri] = useState(null);
    const [pdfName,setPdfName]=useState('');
    const [pdfContent, setPdfContent] = useState('');
    const [objOfPdfs, setobjOfPdfs] = useState({});
    const {API, email, userToken}=useContext(AuthContext);
    const [progress,setProgress]=useState(false);
    const data = [
        {
            value: '1',
            label: 'Salon',
            avatarSource: {
                uri: 'https://img.icons8.com/color/344/circled-user-male-skin-type-5.png',
            },
        },
        {
            value: '2',
            label: 'Barber',
            avatarSource: {
                uri: 'https://img.icons8.com/color/344/circled-user-male-skin-type-5.png',
            },
        },
        {
            value: '3',
            label: 'Painter',
            avatarSource: {
                uri: 'https://img.icons8.com/color/344/circled-user-male-skin-type-5.png',
            },
        },
        {
            value: '4',
            label: 'Home Clean',
            avatarSource: {
                uri: 'https://img.icons8.com/color/344/circled-user-male-skin-type-5.png',
            },
        },
        {
            value: '5',
            label: 'Carpentry',
            avatarSource: {
                uri: 'https://img.icons8.com/color/344/circled-user-male-skin-type-5.png',
            },
        },
    ];

    const selectPdf = async () => {
        try {
            const result = await DocumentPicker.getDocumentAsync({
                copyToCacheDirectory : true,
                multiple: true,
                type: "*/*",
            });
            // fetchUserData();
            console.log("RESULT : ", result)

            if (result.canceled === false) {
                console.log('Document picked:', result.assets[0].uri)
                setPdfUri(result.assets[0].uri);
                setPdfName(result.assets[0].name);
                setobjOfPdfs({...objOfPdfs,[result.assets[0].name]:result.assets[0].uri});
                // console.log("PDF URI : ", result.assets[0].uri)
                const pdfContent = await FileSystem.readAsStringAsync(result.assets[0].uri, {
                    encoding: FileSystem.EncodingType.Base64,
                });
                // console.log("PDF CONTENT : ", pdfContent)
                setPdfContent(pdfContent);
                alert("Uploaded")
                // console.log(result.assets[0].uri);
            } else {
                console.log('Document picking cancelled');
            }
        } catch (error) {
            console.log('Error picking document:', error);
        }
    };
    const handleSubmit = async () => {
        setProgress(true);
        const mapping={"1":"Salon","2":"Barber","3":"Painter","4":"Home Clean","5":"Carpentry"};
        const serviceNames = valueMS.map(item => mapping[item]);

        // console.log("email=",email)
        
        const resp=await fetch(`${API}/update_services`, {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
            },
            credentials: 'include',
            body: JSON.stringify({ email: email, services: serviceNames, token: userToken}),
          });
          const data = await resp.json();
          if (!resp.ok){
            alert(data.error);
          } 
          else {
            alert("Service Updated Successfully");
          }
        const resp2=await fetch(`${API}/upload_certificate`, {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
            },
            credentials: 'include',
            body: JSON.stringify({ email: email, certificate: pdfContent, certificate_name: pdfName, token: userToken}),
          });
        const data2 = await resp2.json();
        if (!resp2.ok){
            alert(data2.error);
        }
        else{
            alert("Certificates Updated Successfully");
        }
        setProgress(false);
    }
    return (
        <View style={styles.container}>
            <ScrollView>
                <UserProfile />
                <View style={styles.contentContainer}>
                    <Text style={styles.title} className="pt-2 text-gray-900">Edit Professional Details</Text>
                    <MultiselectDropdown
                        label="Select Skills"
                        data={data}
                        enableAvatar
                        chipType="outlined"
                        value={valueMS}
                        // onChange={setValueMS}
                        onChange={(e)=>{console.log(e); setValueMS(e); console.log(valueMS)}}
                        style={styles.dropdown}
                    />
                    <TouchableOpacity style={styles.uploadButton} onPress={selectPdf}>
                        <Text style={styles.uploadButtonText}>Upload PDF</Text>
                    </TouchableOpacity>
                    {Object.entries(objOfPdfs).map(([pdfName, pdfUri])=>(
                        <View style={styles.pdfContainer}>
                            <Text style={styles.pdfTitle}>{pdfName}</Text>
                            <WebView
                                source={{ uri: pdfUri }}
                                allowFileAccess
                                style={styles.pdf}
                            />
                        </View>
                    ))}
                </View>
            </ScrollView>
            {progress && <LoadingScreen />}
            <TouchableOpacity style={styles.uploadButton} onPress={handleSubmit}>
                <Text style={styles.uploadButtonText}>Submit</Text>
            </TouchableOpacity>
        </View>
    );
};

export default EditProffDetails;

const styles = StyleSheet.create({
    dropdown: {
        backgroundColor: '#fff', borderColor: '#ccc', borderWidth: 1 
    },
    container: {
        flex: 1,
        backgroundColor: '#fff',
    },
    contentContainer: {
        paddingVertical: 30,
        paddingHorizontal: 20,
    },
    title: {
        fontSize: 25,
        fontWeight: 'bold',
        marginBottom: 20,
    },
    uploadButton: {
        backgroundColor: '#2196F3',
        padding: 15,
        borderRadius: 8,
        marginTop: 20,
        alignItems: 'center',
    },
    uploadButtonText: {
        color: 'white',
        fontSize: 16,
        fontWeight: 'bold',
    },
    pdfContainer: {
        marginTop: 20,
        alignItems: 'center',
    },
    pdfTitle: {
        fontSize: 18,
        fontWeight: 'bold',
        marginBottom: 10,
    },
    pdf: {
        width: 300,
        height: 200,
    },
    userProfileContainer: {
        flexDirection: 'row',
        alignItems: 'center',
        marginBottom: 10,
        paddingHorizontal: 20,
        paddingTop: 25
    },
    avatar: {
        width: 80,
        height: 80,
        borderRadius: 40,
        marginRight: 20,
    },
    userInfo: {
        flex: 1,
    },
    name: {
        fontSize: 24,
        fontWeight: 'bold',
        marginBottom: 5,
    },
    details: {
        fontSize: 16,
        color: '#888',
    },
    reloadButtonContainer: {
        position: 'absolute',
        bottom: -10,
        right: 10,
      },
      reloadButton: {
        backgroundColor: '#3498db',
        borderRadius: 50,
        width: 50,
        height: 50,
        alignItems: 'center',
        justifyContent: 'center',
      },
});
