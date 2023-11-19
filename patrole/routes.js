const express = require("express");
const { Client } = require("pg");

const client = new Client({
    user: "teste",
    database: "patrole_iw3",
    password: "teste123",
    port: 5432,
    host: "patrole-iw3.cfx3sunjcddh.us-east-1.rds.amazonaws.com",
    ssl: {
        rejectUnauthorized: false,
    },
});

const app = express();

app.get("/", function (req, res) {
    res.send("NOTHING TO SEE HERE");
    return;
});

// Criando uma rota GET que retorna os dados da tabela usuários.
app.get("/users", function (req, res) {
    client.query("SELECT * FROM user_patrole", async function (err, result) {
        if (err) {
            return console.error("error running query", err);
        }
        res.send(result.rows);
        return;
    });
});

app.get("/robots", function (req, res) {
    client.query("SELECT * FROM robot", async function (err, result) {
        if (err) {
            return console.error("error running query", err);
        }
        res.send(result.rows);

        return;
    });
});

//get route list
app.get("/routes", function (req, res) {
    client.query("SELECT * FROM route", async function (err, result) {
        if (err) {
            return console.error("error running query", err);
        }
        res.send(result.rows);

        return;
    });
});

app.get("/connect", function (req, res) {
    // Conectando ao banco.
    client.connect((err) => {
        if (err) {
            res.send("ERROR: " + err);
            return;
        }
        res.send("Connected");
    });
});

app.get("/disconnect", function (req, res) {
    // Conectando ao banco.
    client.end((err) => {
        if (err) {
            res.send("ERROR: " + err);
            return;
        }
        res.send("Disconnected");
    });
});

app.get("/notification/:id", function (req, res) {
    client.query(
        `SELECT * FROM route_execution INNER JOIN route ON route.id_route = route_execution.id_route INNER JOIN notification ON notification.id_route_execution = route_execution.id_route_execution WHERE route.id_route = ${req.params.id}`,
        async function (err, result) {
            if (err) {
                return console.error("error running query", err);
            }
            res.send(result.rows);

            return;
        }
    );
});

app.get("/camera_triggering/:id", function (req, res) {
    client.query(
        `SELECT * FROM camera_triggering WHERE id_camera_triggering = ${req.params.id}`,
        async function (err, result) {
            if (err) {
                return console.error("error running query", err);
            }
            res.send(result.rows);

            return;
        }
    );
});

//97

app.get("/stop_alarm_continue_route/:id", function (req, res) {
    client.query(
        `INSERT INTO notification (id_route_execution, message, value, moment) VALUES (${
            req.params.id
        }, 'continue_route_stop_alarm', True, to_timestamp((${
            Date.now() + 1000 * 60 * -new Date().getTimezoneOffset()
        }) / 1000.0))`,
        async function (err, result) {
            if (err) {
                return console.error("error running query", err);
            }
            res.send(result.rows);

            return;
        }
    );
});

app.get("/stop_alarm_stop_route/:id", function (req, res) {
    client.query(
        `INSERT INTO notification (id_route_execution, message, value, moment) VALUES (${
            req.params.id
        }, 'continue_route_stop_alarm', False, to_timestamp((${
            Date.now() + 1000 * 60 * -new Date().getTimezoneOffset()
        }) / 1000.0))`,
        async function (err, result) {
            if (err) {
                return console.error("error running query", err);
            }
            res.send(result.rows);

            return;
        }
    );
});

app.listen(3001, "0.0.0.0", () => {
    console.log("Vai no navegador e entra em http://107.20.130.209:3001/");
});
