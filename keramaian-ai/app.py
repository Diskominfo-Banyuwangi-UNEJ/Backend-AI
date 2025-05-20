from ultralytics import YOLO
import supervision as sv
import cv2
import numpy as np
import os
import time

# Configuration
MODEL_PATH = "best.pt"
STREAM_URL = "https://livepantau.semarangkota.go.id/hls/10441/101/2024/90aa125a-8234-48e8-97ac-a0d95019ece2_101.m3u8"

# Colors
PERSON_COLOR = (0, 255, 0)  # Green for person boxes
STATUS_COLORS = {
    "Sepi": (0, 255, 0),    # Green
    "Normal": (0, 255, 255), # Yellow
    "Padat": (0, 0, 255)     # Red
}

def classify_crowd_density(people_count):
    """Classify crowd density based on number of people detected."""
    if people_count <= 20:
        return "Sepi"
    elif 21 <= people_count <= 50:
        return "Normal"
    else:
        return "Padat"

def process_frame(frame):
    """Process a single frame for human detection."""
    model = YOLO(MODEL_PATH)
    results = model(frame, conf=0.05, iou=0.5)
    detections = sv.Detections.from_ultralytics(results[0])
    
    person_detections = detections[detections.class_id == 0]
    people_count = len(person_detections)
    density_status = classify_crowd_density(people_count)
    status_color = STATUS_COLORS[density_status]

    labels = [
        f"Person {confidence:.2f}" 
        for confidence in person_detections.confidence
    ]

    box_annotator = sv.BoxAnnotator(
        thickness=2,
        color=sv.Color(r=PERSON_COLOR[0], g=PERSON_COLOR[1], b=PERSON_COLOR[2]),
        color_lookup=sv.ColorLookup.CLASS
    )

    label_annotator = sv.LabelAnnotator(
        text_color=sv.Color(r=255, g=255, b=255),
        text_scale=0.6,
        text_thickness=1,
        text_padding=5,
        text_position=sv.Position.TOP_LEFT,
        color_lookup=sv.ColorLookup.CLASS
    )

    annotated_frame = box_annotator.annotate(scene=frame.copy(), detections=person_detections)
    annotated_frame = label_annotator.annotate(
        scene=annotated_frame,
        detections=person_detections,
        labels=labels
    )

    overlay = annotated_frame.copy()
    cv2.rectangle(overlay, (10, 10), (250, 80), (0, 0, 0), -1)
    annotated_frame = cv2.addWeighted(overlay, 0.7, annotated_frame, 0.3, 0)
    
    cv2.putText(annotated_frame, f"People: {people_count}", (20, 40), 
               cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
    cv2.putText(annotated_frame, f"Status: {density_status}", (20, 70), 
               cv2.FONT_HERSHEY_SIMPLEX, 0.7, status_color, 2)

    return annotated_frame, people_count, density_status

def process_m3u8_stream():
    """Process m3u8 video stream with human detection."""
    cap = cv2.VideoCapture(STREAM_URL)
    
    if not cap.isOpened():
        print(f"Error: Could not open stream {STREAM_URL}")
        return
    
    # Get video properties for VideoWriter
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    
    # Prepare output
    os.makedirs("output", exist_ok=True)
    output_path = "output/processed_stream.mp4"
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))
    
    model = YOLO(MODEL_PATH)
    
    frame_count = 0
    start_time = time.time()
    
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Stream ended or error reading frame")
            break
        
        # Process every 5th frame to reduce processing load
        if frame_count % 5 == 0:
            results = model(frame, conf=0.02, iou=0.5)
            detections = sv.Detections.from_ultralytics(results[0])
            
            person_detections = detections[detections.class_id == 0]
            people_count = len(person_detections)
            density_status = classify_crowd_density(people_count)
            status_color = STATUS_COLORS[density_status]

            # Annotate frame
            box_annotator = sv.BoxAnnotator(
                thickness=2,
                color=sv.Color(*PERSON_COLOR),
                color_lookup=sv.ColorLookup.CLASS
            )
            
            label_annotator = sv.LabelAnnotator(
                text_color=sv.Color(255, 255, 255),
                text_scale=0.6,
                text_thickness=1,
                text_padding=5,
                text_position=sv.Position.TOP_LEFT,
                color_lookup=sv.ColorLookup.CLASS
            )
            
            labels = [f"Person {conf:.2f}" for conf in person_detections.confidence]
            annotated_frame = box_annotator.annotate(frame.copy(), person_detections)
            annotated_frame = label_annotator.annotate(annotated_frame, person_detections, labels)
            
            # Add status overlay
            overlay = annotated_frame.copy()
            cv2.rectangle(overlay, (10, 10), (250, 80), (0, 0, 0), -1)
            annotated_frame = cv2.addWeighted(overlay, 0.7, annotated_frame, 0.3, 0)
            
            cv2.putText(annotated_frame, f"People: {people_count}", (20, 40), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
            cv2.putText(annotated_frame, f"Status: {density_status}", (20, 70), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, status_color, 2)
            
            # Write to output
            out.write(annotated_frame)
            
            # Display
            cv2.imshow('Processed Stream', annotated_frame)
            
            # Print stats periodically
            if frame_count % 100 == 0:
                elapsed = time.time() - start_time
                print(f"Processed {frame_count} frames in {elapsed:.2f}s ({frame_count/elapsed:.2f} FPS)")
        
        frame_count += 1
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    cap.release()
    out.release()
    cv2.destroyAllWindows()
    
    print(f"Processing complete. Output saved to {output_path}")

if __name__ == "__main__":
    process_m3u8_stream()