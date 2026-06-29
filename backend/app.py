from flask import Flask, request, jsonify
import os
import uuid

from model import predict_image
from utils import process_results
from history import save_prediction, get_history
from s3_utils import upload_file, get_file_url

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
PREDICTION_FOLDER = "predictions"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(PREDICTION_FOLDER, exist_ok=True)


@app.route("/")
def home():
    return jsonify({
        "message": "Pothole Detection API Running",
        "status": "success"
    })


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

    # Upload original image
    upload_file(
        image_path,
        "uploads/" + filename
    )

    # Run prediction
    result, inference_time = predict_image(image_path)

    response = process_results(
        result,
        inference_time
    )

    prediction_name = response["annotated_image"]
    prediction_path = response["annotated_image_path"]

    # Upload prediction image
    upload_file(
        prediction_path,
        "predictions/" + prediction_name
    )

    # Replace local path with S3 URL
    response["annotated_image_url"] = get_file_url(
        "predictions/" + prediction_name
    )

    if "annotated_image_path" in response:
        del response["annotated_image_path"]

    save_prediction(response)

    # Delete temporary files
    if os.path.exists(image_path):
        os.remove(image_path)

    if os.path.exists(prediction_path):
        os.remove(prediction_path)

    return jsonify(response)


@app.route("/history", methods=["GET"])
def history():
    return jsonify(get_history())


@app.route("/health", methods=["GET"])
def health():
    return jsonify({
        "status": "healthy",
        "model": "loaded",
        "version": "1.0.0"
    })


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )
