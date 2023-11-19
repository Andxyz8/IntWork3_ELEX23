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
import HeaderP from "../../Components/HeaderP";
import ButtonP from "../../Components/ButtonP";

interface Route {
    id_route: number;
    title: string;
    description: string;
    status: boolean;
    number_repeats: number;
    created_at: Date;
    interval_between_repeats: number;
    total_readed_aruco_markers: number;
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

    function executeRoute(exectRoute: Route) {
        startRouteExct(address, exectRoute.id_route);
        setRoutes([]);
        setFlag(!flag);
        navigation.navigate("Monitor", {
            address: route.params,
            id_route: exectRoute.id_route,
            number_patrols: exectRoute.number_repeats,
            interval_patrols: exectRoute.interval_between_repeats,
            total_arucos: exectRoute.total_readed_aruco_markers,
        });
    }
    return (
        <View style={styles.container}>
            <HeaderP text={false} txt1={""} txt2={""} />

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
                                        onPress={() => executeRoute(route)}
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
                <ButtonP
                    primary={true}
                    txt={"Add New Route"}
                    onPress={() => addRoute()}
                />
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
    routesTitle: {
        position: "relative",
        color: "black",
        fontSize: 25,
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
        flex: 1, // This makes the body take up the remaining space
        width: "100%", // Ensure the body takes up the full width
        padding: 20, // Add padding as needed
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
        maxHeight: `${65}%`,
    },
});
