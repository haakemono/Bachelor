import cv2
import mediapipe as mp

# Initialize MediaPipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=1, min_detection_confidence=0.5, min_tracking_confidence=0.5)

# Initialize MediaPipe Drawing
mp_drawing = mp.solutions.drawing_utils

# Function to recognize hand gestures
def recognize_gesture(hand_landmarks):
    landmarks = hand_landmarks.landmark

    # Get landmark positions
    thumb_tip = landmarks[mp_hands.HandLandmark.THUMB_TIP]
    thumb_ip = landmarks[mp_hands.HandLandmark.THUMB_IP]
    index_tip = landmarks[mp_hands.HandLandmark.INDEX_FINGER_TIP]
    index_pip = landmarks[mp_hands.HandLandmark.INDEX_FINGER_PIP]
    middle_tip = landmarks[mp_hands.HandLandmark.MIDDLE_FINGER_TIP]
    middle_pip = landmarks[mp_hands.HandLandmark.MIDDLE_FINGER_PIP]
    ring_tip = landmarks[mp_hands.HandLandmark.RING_FINGER_TIP]
    ring_pip = landmarks[mp_hands.HandLandmark.RING_FINGER_PIP]
    pinky_tip = landmarks[mp_hands.HandLandmark.PINKY_TIP]
    pinky_pip = landmarks[mp_hands.HandLandmark.PINKY_PIP]

    # Gesture Conditions:
    # 👍 **Thumbs Up**: Thumb extended, all other fingers folded
    if thumb_tip.y < thumb_ip.y and index_tip.y > index_pip.y and middle_tip.y > middle_pip.y:
        return "Thumbs Up"

    # ✌️ **Peace Sign**: Index and Middle fingers extended, others folded
    if index_tip.y < index_pip.y and middle_tip.y < middle_pip.y and ring_tip.y > ring_pip.y and pinky_tip.y > pinky_pip.y:
        return "Peace Sign"

    # ✊ **Fist**: All fingers folded
    if all(landmarks[finger].y > landmarks[finger - 2].y for finger in [
        mp_hands.HandLandmark.THUMB_TIP,
        mp_hands.HandLandmark.INDEX_FINGER_TIP,
        mp_hands.HandLandmark.MIDDLE_FINGER_TIP,
        mp_hands.HandLandmark.RING_FINGER_TIP,
        mp_hands.HandLandmark.PINKY_TIP,
    ]):
        return "Fist"

    # 👌 **OK Sign**: Thumb and Index touching, others extended
    if abs(thumb_tip.x - index_tip.x) < 0.05 and abs(thumb_tip.y - index_tip.y) < 0.05:
        return "OK Sign"

    # 🤘 Rock Sign: Index and Pinky fingers extended, others folded
    if index_tip.y < index_pip.y and pinky_tip.y < pinky_pip.y and middle_tip.y > middle_pip.y and ring_tip.y > ring_pip.y:
        return "Rock Sign"

    return "Unknown Gesture"

# Start Video Capture
cap = cv2.VideoCapture(0)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Convert BGR to RGB
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Process the frame and detect hands
    result = hands.process(rgb_frame)

    # Draw hand landmarks and recognize gestures
    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            # Recognize the gesture
            gesture = recognize_gesture(hand_landmarks)

            # Display gesture on screen
            cv2.putText(frame, f"Gesture: {gesture}", (10, 50), 
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)

    # Show the video feed
    cv2.imshow("Gesture Recognition", frame)

    # Exit if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release resources
cap.release()
cv2.destroyAllWindows()
