import sys
import cv2
import torch

path_to_append = r'c:\Users\haako\OneDrive\Documents\Skole\Bachelor\Bachelor\yolov5'
if path_to_append not in sys.path:
    sys.path.append(path_to_append)


from yolov5.utils.general import non_max_suppression  # Removed scale_coords (deprecated)
from yolov5.utils.plots import Annotator, colors

# Load YOLOv5 model
model_path = "yolov5s.pt"  # Replace with your model path if different
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# Load the YOLOv5 model from Torch Hub
model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)

# Open the camera
cap = cv2.VideoCapture(0)  # Replace 0 with the appropriate index for your camera

if not cap.isOpened():
    print("Error: Could not open camera.")
    exit()

# Real-time detection
while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        print("Error: Could not read frame.")
        break

    # Convert the frame to a tensor and perform inference
    results = model(frame)

    # Annotate the frame with detection results
    annotated_frame = results.render()[0]

    # Display the annotated frame
    cv2.imshow("YOLOv5 Detection", annotated_frame)

    # Break the loop on 'q' key press
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release resources
cap.release()
cv2.destroyAllWindows()
