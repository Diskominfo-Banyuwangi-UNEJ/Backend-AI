from ultralytics import YOLO
import cv2
import matplotlib.pyplot as plt

# Muat model yang sudah dilatih
model = YOLO('runs/detect/train/weights/best.pt')  # Sesuaikan dengan path model yang tersimpan

# Jalankan prediksi pada gambar
image_path = 'foto/test1.jpeg'  # Ganti dengan path gambar yang ingin diuji
results = model(image_path)

# Tampilkan hasil
for r in results:
    img_with_boxes = r.plot()

    # Tampilkan gambar menggunakan OpenCV
    cv2.imshow('Detection Result', img_with_boxes)
    cv2.waitKey(0)
    cv2.destroyAllWindows()