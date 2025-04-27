import cv2
import time
from datetime import datetime
import sqlite3
from ultralytics import YOLO
import supervision as sv
import threading

MODEL_PATH = "train_model.pt"
DATABASE_NAME = "detections.db"
CAPTURE_INTERVAL = 3600
RTSP_URL = "rtsp://username:password@ip_address:port/path"

# Inisialisasi model YOLO
model = YOLO(MODEL_PATH)

def init_db():
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS detections (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp DATETIME,
            image_path TEXT,
            object_class TEXT,
            confidence REAL,
            x_min REAL,
            y_min REAL,
            x_max REAL,
            y_max REAL
        )
    ''')
    conn.commit()
    conn.close()

# Fungsi untuk menyimpan deteksi ke database
def save_to_db(image_path, detections):
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    for i in range(len(detections.class_id)):
        class_id = detections.class_id[i]
        confidence = detections.confidence[i]
        bbox = detections.xyxy[i]
        
        cursor.execute('''
            INSERT INTO detections (
                timestamp, image_path, object_class, confidence,
                x_min, y_min, x_max, y_max
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            timestamp,
            image_path,
            model.model.names[class_id],
            float(confidence),
            float(bbox[0]),
            float(bbox[1]),
            float(bbox[2]),
            float(bbox[3])
        ))
    
    conn.commit()
    conn.close()

def process_frame(frame):
    results = model(frame, conf=0.085, iou=0.5)
    detections = sv.Detections.from_ultralytics(results[0])
    
    # Buat label untuk annotasi
    labels = [
        f"{model.model.names[class_id]} {confidence:.2f}" 
        for class_id, confidence in zip(detections.class_id, detections.confidence)
    ]
    
    # Annotasi frame
    box_annotator = sv.BoxAnnotator(
        thickness=2,
        color=sv.Color(r=0, g=255, b=0),
        color_lookup=sv.ColorLookup.INDEX
    )
    
    label_annotator = sv.LabelAnnotator(
        text_color=sv.Color(r=255, g=255, b=255),
        text_scale=0.6,
        text_thickness=1,
        text_padding=5,
        text_position=sv.Position.TOP_LEFT,
        color_lookup=sv.ColorLookup.INDEX
    )
    
    annotated_frame = box_annotator.annotate(scene=frame.copy(), detections=detections)
    annotated_frame = label_annotator.annotate(
        scene=annotated_frame,
        detections=detections,
        labels=labels
    )
    
    return annotated_frame, detections

def periodic_capture():
    cap = cv2.VideoCapture(RTSP_URL)
    
    if not cap.isOpened():
        print("Error: Tidak dapat terhubung ke CCTV")
        return
    
    last_capture_time = time.time()
    
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error: Gagal mendapatkan frame")
            time.sleep(5)
            continue
        
        processed_frame, _ = process_frame(frame)
        cv2.imshow('CCTV Monitoring', processed_frame)
        
        current_time = time.time()
        if current_time - last_capture_time >= CAPTURE_INTERVAL:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            image_path = f"captures/capture_{timestamp}.jpg"
            
            # Simpan gambar asli
            cv2.imwrite(image_path, frame)
            
            # Proses deteksi
            processed_frame, detections = process_frame(frame)
            
            # Simpan gambar dengan deteksi
            detected_image_path = f"captures/detected_{timestamp}.jpg"
            cv2.imwrite(detected_image_path, processed_frame)
            
            # Simpan ke database
            save_to_db(detected_image_path, detections)
            
            print(f"Capture disimpan: {detected_image_path}")
            last_capture_time = current_time
        
        # Keluar dengan menekan 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    cap.release()
    cv2.destroyAllWindows()

# Fungsi utama
def main():
    # Inisialisasi database
    # init_db()
    
    # Buat folder captures jika belum ada
    # import os
    # os.makedirs("captures", exist_ok=True)
    
    capture_thread = threading.Thread(target=periodic_capture)
    capture_thread.daemon = True
    capture_thread.start()
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Aplikasi dihentikan")

if __name__ == "__main__":
    main()