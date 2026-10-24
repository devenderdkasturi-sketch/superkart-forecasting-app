import os
import io
import joblib
import pandas as pd
import numpy as np
from flask import Flask, request, jsonify

# 1. Initialize the Flask application service blueprint
app = Flask(__name__)

# 2. Define operational pathing configurations
MODEL_PATH = os.path.join(os.path.dirname(__file__), 'superkart_model.joblib')

# Load the production serialized machine learning pipeline asset
if os.path.exists(MODEL_PATH):
    model_pipeline = joblib.load(MODEL_PATH)
    print("🤖 Serialized model pipeline loaded successfully into API runtime.")
else:
    model_pipeline = None
    print("⚠️ Warning: 'superkart_model.joblib' missing from application folder path.")


@app.route('/health', methods=['GET'])
def health_check():
    """
    Operational heartbeat verification checkpoint route.
    """
    status = "healthy" if model_pipeline is not None else "degraded (model missing)"
    return jsonify({"status": status, "service": "superkart-backend"}), 200


@app.route('/v1/predict', methods=['POST'])
def predict_single():
    """
    Endpoint for online single-record vector real-time sales inference.
    """
    if not model_pipeline:
        return jsonify({"error": "Model pipeline asset is not initialized on backend."}), 503
        
    try:
        # Extract incoming JSON payloads
        input_data = request.get_json(force=True)
        
        # Convert the json dictionary vector to a single row DataFrame array
        input_df = pd.DataFrame([input_data])
        
        # Execute estimation prediction processing using the frozen pipeline weights
        prediction = model_pipeline.predict(input_df)
        
        return jsonify({
            "status": "success",
            "prediction": float(prediction[0])
        }), 200
        
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 400


@app.route('/v1/predictbatch', methods=['POST'])
def predict_batch():
    """
    Endpoint for optimized matrix batch document processing file streams.
    """
    if not model_pipeline:
        return jsonify({"error": "Model pipeline asset is not initialized on backend."}), 503
        
    if 'file' not in request.files:
        return jsonify({"error": "No file stream document multipart payload named 'file' found."}), 400
        
    file = request.files['file']
    
    try:
        # Decode streaming continuous binary file array directly into pandas workspace memory
        stream = io.StringIO(file.stream.read().decode("utf-8"), newline=None)
        input_df = pd.read_csv(stream)
        
        # Process and estimate batch predictions
        predictions = model_pipeline.predict(input_df)
        
        # Build index map output payload
        results_map = {str(idx): float(pred) for idx, pred in enumerate(predictions)}
        
        return jsonify(results_map), 200
        
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 400


if __name__ == '__main__':
    # Execute backend microservice listener loop infrastructure binding
    app.run(host='0.0.0.0', port=7860, debug=False)