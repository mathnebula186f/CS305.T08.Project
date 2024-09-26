import React, { useCallback, useContext, useState } from "react";
import { View, StyleSheet} from "react-native";
import Timeline from "react-native-timeline-flatlist";
import { AuthContext } from "../../context/AuthContext";
import AsyncStorage from "@react-native-async-storage/async-storage";
import { useFocusEffect } from "@react-navigation/native";

const Worker_TimeLine = (props) => {
  const { API, logout } = useContext(AuthContext);
  const { email, service,status } = props.route.params;
  const [timelineData, setTimelineData] = useState([]);

  useFocusEffect(
    useCallback(() => {
      fetchTimeline();
    }, [email,service])
  );
  const fetchTimeline = async () => {
    try {
      const worker_email = await AsyncStorage.getItem("email");
      const response = await fetch(`${API}/fetch_timeline_details`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        credentials: "include",
        body: JSON.stringify({
          user_email: email,
          worker_email: worker_email,
          service: service,
          status:status,
        }),
      });
      const data = await response.json();
      if (response.ok) {
        setTimelineData(data.timeline_details);
      } else {
        console.error("Failed to fetch user data:", data.error);
        if (data.error === "Token expired") {
          alert(data.error);
          logout();
        }
      }
    } catch (error) {
      console.error("Error fetching user data:", error);
    }
  };
  const formatDate = (dateTime) => {
    const date = new Date(dateTime);
    const formattedDate = date.toLocaleDateString();
    const formattedTime = date.toLocaleTimeString([], {
      hour: "2-digit",
      minute: "2-digit",
    });
    const [hours, minutes] = formattedTime.split(":");
    const paddedHours = hours.padStart(2, "0");
    console.log(formattedTime);
    return `${formattedDate} ${paddedHours}:${minutes}`;
  };
  return (
    <View style={styles.container}>
      <Timeline
        data={timelineData.map((item) => ({
          ...item,
          time: item.time ? formatDate(item.time) : null,
        }))}
        circleSize={20}
        circleColor={styles.circleColor.color}
        lineColor={styles.lineColor.color}
        timeContainerStyle={styles.timeContainer}
        timeStyle={styles.time}
        titleStyle={styles.title}
        descriptionStyle={styles.description}
        innerCircle={"dot"}
        columnFormat="single-column-left"
        circleInterval={10}
      />
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: "#F5F5F5",
    paddingTop: 10,
  },
  circleColor: {
    color: "rgb(45,200,219)",
  },
  lineColor: {
    color: "rgb(45,156,219)",
  },
  timeContainer: {
    flexDirection: "row",
    alignItems: "center",
    marginTop: 5,
    paddingHorizontal: 10,
  },
  time: {
    textAlign: "center",
    backgroundColor: "#ff9797",
    color: "white",
    padding: 5,
    borderRadius: 13,
    marginRight: 8,
  },
  title: {
    backgroundColor: "#3498db",
    color: "white",
    padding: 5,
    borderRadius: 13,
    marginRight: 8,
  },
  description: {
    color: "gray",
  },
});

export default Worker_TimeLine;
