const express = require('express');
const axios = require('axios');
const bodyParser = require('body-parser');
const multer = require('multer');
const FormData = require('form-data');
const fs = require('fs');
const Queue = require('bull');
const upload = multer({ dest: 'uploads/' });

const app = express();
app.use(bodyParser.json());

const AUTH_SERVICE_URL = 'http://auth_service:5000';
const TRANSCRIPTION_SERVICE_URL = 'http://transcription_service:5001';
const ANALYSIS_SERVICE_URL = 'http://analysis_service:5002';
const STORAGE_SERVICE_URL = 'http://storage_service:5003';
const REPORT_SERVICE_URL = 'http://report_service:5004';

const reportQueue = new Queue('report generation');

app.post('/api/login', async (req, res) => {
    try {
        const response = await axios.post(`${AUTH_SERVICE_URL}/login`, req.body);
        res.json(response.data);
    } catch (error) {
        res.status(error.response.status).json(error.response.data);
    }
});

app.post('/api/start-consultation', upload.single('audio'), async (req, res) => {
    try {
        // Transcripción
        const formData = new FormData();
        formData.append('audio', fs.createReadStream(req.file.path));
        const transcriptionResponse = await axios.post(`${TRANSCRIPTION_SERVICE_URL}/transcribe`, formData, {
            headers: formData.getHeaders()
        });
        const transcription = transcriptionResponse.data.transcription;

        // Análisis
        const analysisResponse = await axios.post(`${ANALYSIS_SERVICE_URL}/analyze`, { transcription });
        const summary = analysisResponse.data.summary;

        // Almacenamiento
        const patient_name = req.body.patient_name || 'Paciente Anónimo';
        await axios.post(`${STORAGE_SERVICE_URL}/history/create`, { patient_name, history: summary });

        // Limpiar archivo temporal
        fs.unlinkSync(req.file.path);

        res.json({ message: 'Consulta procesada exitosamente', summary });
    } catch (error) {
        res.status(500).json({ error: error.message });
    }
});

app.post('/api/generate-report', async (req, res) => {
    try {
        const { patient_name, format } = req.body;

        // Agregar la tarea de generación del reporte a la cola
        const job = await reportQueue.add({ patient_name, format });

        res.json({ message: 'La generación del reporte ha comenzado.', jobId: job.id });
    } catch (error) {
        res.status(500).json({ error: error.message });
    }
});

// Procesar los trabajos en la cola
reportQueue.process(async (job) => {
    const { patient_name, format } = job.data;
    // Llamada al servicio de almacenamiento para obtener el historial
    const historyResponse = await axios.get(`${STORAGE_SERVICE_URL}/history/get`, {
        params: { patient_name }
    });

    const histories = historyResponse.data.histories;
    const latestHistory = histories[histories.length - 1];

    // Generar el reporte
    const reportResponse = await axios.post(`${REPORT_SERVICE_URL}/report/export`, {
        patient_name,
        history: latestHistory.history,
        format
    }, { responseType: 'stream' });

    return { report: reportResponse.data };
});

app.get('/api/job-status/:job_id', async (req, res) => {
    const job = await reportQueue.getJob(req.params.job_id);

    if (job) {
        if (job.finishedOn) {
            return res.json({ status: 'completed' });
        }
        return res.json({ status: 'processing' });
    }

    return res.status(404).json({ error: 'Job not found' });
});

app.listen(8080, () => {
    console.log('API Gateway corriendo en el puerto 8080');
});
