import React, { useMemo, useState } from "react";
import { StyleSheet } from "react-native";
import { TouchableOpacity, View, Text } from "react-native";

import useBLE from "../../useBLE";

import { BleManager, Device } from "react-native-ble-plx";
import { LogBox } from "react-native";
import Icon from "react-native-vector-icons/FontAwesome";

LogBox.ignoreLogs(["new NativeEventEmitter"]); // Ignore log notification by message
LogBox.ignoreAllLogs(); //Ignore all log notifications

const bleManager = new BleManager();

export default function RemoteControls({ navigation }) {
    const {
        requestPermissions,
        scanForPeripherals,
        // connectToDevice,
        // connectedDevice,
        // heartRate,
        // disconnectFromDevice,
    } = useBLE();
    const [isModalVisible, setIsModalVisible] = useState<boolean>(false);
    const [flag, setFlag] = useState<boolean>(false);
    const [test, setTest] = useState<any[]>([]);
    const [allDevices, setAllDevices] = useState<Device[]>([]);

    const getDevices = () => {
        requestPermissions().then((permission: boolean) => {
            if (permission) {
                scanForPeripherals().then((d) => {
                    setTest(d);
                    setFlag(!flag);
                });
            }
        });
    };

    return (
        <View style={styles.container}>
            <View style={styles.header}>
                <Text style={styles.headerTxt1}>STATUS OF SETUP</Text>
                <Text style={styles.headerTxt2}>Routing</Text>
            </View>

            <View style={styles.controls}>
                <TouchableOpacity
                    style={styles.up}
                    onPress={() => console.log("UP")}
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

                <TouchableOpacity
                    style={styles.right}
                    onPress={() => console.log("RIGHT")}
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

                <TouchableOpacity
                    style={styles.left}
                    onPress={() => console.log("LEFT")}
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
                <TouchableOpacity
                    style={styles.read}
                    onPress={() => navigation.navigate("SaveRoute")}
                >
                    <View>
                        <Text
                            style={{
                                textAlign: "center",
                                lineHeight: 70,
                                color: "white",
                                fontSize: 25,
                            }}
                        >
                            Read ArUco
                        </Text>
                    </View>
                </TouchableOpacity>

                <TouchableOpacity
                    style={styles.cancel}
                    onPress={() => navigation.navigate("RouteList")}
                >
                    <View>
                        <Text
                            style={{
                                textAlign: "center",
                                lineHeight: 70,
                                color: "#0864f4",
                                fontSize: 25,
                            }}
                        >
                            Cancel Process
                        </Text>
                    </View>
                </TouchableOpacity>
            </View>
        </View>
    );
}

const styles = StyleSheet.create({
    container: {
        flex: 1,
        backgroundColor: "#fff",
        alignItems: "center",
    },
    header: {
        position: "absolute",
        backgroundColor: "#0864f4",
        height: "30%",
        width: "100%",
        color: "white",
    },
    headerTxt1: {
        position: "relative",
        color: "rgba(255,255,255, 0.7)",
        textAlign: "center",
        fontSize: 20,
        paddingTop: 120,
    },
    headerTxt2: {
        position: "relative",
        color: "white",
        textAlign: "center",
        paddingTop: 20,
        fontSize: 20,
    },
    controls: {
        //position: "absolute",
        alignItems: "center",
    },
    up: {
        backgroundColor: "#0864f4",
        top: 400,
        height: 120,
        width: 120,
        borderRadius: 60,
    },
    right: {
        backgroundColor: "#0864f4",
        top: 430,
        left: 100,
        height: 120,
        width: 120,
        borderRadius: 60,
    },
    left: {
        backgroundColor: "#0864f4",
        top: 310,
        right: 100,
        height: 120,
        width: 120,
        borderRadius: 60,
    },
    read: {
        backgroundColor: "#0864f4",
        top: 380,
        height: 70,
        width: 400,
        borderRadius: 15,
        text: "white",
    },
    cancel: {
        backgroundColor: "white",
        top: 400,
        height: 70,
        width: 400,
        borderRadius: 15,
        text: "#0864f4",
        borderColor: "#0864f4",
        borderStyle: "solid",
        borderWidth: 3,
    },
});
