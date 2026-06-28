from ultralytics import YOLO
import time

# Load model once
model = YOLO("models/best.pt")


def predict_image(image_path):

    start_time = time.time()

    results = model.predict(
        source=image_path,
        conf=0.25,
        save=False,
        verbose=False
    )

    inference_time = (time.time() - start_time) * 1000

    return results[0], inference_time