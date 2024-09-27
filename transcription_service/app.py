from flask import Flask, request, jsonify
import whisper
import tempfile
import os

app = Flask(__name__)
model = whisper.load_model("base")

@app.route('/transcribe', methods=['POST'])
def transcribe():
    if 'audio' not in request.files:
        return jsonify({'error': 'No se proporcionó archivo de audio'}), 400

    audio_file = request.files['audio']
    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        audio_file.save(tmp.name)
        result = model.transcribe(tmp.name, language='es')
        os.unlink(tmp.name)

    return jsonify({'transcription': result['text']}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
