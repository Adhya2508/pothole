import os
import cv2
import uuid


def calculate_severity(count, area_percent):

    if count == 0:
        return "GOOD"

    if area_percent < 2 and count <= 2:
        return "MODERATE"

    if area_percent < 5 and count <= 5:
        return "POOR"

    return "CRITICAL"


def save_prediction_image(result):

    image = result.plot()

    filename = str(uuid.uuid4()) + ".jpg"

    output_path = os.path.join("predictions", filename)

    cv2.imwrite(output_path, image)

    return filename


def process_results(result, inference_time):

    boxes = result.boxes

    pothole_count = len(boxes)

    confidences = []
    detections = []

    image_height, image_width = result.orig_shape

    image_area = image_width * image_height

    total_pothole_area = 0

    for box in boxes:

        confidence = float(box.conf)

        xmin, ymin, xmax, ymax = box.xyxy[0].tolist()

        width = xmax - xmin
        height = ymax - ymin

        pothole_area = width * height

        total_pothole_area += pothole_area

        confidences.append(confidence)

        detections.append({
            "confidence": round(confidence, 3),
            "xmin": int(xmin),
            "ymin": int(ymin),
            "xmax": int(xmax),
            "ymax": int(ymax),
            "width": int(width),
            "height": int(height),
            "area": int(pothole_area)
        })

    if pothole_count == 0:
        average_confidence = 0
    else:
        average_confidence = sum(confidences) / pothole_count

    area_percent = (total_pothole_area / image_area) * 100

    severity = calculate_severity(
        pothole_count,
        area_percent
    )

    image_name = save_prediction_image(result)
    

    return {
        "success": True,

        "pothole_count": pothole_count,

        "average_confidence": round(
            average_confidence,
            3
        ),

        "severity": severity,

        "covered_area_percent": round(
            area_percent,
            2
        ),

        "inference_time_ms": round(
            inference_time,
            2
        ),

        "annotated_image": image_name,
        "annotated_image_url": f"http://127.0.0.1:5000/predictions/{image_name}",

        "detections": detections
    }