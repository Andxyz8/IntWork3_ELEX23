import React, { useMemo, useState } from "react";
import { TouchableOpacity, View, Text } from "react-native";
import { StyleSheet } from "react-native";

export default function StartRouting({ route, navigation }) {
    return (
        <View style={styles.container}>
            <View style={styles.header}>
                <Text style={styles.headerTxt1}>STATUS OF SETUP</Text>
                <Text style={styles.headerTxt2}>Ready for configuration</Text>
            </View>

            <View style={styles.text}>
                <Text
                    style={{
                        textAlign: "center",
                        fontSize: 20,
                        marginBottom: 30,
                    }}
                >
                    Before starting the routing process, don't forget to print
                    the ARUCO tags on the size of an A4 page, so the PatroBot
                    can scan it.
                </Text>
                <Text
                    style={{
                        textAlign: "center",
                        fontSize: 20,
                    }}
                >
                    <Text style={{ fontWeight: "bold" }}>Reminder:</Text> The
                    initial ARUCO must be read at the{" "}
                    <Text style={{ fontWeight: "bold" }}>start and end</Text> of
                    the route.
                </Text>
            </View>

            <TouchableOpacity
                style={styles.start}
                onPress={() =>
                    navigation.navigate("RemoteControls", route.params)
                }
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
                        Start Routing
                    </Text>
                </View>
            </TouchableOpacity>

            <TouchableOpacity
                style={styles.cancel}
                onPress={() => navigation.navigate("RouteList", route.params)}
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
    start: {
        backgroundColor: "#0864f4",
        top: 585,
        height: 70,
        width: 400,
        borderRadius: 15,
        text: "white",
    },
    text: {
        top: 380,
    },
    cancel: {
        backgroundColor: "white",
        top: 605,
        height: 70,
        width: 400,
        borderRadius: 15,
        text: "#0864f4",
        borderColor: "#0864f4",
        borderStyle: "solid",
        borderWidth: 3,
    },
});
