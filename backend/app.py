from flask import Flask, request, jsonify, send_from_directory
import os
import uuid

from model import predict_image
from utils import process_results
from history import save_prediction, get_history

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs("predictions", exist_ok=True)


@app.route("/")
def home():
    return {
        "message": "Pothole Detection API Running"
    }


@app.route("/predict", methods=["POST"])
def predict():

    if "image" not in request.files:
        return jsonify({
            "success": False,
            "message": "No image uploaded."
        }), 400

    image = request.files["image"]

    filename = str(uuid.uuid4()) + ".jpg"

    image_path = os.path.join(
        UPLOAD_FOLDER,
        filename
    )

    image.save(image_path)

    result, inference_time = predict_image(image_path)

    response = process_results(
        result,
        inference_time
    )

    # Save prediction to history.json
    save_prediction(response)

    return jsonify(response)


@app.route("/history", methods=["GET"])
def history():

    history_data = get_history()

    return jsonify(history_data)

@app.route("/health", methods=["GET"])
def health():

    return jsonify({
        "status": "healthy",
        "model": "loaded",
        "version": "1.0.0"
    })

@app.route("/predictions/<filename>", methods=["GET"])
def get_prediction_image(filename):

    return send_from_directory(
        "predictions",
        filename
    )


if __name__ == "__main__":
    app.run(debug=True)