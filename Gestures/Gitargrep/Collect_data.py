import cv2
import mediapipe as mp
import csv
import os

# Initialize MediaPipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=1, min_detection_confidence=0.5)

# Open webcam
cap = cv2.VideoCapture(0)

# Gesture mapping for labels
GESTURES = { 
    '1': "Em", '2': "E", '3': "Am", '4':"C", '5': "A", '6': "G", '7': "D", '8': "Dm", '9': "E7", '10': "D7", '11': "A7", '12': "C7" 
}

# Check if CSV file exists
file_exists = os.path.isfile("gitargrep_H.csv")

# Open CSV file in append mode
with open("gitargrep.csv", "a", newline="") as file:  
    writer = csv.writer(file)

    # Write header only if the file does not exist
    if not file_exists:
        header = ["gesture"]
        for i in range(21):  
            header.extend([f"x{i}", f"y{i}", f"z{i}"])  
        writer.writerow(header)

    print("\n Select a gesture type before starting:")
    for key, value in GESTURES.items():
        print(f"{key}: {value}")

    # Ask user to pick a gesture type once
    selected_gesture = input("\nEnter gesture number (1-12): ")
    while selected_gesture not in GESTURES:
        selected_gesture = input(" Invalid input. Please enter a valid number (1-12): ")

    gesture_name = GESTURES[selected_gesture]
    print(f"\n Recording gesture: {gesture_name}")
    print("\nPress 'S' to start/stop saving frames | Press 'Q' to quit.")

    saving = False  # Flag to track saving state

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            print(" Error: Could not capture frame.")
            break

        # Convert frame to RGB for MediaPipe processing
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        result = hands.process(rgb_frame)

        # Draw hand landmarks if detected
        if result.multi_hand_landmarks:
            for hand_landmarks in result.multi_hand_landmarks:
                mp.solutions.drawing_utils.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

                # Save landmark data if saving is enabled
                if saving:
                    landmark_data = [gesture_name]
                    for landmark in hand_landmarks.landmark:
                        landmark_data.append(landmark.x)
                        landmark_data.append(landmark.y)
                        landmark_data.append(landmark.z)
                    writer.writerow(landmark_data)
                    print(f" Saved landmark data for: {gesture_name}")

        # Show live video feed
        cv2.imshow("Gesture Collection", frame)

        # Wait for user input
        key = cv2.waitKey(1) & 0xFF  

        if key == ord('s'):  # Toggle saving state when 'S' is pressed
            saving = not saving
            if saving:
                print(f"\nStarted saving data for: {gesture_name}")
            else:
                print("\nStopped saving data.")

        elif key == ord('q'):  # Press 'Q' to quit
            print(" Exiting...")
            break

cap.release()
cv2.destroyAllWindows()
