import React, { useMemo, useState } from "react";
import {
    TouchableOpacity,
    PermissionsAndroid,
    View,
    Text,
    Platform,
    SafeAreaView,
} from "react-native";

import useBLE from "../useBLE";

import { Button } from "react-native-elements";

import { BleManager, Device } from "react-native-ble-plx";
import { LogBox } from "react-native";
import DeviceModal from "../DeviceConnectionModal";
import { styles } from "../Styles/styles";
import Icon from "react-native-vector-icons/FontAwesome";

LogBox.ignoreLogs(["new NativeEventEmitter"]); // Ignore log notification by message
LogBox.ignoreAllLogs(); //Ignore all log notifications

const bleManager = new BleManager();

export default function App() {
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
        <View>
            {/* <SafeAreaView>
                <TouchableOpacity onPress={getDevices} style={styles.ctaButton}>
                    <Text style={styles.ctaButtonText}>
                        {"SEARCH FOR DEVICES"}
                    </Text>
                </TouchableOpacity>
                <View>
                    {test.map((device) => (
                        <View key={device.name}>
                            <View>
                                <Text>{device.name}</Text>
                                <Text>{JSON.stringify(device)}</Text>
                            </View>
                            <View style={styles.spaces}></View>
                        </View>
                    ))}
                </View>
            </SafeAreaView> */}
            <View style={styles.header}>
                <Text style={styles.headerTxt1}>STATUS OF SETUP</Text>
                <Text style={styles.headerTxt2}>Routing</Text>
            </View>

            <View style={styles.controls}>
                <View style={styles.up}>
                    <Icon
                        style={{ textAlign: "center", lineHeight: 120 }}
                        name="arrow-up"
                        size={50}
                        color="white"
                    />
                </View>
                <View style={styles.right}>
                    <Icon
                        style={{ textAlign: "center", lineHeight: 120 }}
                        name="arrow-right"
                        size={50}
                        color="white"
                    />
                </View>
                <View style={styles.left}>
                    <Icon
                        style={{ textAlign: "center", lineHeight: 120 }}
                        name="arrow-left"
                        size={50}
                        color="white"
                    />
                </View>
                <View style={styles.read}>
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
                <View style={styles.cancel}>
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
            </View>
        </View>
    );
}
