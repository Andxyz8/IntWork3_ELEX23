import { StyleSheet } from "react-native";

export const styles = StyleSheet.create({
    baseText: {
        fontSize: 15,
        fontFamily: "Cochin",
    },
    titleText: {
        fontSize: 20,
        fontWeight: "bold",
    },
    rowView: {
        justifyContent: "space-around",
        alignItems: "flex-start",
        flexDirection: "row",
    },
    controls: {},
    right: {
        marginRight: 0,
    },
    container: {
        flex: 1,
        backgroundColor: "#f2f2f2",
    },
    heartRateTitleWrapper: {
        flex: 1,
        justifyContent: "center",
        alignItems: "center",
    },
    heartRateTitleText: {
        fontSize: 30,
        fontWeight: "bold",
        textAlign: "center",
        marginHorizontal: 20,
        color: "black",
    },
    heartRateText: {
        fontSize: 25,
        marginTop: 15,
    },
    ctaButton: {
        backgroundColor: "#FF6060",
        justifyContent: "center",
        alignItems: "center",
        height: 50,
        marginHorizontal: 20,
        marginBottom: 5,
        borderRadius: 8,
    },
    ctaButtonText: {
        fontSize: 18,
        fontWeight: "bold",
        color: "white",
    },
    spaces: {
        paddingBottom: 20,
    },
});
