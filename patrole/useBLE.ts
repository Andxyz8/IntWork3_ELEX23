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

const RASPBERRY_UUID = "0000180d-0000-1000-8000-00805f9b34fb";
const RASPBERRY_CHARACTERISTIC = "00002a37-0000-1000-8000-00805f9b34fb";

interface BluetoothLowEnergyApi {
    requestPermissions(): Promise<boolean>;
    scanForPeripherals(): Promise<any[]>;
}

function useBLE(): BluetoothLowEnergyApi {
    const bleManager = useMemo(() => new BleManager(), []);
    const [allDevices, setAllDevices] = useState<Device[]>([]);
    const [test, setTest] = useState<any[]>([]);
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
        let devices: any[] = test;
        setScanning(true);
        bleManager.startDeviceScan([], null, (error, device) => {
            if (error) {
                console.log(error);
            }

            if (device.name != null) {
                console.log(device);
                if (!isDuplicteDevice(devices, device)) {
                    devices.push({
                        name: device.name,
                        uuid: String(device.serviceUUIDs),
                    });
                }
                setTest(devices);
            }
        });

        await timeout(5000);

        bleManager.stopDeviceScan();
        console.log("CABO");
        console.log(test);
        return test;
    };

    const connectToDevice = async (device: Device) => {
        try {
            const deviceConnection = await bleManager.connectToDevice(
                device.id
            );
            setConnectedDevice(deviceConnection);
            await deviceConnection.discoverAllServicesAndCharacteristics();
            bleManager.stopDeviceScan();
            startStreamingData(deviceConnection);
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

    const add = () => {
        let a = test;

        a.push({ date: new Date().toISOString(), name: "OI" });

        console.log(a.length);
        setTest(a);

        return a;
    };

    return {
        scanForPeripherals,
        requestPermissions,
    };
}

export default useBLE;
