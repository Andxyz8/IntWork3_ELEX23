import { StyleSheet } from "react-native";
import useBLE from "./useBLE";
import { useState } from "react";
import RemoteControls from "./pages/routing/RemoteControls";
import { NavigationContainer } from "@react-navigation/native";
import { createNativeStackNavigator } from "@react-navigation/native-stack";
import StartRouting from "./pages/routing/StartRouting";
import SaveRoute from "./pages/routing/SaveRoute";
import ConnectBot from "./pages/home/ConnectBot";
import RouteList from "./pages/home/RouteList";

const Stack = createNativeStackNavigator();

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

    return (
        <NavigationContainer>
            <Stack.Navigator>
                <Stack.Screen
                    name="ConnectBot"
                    component={ConnectBot}
                    options={{ headerShown: false }}
                />
                <Stack.Screen
                    name="RouteList"
                    component={RouteList}
                    options={{ headerShown: false }}
                />
                <Stack.Screen
                    name="StartRouting"
                    component={StartRouting}
                    options={{ headerShown: false }}
                />
                <Stack.Screen
                    name="RemoteControls"
                    component={RemoteControls}
                    options={{ headerShown: false }}
                />
                <Stack.Screen
                    name="SaveRoute"
                    component={SaveRoute}
                    options={{ headerShown: false }}
                />
            </Stack.Navigator>
        </NavigationContainer>
    );
}
