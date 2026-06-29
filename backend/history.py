import boto3
import uuid
from datetime import datetime
from decimal import Decimal

# Connect to DynamoDB
dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table("PredictionHistory")


def save_prediction(data):

    prediction = {
        "prediction_id": str(uuid.uuid4()),
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "pothole_count": int(data["pothole_count"]),
        "average_confidence": Decimal(str(data["average_confidence"])),
        "severity": str(data["severity"]),
        "covered_area_percent": Decimal(str(data["covered_area_percent"])),
        "annotated_image": str(data["annotated_image"]),
        "annotated_image_url": str(data["annotated_image_url"])
    }

    table.put_item(Item=prediction)


def get_history():

    response = table.scan()

    if "Items" in response:
        return response["Items"]

    return []
