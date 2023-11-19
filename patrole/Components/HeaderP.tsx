import React from "react";
import { StyleSheet, View, Text } from "react-native";
import { SvgXml } from "react-native-svg";

interface HeaderProps {
    text: boolean;
    txt1: string;
    txt2: string;
}

export default function HeaderP(props: HeaderProps) {
    const logoImage = `
    <?xml version="1.0" encoding="utf-8"?>
    <svg width="147" height="86" viewBox="0 0 147 86" fill="none" xmlns="http://www.w3.org/2000/svg">
    <path d="M96.5 57C92.8802 55.9208 89.8919 53.4619 87.5352 49.6231C85.1784 45.7844 84 41.5217 84 36.835V25.55L96.5 20L109 25.55V36.835C109 41.5217 107.822 45.7844 105.465 49.6231C103.108 53.4619 100.12 55.9208 96.5 57ZM96.5 53.115C99.2083 52.0975 101.448 50.0625 103.219 47.01C104.99 43.9575 105.875 40.5658 105.875 36.835V28.0938L96.5 23.9312L87.125 28.0938V36.835C87.125 40.5658 88.0104 43.9575 89.7812 47.01C91.5521 50.0625 93.7917 52.0975 96.5 53.115Z" fill="white"/>
    <path d="M3.37766 19.68H14.2377C17.3977 19.68 18.9777 21.26 18.9777 24.42V37.26C18.9777 40.42 17.3977 42 14.2377 42H7.45766V57H3.37766V19.68ZM14.8977 36.6V25.08C14.8977 24.28 14.7777 23.78 14.5377 23.58C14.3377 23.34 13.8377 23.22 13.0377 23.22H7.45766V38.46H13.0377C13.8377 38.46 14.3377 38.36 14.5377 38.16C14.7777 37.92 14.8977 37.4 14.8977 36.6ZM36.9813 57L35.4213 47.52H27.8613L26.4813 57H22.3412L28.1613 19.68H34.7013L41.1213 57H36.9813ZM28.3412 43.98H34.8813L31.4013 22.56L28.3412 43.98ZM59.0677 19.68V23.22H53.0677V57H48.9877V23.22H42.9877V19.68H59.0677ZM67.4469 41.4V57H63.3669V19.68H74.2269C77.3869 19.68 78.9669 21.26 78.9669 24.42V36.66C78.9669 39.5 77.7269 41.06 75.2469 41.34L80.8869 57H76.4469L70.9869 41.4H67.4469ZM67.4469 23.22V37.86H73.0269C73.8269 37.86 74.3269 37.76 74.5269 37.56C74.7669 37.32 74.8869 36.8 74.8869 36V25.08C74.8869 24.28 74.7669 23.78 74.5269 23.58C74.3269 23.34 73.8269 23.22 73.0269 23.22H67.4469Z" fill="white"/>
    <path d="M118.433 53.46H127.013V57H114.353V19.68H118.433V53.46ZM135.462 53.46H145.722V57H131.322V19.68H145.302V23.22H135.462V35.82H143.502V39.36H135.462V53.46Z" fill="white"/>
    </svg>
    `;

    return (
        <>
            {props.text ? (
                <View style={styles.header}>
                    <SvgXml
                        xml={logoImage}
                        width="100"
                        height="100"
                        style={styles.headerImage}
                    />
                    <Text style={styles.headerTxt1}>{props.txt1}</Text>
                    <Text style={styles.headerTxt2}>{props.txt2}</Text>
                </View>
            ) : (
                <View style={styles.header}>
                    <SvgXml
                        xml={logoImage}
                        width="100"
                        height="100"
                        style={styles.headerImage}
                    />
                </View>
            )}
        </>
    );
}

const styles = StyleSheet.create({
    header: {
        backgroundColor: "#0065F7",
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
        paddingTop: 30,
        paddingLeft: 10,
        paddingRight: 10,
        marginBottom: 10,
        alignSelf: "stretch",
    },
    headerImage: {
        width: 100, // Set the width of your image as needed
        height: 60, // Set the height of your image as needed
    },
    headerTxt1: {
        color: "rgba(255,255,255, 0.7)",
        textAlign: "center",
        fontSize: 20,
        paddingBottom: 10,
    },
    headerTxt2: {
        color: "white",
        textAlign: "center",
        fontSize: 20,
        paddingBottom: 20,
    },
});
