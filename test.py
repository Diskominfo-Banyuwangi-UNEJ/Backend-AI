from ultralytics import YOLO
import cv2
import matplotlib.pyplot as plt

# Muat model yang sudah dilatih
model = YOLO('runs/detect/train/weights/best.pt')  # Sesuaikan dengan path model yang tersimpan

image_path = 'test3.jpeg'
results = model(image_path)

# Tampilkan hasil
for r in results:
    img_with_boxes = r.plot()

    cv2.imshow('Detection Result', img_with_boxes)
    cv2.waitKey(0)
    cv2.destroyAllWindows()