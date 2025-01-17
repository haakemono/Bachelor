import cv2
import mediapipe as mp
import numpy as np
import random
import time
from collections import deque

# Initialize MediaPipe Hands
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

# Initialize the camera
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Error: Could not open camera.")
    exit()

# Game Variables
xy_plane = np.zeros((500, 500, 3), dtype=np.uint8)
basket_width = 100  # Width of the basket
basket_height = 20  # Height of the basket
basket_y = 480      # Fixed Y position of the basket
apple_radius = 10   # Radius of the apple
apples = []         # List to hold falling apples
score = 0           # Player's score
last_apple_time = time.time()  # Time when the last apple was generated
apple_spawn_interval = 1  # Time interval between apple spawns (in seconds)

# Smoothing parameters
smoothing_window_size = 5
position_history = deque(maxlen=smoothing_window_size)  # Stores the last few positions

# Function to spawn a new apple
def spawn_apple():
    x = random.randint(apple_radius, 500 - apple_radius)
    y = 0
    apples.append([x, y])

# Initialize MediaPipe Hands
with mp_hands.Hands(min_detection_confidence=0.5, min_tracking_confidence=0.5) as hands:
    try:
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            # Resize the frame for faster processing
            small_frame = cv2.resize(frame, (640, 480))
            rgb_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)

            # Process the frame
            results = hands.process(rgb_frame)

            # Control basket position using hand
            basket_x = 250  # Default position of the basket (centered)
            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    mp_drawing.draw_landmarks(small_frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

                    # Get wrist position (landmark 0)
                    wrist = hand_landmarks.landmark[mp_hands.HandLandmark.WRIST]

                    # Map wrist X position to the basket position on the XY plane
                    basket_x = int((wrist.x) * 500)

                    # Add the current position to the history
                    position_history.append(basket_x)

            # Smooth the basket position using a moving average
            if position_history:
                basket_x = int(sum(position_history) / len(position_history))

            # Constrain basket position within the plane
            basket_x = max(basket_width // 2, min(500 - basket_width // 2, basket_x))

            # Update and draw apples
            new_apples = []
            for apple in apples:
                apple[1] += 5  # Move apple down
                if apple[1] < 500:  # Keep apple on screen
                    new_apples.append(apple)

                # Check for collision with basket
                if basket_y - apple_radius <= apple[1] <= basket_y + basket_height and \
                        basket_x - basket_width // 2 <= apple[0] <= basket_x + basket_width // 2:
                    score += 1  # Increase score for catching apple
                else:
                    # Draw the apple
                    cv2.circle(xy_plane, (apple[0], apple[1]), apple_radius, (0, 0, 255), -1)

            apples = new_apples

            # Spawn a new apple at intervals
            if time.time() - last_apple_time > apple_spawn_interval:
                spawn_apple()
                last_apple_time = time.time()

            # Draw the basket
            cv2.rectangle(
                xy_plane,
                (basket_x - basket_width // 2, basket_y),
                (basket_x + basket_width // 2, basket_y + basket_height),
                (255, 255, 255),
                -1
            )

            # Display the score
            cv2.putText(
                xy_plane,
                f"Score: {score}",
                (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (255, 255, 255),
                2
            )

            # Display the annotated frame and game
            cv2.imshow("Hand Movement Tracking", small_frame)
            cv2.imshow("Apple Falling Game", xy_plane)

            # Clear the XY plane for fresh drawing
            xy_plane = np.zeros((500, 500, 3), dtype=np.uint8)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    except KeyboardInterrupt:
        print("Program interrupted.")
    finally:
        cap.release()
        cv2.destroyAllWindows()
