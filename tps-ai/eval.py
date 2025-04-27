from ultralytics import YOLO

# Load model
model = YOLO("runs/detect/train/weights/best.pt")

# Evaluasi dengan dataset validasi
metrics = model.val(data="data/data.yaml")