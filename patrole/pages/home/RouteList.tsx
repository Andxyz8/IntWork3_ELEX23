import React, { useEffect, useMemo, useState } from "react";
import {
    TouchableOpacity,
    PermissionsAndroid,
    View,
    Text,
    Platform,
    SafeAreaView,
    TextInput,
    ScrollView,
} from "react-native";
import { StyleSheet } from "react-native";
import raspberryAPI from "../../services/raspberryAPI";
import { ScrollableComponent } from "react-native-keyboard-aware-scroll-view";
import { useFocusEffect } from "@react-navigation/native";

interface Route {
    id_route: number;
    title: string;
    description: string;
    status: boolean;
    number_repeats: number;
    created_at: Date;
    interval_between_repeats: number;
}

export default function RouteList({ route, navigation }) {
    const { startRouting, getRoutes, startRouteExct } = raspberryAPI();

    const [routes, setRoutes] = useState<Route[]>([]);
    const [flag, setFlag] = useState(false);

    const address = route.params;

    useFocusEffect(
        React.useCallback(() => {
            getRoutes().then((res) => {
                setRoutes(res);
                setFlag(!flag);
            });
        }, [])
    );

    useEffect(() => {}, [flag]);

    function addRoute() {
        startRouting(route.params).then((res) => {
            if (res) {
                setRoutes([]);
                setFlag(!flag);
                navigation.navigate("RemoteControls", route.params);
            }
        });
    }

    function executeRoute(id_route: any) {
        startRouteExct(address, id_route).then((res) => {
            setRoutes([]);
            setFlag(!flag);
            if (res) navigation.navigate("Monitor", route.params);
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

            <ScrollView style={styles.scrollView}>
                {routes.length > 0 ? (
                    <>
                        {routes.map((route) => {
                            return (
                                <View
                                    key={route.id_route}
                                    style={styles.routeContainer}
                                >
                                    <TouchableOpacity
                                        onPress={() =>
                                            executeRoute(route.id_route)
                                        }
                                        style={styles.routeText}
                                    >
                                        <Text style={styles.routeTitle}>
                                            {route.title}
                                        </Text>
                                        <Text>
                                            Interval between routes:{" "}
                                            {route.interval_between_repeats}
                                        </Text>
                                        <Text>
                                            Number of patrols:{" "}
                                            {route.number_repeats}
                                        </Text>
                                    </TouchableOpacity>
                                </View>
                            );
                        })}
                    </>
                ) : (
                    <View>
                        <Text style={styles.noRoutes}>
                            You have no saved routes
                        </Text>
                    </View>
                )}
            </ScrollView>

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
        textAlign: "center",
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
    routeContainer: {
        marginTop: 10,
        marginHorizontal: 20,
        borderRadius: 10,
        borderColor: "black",
        borderStyle: "solid",
        borderWidth: 3,
        text: "white",
    },
    routeText: {
        marginHorizontal: 10,
        paddingBottom: 3,
    },
    routeTitle: {
        fontSize: 20,
        fontWeight: "bold",
    },
    scrollView: {
        width: `${100}%`,
        maxHeight: `${55}%`,
    },
});
