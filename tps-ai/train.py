from ultralytics import YOLO

# Load model
model = YOLO("yolo11n.pt")

# Train with custom augmentations
model.train(
    data="data/data.yaml",
    epochs=50,
    imgsz=640,
    batch=16,
    hsv_h=0.015,    # Hue augmentation
    hsv_s=0.7,      # Saturation augmentation
    hsv_v=0.4,      # Value (brightness) augmentation
    flipud=0.5,     # Vertical flip
    fliplr=0.5,     # Horizontal flip
    mosaic=1.0,     # Mosaic augmentation
    mixup=0.2,      # Mixup augmentation
)