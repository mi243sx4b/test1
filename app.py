from flask import Flask, request, jsonify, render_template
import spacy

app = Flask(__name__)
# Ginza（日本語用のspaCyモデル）を読み込みます
nlp = spacy.load("ja_ginza")

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    text = request.json.get('text')
    if not text:
        return jsonify({'error': 'No text provided'}), 400

    doc = nlp(text)
    tokens = [{'text': token.text, 'lemma': token.lemma_, 'pos': token.pos_, 'dep': token.dep_} for token in doc]
    entities = [{'text': ent.text, 'label': ent.label_} for ent in doc.ents]
    
    result = {
        'tokens': tokens,
        'entities': entities
    }
    return jsonify(result)

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=False)
