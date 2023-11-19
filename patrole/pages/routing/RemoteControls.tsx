import React, { useEffect, useMemo, useState } from "react";
import { StyleSheet } from "react-native";
import { TouchableOpacity, View, Text } from "react-native";

import Icon from "react-native-vector-icons/FontAwesome";
import raspberryAPI from "../../services/raspberryAPI";
import HeaderP from "../../Components/HeaderP";
import ButtonP from "../../Components/ButtonP";

export default function RemoteControls({ route, navigation }) {
    const {
        sendCommandFoward,
        sendCommandLeft,
        sendCommandRight,
        sendCommandRead,
    } = raspberryAPI();
    const address = route.params;
    const [controls, setControls] = useState(false);
    const [firstAruco, setFirstAruco] = useState(null);

    function sendControl(command) {
        if (command == "UP") {
            sendCommandFoward(address).then((res) => {
                setControls(!res);
            });
        } else if (command == "RIGHT") {
            sendCommandRight(address).then((res) => {
                console.log(res);
                setControls(!res);
            });
        } else if (command == "LEFT") {
            sendCommandLeft(address).then((res) => {
                setControls(!res);
            });
        } else if (command == "READ") {
            sendCommandRead(address).then((res) => {
                if (firstAruco == res) setControls(true);
                else if (firstAruco == null && res != null) setFirstAruco(res);
            });
        }
    }

    return (
        <View style={styles.container}>
            <HeaderP text={true} txt1="STATUS OF SETUP" txt2="Routing" />

            <View style={styles.upContainer}>
                <TouchableOpacity
                    style={styles.up}
                    disabled={controls}
                    onPress={() => sendControl("UP")}
                >
                    <View>
                        <Icon
                            style={{ textAlign: "center", lineHeight: 120 }}
                            name="arrow-up"
                            size={50}
                            color="white"
                        />
                    </View>
                </TouchableOpacity>
            </View>

            <View style={styles.rightContainer}>
                <TouchableOpacity
                    style={styles.right}
                    disabled={controls}
                    onPress={() => sendControl("RIGHT")}
                >
                    <View>
                        <Icon
                            style={{ textAlign: "center", lineHeight: 120 }}
                            name="arrow-right"
                            size={50}
                            color="white"
                        />
                    </View>
                </TouchableOpacity>
            </View>
            <View style={styles.leftContainer}>
                <TouchableOpacity
                    style={styles.left}
                    disabled={controls}
                    onPress={() => sendControl("LEFT")}
                >
                    <View>
                        <Icon
                            style={{ textAlign: "center", lineHeight: 120 }}
                            name="arrow-left"
                            size={50}
                            color="white"
                        />
                    </View>
                </TouchableOpacity>
            </View>

            <View style={styles.cancelContainer}>
                <ButtonP
                    primary={false}
                    txt={"Cancel Process"}
                    onPress={() =>
                        navigation.navigate("RouteList", route.params)
                    }
                />
            </View>
            {!controls ? (
                <View style={styles.readContainer}>
                    <ButtonP
                        primary={true}
                        txt={"Read ArUco"}
                        onPress={() => sendControl("READ")}
                    />
                </View>
            ) : (
                <View style={styles.readContainer}>
                    <ButtonP
                        primary={true}
                        txt={"Save Route"}
                        onPress={() =>
                            navigation.navigate("SaveRoute", route.params)
                        }
                    />
                </View>
            )}
        </View>
    );
}

const styles = StyleSheet.create({
    container: {
        flex: 1,
        backgroundColor: "#fff",
        alignItems: "center",
    },
    controls: {
        //position: "absolute",
        flex: 1, // This makes the body take up the remaining space
        width: "100%", // Ensure the body takes up the full width
        padding: 16, // Add padding as needed
    },
    up: {
        backgroundColor: "#0864f4",
        height: 120,
        width: 120,
        borderRadius: 60,
    },
    right: {
        backgroundColor: "#0864f4",
        height: 120,
        width: 120,
        borderRadius: 60,
    },
    left: {
        backgroundColor: "#0864f4",
        height: 120,
        width: 120,
        borderRadius: 60,
    },
    read: {
        backgroundColor: "#0864f4",
        height: 70,
        width: 400,
        borderRadius: 15,
        text: "white",
    },
    cancel: {
        backgroundColor: "white",
        height: 70,
        width: 400,
        borderRadius: 15,
        text: "#0864f4",
        borderColor: "#0864f4",
        borderStyle: "solid",
        borderWidth: 3,
    },
    upContainer: {
        position: "absolute",
        bottom: 450,
    },
    leftContainer: {
        position: "absolute",
        bottom: 300,
        left: 50,
    },
    rightContainer: {
        position: "absolute",
        bottom: 300,
        right: 50,
    },
    readContainer: {
        position: "absolute",
        bottom: 130,
        width: `${90}%`,
    },
    cancelContainer: {
        position: "absolute",
        bottom: 50,
        width: `${90}%`,
    },
});
