import sys
sys.path.append(r'c:\Users\haako\OneDrive\Documents\Skole\Bachelor\Bachelor\yolov5')

from yolov5.models.common import DetectMultiBackend
# Add the rest of your code here

import cv2
import torch
from yolov5.models.common import DetectMultiBackend
from yolov5.utils.dataloaders import LoadImages
from yolov5.utils.general import non_max_suppression, scale_coords
from yolov5.utils.plots import Annotator, colors

# Load YOLOv5 model
model_path = "yolov5s.pt"  # Use the appropriate YOLOv5 model (s, m, l, or custom)
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = torch.hub.load('ultralytics/yolov5', 'custom', path=model_path, force_reload=True)

# Open the camera
cap = cv2.VideoCapture(0)  # Change to 1 or another number if you have multiple cameras

if not cap.isOpened():
    print("Error: Could not open camera.")
    exit()

# Real-time detection
while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        print("Error: Could not read frame.")
        break

    # Inference
    results = model(frame)

    # Annotate the frame
    frame = results.render()[0]

    # Display the frame
    cv2.imshow("YOLOv5 Detection", frame)

    # Break the loop on 'q' key press
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release resources
cap.release()
cv2.destroyAllWindows()
