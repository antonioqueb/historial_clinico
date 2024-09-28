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

// Crear tabla si no existe
db.run(`CREATE TABLE IF NOT EXISTS histories (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    patient_name TEXT NOT NULL,
    history TEXT NOT NULL
)`);

// Ruta para crear historial
app.post('/history/create', (req, res) => {
    const { patient_name, history } = req.body;
    if (!patient_name || !history) {
        return res.status(400).json({ error: 'El nombre del paciente y el historial son requeridos.' });
    }

    db.run(`INSERT INTO histories (patient_name, history) VALUES (?, ?)`, [patient_name, history], function(err) {
        if (err) {
            return res.status(500).json({ error: err.message });
        }
        res.json({ message: 'Historial guardado', id: this.lastID });
    });
});

// Ruta para obtener historial por nombre de paciente
app.get('/history/get', (req, res) => {
    const { patient_name } = req.query;
    if (!patient_name) {
        return res.status(400).json({ error: 'El nombre del paciente es requerido.' });
    }

    db.all(`SELECT * FROM histories WHERE patient_name = ?`, [patient_name], (err, rows) => {
        if (err) {
            return res.status(500).json({ error: err.message });
        }
        if (rows.length === 0) {
            return res.status(404).json({ message: 'No se encontró historial para este paciente.' });
        }
        res.json({ histories: rows });
    });
});

// Iniciar el servidor
app.listen(5003, () => {
    console.log('Storage service running on port 5003');
});
