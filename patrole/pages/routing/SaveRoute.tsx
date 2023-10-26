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

export default function SaveRoute({ navigation }) {
    return (
        <View style={styles.container}>
            <View style={styles.header}>
                <Text style={styles.headerTxt1}>STATUS OF SETUP</Text>
                <Text style={styles.headerTxt2}>Routing Completed</Text>
            </View>

            <View style={styles.config}>
                <Text style={{ fontSize: 20 }}> Name of the Route: </Text>
                <TextInput style={styles.input} onChangeText={() => {}} />

                <Text style={{ fontSize: 20 }}>Interval between routes</Text>
                <TextInput
                    style={styles.input}
                    onChangeText={() => {}}
                    keyboardType="numeric"
                />

                <Text style={{ fontSize: 20 }}> Number of patrols: </Text>
                <TextInput
                    style={styles.input}
                    onChangeText={() => {}}
                    keyboardType="numeric"
                />
            </View>

            <View>
                <TouchableOpacity
                    style={styles.save}
                    onPress={() => navigation.navigate("RouteList")}
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
                            Save Route
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
                            Cancel
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
        backgroundColor: "white",
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
    config: {
        position: "relative",
        top: 300,
        right: 30,
    },
    input: {
        height: 40,
        margin: 12,
        width: 300,
        borderWidth: 1,
        borderColor: "#0864f4",
        borderRadius: 10,
        padding: 10,
    },
    save: {
        backgroundColor: "#0864f4",
        top: 470,
        height: 70,
        width: 400,
        borderRadius: 15,
        text: "white",
    },
    cancel: {
        backgroundColor: "white",
        top: 490,
        height: 70,
        width: 400,
        borderRadius: 15,
        text: "#0864f4",
        borderColor: "#0864f4",
        borderStyle: "solid",
        borderWidth: 3,
    },
});
