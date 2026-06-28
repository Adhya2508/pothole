from ultralytics import YOLO
import torch

# Check if Apple Metal (MPS) is available
if torch.backends.mps.is_available():
    device = "mps"
    print("Using Apple Metal (MPS) GPU")
else:
    device = "cpu"
    print("Using CPU")

# Load pretrained YOLOv8 Nano model
model = YOLO("yolov8n.pt")

# Train
model.train(
    data="dataset/data.yaml",
    epochs=50,
    imgsz=640,

    # Hardware
    device=device,
    batch=16,
    workers=4,

    # Output
    project="runs",
    name="pothole_detection",
    exist_ok=True,

    # Save best model
    save=True,
    save_period=-1,

    # Validation
    val=True,
    plots=True,

    # Reproducibility
    seed=42,

    # Early stopping
    patience=20,

    # Use pretrained weights
    pretrained=True,

    # Mixed precision (helps on supported hardware)
    amp=True
)

print("\nTraining completed!")
print("Best model saved at:")
print("runs/pothole_detection/weights/best.pt")