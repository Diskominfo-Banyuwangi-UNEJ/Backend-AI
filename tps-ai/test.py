from ultralytics import YOLO
import supervision as sv
import cv2
import numpy as np
import os

# Configuration
MODEL_PATH = "train_model.pt"
TEST_IMAGE = "image-testing/full.jpeg"

# Container level thresholds
LEVEL_THRESHOLDS = {
    'low': 0.3,     # <30% full
    'medium': 0.6,  # 30-60% full
    'high': 1.0     # >60% full
}

# Color coding for levels
LEVEL_COLORS = {
    'low': (0, 255, 0),      # Green
    'medium': (0, 255, 255), # Yellow
    'high': (0, 0, 255)      # Red
}

def calculate_container_level(detection_boxes, image_height):
    """Hybrid method: combine average and max position for fill level"""
    if len(detection_boxes) == 0:
        return 'empty', 0.0

    bottom_positions = [box[3] for box in detection_boxes]  # box[3] = ymax
    avg_y = np.mean(bottom_positions)
    max_y = max(bottom_positions)
    hybrid_y = (avg_y + max_y) / 2

    fill_ratio = max(0.0, min(1.0, hybrid_y / image_height))

    if fill_ratio < LEVEL_THRESHOLDS['low']:
        return 'low', fill_ratio
    elif fill_ratio < LEVEL_THRESHOLDS['medium']:
        return 'medium', fill_ratio
    else:
        return 'high', fill_ratio

def process_image(image_path):
    # Load image
    image = cv2.imread(image_path)
    if image is None:
        print(f"Error: Cannot read image {image_path}")
        return None

    image_height = image.shape[0]

    # Load model and perform detection
    model = YOLO(MODEL_PATH)
    results = model(image, conf=0.085, iou=0.5)
    detections = sv.Detections.from_ultralytics(results[0])

    # Calculate container level
    level, fill_ratio = calculate_container_level(detections.xyxy, image_height)

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

    # Add container level indicator
    level_color = LEVEL_COLORS.get(level, (255, 255, 255))
    cv2.rectangle(annotated_image, (10, 10), (350, 80), (0, 0, 0), -1)
    cv2.putText(annotated_image, 
                f"Container Level: {level.upper()}",
                (20, 40), 
                cv2.FONT_HERSHEY_SIMPLEX, 
                1, 
                level_color, 
                2)
    cv2.putText(annotated_image, 
                f"Fill Ratio: {fill_ratio:.1%}",
                (20, 70), 
                cv2.FONT_HERSHEY_SIMPLEX, 
                0.8, 
                level_color, 
                2)

    return annotated_image, level, fill_ratio

def main():
    # Process the image
    print(f"Processing image: {TEST_IMAGE}")
    result, level, fill_ratio = process_image(TEST_IMAGE)

    if result is not None:
        # Save output
        os.makedirs("output", exist_ok=True)
        output_path = f"output/detected_{os.path.basename(TEST_IMAGE)}"
        cv2.imwrite(output_path, result)
        print(f"Result saved to: {output_path}")
        print(f"Container Status: {level.upper()} ({fill_ratio:.1%} full)")

        # Display result
        cv2.imshow("Waste Detection Result", result)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
