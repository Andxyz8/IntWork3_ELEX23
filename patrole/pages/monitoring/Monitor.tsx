import React, { useMemo, useState, useEffect } from "react";
import {
    TouchableOpacity,
    PermissionsAndroid,
    View,
    Text,
    Platform,
    Image,
    SafeAreaView,
    TextInput,
} from "react-native";
import { StyleSheet } from "react-native";
import useBLE from "../../services/useBLE";
import { SvgXml } from "react-native-svg";

import * as Notifications from "expo-notifications";
import { Alert } from "react-native";
import Constants from "expo-constants";

import firebase from "@react-native-firebase/app";
import firestore from "@react-native-firebase/firestore";
import storage from "@react-native-firebase/storage";
import raspberryAPI from "../../services/raspberryAPI";

import BackgroundTimer from 'react-native-background-timer';

const firebaseConfig = {
    apiKey: "AIzaSyCQWGj9ce_s0D_Z--GMk3Zv0Ko1DZLRgxc",
    authDomain: "mall-security-robot-e52f0.firebaseapp.com",
    projectId: "mall-security-robot-e52f0",
    storageBucket: "mall-security-robot-e52f0.appspot.com",
    messagingSenderId: "339307833562",
    appId: "1:339307833562:web:3cea7b202f6a4ddfd95de3",
    measurementId: "G-8LF452GW03",
    databaseURL: "",
};

export default function Monitor({ route, navigation }) {
    const { getNotifications, getImage } = raspberryAPI();

    const logoImage = `
        <?xml version="1.0" encoding="utf-8"?>
        <svg width="147" height="86" viewBox="0 0 147 86" fill="none" xmlns="http://www.w3.org/2000/svg">
        <path d="M96.5 57C92.8802 55.9208 89.8919 53.4619 87.5352 49.6231C85.1784 45.7844 84 41.5217 84 36.835V25.55L96.5 20L109 25.55V36.835C109 41.5217 107.822 45.7844 105.465 49.6231C103.108 53.4619 100.12 55.9208 96.5 57ZM96.5 53.115C99.2083 52.0975 101.448 50.0625 103.219 47.01C104.99 43.9575 105.875 40.5658 105.875 36.835V28.0938L96.5 23.9312L87.125 28.0938V36.835C87.125 40.5658 88.0104 43.9575 89.7812 47.01C91.5521 50.0625 93.7917 52.0975 96.5 53.115Z" fill="white"/>
        <path d="M3.37766 19.68H14.2377C17.3977 19.68 18.9777 21.26 18.9777 24.42V37.26C18.9777 40.42 17.3977 42 14.2377 42H7.45766V57H3.37766V19.68ZM14.8977 36.6V25.08C14.8977 24.28 14.7777 23.78 14.5377 23.58C14.3377 23.34 13.8377 23.22 13.0377 23.22H7.45766V38.46H13.0377C13.8377 38.46 14.3377 38.36 14.5377 38.16C14.7777 37.92 14.8977 37.4 14.8977 36.6ZM36.9813 57L35.4213 47.52H27.8613L26.4813 57H22.3412L28.1613 19.68H34.7013L41.1213 57H36.9813ZM28.3412 43.98H34.8813L31.4013 22.56L28.3412 43.98ZM59.0677 19.68V23.22H53.0677V57H48.9877V23.22H42.9877V19.68H59.0677ZM67.4469 41.4V57H63.3669V19.68H74.2269C77.3869 19.68 78.9669 21.26 78.9669 24.42V36.66C78.9669 39.5 77.7269 41.06 75.2469 41.34L80.8869 57H76.4469L70.9869 41.4H67.4469ZM67.4469 23.22V37.86H73.0269C73.8269 37.86 74.3269 37.76 74.5269 37.56C74.7669 37.32 74.8869 36.8 74.8869 36V25.08C74.8869 24.28 74.7669 23.78 74.5269 23.58C74.3269 23.34 73.8269 23.22 73.0269 23.22H67.4469Z" fill="white"/>
        <path d="M118.433 53.46H127.013V57H114.353V19.68H118.433V53.46ZM135.462 53.46H145.722V57H131.322V19.68H145.302V23.22H135.462V35.82H143.502V39.36H135.462V53.46Z" fill="white"/>
        </svg>
    `;

    var imageReference = "";

    var warning = true;
    var statusTextStyle = warning
        ? styles.statusBoxTextWarning
        : styles.statusBoxText;

    const [isAlert, setIsAlert] = useState(false);
    const [imageUrl, setImageUrl] = useState(
        "https://i.pinimg.com/736x/43/ca/f7/43caf7050017bdae87b1a87551b00961.jpg"
    );
    const [imageName, setImageName] = useState("images");
    const [notificationIds, setNotificationIds] = useState([])
    const [statusMessage, setStatusMessage] = useState("Starting route")
    const [lastAruco, setLastAruco] = useState("")
    var startTime = new Date();
    var aruco_read = 0;
    const id_route = route.params.id_route
    const [currentDateTime, setCurrentDateTime] = useState(null);

    useEffect(() => {
        // Verifica se a data já foi obtida antes de buscar novamente
        if (!currentDateTime) {
          // Obtém a data e hora do momento atual
          const currentDate = new Date();
          
          // Atualiza o estado com a data e hora atual
          setCurrentDateTime(currentDate);
    
          // Pode fazer outras operações relacionadas à primeira entrada aqui
          console.log('Data obtida pela primeira vez:', currentDate);
        }
      }, [currentDateTime]);

    const handleNotifications = async (title: string) => {
        const { status } = await Notifications.getPermissionsAsync();

        if (status !== "granted") {
            Alert.alert("Você não deixou as notificações ativas");

            return;
        }

        await Notifications.scheduleNotificationAsync({
            content: {
                title: title,
                body: "Please open the app to see more about the information."
            },
            trigger: {
                seconds: 1
            }
        });
    };

    useEffect(() => {

        console.log("id_route", id_route)

        

        const yourFunction = async () => {
            
            if(isAlert == true) return;
            
            try {
                const res = await getNotifications(id_route);
                

                for (var notification of res) {
                    const data = new Date(notification.moment);
                    console.log(data)


                    // if(data > currentDateTime){
                    //     console.log("nova data")
                    //     break;
                    // } else if (data == currentDateTime) {
                    //     console.log("data igual")
                    // } else {
                    //     console.log("????")
                    // }
                    const newId = notificationIds.find(id => id == notification.id_notification);
                    if (newId) { continue; }

                    var aux = notificationIds
                    aux.push(notification.id_notification)
                    setNotificationIds(aux);

                    // console.log("notification ids")
                    console.log(notificationIds)
                    // console.log(notification)

                    if(notification.message == "person_detection"){
                        await handleNotifications("Patrole detected a person!");
                        setStatusMessage(`Person detected after ${aruco_read} ArUCo Marker.`)
                        setIsAlert(true)

                        const images = await getImage(notification.value)
                        if(images){
                            const img = images[images.length - 1]
                            const url = img.image_url

                            if(url){
                                setImageUrl(url)
                            } else {
                                setImageUrl('https://s2-valor-investe.glbimg.com/6rz0LBRXcB9VjxPjwE7b7f57enI=/0x0:2121x1414/984x0/smart/filters:strip_icc()/i.s3.glbimg.com/v1/AUTH_f035dd6fd91c438fa04ab718d608bbaa/internal_photos/bs/2019/W/b/DwpFARQielKiHhdUFi1Q/gettyimages-1126107652-1-.jpg')
                            }
                        }

                    } else if (notification.message == "movement_detection"){
                        await handleNotifications("Patrole detected movement!");
                        setStatusMessage(`Movement detected after ArUCo ${aruco_read}.`)
                        setIsAlert(true)

                        const images = await getImage(notification.value)
                        if(images){
                            const img = images[images.length - 1]
                            const url = img.image_url

                            if(url){
                                setImageUrl(url)
                            } else {
                                setImageUrl('https://imageio.forbes.com/specials-images/imageserve/5ed68e8310716f0007411996/A-black-screen--like-the-one-that-overtook-the-internet-on-the-morning-of-June-2-/960x0.jpg?format=jpg&width=960')
                            }
                        }
                    } else if (notification.message == "aruco_read"){
                        const numberAruco = Number(notification.value)
                        console.log(notification.value)
                        console.log(numberAruco)
                        console.log("entrei")
                        setLastAruco(notification.value)
                        aruco_read = numberAruco
                        console.log(lastAruco)
                        setStatusMessage(`Last ArUCo read was ${aruco_read}`)
                    } else if (notification.message == "route_execution_status"){
                        if(notification.value == "Executing"){
                            if (lastAruco == "") {
                                setStatusMessage("Executing")
                            }
                        }

                        if(notification.value == "Finalized"){
                            setStatusMessage("Finalized Route")
                        }
                    }
                    
                    break;
                    
                    
                }
                // setFlag(!flag);
            } catch (error) {
                console.error('Error fetching notifications:', error);
            }
        };
      
        const intervalId = BackgroundTimer.setInterval(() => {
            yourFunction();
            
        }, 5*1000);
      
        return () => {
          BackgroundTimer.clearInterval(intervalId);
        };
      }, [id_route, isAlert]);

    // TODO save notification id when resolved

    useEffect(() => {

        const initializeFirebase = async () => {
            if (!firebase.apps.length) {
                const firebaseApp = await firebase.initializeApp(
                    firebaseConfig
                );
            } else {
                const firebaseApp = firebase.app();
            }
        };

        initializeFirebase();
    }, []);

    const continueRoute = async () => {
        setIsAlert(false)
    };

    const stopRoute = async () => {
        setIsAlert(true)
    };

    return (
        <SafeAreaView style={styles.container}>

            <View style={styles.header}>
                <SvgXml
                    xml={logoImage}
                    width="100"
                    height="100"
                    style={styles.headerImage}
                />
            </View>

            <View style={styles.body}>
                <View>
                    <Text style={styles.statusTitle}>Status of Route 1</Text>
                </View>
                <View style={styles.statusBox}>
                    <Text
                        style={
                            isAlert
                                ? styles.statusBoxTextWarning
                                : styles.statusBoxText
                        }
                    >
                        {statusMessage}
                    </Text>
                </View>

                <View>
                    <Text style={styles.descriptionContainer}>
                        <Text style={styles.boldText}>
                            Total of ArUCo Markers:{" "}
                        </Text>
                        <Text style={styles.normalText}>27</Text>
                    </Text>
                    <Text style={styles.descriptionContainer}>
                        <Text style={styles.boldText}>Patrols done: </Text>
                        <Text style={styles.normalText}>2</Text>
                    </Text>
                    <Text style={styles.descriptionContainer}>
                        <Text style={styles.boldText}>
                            Interval between routes:{" "}
                        </Text>
                        <Text style={styles.normalText}>3</Text>
                    </Text>
                    <Text style={styles.descriptionContainer}>
                        <Text style={styles.boldText}>Number of patrols: </Text>
                        <Text style={styles.normalText}>4</Text>
                    </Text>
                    {isAlert && (
                        <View>
                            <View style={styles.imageContainer}>
                                <Image
                                    source={{ uri: imageUrl }} // Adjust the path to your image
                                    style={styles.image}
                                />
                                <Text>Image Captured by Patrole</Text>
                            </View>

                            <View style={styles.filler} />

                            <TouchableOpacity
                                onPress={stopRoute}
                                style={styles.buttonSecondary}
                            >
                                <Text style={styles.buttonTextSecondary}>
                                    Stop Alarm and Stop Route
                                </Text>
                            </TouchableOpacity>

                            <TouchableOpacity onPress={continueRoute} style={styles.buttonPrimary}>
                                <Text style={styles.buttonTextPrimary}>
                                    Stop Alarm and Continue Route
                                </Text>
                            </TouchableOpacity>
                        </View>
                    )}
                </View>
            </View>

            {/* <View style={styles.title}>
                <Text style={styles.routesTitle}>Your Routes</Text>
            </View>

            <View>
                <Text style={styles.noRoutes}>You have no saved routes</Text>
            </View> */}
        </SafeAreaView>
    );
}

const styles = StyleSheet.create({
    filler: {
        height: 50,
    },
    boldText: {
        fontWeight: "bold",
    },
    normalText: {
        fontWeight: "normal",
    },
    statusTitle: {
        color: "#3286FF", // Text color
        fontSize: 16, // Font size
        fontFamily: "SF Pro Display", // Font family
        fontWeight: "bold", // Font weight (700)
        letterSpacing: 0.35, // Letter spacing
        textTransform: "uppercase", // Text transform (uppercase)
        textAlign: "center",
        marginBottom: 10,
    },
    container: {
        flex: 1,
        backgroundColor: "white",
        alignItems: "center",
        justifyContent: "center",
    },
    headerLogo: {
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
        padding: 4,
        paddingLeft: 10,
        paddingRight: 10,
        marginBottom: 10,
        alignSelf: "stretch",
    },
    header: {
        backgroundColor: "#0065F7",
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
        paddingTop: 30,
        paddingLeft: 10,
        paddingRight: 10,
        marginBottom: 10,
        alignSelf: "stretch",
    },
    headerImage: {
        width: 100, // Set the width of your image as needed
        height: 60, // Set the height of your image as needed
    },
    body: {
        flex: 1, // This makes the body take up the remaining space
        width: "100%", // Ensure the body takes up the full width
        padding: 16, // Add padding as needed
    },
    statusBox: {
        display: "flex",
        padding: 16,
        paddingLeft: 10,
        paddingRight: 10,
        flexDirection: "column",
        alignItems: "center",
        alignSelf: "stretch",
        gap: 10,

        borderRadius: 8,
        borderWidth: 1,
        borderColor: "#3286FF",

        marginBottom: 16,
    },
    statusBoxText: {
        alignSelf: "stretch",
        // Typography
        color: "#000",
        textAlign: "center",
        fontFamily: "SF Pro Text",
        fontSize: 24,
        fontStyle: "normal",
        fontWeight: "bold",
        lineHeight: 26, // You can use a number here for line height, or use relative values like '108.333%'
        letterSpacing: -0.408,
    },
    statusBoxTextWarning: {
        alignSelf: "stretch",
        // Typography
        color: "#F00",
        textAlign: "center",
        fontFamily: "SF Pro Text",
        fontSize: 24,
        fontStyle: "normal",
        fontWeight: "bold",
        lineHeight: 26, // You can use a number here for line height, or use relative values like '108.333%'
        letterSpacing: -0.408,
    },

    descriptionContainer: {
        textAlign: "center",
        fontSize: 16,
    },

    buttonSecondary: {
        display: "flex",
        padding: 12,
        paddingLeft: 24,
        paddingRight: 24,
        flexDirection: "column",
        alignItems: "center",
        alignSelf: "stretch",

        borderRadius: 12, // Border radius
        borderWidth: 1,
        borderColor: "#FA0000", // Border color

        marginBottom: 16,
    },
    buttonTextSecondary: {
        color: "#FA0000",
        textAlign: "center",
        fontFamily: "SF Pro", // Replace with your desired font family
        fontSize: 16,
        fontStyle: "normal",
        fontWeight: "700",
        lineHeight: 28,
        letterSpacing: 0.35,
    },

    buttonPrimary: {
        display: "flex",
        padding: 12,
        paddingLeft: 24,
        paddingRight: 24,
        flexDirection: "column",
        alignItems: "center",
        alignSelf: "stretch",

        backgroundColor: "#FA0000",
        borderRadius: 12, // Border radius
        borderWidth: 1,
        borderColor: "#FA0000", // Border color
    },
    buttonTextPrimary: {
        color: "white",
        textAlign: "center",
        fontFamily: "SF Pro", // Replace with your desired font family
        fontSize: 16,
        fontStyle: "normal",
        fontWeight: "700",
        lineHeight: 28,
        letterSpacing: 0.35,
    },

    title: {
        borderBottomColor: "black",
        borderBottomWidth: 2,
        width: "90%",
    },
    noRoutes: {
        position: "relative",
        opacity: 0.5,
        color: "black",
        fontSize: 25,
        paddingTop: 220,
        fontWeight: "bold",
    },
    add: {
        backgroundColor: "#0864f4",
        top: 300,
        height: 70,
        width: 400,
        borderRadius: 15,
        text: "white",
    },

    imageContainer: {
        display: "flex",
        padding: 16,
        flexDirection: "column",
        alignItems: "center",
        alignSelf: "stretch",
        gap: 4,

        marginTop: 10,
    },
    image: {
        width: 300, // Set the width of the image
        height: 200, // Set the height of the image
    },
});
