import React, { useMemo, useState } from "react";
import {
    TouchableOpacity,
    PermissionsAndroid,
    View,
    Text,
    Platform,
    SafeAreaView,
    TextInput,
} from "react-native";
import { StyleSheet } from "react-native";
import Icon from "react-native-vector-icons/FontAwesome5";

export default function ConnectBot({ navigation }) {
    return (
        <View style={styles.container}>
            <View style={styles.header}>
                <Text style={styles.headerTxt}>PATROLE</Text>
            </View>

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
                <TouchableOpacity
                    style={styles.connect}
                    onPress={() => navigation.navigate("RouteList")}
                >
                    <View>
                        <Text
                            style={{
                                textAlign: "center",
                                top: 10,
                                color: "#0864f4",
                                fontSize: 20,
                                fontWeight: "bold",
                            }}
                        >
                            PLEASE CONNET A
                        </Text>
                        <Text
                            style={{
                                textAlign: "center",
                                top: 10,
                                color: "#0864f4",
                                fontSize: 20,
                                fontWeight: "bold",
                            }}
                        >
                            PATROLBOT
                        </Text>
                        <Icon
                            style={{
                                textAlign: "center",
                                top: 40,
                            }}
                            name="wifi"
                            size={100}
                            color="#0864f4"
                        />
                    </View>
                </TouchableOpacity>
            </View>
        </View>
    );
}

const styles = StyleSheet.create({
    container: {
        flex: 1,
        backgroundColor: "white",
        alignItems: "center",
    },
    header: {
        position: "absolute",
        backgroundColor: "#0864f4",
        height: "100%",
        width: "100%",
        color: "white",
    },
    headerTxt: {
        position: "relative",
        color: "white",
        textAlign: "center",
        fontSize: 30,
        paddingTop: 300,
    },
    connect: {
        backgroundColor: "white",
        top: 400,
        height: 250,
        width: 350,
        borderRadius: 30,
        text: "#0864f4",
        borderColor: "#0864f4",
        borderStyle: "solid",
        borderWidth: 3,
    },
});
