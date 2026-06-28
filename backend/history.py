import json
import os
from datetime import datetime
import uuid

HISTORY_FILE = "history.json"


def save_prediction(data):

    if not os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "w") as f:
            json.dump([], f)

    with open(HISTORY_FILE, "r") as f:
        history = json.load(f)

    prediction = {
        "prediction_id": str(uuid.uuid4()),
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "pothole_count": data["pothole_count"],
        "average_confidence": data["average_confidence"],
        "severity": data["severity"],
        "covered_area_percent": data["covered_area_percent"],
        "annotated_image": data["annotated_image"]
    }

    history.append(prediction)

    with open(HISTORY_FILE, "w") as f:
        json.dump(history, f, indent=4)


def get_history():

    if not os.path.exists(HISTORY_FILE):
        return []

    with open(HISTORY_FILE, "r") as f:
        history = json.load(f)

    return history