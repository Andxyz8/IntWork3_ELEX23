import React, { useMemo, useState } from "react";
import {
    TouchableOpacity,
    View,
    Text,
    Alert,
    Modal,
    Pressable,
    Image,
} from "react-native";
import { StyleSheet } from "react-native";
import Icon from "react-native-vector-icons/FontAwesome5";
import raspberryAPI from "../../services/raspberryAPI";
import HeaderP from "../../Components/HeaderP";

export default function ConnectBot({ navigation }) {
    const [connecting, setConnecting] = useState(false);

    const { getConnection } = raspberryAPI();

    const t = () => {
        setConnecting(true);
        getConnection().then((address) => {
            setConnecting(false);
            if (address != null) navigation.navigate("RouteList", address);
        });
    };

    return (
        <View style={styles.container}>
            <View style={styles.header}>
                <HeaderP text={false} txt1={""} txt2={""} />
            </View>
            {connecting ? (
                <View style={styles.connect}>
                    <Text
                        style={{
                            textAlign: "center",
                            top: 10,
                            color: "#0864f4",
                            fontSize: 20,
                            fontWeight: "bold",
                        }}
                    >
                        SEARCHING FOR
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
                    <Image
                        style={{ width: 320, height: 150, top: 20 }}
                        source={require("../../assets/loading-load.gif")}
                    ></Image>
                </View>
            ) : (
                <View>
                    <TouchableOpacity
                        style={styles.connect}
                        onPress={() => t()}
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
            )}
        </View>
    );
}

const styles = StyleSheet.create({
    container: {
        flex: 1,
        backgroundColor: "rgba(0,0,0,0.5)",
        alignItems: "center",
    },
    header: {
        paddingTop: 200,
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
