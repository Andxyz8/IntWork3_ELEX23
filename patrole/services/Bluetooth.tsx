import React, {useState} from 'react';
import {
  TouchableOpacity,
  Button,
  PermissionsAndroid,
  View,
  Text,
} from 'react-native';

import base64 from 'react-native-base64';

import CheckBox from '@react-native-community/checkbox';

import {styles} from '../Styles/styles';
import {LogBox} from 'react-native';
//import BleManager from 'react-native-ble-manager';


// BleManager.start({ showAlert: false }).then(() => {
//   // Success code
//   console.log("Module initialized");
// }).catch((e) => {
//   console.log(e);
// });

import { BleManager } from 'react-native-ble-plx';

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
}

const manager = new BleManager()



export default function App() {

  function test(){
    console.log("AAAAAAAAAAAAA")
  }


  return (
    <View>
      <Text>OIIIII</Text>
      <Button title='CONNECT' onPress={test}></Button>
    </View>
  );
}