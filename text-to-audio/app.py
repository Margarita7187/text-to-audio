from flask import Flask, render_template, request, jsonify, send_file
import os
import uuid
import io
from gtts import gTTS

app = Flask(__name__)

os.makedirs('static/audio', exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    try:
        data = request.get_json()
        text = data.get('text', '')
        lang = 'ru' if data.get('model') == 'russian' else 'en'
        
        if not text:
            return jsonify({'error': 'Введите текст'}), 400
        
        # Генерация через Google TTS (бесплатно, без ключа)
        tts = gTTS(text=text, lang=lang, slow=False)
        
        filename = f"speech_{uuid.uuid4().hex}.mp3"
        filepath = os.path.join('static/audio', filename)
        tts.save(filepath)
        
        return jsonify({
            'success': True,
            'audio_url': f'/static/audio/{filename}'
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)