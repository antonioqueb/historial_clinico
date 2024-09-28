from flask import Flask, render_template, request, redirect, url_for, flash, send_file
import requests

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

    # Realizar solicitud al api_gateway para generar el reporte
    response = requests.post(f'{API_GATEWAY_URL}/api/generate-report', json={
        'patient_name': patient_name,
        'format': format_type
    }, stream=True)

    if response.status_code == 200:
        # Descargar el archivo
        return send_file(response.raw, as_attachment=True, download_name=f"{patient_name}_report.{format_type}")
    else:
        flash('Error al generar el reporte', 'error')

    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5005)
