import { Text, View, TextInput, searchText, TouchableOpacity, Keyboard, BackHandler } from "react-native";
import { useState, useEffect, useRef, useContext } from "react";
import * as Icon from 'react-native-feather';
import { useNavigation } from "@react-navigation/native";
import { AuthContext } from '../context/AuthContext';

export default function Search() {
  const [showRecentSearches, setShowRecentSearches] = useState(false);
  const textInputRef = useRef(null);
  const [searchText, setSearchText] = useState('');
  const { API, email } = useContext(AuthContext);
  const navigation = useNavigation();

  const handleSearchBarClick = () => {
    setShowRecentSearches(true);
    // navigation.navigate("Search");
  };
  const handleEnterPress = () => {
    if (searchText.trim() !== '') {
      // Call API here with searchText
      fetchSearchResults(searchText);
    }
  };

  const fetchSearchResults = async (query) => {
    try {
      navigation.navigate("Loading")
      const response = await fetch(`${API}/get_closest_services`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          query: query,
          email: email // Provide the user's email here
        })
      });

      if (!response.ok) {
        throw new Error('Network response was not ok');
      }

      const data = await response.json();
      // Handle API response data
      console.log("Searched result=",data);
      navigation.navigate("Search", { searchResults: data });
    } catch (error) {
      console.error('There was a problem with the fetch operation:', error);
    }
  };
  const handleSearchTextChange = (text) => {
    setSearchText(text);
    // navigation.navigate("Search");

  };


  useEffect(() => {
    const keyboardDidHideListener = Keyboard.addListener('keyboardDidHide', () => {
      setShowRecentSearches(false);
    });

    const backHandler = BackHandler.addEventListener('hardwareBackPress', () => {
      console.log("Back button pressed");
      textInputRef.current.blur();
      if (showRecentSearches) {
        setShowRecentSearches(false);

        return true;
      }
      return false;
    });

    return () => {
      keyboardDidHideListener.remove();
      backHandler.remove();
    };
  }, [showRecentSearches]);
  return (
    <View
      style={{
        flexDirection: "row",
        alignItems: "center",
        justifyContent: "space-between",
        paddingHorizontal: 4,
        paddingBottom: 2,
        marginLeft: 30,
      }}
    >
      <View
        style={{
          flexDirection: "row",
          alignItems: "center",
          flex: 1,
          backgroundColor: "#edf2f7",
          padding: 10,
          borderRadius: 50,
          borderWidth: 1,
          borderColor: "gray",
          height: 40,
        }}
      >
        <Icon.Search height={25} width={25} stroke="gray" />
        <TextInput
          ref={textInputRef}
          placeholder="Search"
          style={{ marginLeft: 10, flex: 1 }}
          onFocus={handleSearchBarClick}
          onChangeText={handleSearchTextChange}
          onSubmitEditing={handleEnterPress}
          value={searchText}
        />
        <View
          style={{
            flexDirection: "row",
            alignItems: "center",
            justifyContent: "space-between",
            borderWidth: 0,
          }}
        >
          <TouchableOpacity onPress={() => navigation.navigate("Map")}>
            <Icon.MapPin height={20} width={20} stroke="gray" />
          </TouchableOpacity>
        </View>
      </View>
    </View>
  );
};