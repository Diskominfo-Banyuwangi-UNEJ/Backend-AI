from ultralytics import YOLO
import supervision as sv
import cv2

# Load your local YOLO model
model = YOLO("best.pt")

# Perform prediction
results = model("test3.jpeg", conf=0.05, iou=0.8)

detections = sv.Detections.from_ultralytics(results[0])

labels = [
    model.model.names[class_id]
    for class_id in detections.class_id
]

box_annotator = sv.BoxAnnotator()
label_annotator = sv.LabelAnnotator()

image = cv2.imread("test3.jpeg")
annotated_image = box_annotator.annotate(scene=image, detections=detections)
annotated_image = label_annotator.annotate(
    scene=annotated_image,
    detections=detections,
    labels=labels
)

sv.plot_image(image=annotated_image, size=(16, 16)