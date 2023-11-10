import fetch from "node-fetch";
import { NetworkInfo } from "react-native-network-info";

interface Api {
    getConnection(): Promise<any>;
    sendCommandFoward(address: string): Promise<boolean>;
    sendCommandRight(address: string): Promise<boolean>;
    sendCommandLeft(address: string): Promise<boolean>;
    sendCommandRead(address: string): Promise<boolean>;
    startRouting(address: string): Promise<boolean>;
    endRouting(address: string, body: any): Promise<boolean>;
}

function raspberryAPI(): Api {
    const getConnection = async () => {
        try {
            let address: String;

            let ip = (await NetworkInfo.getIPV4Address()).split(".");

            let ipString = ip[0] + "." + ip[1] + "." + ip[2];

            for (let i = 1; i <= 15; i++) {
                address = `http://${ipString}.${i}:5002/command`;

                console.log(address);
                try {
                    const response = await fetch(address, {
                        method: "GET",
                        headers: {
                            Accept: "application/json",
                            ContentType: "application/json",
                        },
                    });

                    const result = await response.json();

                    if (response.ok && result.found) {
                        console.log("FOUND: " + result);
                        return address;
                    }
                } catch (error) {
                    continue;
                }
            }
        } catch (error) {
            if (error instanceof Error) {
                console.log("error message: ", error.message);
            } else {
                console.log("unexpected error: ", error);
            }

            return null;
        }
    };

    const sendCommandFoward = async (address) => {
        const response = await fetch(address + "/recording_move_forward", {
            method: "POST",
            body: "",
            headers: {
                "Content-Type": "application/json",
                Accept: "application/json",
            },
        });

        if (response.ok) return true;
        return false;
    };

    const sendCommandRight = async (address) => {
        const response = await fetch(address + "/recording_rotate_right", {
            method: "POST",
            body: "",
            headers: {
                "Content-Type": "application/json",
                Accept: "application/json",
            },
        });

        if (response.ok) return true;
        return false;
    };

    const sendCommandLeft = async (address) => {
        const response = await fetch(address + "/recording_rotate_left", {
            method: "POST",
            body: "",
            headers: {
                "Content-Type": "application/json",
                Accept: "application/json",
            },
        });

        if (response.ok) return true;
        return false;
    };

    const sendCommandRead = async (address) => {
        const response = await fetch(address + "/recording_read_aruco", {
            method: "POST",
            body: "",
            headers: {
                "Content-Type": "application/json",
                Accept: "application/json",
            },
        });
        const result = await response.json();

        if (response.ok && result.aruco) return result.aruco;
        return null;
    };

    const startRouting = async (address) => {
        const response = await fetch(address + "/route_recording_mode", {
            method: "POST",
            body: "",
            headers: {
                "Content-Type": "application/json",
                Accept: "application/json",
            },
        });

        if (response.ok) return true;
        return false;
    };

    const endRouting = async (address, body) => {
        console.log(body);
        const response = await fetch(address + "/end_route_recording_mode", {
            method: "POST",
            body: JSON.stringify(body),
            headers: {
                "Content-Type": "application/json",
                Accept: "application/json",
            },
        });

        if (response.ok) return true;
        return false;
    };

    const startRouteExct = async (address) => {
        const response = await fetch(address + "/route_execution_mode", {
            method: "POST",
            body: "",
            headers: {
                "Content-Type": "application/json",
                Accept: "application/json",
            },
        });

        if (response.ok) return true;
        return false;
    };

    return {
        getConnection,
        sendCommandFoward,
        sendCommandRight,
        sendCommandLeft,
        sendCommandRead,
        startRouting,
        endRouting,
    };
}

export default raspberryAPI;
