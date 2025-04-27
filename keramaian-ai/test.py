from ultralytics import YOLO
import supervision as sv
import cv2
import numpy as np
import os

# Configuration
MODEL_PATH = "runs/detect/train/weights/best.pt"  # Ganti dengan model deteksi manusia Anda jika berbeda
TEST_IMAGE = "image-testing/test.jpg"

# Color for person detection
PERSON_COLOR = (0, 255, 0)  # Green

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

    # Add people count indicator
    cv2.rectangle(annotated_image, (10, 10), (350, 80), (0, 0, 0), -1)
    cv2.putText(annotated_image, 
                f"People Detected: {people_count}",
                (20, 40), 
                cv2.FONT_HERSHEY_SIMPLEX, 
                1, 
                PERSON_COLOR, 
                2)
    
    # Add detection confidence info if any people detected
    if people_count > 0:
        avg_confidence = np.mean(person_detections.confidence)
        cv2.putText(annotated_image, 
                    f"Avg Confidence: {avg_confidence:.2f}",
                    (20, 70), 
                    cv2.FONT_HERSHEY_SIMPLEX, 
                    0.8, 
                    PERSON_COLOR, 
                    2)

    return annotated_image, people_count

def main():
    # Process the image
    print(f"Processing image: {TEST_IMAGE}")
    result, people_count = process_human_detection(TEST_IMAGE)

    if result is not None:
        # Save output
        os.makedirs("output", exist_ok=True)
        output_path = f"output/detected_{os.path.basename(TEST_IMAGE)}"
        cv2.imwrite(output_path, result)
        print(f"Result saved to: {output_path}")
        print(f"Number of people detected: {people_count}")

        # Display result
        cv2.imshow("Human Detection Result", result)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

if __name__ == "__main__":
    main()