from flask import Flask, request, jsonify
from transformers import pipeline

app = Flask(__name__)

# Cargar el modelo de resumen
summarizer = pipeline('summarization', model='sshleifer/distilbart-cnn-12-6')

@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.get_json()
    transcription = data.get('transcription')
    
    # Verificar si la transcripción se proporcionó
    if not transcription:
        app.logger.error("No se proporcionó transcripción")
        return jsonify({'error': 'No se proporcionó transcripción'}), 400

    try:
        # Generar resumen
        app.logger.info(f"Transcripción recibida para resumen: {transcription}")
        summary = summarizer(transcription, max_length=150, min_length=30, do_sample=False)
        app.logger.info(f"Resumen generado: {summary[0]['summary_text']}")
    except Exception as e:
        app.logger.error(f"Error al generar el resumen: {str(e)}")
        return jsonify({'error': f"Error al generar el resumen: {str(e)}"}), 500

    return jsonify({'summary': summary[0]['summary_text']}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002, debug=True)
