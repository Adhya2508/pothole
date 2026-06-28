from flask import Flask, request, jsonify
import os
import uuid

from model import predict_image
from utils import process_results
from history import save_prediction, get_history
from s3_utils import upload_file, get_file_url

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

    # Generate unique filename
    filename = str(uuid.uuid4()) + ".jpg"

    image_path = os.path.join(
        UPLOAD_FOLDER,
        filename
    )

    # Save uploaded image locally
    image.save(image_path)

    # Upload original image to S3
    upload_file(
        image_path,
        "uploads/" + filename
    )

    # Run YOLO prediction
    result, inference_time = predict_image(image_path)

    # Process prediction
    response = process_results(
        result,
        inference_time
    )

    # Upload annotated prediction image to S3
    prediction_name = response["annotated_image"]
    prediction_path = response["annotated_image_path"]

    upload_file(
        prediction_path,
        "predictions/" + prediction_name
    )

    # Replace local URL with S3 URL
    response["annotated_image_url"] = get_file_url(
        "predictions/" + prediction_name
    )

    # Remove temporary path from response
    del response["annotated_image_path"]

    # Save history
    save_prediction(response)

    # Delete temporary local files
    if os.path.exists(image_path):
        os.remove(image_path)

    if os.path.exists(prediction_path):
        os.remove(prediction_path)

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


if __name__ == "__main__":
    app.run(debug=True)