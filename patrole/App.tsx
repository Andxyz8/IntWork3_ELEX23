import { StyleSheet } from "react-native";
import useBLE from "./services/useBLE";
import { useState } from "react";
import RemoteControls from "./pages/routing/RemoteControls";
import { NavigationContainer } from "@react-navigation/native";
import { createNativeStackNavigator } from "@react-navigation/native-stack";
import StartRouting from "./pages/routing/StartRouting";
import SaveRoute from "./pages/routing/SaveRoute";
import ConnectBot from "./pages/home/ConnectBot";
import RouteList from "./pages/home/RouteList";
import Monitor from "./pages/monitoring/Monitor";


// Notificacoes
import * as Notifications from "expo-notifications";
import { Alert } from "react-native";


const Stack = createNativeStackNavigator();

Notifications.setNotificationHandler({
    handleNotification: async () => ({
      shouldShowAlert: true,
      shouldPlaySound: true,
      shouldSetBadge: true,
    }),
  });

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

    const handleCallNotifications = async ()=> {
        const { status } = await Notifications.getPermissionsAsync();

        if( status !== 'granted'){
            Alert.alert("Você não deixou as notificações ativas");

            return;
        }

        console.log("Notificacoes");
    }


    return (
        <NavigationContainer>
            <Stack.Navigator>
                <Stack.Screen
                        name="Monitor"
                        component={Monitor}
                        options={{ headerShown: false }}
                />
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
