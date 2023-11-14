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
    getRoutes(): Promise<Route[]>;
    startRouteExct(address: string, id_route: any): Promise<boolean>;
    getNotifications(id: string): Promise<Notification[]>;
}

interface Route {
    id_route: number;
    title: string;
    description: string;
    status: boolean;
    number_repeats: number;
    created_at: Date;
    interval_between_repeats: number;
}

interface Notification {
    id_notification: number;
    id_route_execution: number;
    message: string;
    value: string;
    moment: Date;
}

//AWS server ip
const server = "http://107.20.130.209:3001";

function raspberryAPI(): Api {
    const getConnection = async () => {
        try {
            let address: String;

            let ip = (await NetworkInfo.getIPV4Address()).split(".");

            let ipString = ip[0] + "." + ip[1] + "." + ip[2];

            for (let i = 1; i <= 254; i++) {
                address = `http://${ipString}.${i}:5002/command`;

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

    const startRouteExct = async (address, id_route) => {
        let body = {
            id_route: String(id_route),
            id_robot: "1",
        };

        const response = await fetch(address + "/route_execution_mode", {
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

    const connect = async () => {
        const response = await fetch(server + "/connect", {
            method: "get",
            headers: {
                "Content-Type": "application/json",
                Accept: "application/json",
            },
        });

        if (response.ok) return true;
        return false;
    };

    const getRoutes = async () => {
        let routes: Route[] = [];
        return connect().then(async (res) => {
            if (res) {
                const response = await fetch(server + "/routes", {
                    method: "get",
                    headers: {
                        "Content-Type": "application/json",
                        Accept: "application/json",
                    },
                });

                const result = await response.json();

                routes = result;

                return routes;
            }
        });
    };

    const getNotifications = async (id: string) => {
        let notifications: Notification[] = [];
        return connect().then(async (res) => {
            if (res) {
                const response = await fetch(server + `/notification/${id}`, {
                    method: "get",
                    headers: {
                        "Content-Type": "application/json",
                        Accept: "application/json",
                    },
                });

                const result = await response.json();

                notifications = result;

                return notifications;
            }
        });
    };

    return {
        getConnection,
        sendCommandFoward,
        sendCommandRight,
        sendCommandLeft,
        sendCommandRead,
        startRouting,
        endRouting,
        getRoutes,
        startRouteExct,
        getNotifications,
    };
}

export default raspberryAPI;
