# 🛣️ AWS-Powered Smart Pothole Detection System

An end-to-end AI-powered web application that detects potholes from road images using **YOLOv8**, evaluates road severity in real time, and demonstrates a complete cloud-native deployment on **AWS**.

The project combines **Computer Vision**, **Flask**, **React**, and multiple **AWS services** — including **EC2, Lambda, API Gateway, SNS, CloudWatch, and AWS Amplify** — to simulate a production-ready, full-stack AI application from model training to cloud deployment.

---

## 🌟 Features

- 🚗 Detect potholes from uploaded road images using a custom-trained YOLOv8 model
- 📦 Transfer-learned object detection (YOLOv8 Nano, trained on a custom pothole dataset)
- 📊 Road severity analysis based on pothole **count** and **size**
- 🖼️ Annotated prediction images with bounding boxes and confidence scores
- 📜 Prediction history tracking
- ☁️ Cloud-native architecture using AWS (S3, EC2, Lambda, API Gateway, SNS, CloudWatch, Amplify)
- ⚡ REST API architecture with clean JSON responses
- 📱 Responsive React frontend

---

## 🏗️ System Architecture

```
            React Frontend (AWS Amplify)
                        │
                        ▼
                  API Gateway
                        │
                        ▼
                  AWS Lambda
                        │
                        ▼
              Flask API (Amazon EC2)
                        │
                        ▼
                  YOLOv8 Model
                        │
                        ▼
              Prediction Processing
                        │
        ┌───────────────┼───────────────┐
        ▼               ▼               ▼
   CloudWatch      Prediction        Amazon SNS
     Logs        History (JSON /     Email Alerts
                  DynamoDB-ready)   (CRITICAL severity)
```

---

## 🛠️ Tech Stack

### Machine Learning
- YOLOv8 Nano (Ultralytics)
- OpenCV
- Python

### Backend
- Flask (REST API)
- UUID-based file handling
- JSON-based history storage
- AWS S3 / SNS utility modules
- Gunicorn (deployment)

### Frontend
- React (Vite)
- Axios
- React Router
- Component-based UI architecture

### Cloud (AWS)
- Amazon EC2
- AWS Lambda
- Amazon API Gateway
- Amazon SNS
- Amazon CloudWatch
- AWS Amplify

### Version Control
- Git & GitHub

---

## 📂 Project Structure

```
pothole-detection/
│
├── archive/
│   ├── annotated-images/
│   └── README.md
│
├── backend/
│   ├── models/
│   │   └── best.pt                 # Trained YOLOv8 weights
│   ├── predictions/                # Annotated output images
│   ├── uploads/                    # User-uploaded images
│   ├── venv/
│   ├── app.py                      # Main Flask application
│   ├── config.py                   # Configuration / env settings
│   ├── history.json                # Local prediction history store
│   ├── history.py                  # History read/write logic
│   ├── model.py                    # YOLO model loading & inference
│   ├── s3_utils.py                 # AWS S3 upload/integration helpers
│   ├── sns_utils.py                # AWS SNS notification helpers
│   └── utils.py                    # Severity calc, response formatting
│
├── dataset/                        # Converted YOLO-format dataset
│
├── frontend/
│   ├── dist/                       # Production build output
│   ├── node_modules/
│   ├── public/
│   ├── src/
│   │   ├── assets/
│   │   │   ├── hero.png
│   │   │   └── vite.svg
│   │   ├── components/
│   │   │   ├── Footer.jsx
│   │   │   ├── Loader.jsx
│   │   │   ├── Navbar.jsx
│   │   │   ├── ResultCard.jsx
│   │   │   └── UploadCard.jsx
│   │   ├── pages/
│   │   │   ├── About.jsx
│   │   │   ├── History.jsx
│   │   │   └── Home.jsx
│   │   ├── services/
│   │   │   └── api.js
│   │   ├── styles/
│   │   │   ├── about.css
│   │   │   ├── footer.css
│   │   │   ├── global.css
│   │   │   ├── history.css
│   │   │   ├── home.css
│   │   │   ├── navbar.css
│   │   │   ├── result.css
│   │   │   └── upload.css
│   │   ├── App.jsx
│   │   └── main.jsx
│   ├── .gitignore
│   ├── eslint.config.js
│   ├── index.html
│   ├── package.json
│   ├── package-lock.json
│   ├── README.md
│   └── vite.config.js
│
├── runs/                           # YOLO training run outputs (graphs, weights)
│
├── scripts/
│   ├── convert_dataset.py          # Pascal VOC → YOLO format converter
│   └── train.py                    # YOLOv8 training script
│
├── .gitignore
├── README.md
└── splits.json                     # Predefined train/test split reference
```

---

## 📊 Dataset

The dataset was sourced from **Kaggle**, and originally contained:

- Road images in `.jpg` format
- Annotations in **Pascal VOC** `.xml` format (bounding boxes for each pothole)

Since YOLOv8 requires labels in YOLO format (`class_id x_center y_center width height`, normalized), a custom script — `convert_dataset.py` — was built to handle the conversion automatically.

**Conversion pipeline:**
1. Read `splits.json` for predefined train/test image splits.
2. Auto-generate a validation split (~20% of training images).
3. Parse each `.xml` file using `xml.etree.ElementTree`.
4. Convert bounding boxes to normalized YOLO coordinates:
   ```
   x_center = ((xmin + xmax) / 2) / image_width
   y_center = ((ymin + ymax) / 2) / image_height
   width    = (xmax - xmin) / image_width
   height   = (ymax - ymin) / image_height
   ```
5. Assign class ID `0` to every annotation (single class: `pothole`).
6. Generate `.txt` label files and organize images/labels into the YOLO directory structure.
7. Generate a `data.yaml` file describing dataset paths and class info (`nc: 1`, `names: ['pothole']`).

**Final dataset split:**
| Split | Percentage |
|-------|-----------|
| Train | 70% |
| Validation | 20% |
| Test | 10% |

---

## 🧠 Model Training

Trained using **YOLOv8 Nano** with transfer learning (pretrained on COCO, fine-tuned for pothole detection).

| Parameter | Value |
|-----------|-------|
| Base Model | `yolov8n.pt` |
| Epochs | 50 |
| Image Size | 640 × 640 |
| Classes | 1 (`pothole`) |

**Evaluation metrics tracked:**
- Precision
- Recall
- mAP@50
- mAP@50-95
- F1 Score
- Confusion Matrix

The best-performing weights (chosen automatically based on validation performance) are saved at:
```
backend/models/best.pt
```

Training also generates loss curves, precision-recall curves, F1 curves, and sample predictions, stored under `runs/`.

---

## ⚙️ Backend Workflow

1. User uploads a road image via the frontend or API.
2. Flask saves the image locally (and/or to S3) using a randomly generated UUID filename.
3. The YOLOv8 model (`model.py`) is loaded **once at startup** for fast inference.
4. YOLO performs inference and returns bounding boxes + confidence scores.
5. `utils.py` processes the raw output:
   - Counts detected potholes
   - Computes average confidence
   - Calculates road severity (count + size based)
   - Generates an annotated image using YOLO's built-in plotting
6. The annotated image is saved to the `predictions/` folder (and/or S3).
7. The prediction is logged to `history.json` via `history.py`.
8. A clean JSON response is returned to the client.

---

## 🚦 Road Severity Levels

Severity is calculated using both the **number of detected potholes** and their **relative sizes** (larger potholes weigh more heavily than smaller ones).

| Severity | Description |
|----------|-------------|
| 🟢 GOOD | No potholes detected |
| 🟡 MODERATE | Few / small potholes |
| 🟠 POOR | Multiple potholes |
| 🔴 CRITICAL | Large or numerous potholes — triggers an SNS alert |

---

## ☁️ AWS Services Used

| Service | Purpose |
|---------|---------|
| **AWS Budgets** | Sets a predefined spending limit to prevent accidental overcharges |
| **IAM** | Dedicated IAM user with scoped, least-privilege permissions (instead of root account) for programmatic access |
| **Amazon S3** | Stores uploaded and annotated images in the cloud, replacing local `uploads/` and `predictions/` folders |
| **Amazon EC2** | Hosts the Flask backend and YOLOv8 inference engine |
| **Amazon DynamoDB** | Stores prediction history (prediction ID, timestamps, image URLs, severity, etc.), replacing local `history.json` |
| **Amazon SNS** | Sends email alerts when road severity is classified as **CRITICAL** |
| **AWS Lambda** | Middleware coordinating requests between API Gateway and EC2 |
| **API Gateway** | Public REST API endpoint, without exposing EC2 directly |
| **Amazon CloudWatch** | Monitors Lambda execution, request/response logs, and errors in real time |
| **AWS Amplify** | Hosts and serves the React frontend |

---

## 🗺️ AWS Migration Roadmap

The project is being migrated step-by-step from a purely local application into a fully cloud-native, production-style architecture on AWS. Below is the detailed plan being followed.

### 1. AWS Budget
An **AWS Budget** is created first, as a safety measure, so that accidental usage never exceeds a small predefined limit. This protects against unexpected charges while learning and experimenting with AWS services.

### 2. IAM User
Instead of using the AWS root account for programming, a dedicated **IAM user** is created with only the permissions required for this project. Programmatic access credentials (Access Key ID and Secret Access Key) are generated, allowing the Flask application to securely communicate with AWS services.

### 3. Amazon S3 — Cloud Image Storage
Currently, uploaded images are saved locally in the `uploads/` folder, and annotated images are stored locally in the `predictions/` folder. After integrating S3:
- Uploaded images are sent directly to an S3 bucket.
- Annotated prediction images are also uploaded to S3.
- Instead of returning local filenames, the API returns publicly accessible or pre-signed S3 URLs, letting the frontend display images directly from cloud storage.
- This makes the application scalable, since storage is no longer limited to a single machine.

### 4. Amazon EC2 — Backend Deployment
Once S3 integration is complete, the backend is deployed on an **Amazon EC2** instance:
- The same Flask application that runs locally is installed on an EC2 virtual machine.
- Python, OpenCV, Ultralytics, Flask, and all required dependencies are installed on the instance.
- The trained `best.pt` model and backend code are copied to EC2.
- The Flask server is configured to run remotely so clients can send prediction requests over the internet.

### 5. Amazon DynamoDB — Persistent History
After EC2 is operational, the local `history.json` storage is replaced by **Amazon DynamoDB**:
- Every prediction — including prediction ID, timestamp, uploaded image URL, annotated image URL, pothole count, average confidence, inference time, and severity — is stored as a separate item in a DynamoDB table.
- The `/history` endpoint retrieves records directly from DynamoDB instead of reading a local file, allowing prediction history to persist even if the server restarts.

### 6. Amazon SNS — Critical Alerts
Following DynamoDB integration, **Amazon SNS** is added:
- Whenever the severity of a detected road is classified as **CRITICAL**, the backend automatically publishes a message to an SNS topic.
- Anyone subscribed to that topic (e.g., a road maintenance engineer) instantly receives an email notification indicating that immediate repair is required.

### 7. AWS Lambda + API Gateway — Secure, Production-Style Architecture
The architecture is further improved using **AWS Lambda** and **API Gateway**, instead of exposing the EC2 instance directly to the frontend:
- **API Gateway** receives incoming requests.
- It triggers a **Lambda function**, which coordinates the complete workflow:
  - Forwards requests to the Flask inference service running on EC2 (`/predict` and `/history`)
  - Uploads images to S3 (where applicable)
  - Stores results in DynamoDB
  - Publishes SNS notifications when necessary
  - Returns the final response to the client
- This creates a cleaner, more secure, production-style architecture, since the EC2 instance is never exposed directly to the public internet.

**Current Lambda implementation** (proxies requests to the Flask/EC2 backend):

```python
import json
import base64
import urllib.request
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

EC2_BASE_URL = "http://3.110.222.147:5000"

def lambda_handler(event, context):
    logger.info("=== Request Received ===")
    try:
        path = event.get("rawPath") or event.get("resource") or ""
        method = event.get("requestContext", {}).get("http", {}).get("method") \
            or event.get("httpMethod", "GET")
        logger.info(f"Path: {path}")
        logger.info(f"Method: {method}")

        if path.endswith("/history") and method == "GET":
            logger.info("Fetching history from EC2")
            req = urllib.request.Request(
                f"{EC2_BASE_URL}/history",
                method="GET"
            )
            with urllib.request.urlopen(req) as response:
                result = response.read().decode()
            return {
                "statusCode": response.status,
                "headers": {
                    "Access-Control-Allow-Origin": "*",
                    "Content-Type": "application/json"
                },
                "body": result
            }

        body = event["body"]
        if event.get("isBase64Encoded", False):
            body = base64.b64decode(body)
        else:
            body = body.encode()

        headers = event.get("headers", {})
        content_type = (
            headers.get("content-type")
            or headers.get("Content-Type")
            or "application/octet-stream"
        )

        logger.info("Forwarding prediction to EC2")
        req = urllib.request.Request(
            f"{EC2_BASE_URL}/predict",
            data=body,
            method="POST"
        )
        req.add_header("Content-Type", content_type)
        with urllib.request.urlopen(req) as response:
            result = response.read().decode()
        return {
            "statusCode": response.status,
            "headers": {
                "Access-Control-Allow-Origin": "*",
                "Content-Type": "application/json"
            },
            "body": result
        }

    except Exception as e:
        logger.exception("Request failed")
        return {
            "statusCode": 500,
            "headers": {
                "Access-Control-Allow-Origin": "*",
                "Content-Type": "application/json"
            },
            "body": json.dumps({"error": str(e)})
        }
```

**What this Lambda function does:**
- Logs every incoming request (path, method) to **CloudWatch Logs**.
- Routes `GET` requests ending in `/history` straight to the EC2 Flask backend's `/history` endpoint.
- Routes all other requests (image uploads) to the EC2 Flask backend's `/predict` endpoint, correctly handling both base64-encoded and raw request bodies.
- Forwards the original `Content-Type` header so multipart image uploads are processed correctly by Flask.
- Adds `Access-Control-Allow-Origin: *` headers to every response, enabling CORS for the React frontend.
- Wraps everything in a try/except block, logging full stack traces via `logger.exception()` and returning a clean `500` JSON error response on failure — all visible in **CloudWatch Logs** for debugging.

### 8. Amazon CloudWatch — Monitoring & Logging
**CloudWatch** is used throughout the Lambda + API Gateway layer to monitor the system in production:
- Every request path, HTTP method, and outcome is logged via Python's `logging` module inside the Lambda function.
- Successful forwarded requests, as well as failures (with full exception tracebacks via `logger.exception`), are captured in **CloudWatch Logs**.
- This enables debugging of the EC2 ↔ Lambda ↔ API Gateway pipeline without needing direct SSH access to EC2, and can later be extended with **CloudWatch Alarms** for proactive error/latency alerting.

### 9. React Frontend
Finally, the **React frontend** is built so users can:
- Upload images and view annotated predictions
- Inspect pothole counts, confidence scores, inference times, and severity levels
- Browse historical predictions retrieved from DynamoDB
- Visualize cloud-hosted images directly from S3

The React application communicates with **API Gateway** rather than directly with EC2, and is deployed using **AWS Amplify**.

---

## 🌐 Live Demo

### Frontend (AWS Amplify)
🔗 [https://main.d2y9t9lgegs9ex.amplifyapp.com](https://main.d2y9t9lgegs9ex.amplifyapp.com)

History page: [https://main.d2y9t9lgegs9ex.amplifyapp.com/history](https://main.d2y9t9lgegs9ex.amplifyapp.com/history)

### API Endpoint (EC2 via API Gateway)
```
POST https://wf78nddt67.execute-api.ap-south-1.amazonaws.com/prod/predict
```

> ⚠️ **Note:** The live prediction API may be unavailable when the EC2 instance is stopped to conserve AWS credits. The frontend itself remains accessible via AWS Amplify, but live inference calls may fail until the instance is restarted. A full walkthrough video (linked below) demonstrates the complete working pipeline.

📹 **Google Drive Video:**  
https://drive.google.com/file/d/1aYSqP2TGZTw1JfFNJpgJV3FRhN5JD8fo/view?usp=sharing

---

## 💻 Local Development

### Backend Setup

```bash
cd backend

python -m venv venv
source venv/bin/activate      # On Windows: venv\Scripts\activate

pip install -r requirements.txt

python app.py
```

Runs on:
```
http://localhost:5000
```

### Frontend Setup

```bash
cd frontend

npm install
npm run dev
```

Runs on:
```
http://localhost:5173
```

Production preview build:
```
http://localhost:4173
```

---

## 📡 API Endpoints

### Local

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | API status check |
| GET | `/health` | Health check |
| POST | `/predict` | Upload an image and get pothole predictions |
| GET | `/history` | Retrieve prediction history |

**Base URL:** `http://localhost:5000`

### Deployed

| Method | Endpoint |
|--------|----------|
| POST | `https://wf78nddt67.execute-api.ap-south-1.amazonaws.com/prod/predict` |

---

## 📷 Sample Output

For every uploaded image, the API returns:

- Number of potholes detected
- Average confidence score
- Inference time (ms)
- Road severity classification
- Filename/URL of the annotated prediction image

---

## 🚀 Future Improvements

- 🔐 User authentication
- 🔁 CloudWatch Alarms for proactive error/latency alerting
- 📊 Real-time analytics dashboard
- 📱 Mobile application
- 🗺️ GPS integration for geo-tagged pothole reports
- 🛠️ Road maintenance analytics and reporting

---

## 📚 Learning Outcomes

This project demonstrates hands-on, end-to-end experience with:

- Computer Vision & Deep Learning (YOLOv8)
- Transfer Learning
- Dataset preprocessing (Pascal VOC → YOLO format conversion)
- REST API design with Flask
- Frontend development with React
- Git & GitHub version control
- AWS EC2, Lambda, API Gateway
- AWS SNS (event-driven notifications)
- AWS CloudWatch (monitoring & logging)
- AWS Amplify (frontend hosting/deployment)
- End-to-end cloud-native AI application architecture

---

## 👨‍💻 Author

**Adhya 2508**

If you found this project helpful, feel free to ⭐ the repository!
