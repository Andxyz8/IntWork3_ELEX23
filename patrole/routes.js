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

// Criando uma rota GET que retorna os dados da tabela usuários.
app.get("/users", function (req, res) {
    client.query("SELECT * FROM user_patrole", async function (err, result) {
        if (err) {
            return console.error("error running query", err);
        }
        console.log(result);
        res.send(result.rows);
        return;
    });
});

app.get("/robots", function (req, res) {
    client.query("SELECT * FROM robot", async function (err, result) {
        if (err) {
            return console.error("error running query", err);
        }
        console.log(result);
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
        console.log(result);
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

app.listen(3000, () => {
    console.log(
        "Vai no navegador e entra em http://localhost:3000/users pra ver os usuários cadastrados."
    );
});
