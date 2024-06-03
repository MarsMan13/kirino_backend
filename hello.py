# ~/flask_app/hello.py

from flask import Flask, request, jsonify
app = Flask(__name__)

training_data = {}

@app.route('/train', methods=['POST'])
def train():
    data = request.get_json()
    id = data.get('id')
    Q = data.get('Q')
    A = data.get('A')
    
    if not id or not Q or not A:
        return jsonify({'error': 'Missing required parameters'}), 400
    
    training_data[id] = {'Q': Q, 'A': A}
    return jsonify({'message': f'Training data stored for id {id}'}), 200

@app.route('/run', methods=['POST'])
def run():
    data = request.get_json()
    myId = data.get('myId')
    targetId = data.get('targetId')
    Q = data.get('Q')
    
    if not myId or not targetId or not Q:
        return jsonify({'error': 'Missing required parameters'}), 400
    
    if targetId not in training_data:
        return jsonify({'error': f'No training data found for id {targetId}'}), 404
    
    stored_data = training_data[targetId]
    if stored_data['Q'] == Q:
        response = stored_data['A']
    else:
        response = 'No matching question found'
    
    return jsonify({'response': response}), 200

if __name__ == "__main__":
    app.run(host='127.0.0.1', port=5000)