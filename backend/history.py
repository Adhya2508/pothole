import boto3
import uuid
from datetime import datetime

# Connect to DynamoDB
dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table("PredictionHistory")


def save_prediction(data):

    prediction = {
        "prediction_id": str(uuid.uuid4()),
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "pothole_count": data["pothole_count"],
        "average_confidence": data["average_confidence"],
        "severity": data["severity"],
        "covered_area_percent": data["covered_area_percent"],
        "annotated_image": data["annotated_image"],
        "annotated_image_url": data["annotated_image_url"]
    }

    table.put_item(Item=prediction)


def get_history():

    response = table.scan()

    if "Items" in response:
        return response["Items"]

    return []
