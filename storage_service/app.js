const express = require('express');
const bodyParser = require('body-parser');
const sqlite3 = require('sqlite3').verbose();
const path = require('path');
const app = express();

app.use(bodyParser.json());

// Especifica una ruta absoluta para la base de datos
const dbPath = path.resolve(__dirname, 'database.sqlite');
let db = new sqlite3.Database(dbPath, (err) => {
    if (err) {
        console.error("Error al abrir la base de datos:", err.message);
    } else {
        console.log("Conexión a la base de datos SQLite establecida.");
    }
});

db.run(`CREATE TABLE IF NOT EXISTS histories (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    patient_name TEXT,
    history TEXT
)`);

app.post('/history/create', (req, res) => {
    const { patient_name, history } = req.body;
    db.run(`INSERT INTO histories (patient_name, history) VALUES (?, ?)`, [patient_name, history], function(err) {
        if (err) {
            return res.status(500).json({ error: err.message });
        }
        res.json({ message: 'Historial guardado', id: this.lastID });
    });
});

app.get('/history/get', (req, res) => {
    const { patient_name } = req.query;
    db.all(`SELECT * FROM histories WHERE patient_name = ?`, [patient_name], (err, rows) => {
        if (err) {
            return res.status(500).json({ error: err.message });
        }
        res.json({ histories: rows });
    });
});

app.listen(5003, () => {
    console.log('Storage service running on port 5003');
});
