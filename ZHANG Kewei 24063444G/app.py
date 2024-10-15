from flask import Flask, render_template, request, jsonify
import requests
from flask_cors import CORS  
import logging

app = Flask(__name__)
CORS(app)  

logging.basicConfig(level=logging.DEBUG)

LM_STUDIO_API_URL = 'http://127.0.0.1:1234/v1/completions'  

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate_quote():
    data = request.get_json()
    input_text = data.get('input_text', '')
    if not input_text:
        return jsonify({'error': 'No input text provided'}), 400

    prompt = f"Generate a short philosophical quote in English that includes the word '{input_text}'. The quote should not exceed 20 words."
    lm_studio_payload = {
        "prompt": prompt,
        "max_tokens": 30,
        "temperature": 0.7,
        "top_p": 0.95,
        "stop": ["\n", ".", "!"]
    }

    try:
        response = requests.post(LM_STUDIO_API_URL, json=lm_studio_payload)
        response.raise_for_status()
        
        lm_studio_response = response.json()
        generated_quote = lm_studio_response['choices'][0]['text'].strip()
        
        # Ensure the quote ends with a period
        if not generated_quote.endswith('.'):
            generated_quote += '.'
        
        return jsonify({'english': generated_quote})
    except requests.RequestException as e:
        return jsonify({'error': 'Failed to generate quote, please try again'}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
