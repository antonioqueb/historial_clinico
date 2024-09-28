from flask import Flask, request, jsonify, send_file
import os

app = Flask(__name__)

# Ruta al directorio de reportes
REPORTS_DIR = '/app/reports'

@app.route('/report/export', methods=['POST'])
def export_report():
    try:
        data = request.get_json()
        patient_name = data.get('patient_name')
        history = data.get('history')
        format_type = data.get('format')

        # Verificar si se proporcionaron todos los datos necesarios
        if not patient_name or not history or not format_type:
            app.logger.error("Datos incompletos para generar el reporte")
            return jsonify({'error': 'Datos incompletos para generar el reporte'}), 400

        # Lógica para generar el reporte
        report_filename = f"{patient_name}_report.{format_type}"
        report_path = os.path.join(REPORTS_DIR, report_filename)

        try:
            # Simulación de generación de reporte
            app.logger.info(f"Generando reporte para {patient_name} en formato {format_type}")
            with open(report_path, 'w') as f:
                f.write(f"Reporte de {patient_name}\n\nHistorial:\n{history}")

            # Verificar que el archivo se generó correctamente
            if not os.path.exists(report_path):
                app.logger.error("No se pudo generar el archivo de reporte")
                return jsonify({'error': 'No se pudo generar el archivo de reporte'}), 500

            # Enviar el archivo generado
            app.logger.info(f"Enviando reporte generado: {report_filename}")
            return send_file(report_path, as_attachment=True, attachment_filename=report_filename)

        except Exception as e:
            app.logger.error(f"Error al generar el archivo de reporte: {str(e)}")
            return jsonify({'error': f"Error al generar el archivo de reporte: {str(e)}"}), 500

    except Exception as e:
        app.logger.error(f"Error en la solicitud: {str(e)}")
        return jsonify({'error': f"Error en la solicitud: {str(e)}"}), 500


if __name__ == '__main__':
    # Asegurarse de que el directorio de reportes exista
    os.makedirs(REPORTS_DIR, exist_ok=True)
    app.run(host='0.0.0.0', port=5004)
