import React, { useEffect, useMemo, useState } from "react";
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
import raspberryAPI from "../../services/raspberryAPI";

export default function RouteList({ route, navigation }) {
    const { startRouting } = raspberryAPI();

    useEffect(() => {
        //getRoutes
    });

    function addRoute() {
        startRouting(route.params).then((res) => {
            if (res) navigation.navigate("RemoteControls", route.params);
        });
    }
    return (
        <View style={styles.container}>
            <View style={styles.header}>
                <Text style={styles.headerTxt}>PATROLE</Text>
            </View>

            <View style={styles.title}>
                <Text style={styles.routesTitle}>Your Routes</Text>
            </View>

            <View>
                <Text style={styles.noRoutes}>You have no saved routes</Text>
            </View>

            <View style={styles.addContainer}>
                <TouchableOpacity style={styles.add} onPress={() => addRoute()}>
                    <View>
                        <Text
                            style={{
                                textAlign: "center",
                                lineHeight: 70,
                                color: "white",
                                fontSize: 25,
                            }}
                        >
                            Add New Route
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
        height: "20%",
        width: "100%",
        color: "white",
    },
    headerTxt: {
        position: "relative",
        color: "white",
        textAlign: "center",
        fontSize: 30,
        paddingTop: 80,
    },
    routesTitle: {
        position: "relative",
        color: "black",
        fontSize: 25,
        paddingTop: 220,
        fontWeight: "bold",
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
        height: 70,
        width: 400,
        borderRadius: 15,
        text: "white",
    },
    addContainer: {
        position: "absolute",
        bottom: 50,
    },
});
