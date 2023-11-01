import fetch from "node-fetch";
import { NetworkInfo } from "react-native-network-info";

interface Api {
    getConnection(): Promise<any>;
    getRecordedSteps(address: string): Promise<void>;
    sendCommand(command: string, address: string): Promise<boolean>;
    parseRecordedSteps(steps: any): Promise<boolean>;
}

function raspberryAPI(): Api {
    const getConnection = async () => {
        try {
            let address: String;

            let ip = (await NetworkInfo.getIPV4Address()).split(".");

            let ipString = ip[0] + "." + ip[1] + "." + ip[2];

            for (let i = 13; i < 33; i++) {
                address = `http://${ipString}.${i}:5000/`;

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

    const sendCommand = async (command, address) => {
        const response = await fetch(address + "command", {
            method: "POST",
            body: JSON.stringify({
                command: command,
            }),
            headers: {
                "Content-Type": "application/json",
                Accept: "application/json",
            },
        });

        if (response.ok) {
            const result = await response.json();
            console.log("last: " + result.last);

            return result.last;
        } else return false;
    };

    const getRecordedSteps = async (address) => {
        const response = await fetch(address + "route", {
            method: "GET",
            headers: {
                "Content-Type": "application/json",
                Accept: "application/json",
            },
        });

        if (response.ok) {
            const result = await response.json();
            console.log("steps: " + JSON.stringify(result[0]));
            return result;
        }
        return null;
    };

    const parseRecordedSteps = async (steps) => {
        //Order by id
        //Fix for each step
        //Send to firebase
        return true;
    };

    return { getConnection, sendCommand, getRecordedSteps, parseRecordedSteps };
}

export default raspberryAPI;
