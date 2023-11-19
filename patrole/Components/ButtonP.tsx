import React, { Component } from "react";
import { StyleSheet, View, Text, TouchableOpacity } from "react-native";

// interface ButtonProps {
//     primary: boolean;
//     txt: string;
// }

export default function ButtonP(props) {
    return (
        <>
            {props.primary ? (
                <TouchableOpacity
                    style={styles.buttonPrimary}
                    onPress={props.onPress}
                >
                    <Text style={styles.buttonTextPrimary}>{props.txt}</Text>
                </TouchableOpacity>
            ) : (
                <TouchableOpacity
                    style={styles.buttonSecondary}
                    onPress={props.onPress}
                >
                    <Text style={styles.buttonTextSecondary}>{props.txt}</Text>
                </TouchableOpacity>
            )}
        </>
    );
}

const styles = StyleSheet.create({
    buttonPrimary: {
        display: "flex",
        padding: 12,
        paddingLeft: 24,
        paddingRight: 24,
        flexDirection: "column",
        alignItems: "center",
        alignSelf: "stretch",

        backgroundColor: "#0864f4",
        borderRadius: 12, // Border radius
        marginBottom: 16,
    },
    buttonSecondary: {
        backgroundColor: "white",

        display: "flex",
        padding: 12,
        paddingLeft: 24,
        paddingRight: 24,
        flexDirection: "column",
        alignItems: "center",
        alignSelf: "stretch",

        borderRadius: 12, // Border radius
        borderWidth: 1,
        borderColor: "#0864f4", // Border color
        marginBottom: 16,
    },

    buttonTextPrimary: {
        color: "white",
        textAlign: "center",
        fontFamily: "SF Pro", // Replace with your desired font family
        fontSize: 16,
        fontStyle: "normal",
        fontWeight: "700",
        lineHeight: 28,
        letterSpacing: 0.35,
    },
    buttonTextSecondary: {
        color: "#0864f4",
        textAlign: "center",
        fontFamily: "SF Pro", // Replace with your desired font family
        fontSize: 16,
        fontStyle: "normal",
        fontWeight: "700",
        lineHeight: 28,
        letterSpacing: 0.35,
    },
});
