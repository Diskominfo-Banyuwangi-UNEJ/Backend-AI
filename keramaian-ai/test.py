from ultralytics import YOLO
import supervision as sv
import cv2
import numpy as np
import os

# Configuration
MODEL_PATH = "runs/detect/train/weights/best.pt"
TEST_IMAGE = "image-testing/test.jpg"

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

def process_human_detection(image_path):
    # Load image
    image = cv2.imread(image_path)
    if image is None:
        print(f"Error: Cannot read image {image_path}")
        return None

    # Load model and perform detection
    model = YOLO(MODEL_PATH)
    results = model(image, conf=0.2, iou=0.5)
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

    # Annotate detections
    annotated_image = box_annotator.annotate(scene=image.copy(), detections=person_detections)
    annotated_image = label_annotator.annotate(
        scene=annotated_image,
        detections=person_detections,
        labels=labels
    )

    # Create a compact status box on the left side
    box_width = 250  # Width of the status box
    box_height = 80  # Height of the status box
    margin = 10      # Margin from the edges
    
    # Create semi-transparent black rectangle
    overlay = annotated_image.copy()
    cv2.rectangle(overlay, 
                 (margin, margin), 
                 (box_width, box_height), 
                 (0, 0, 0), -1)
    
    # Add transparency
    alpha = 0.7  # Transparency factor
    annotated_image = cv2.addWeighted(overlay, alpha, annotated_image, 1 - alpha, 0)
    
    # Add people count
    cv2.putText(annotated_image, 
               f"People: {people_count}",
               (margin + 10, margin + 30), 
               cv2.FONT_HERSHEY_SIMPLEX, 
               0.7, 
               (255, 255, 255), 
               2)
    
    # Add status with color coding
    cv2.putText(annotated_image, 
               f"Status: {density_status}",
               (margin + 10, margin + 60), 
               cv2.FONT_HERSHEY_SIMPLEX, 
               0.7, 
               status_color, 
               2)

    return annotated_image, people_count, density_status

def main():
    # Process the image
    print(f"Processing image: {TEST_IMAGE}")
    result, people_count, density_status = process_human_detection(TEST_IMAGE)

    if result is not None:
        # Save output
        os.makedirs("output", exist_ok=True)
        output_path = f"output/detected_{os.path.basename(TEST_IMAGE)}"
        cv2.imwrite(output_path, result)
        print(f"Result saved to: {output_path}")
        print(f"Number of people detected: {people_count}")
        print(f"Crowd density status: {density_status}")

        # Display result
        cv2.imshow("Human Detection Result", result)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

if __name__ == "__main__":
    main()