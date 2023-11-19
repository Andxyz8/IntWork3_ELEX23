import React, { useMemo, useState } from "react";
import { View, Text, SafeAreaView, TextInput, ScrollView } from "react-native";
import { StyleSheet } from "react-native";
import raspberryAPI from "../../services/raspberryAPI";
import HeaderP from "../../Components/HeaderP";
import ButtonP from "../../Components/ButtonP";

export default function SaveRoute({ route, navigation }) {
    const [name, setName] = useState("");
    const [interval, setInterval] = useState("");
    const [patrols, setPatrols] = useState("");
    const { endRouting } = raspberryAPI();
    const address = route.params;

    function saveRoute() {
        console.log(name, interval, patrols);
        let body = {
            title: name,
            interval_between_repeats: interval,
            n_repeats: patrols,
            description: "test",
        };
        endRouting(address, body).then((res) => {
            if (res) navigation.navigate("RouteList", route.params);
            else console.log("erro");
        });
    }

    return (
        <SafeAreaView style={styles.container}>
            <HeaderP
                text={true}
                txt1="STATUS OF SETUP"
                txt2="Routing Completed"
            />

            <ScrollView style={styles.scrollView}>
                <View style={styles.config}>
                    <Text style={{ fontSize: 20 }}> Name of the Route: </Text>
                    <TextInput
                        style={styles.input}
                        onChangeText={(nme) => {
                            setName(nme);
                        }}
                    />

                    <Text style={{ fontSize: 20 }}>
                        Interval between routes
                    </Text>
                    <TextInput
                        style={styles.input}
                        onChangeText={(interv) => {
                            setInterval(interv);
                        }}
                        keyboardType="numeric"
                    />

                    <Text style={{ fontSize: 20 }}> Number of patrols: </Text>
                    <TextInput
                        style={styles.input}
                        onChangeText={(patr) => {
                            setPatrols(patr);
                        }}
                        keyboardType="numeric"
                    />

                    <View style={styles.filler} />
                    <ButtonP
                        primary={true}
                        txt={"Save"}
                        onPress={() => saveRoute()}
                    />

                    <ButtonP
                        primary={false}
                        txt={"Cancel"}
                        onPress={() =>
                            navigation.navigate("RouteList", route.params)
                        }
                    />
                </View>
            </ScrollView>
        </SafeAreaView>
    );
}

const styles = StyleSheet.create({
    scrollView: {
        width: `${100}%`,
    },
    container: {
        flex: 1,
        backgroundColor: "white",
        alignItems: "center",
        justifyContent: "center",
    },
    header: {
        width: "100%",
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
        flex: 1, // This makes the body take up the remaining space
        width: "100%", // Ensure the body takes up the full width
        padding: 16, // Add padding as needed
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

    filler: {
        height: 200,
    },
});
