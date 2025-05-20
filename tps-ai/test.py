from ultralytics import YOLO
import supervision as sv
import cv2
import numpy as np
import os

# Configuration
MODEL_PATH = "train_model.pt"
TEST_IMAGE = "image-testing/full.jpeg"

# Waste pile status thresholds and colors
STATUS_THRESHOLDS = {
    'empty': (0.0, 0.0),
    'low': (0.0, 0.5),
    'normal': (0.5, 1.0),
    'high': (1.0, float('inf'))
}

STATUS_COLORS = {
    'empty': (100, 100, 100),
    'low': (0, 255, 0),
    'normal': (0, 255, 255),
    'high': (0, 0, 255)
}

def calculate_waste_pile_level(garbage_boxes, container_box):
    """Calculate waste pile height relative to container height"""
    if len(garbage_boxes) == 0 or container_box is None:
        return 'empty', 0.0

    # Calculate the highest and lowest points of garbage detections
    top_positions = [box[1] for box in garbage_boxes]  # ymin
    bottom_positions = [box[3] for box in garbage_boxes]  # ymax

    min_y = min(top_positions)  # Highest point (smallest y value)
    max_y = max(bottom_positions)  # Lowest point (largest y value)

    waste_height = max_y - min_y

    # Calculate container height
    container_ymin, container_ymax = container_box[1], container_box[3]
    container_height = container_ymax - container_ymin

    if container_height <= 0:
        return 'empty', 0.0

    fill_ratio = waste_height / container_height

    # Determine status
    for status, (min_thresh, max_thresh) in STATUS_THRESHOLDS.items():
        if min_thresh <= fill_ratio < max_thresh:
            return status, fill_ratio
    return 'high', fill_ratio

def process_image(image_path):
    # Load image
    image = cv2.imread(image_path)
    if image is None:
        print(f"Error: Cannot read image {image_path}")
        return None, None, None

    # Load model and perform detection
    model = YOLO(MODEL_PATH)
    results = model(image, conf=0.085, iou=0.5)
    detections = sv.Detections.from_ultralytics(results[0])

    container_boxes = []
    garbage_boxes = []

    for class_id, box in zip(detections.class_id, detections.xyxy):
        class_name = model.model.names[class_id].lower()
        if class_name == "container":
            container_boxes.append(box)
        elif class_name == "garbage":
            garbage_boxes.append(box)

    # Assume only one container
    container_box = container_boxes[0] if container_boxes else None

    # Calculate waste pile level
    level, fill_ratio = calculate_waste_pile_level(garbage_boxes, container_box)
    status_color = STATUS_COLORS.get(level, (255, 255, 255))

    # Create labels for detections
    labels = [
        f"{model.model.names[class_id]} {confidence:.2f}"
        for class_id, confidence in zip(detections.class_id, detections.confidence)
    ]

    # Setup annotators
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

    # Annotate detections
    annotated_image = box_annotator.annotate(scene=image.copy(), detections=detections)
    annotated_image = label_annotator.annotate(
        scene=annotated_image,
        detections=detections,
        labels=labels
    )

    # Create compact status box on the left side
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
    
    # Add status with color coding
    cv2.putText(annotated_image, 
               f"Status: {level.upper()}",
               (margin + 10, margin + 30), 
               cv2.FONT_HERSHEY_SIMPLEX, 
               0.7, 
               status_color, 
               2)
    
    # Add fill ratio
    cv2.putText(annotated_image, 
               f"Fill: {fill_ratio:.1%}",
               (margin + 10, margin + 60), 
               cv2.FONT_HERSHEY_SIMPLEX, 
               0.7, 
               (255, 255, 255), 
               2)

    return annotated_image, level, fill_ratio
 
def main():
    print(f"Processing image: {TEST_IMAGE}")
    result, level, fill_ratio = process_image(TEST_IMAGE)

    if result is not None:
        os.makedirs("output", exist_ok=True)
        output_path = f"output/detected_{os.path.basename(TEST_IMAGE)}"
        cv2.imwrite(output_path, result)
        print(f"Result saved to: {output_path}")
        print(f"Waste Pile Status: {level.upper()}")
        print(f"Container Fill Ratio: {fill_ratio:.1%}")

        h, w = result.shape[:2]
        max_height = 800
        scale = max_height / h
        resized = cv2.resize(result, (int(w * scale), int(h * scale)))
        cv2.imshow("Waste Detection Result", resized)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

if __name__ == "__main__":
    main()