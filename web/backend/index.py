from flask import Flask, request, jsonify
from keras.models import load_model
import dill
import keras.layers as tfl
import tensorflow as tf
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
from_disk = dill.load(open("./tokenizers/tokenizer.dill", "rb"))
tokenizer = tfl.TextVectorization.from_config(from_disk['config'])
tokenizer.adapt(tf.data.Dataset.from_tensor_slices(["xyz"]))
tokenizer.set_weights(from_disk['weights'])
model = load_model('./model/model.h5')

@app.route('/predict', methods=['POST'])
def predict():
    data = request.json
    article = data['article']
    if not article:
        return jsonify({'error': 'No article found in request'}), 400
    prediction = model.predict(tokenizer([article])) # Adjust preprocessing and input format
    return jsonify({'prediction': {
        'score': f"{prediction[0][0]}",
        'article': article
        }
    })

if __name__ == '__main__':
    app.run(debug=True)



