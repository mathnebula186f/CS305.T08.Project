import * as React from "react";
import { Button, View, Text, Avatar, Image, Pressable, StyleSheet, TouchableOpacity } from "react-native";
import { createDrawerNavigator, DrawerContentScrollView, DrawerItemList } from "@react-navigation/drawer";
import { createStackNavigator } from "@react-navigation/stack";
import { createBottomTabNavigator } from '@react-navigation/bottom-tabs';
import Ionicons from 'react-native-vector-icons/Ionicons';

import { AuthContext } from "../context/AuthContext";
import Home from "../screens/User/Home";
import Map from '../screens/User/Map';
import Profile from "../screens/Profile/Profile"
import WorkerInfo from "../screens/User/WokerInfo";
import EditProfile from "../screens/Profile/EditProfile";
import RequestPage from "../screens/User/RequestPage";
import Search from "../components/Search";
import SearchResults from "../screens/User/SearchResults";
import LoadingScreen from "../screens/Loading/LoadingScreen";
import User_History from "../screens/User/User_History";
import User_InteractionPage from "../screens/User/User_InteractionPage";
import Icon from 'react-native-vector-icons/MaterialCommunityIcons';
import TimeLine from "../screens/User/TimeLine";

const Tab = createBottomTabNavigator();
const Drawer = createDrawerNavigator();
const Stack = createStackNavigator();

const CustomDrawerContent = (props) => {
  const { logout, user,imageUri } = React.useContext(AuthContext);

  return (
    <View style={styles.container}>
      <DrawerContentScrollView {...props} contentContainerStyle={styles.scrollViewContent}>
        <View style={styles.profileContainer}>
          <Image
            style={styles.profilePicture}
            source={user?.profile_pic ? { uri: imageUri } : require('../assets/Profile.jpg')}
          />
          <View style={styles.profileInfo}>
            <Text style={styles.name}>{user?.first_name} {user?.last_name}</Text>
            <Text style={styles.detail}>Age: {user?.age}</Text>
            <Text style={styles.detail}>Gender: {user?.gender}</Text>
          </View>
        </View>
        <DrawerItemList {...props} />
        <View style={styles.logoutContainer}>
          <TouchableOpacity style={styles.logoutButton} onPress={logout}>
            <Icon name="logout" size={24} color="#fff" />
            <Text style={styles.logoutText}>Logout</Text>
          </TouchableOpacity>
        </View>
      </DrawerContentScrollView>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
  },
  scrollViewContent: {
    paddingVertical: 20,
  },
  profileContainer: {
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: 20,
    paddingHorizontal: 16,
    marginTop: 20,
  },
  profilePicture: {
    width: 80,
    height: 80,
    borderRadius: 40,
    marginRight: 16,
  },
  profileInfo: {
    flex: 1,
  },
  name: {
    fontSize: 18,
    fontWeight: 'bold',
    marginBottom: 4,
  },
  detail: {
    fontSize: 16,
    color: '#666',
  },
  logoutContainer: {
    paddingHorizontal: 16,
    marginTop: 20,
  },
  logoutButton: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: '#ff5252',
    paddingVertical: 12,
    paddingHorizontal: 16,
    borderRadius: 8,
  },
  logoutText: {
    color: '#fff',
    fontSize: 16,
    fontWeight: 'bold',
    marginLeft: 8,
  },
});


function DrawerNavigator() {
  const { logout, isWorker, setIsLoading, API, email, userToken, imageUri, setImageUri, user } = React.useContext(AuthContext);
  // const { user, setUser } = React.useState(null);
  const [imageURL, setImage] = React.useState("");

  React.useEffect(() => {
    console.log("Here is the image", imageUri);
    setImage(imageUri);
  }, [imageUri]);


  return (
    <Drawer.Navigator
      screenOptions={({ navigation }) => ({
        headerRight: () => (
          <Pressable
            style={{ flexDirection: "row", alignItems: "center" }}
            onPress={navigation.toggleDrawer}
          >
            {/* <Search /> */}
            <Image
            size={5}
            className='h-12 w-12 rounded-full mr-2 '
            source={
              user?.profile_pic ? { uri: imageUri } : require("../assets/Profile.jpg")
            }
          />
          </Pressable>
        ),
        headerLeft: () => (
          <View style={{ flexDirection: "row", alignItems: "center" }}>
            <Image
              className='radius-full ml-2 w-12 h-12'
              source={require("../assets/icon.png")}
            />
            <Search />
          </View>
        ),
        headerLeftContainerStyle: { width: 250, maxWidth: 300, marginLeft: 20 },
        headerBackgroundContainerStyle: { borderWidth: 1 },
      })}
      drawerContent={(props) => <CustomDrawerContent {...props} />}
    >
      <Drawer.Screen
        name="Home Page"
        component={TabNavigator}
        options={{ headerTitleContainerStyle: { width: 0 } }}
      />
    </Drawer.Navigator>
  );
}

export default function AppStack() {
  return (
    <Stack.Navigator>
      <Stack.Screen name="DrawerNavigator" component={DrawerNavigator} options={{ headerShown: false }} />
    </Stack.Navigator>

  );
};

function TabNavigator() {
  return (
    <Tab.Navigator initialRouteName="Home"
      screenOptions={({ route }) => ({
        tabBarIcon: ({ focused, color, size }) => {
          let iconName;

          if (route.name === 'ZappFix') {
            iconName = 'flash-outline';
          } else if (route.name === 'Map') {
            iconName = 'map';
          } else if (route.name === 'EditProfile') {
            iconName = 'create-outline';
          } else if (route.name === 'WorkerInfo') {
            iconName = 'information-circle';
          } else if (route.name === 'Profile') {
            iconName = 'person-outline';
          } else if (route.name == 'User History') {
            iconName = 'albums-outline';
          }

          // You can return any component that you like here!
          return <Ionicons name={iconName} size={size} color={color} />;
        },
        headerShown: false
      })}
    >
      <Tab.Screen name="ZappFix" component={Home} options={{ headerShown: false }} />
      <Tab.Screen name="Map" component={Map} options={{ tabBarButton: () => null }} />
      <Tab.Screen name="EditProfile" component={EditProfile} options={{ tabBarButton: () => null }} />
      <Tab.Screen name="Profile" component={Profile} />
      <Tab.Screen name="WorkerInfo" component={WorkerInfo} options={{ tabBarButton: () => null }} />
      <Tab.Screen name="RequestPage" component={RequestPage} options={{ tabBarButton: () => null }} />
      <Tab.Screen name="Search" component={SearchResults} options={{ tabBarButton: () => null }} />
      <Tab.Screen name="Loading" component={LoadingScreen} options={{ tabBarButton: () => null }} />
      <Tab.Screen name="User History" component={User_History} />
      <Tab.Screen name="Interaction Page" component={User_InteractionPage} options={{ tabBarButton: () => null }} />
      <Tab.Screen name="TimeLine" component={TimeLine} options={{ tabBarButton: () => null }} />
    </Tab.Navigator>
  );
}


