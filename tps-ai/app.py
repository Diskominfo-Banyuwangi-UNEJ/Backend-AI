from datetime import datetime
from ultralytics import YOLO
import cv2
import supervision as sv
import threading
import os
import numpy as np
from flask import Flask
from api.src import create_app, db
from api.src.models.analisis_tumpukan_model import AnalisisTumpukan, StatusAnalisis

# Configuration
MODEL_PATH = "train_model.pt"
CAPTURE_INTERVAL = 3600  # 1 hour in seconds
RTSP_URL = "rtsp://username:password@ip_address:port/path"
UPLOAD_FOLDER = "captures"

# Initialize Flask app and create database tables
app = create_app()
with app.app_context():
    db.create_all()

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

model = YOLO(MODEL_PATH)

def calculate_waste_pile_level(garbage_boxes, container_box):
    """Calculate waste pile height relative to container height"""
    if len(garbage_boxes) == 0 or container_box is None:
        return 0.0, 0.0  # capacity_level, confidence_score

    top_positions = [box[1] for box in garbage_boxes]
    bottom_positions = [box[3] for box in garbage_boxes]
    
    min_y = min(top_positions)
    max_y = max(bottom_positions)
    waste_height = max_y - min_y

    container_ymin, container_ymax = container_box[1], container_box[3]
    container_height = container_ymax - container_ymin

    if container_height <= 0:
        return 0.0, 0.0

    capacity_level = waste_height / container_height
    confidence_score = 0.85
    
    return capacity_level, confidence_score

def process_frame(frame):
    results = model(frame, conf=0.085, iou=0.5)
    detections = sv.Detections.from_ultralytics(results[0])

    container_boxes = []
    garbage_boxes = []

    for class_id, box in zip(detections.class_id, detections.xyxy):
        class_name = model.model.names[class_id].lower()
        if class_name == "container":
            container_boxes.append(box)
        elif class_name == "garbage":
            garbage_boxes.append(box)

    container_box = container_boxes[0] if container_boxes else None
    capacity_level, confidence_score = calculate_waste_pile_level(garbage_boxes, container_box)

    # Annotate frame
    annotated_frame = frame.copy()
    box_annotator = sv.BoxAnnotator(thickness=2)

    box_width = 250
    box_height = 80
    margin = 10
    
    overlay = annotated_frame.copy()
    cv2.rectangle(overlay, (margin, margin), (box_width, box_height), (0, 0, 0), -1)
    alpha = 0.7
    annotated_frame = cv2.addWeighted(overlay, alpha, annotated_frame, 1 - alpha, 0)
    
    cv2.putText(annotated_frame, 
                f"Capacity: {capacity_level:.1%}",
                (margin + 10, margin + 30),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (255, 255, 255),
                2)
    
    cv2.putText(annotated_frame,
                f"Confidence: {confidence_score:.1%}",
                (margin + 10, margin + 60),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (255, 255, 255),
                2)

    return annotated_frame, capacity_level, confidence_score, bool(container_box), len(garbage_boxes)

def determine_status(capacity_level):
    """Determine status based on capacity level"""
    if 0 <= capacity_level < 0.3:
        return StatusAnalisis.EMPTY
    elif 0.3 <= capacity_level < 0.5:
        return StatusAnalisis.LOW
    elif 0.5 <= capacity_level < 0.8:
        return StatusAnalisis.NORMAL
    else:
        return StatusAnalisis.HIGH

def save_analysis(image_path, capacity_level, confidence_score, id_tumpukan=1):
    """Save analysis results to MySQL database using SQLAlchemy"""
    try:
        with app.app_context():
            status = determine_status(capacity_level)
            
            analysis = AnalisisTumpukan(
                id_tumpukan=id_tumpukan,
                image=image_path,
                status=status,
                capacity_level=float(capacity_level),
                confidence_score=float(confidence_score),
                keterangan=f"Auto analysis: {status.value} full"
            )
            
            db.session.add(analysis)
            db.session.commit()
            
            print(f"Successfully saved analysis with status: {status.value}")
            return True
            
    except Exception as e:
        print(f"Database error: {str(e)}")
        if 'db' in locals():
            db.session.rollback()
        return False

def periodic_capture():
    cap = cv2.VideoCapture(RTSP_URL)
    
    if not cap.isOpened():
        print("Error: Cannot connect to CCTV")
        return
    
    last_capture_time = time.time()
    
    while True:
        try:
            ret, frame = cap.read()
            if not ret:
                print("Error: Failed to get frame")
                time.sleep(5)
                continue
            
            processed_frame, capacity_level, confidence_score, container_detected, garbage_count = process_frame(frame)
            cv2.imshow('CCTV Monitoring', processed_frame)
            
            current_time = time.time()
            if current_time - last_capture_time >= CAPTURE_INTERVAL:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                image_path = os.path.join(UPLOAD_FOLDER, f"detected_{timestamp}.jpg")
                
                # Save annotated image
                cv2.imwrite(image_path, processed_frame)
                
                # Save to MySQL database
                if save_analysis(image_path, capacity_level, confidence_score):
                    print(f"Analysis saved: {image_path}")
                    print(f"Capacity Level: {capacity_level:.1%}")
                    print(f"Confidence Score: {confidence_score:.1%}")
                else:
                    print("Failed to save analysis to database")
                    
                last_capture_time = current_time
            
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
                
        except Exception as e:
            print(f"Error in capture loop: {str(e)}")
            time.sleep(5)
    
    cap.release()
    cv2.destroyAllWindows()

def main():
    with app.app_context():
        capture_thread = threading.Thread(target=periodic_capture)
        capture_thread.daemon = True
        capture_thread.start()
        
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("Application stopped")

if __name__ == "__main__":
    main()