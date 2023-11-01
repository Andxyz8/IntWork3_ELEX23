/* eslint-disable no-bitwise */
import { useMemo, useState } from "react";
import { PermissionsAndroid, Platform } from "react-native";
import {
    BleError,
    BleManager,
    Characteristic,
    Device,
} from "react-native-ble-plx";

import * as ExpoDevice from "expo-device";

import base64 from "react-native-base64";

const RASPBERRY_UUID = "00001801-0000-1000-8000-00805f9b34fb";
const RASPBERRY_CHARACTERISTIC = "00001234-0000-1000-8000-00805f9b34fb";

interface BluetoothLowEnergyApi {
    requestPermissions(): Promise<boolean>;
    scanForPeripherals(): Promise<Device>;
    connectToDevice(device: Device): Promise<Device>;
    add(): void;
    sendCommand(device: Device, command: string): void;
}

function useBLE(): BluetoothLowEnergyApi {
    const bleManager = useMemo(() => new BleManager(), []);
    const [allDevices, setAllDevices] = useState<Device[]>([]);
    const [test, setTest] = useState<String>("NAO FOI");
    const [connectedDevice, setConnectedDevice] = useState<Device | null>(null);
    const [heartRate, setHeartRate] = useState<number>(0);
    const [scanning, setScanning] = useState<Boolean>(false);

    const requestAndroid31Permissions = async () => {
        const bluetoothScanPermission = await PermissionsAndroid.request(
            PermissionsAndroid.PERMISSIONS.BLUETOOTH_SCAN,
            {
                title: "Location Permission",
                message: "Bluetooth Low Energy requires Location",
                buttonPositive: "OK",
            }
        );
        const bluetoothConnectPermission = await PermissionsAndroid.request(
            PermissionsAndroid.PERMISSIONS.BLUETOOTH_CONNECT,
            {
                title: "Location Permission",
                message: "Bluetooth Low Energy requires Location",
                buttonPositive: "OK",
            }
        );
        const fineLocationPermission = await PermissionsAndroid.request(
            PermissionsAndroid.PERMISSIONS.ACCESS_FINE_LOCATION,
            {
                title: "Location Permission",
                message: "Bluetooth Low Energy requires Location",
                buttonPositive: "OK",
            }
        );

        return (
            bluetoothScanPermission === "granted" &&
            bluetoothConnectPermission === "granted" &&
            fineLocationPermission === "granted"
        );
    };

    const requestPermissions = async () => {
        if (Platform.OS === "android") {
            if ((ExpoDevice.platformApiLevel ?? -1) < 31) {
                const granted = await PermissionsAndroid.request(
                    PermissionsAndroid.PERMISSIONS.ACCESS_FINE_LOCATION,
                    {
                        title: "Location Permission",
                        message: "Bluetooth Low Energy requires Location",
                        buttonPositive: "OK",
                    }
                );
                return granted === PermissionsAndroid.RESULTS.GRANTED;
            } else {
                const isAndroid31PermissionsGranted =
                    await requestAndroid31Permissions();

                return isAndroid31PermissionsGranted;
            }
        } else {
            return true;
        }
    };

    const isDuplicteDevice = (devices: Device[], nextDevice: Device) =>
        devices.findIndex((device) => nextDevice.name === device.name) > -1;

    function timeout(delay: number) {
        return new Promise((res) => setTimeout(res, delay));
    }

    const scanForPeripherals = async () => {
        console.log("scan");
        let dvice: Device = null;
        setScanning(true);
        bleManager.startDeviceScan([], null, (error, device) => {
            if (error) {
                console.log(error);
            }

            if (device.id == "B8:27:EB:EF:69:21") {
                //if (device.name == "raspberrypi") {
                //console.log(device);
                connectToDevice(device);
                dvice = device;
            }
        });

        await timeout(30000);
        console.log("stop scan");
        bleManager.stopDeviceScan();

        return dvice;
    };

    const connectToDevice = async (device: Device) => {
        try {
            const deviceConnection = await bleManager.connectToDevice(
                device.id
            );
            setConnectedDevice(deviceConnection);
            let d =
                await deviceConnection.discoverAllServicesAndCharacteristics();
            console.log("FOI");
            sendCommand(deviceConnection, "UP");
            bleManager.stopDeviceScan();

            return deviceConnection;
        } catch (e) {
            console.log("FAILED TO CONNECT", e);
        }
    };

    const disconnectFromDevice = () => {
        if (connectedDevice) {
            bleManager.cancelDeviceConnection(connectedDevice.id);
            setConnectedDevice(null);
            setHeartRate(0);
        }
    };

    const startStreamingData = async (device: Device) => {
        // if (device) {
        //     device.monitorCharacteristicForService(
        //         RASPBERRY_UUID,
        //         RASPBERRY_CHARACTERISTIC,
        //     );
        // } else {
        //     console.log("No Device Connected");
        // }
    };

    const sendCommand = async (device: Device, command: string) => {
        if (device) {
            device
                // .writeCharacteristicWithResponseForService(
                //     RASPBERRY_UUID,
                //     RASPBERRY_CHARACTERISTIC,
                //     base64.encode(command)
                // )
                // .then((characteristic) => {
                //     console.log(
                //         "Command sended:",
                //         base64.decode(characteristic.value)
                //     );
                // });
                .readCharacteristicForService(
                    RASPBERRY_UUID,
                    RASPBERRY_CHARACTERISTIC
                )
                .then((characteristic) => {
                    console.log(
                        "Command read:",
                        characteristic.value,
                        base64.decode(characteristic.value),
                        parseFloat(base64.decode(characteristic.value))
                    );
                });
            //         .characteristicsForService(RASPBERRY_UUID)
            //         .then((characteristic) => {
            //             console.log("Command read:", characteristic);
            //         });
            // } else {
            console.log("No Device Connected");
        }
    };

    const add = () => {
        console.log(test);
        setTest("FOI");
    };

    return {
        scanForPeripherals,
        requestPermissions,
        connectToDevice,
        add,
        sendCommand,
    };
}

export default useBLE;
