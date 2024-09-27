from flask import Flask, request, jsonify
import whisper
import tempfile
import os

app = Flask(__name__)

# Cargar el modelo Whisper (base)
model = whisper.load_model("base")

@app.route('/transcribe', methods=['POST'])
def transcribe():
    if 'audio' not in request.files:
        app.logger.error("No se proporcionó archivo de audio")
        return jsonify({'error': 'No se proporcionó archivo de audio'}), 400

    audio_file = request.files['audio']
    
    # Validar que el archivo tiene un nombre y extensión válidos
    if audio_file.filename == '':
        app.logger.error("El nombre del archivo no es válido")
        return jsonify({'error': 'El nombre del archivo no es válido'}), 400

    try:
        # Crear un archivo temporal de forma segura
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
            audio_file.save(tmp.name)
            app.logger.info(f"Archivo temporal creado en: {tmp.name}")
            tmp.close()  # Cerrar el archivo antes de pasarlo a Whisper

            # Usar Whisper para transcribir el archivo de audio con FP32 explícito
            device = "cpu"  # Asegurarse de que se utilice CPU
            result = model.transcribe(tmp.name, fp16=False, language='es')  # Desactivar FP16
            transcription = result.get('text', '')
            app.logger.info(f"Transcripción obtenida: {transcription}")

    except whisper.WhisperException as e:
        app.logger.error(f"Error de Whisper: {e}")
        return jsonify({'error': 'Error al procesar el audio con Whisper'}), 500

    except Exception as e:
        app.logger.error(f"Error inesperado: {str(e)}")
        return jsonify({'error': f"Error inesperado: {str(e)}"}), 500

    finally:
        # Asegurarse de que el archivo temporal se elimine
        if os.path.exists(tmp.name):
            os.unlink(tmp.name)
            app.logger.info(f"Archivo temporal eliminado: {tmp.name}")

    return jsonify({'transcription': transcription}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
