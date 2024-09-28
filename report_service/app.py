from flask import Flask, request, jsonify, send_file
import os

app = Flask(__name__)

# Ruta al directorio de reportes
REPORTS_DIR = '/app/reports'

@app.route('/report/export', methods=['POST'])
def export_report():
    data = request.get_json()
    patient_name = data.get('patient_name')
    history = data.get('history')
    format_type = data.get('format')

    if not patient_name or not history or not format_type:
        return jsonify({'error': 'Datos incompletos para generar el reporte'}), 400

    # Lógica para generar el reporte
    report_filename = f"{patient_name}_report.{format_type}"
    report_path = os.path.join(REPORTS_DIR, report_filename)

    # Simulación de generación de reporte
    with open(report_path, 'w') as f:
        f.write(f"Reporte de {patient_name}\n\nHistorial:\n{history}")

    # Enviar el archivo generado
    return send_file(report_path, as_attachment=True, attachment_filename=report_filename)

if __name__ == '__main__':
    # Asegurarse de que el directorio de reportes exista
    os.makedirs(REPORTS_DIR, exist_ok=True)
    app.run(host='0.0.0.0', port=5004)
