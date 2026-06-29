import boto3
import json

# SNS client (make sure region matches EC2)
sns = boto3.client("sns", region_name="ap-south-1")

# Your correct topic ARN
SNS_TOPIC_ARN = "arn:aws:sns:ap-south-1:537287250200:pothole-alerts"


def send_alert(severity, prediction_id, pothole_count):
    message = {
        "severity": severity,
        "prediction_id": prediction_id,
        "pothole_count": pothole_count,
        "message": "CRITICAL ROAD CONDITION DETECTED"
    }

    try:
        response = sns.publish(
            TopicArn=SNS_TOPIC_ARN,
            Message=json.dumps(message),
            Subject="🚨 Pothole Alert - CRITICAL"
        )

        print("✅ SNS SENT SUCCESSFULLY")
        print("MessageId:", response.get("MessageId"))

        return response

    except Exception as e:
        print("❌ SNS ERROR:", str(e))
        return None
