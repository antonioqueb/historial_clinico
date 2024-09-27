from flask import Flask, request, jsonify
from transformers import pipeline

app = Flask(__name__)
summarizer = pipeline('summarization', model='sshleifer/distilbart-cnn-12-6')

@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.get_json()
    transcription = data.get('transcription')
    if not transcription:
        return jsonify({'error': 'No se proporcionó transcripción'}), 400

    summary = summarizer(transcription, max_length=150, min_length=30, do_sample=False)
    return jsonify({'summary': summary[0]['summary_text']}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002)