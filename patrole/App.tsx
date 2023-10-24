import { StatusBar } from "expo-status-bar";
import {
    Button,
    SafeAreaView,
    StyleSheet,
    Text,
    TouchableOpacity,
    View,
} from "react-native";
import Bluetooth from "./services/Bluetooth";
import DeviceModal from "./DeviceConnectionModal";
import useBLE from "./useBLE";
import { useState } from "react";
import RemoteControls from "./components/RemoteControls";

export default function App() {
    const {
        requestPermissions,
        scanForPeripherals,
        // allDevices,
        // connectToDevice,
        // connectedDevice,
        // heartRate,
        // disconnectFromDevice,
    } = useBLE();
    const [isModalVisible, setIsModalVisible] = useState<boolean>(false);

    const scanForDevices = async () => {
        const isPermissionsEnabled = await requestPermissions();
        if (isPermissionsEnabled) {
            scanForPeripherals();
        }
    };

    const hideModal = () => {
        setIsModalVisible(false);
    };

    const openModal = async () => {
        scanForDevices();
        setIsModalVisible(true);
    };

    return (
        <SafeAreaView style={styles.container}>
            {/* <View>
        <Text>
          Please Connect to a Heart Rate Monitor
        </Text>
      </View>
      <Button title='Connect' onPress={openModal}></Button>
      <DeviceModal
        closeModal={hideModal}
        visible={isModalVisible}
        connectToPeripheral={() => {}}
        devices={[]}
      /> */}
            <RemoteControls></RemoteControls>
        </SafeAreaView>
    );
}

const styles = StyleSheet.create({
    container: {
        flex: 1,
        backgroundColor: "#fff",
        alignItems: "center",
        justifyContent: "center",
    },
});
