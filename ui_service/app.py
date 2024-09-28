from flask import Flask, render_template, request, redirect, url_for, flash, Response
import requests
import time

app = Flask(__name__)
app.secret_key = 'supersecretkey'

# URL del API Gateway
API_GATEWAY_URL = 'http://api_gateway:8080'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')
    
    # Realizar solicitud al api_gateway para autenticación
    response = requests.post(f'{API_GATEWAY_URL}/api/login', json={
        'username': username,
        'password': password
    })

    if response.status_code == 200:
        flash('Login exitoso', 'success')
    else:
        flash('Credenciales incorrectas', 'error')
    
    return redirect(url_for('index'))

@app.route('/start-consultation', methods=['POST'])
def start_consultation():
    patient_name = request.form.get('patient_name')
    audio = request.files.get('audio')

    # Realizar solicitud al api_gateway para iniciar consulta
    files = {'audio': audio.stream}
    response = requests.post(f'{API_GATEWAY_URL}/api/start-consultation', files=files, data={
        'patient_name': patient_name
    })

    if response.status_code == 200:
        summary = response.json().get('summary')
        flash(f'Consulta procesada exitosamente. Resumen: {summary}', 'success')
    else:
        flash('Error al procesar la consulta', 'error')

    return redirect(url_for('index'))

@app.route('/generate-report', methods=['POST'])
def generate_report():
    patient_name = request.form.get('patient_name')
    format_type = request.form.get('format')

    # Realizar solicitud al api_gateway para iniciar la generación del reporte en segundo plano
    response = requests.post(f'{API_GATEWAY_URL}/api/generate-report', json={
        'patient_name': patient_name,
        'format': format_type
    })

    if response.status_code == 200:
        flash('El reporte está siendo generado. Recibirás una notificación cuando esté listo.', 'success')
    else:
        flash('Error al iniciar la generación del reporte', 'error')

    return redirect(url_for('index'))

@app.route('/report-status/<job_id>', methods=['GET'])
def report_status(job_id):
    def event_stream():
        while True:
            response = requests.get(f'{API_GATEWAY_URL}/api/job-status/{job_id}')
            status = response.json().get('status')

            if status == 'completed':
                yield f"data: El reporte está listo\n\n"
                break
            elif status == 'processing':
                yield f"data: El reporte está en proceso\n\n"
            time.sleep(5)
    
    return Response(event_stream(), content_type='text/event-stream')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5005)
