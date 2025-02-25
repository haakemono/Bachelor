import cv2
import numpy as np
import tensorflow as tf
import joblib
import mediapipe as mp

class GestureRecognizer:
    def __init__(self, model_path="gesture_recognition_model.h5", encoder_path="label_encoder.pkl", scaler_path="scaler.pkl"):
        # Load the trained model, label encoder, and scaler
        self.model = tf.keras.models.load_model(model_path)
        self.label_encoder = joblib.load(encoder_path)
        self.scaler = joblib.load(scaler_path)

        # Initialize MediaPipe Hand Tracking
        self.mp_hands = mp.solutions.hands
        self.mp_drawing = mp.solutions.drawing_utils
        self.hands = self.mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7)

        # Start video capture
        self.cap = cv2.VideoCapture(0)
        self.last_prediction = None  # Store last recognized gesture

    def get_gesture(self):
        """
        Captures a frame, processes hand landmarks, and predicts a gesture.
        Returns:
            str: Predicted gesture label or None if no valid hand detected.
        """
        ret, frame = self.cap.read()
        if not ret:
            return None

        # Flip the frame for natural hand tracking
        frame = cv2.flip(frame, 1)
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.hands.process(rgb_frame)

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                # Extract landmark coordinates
                landmarks = []
                for lm in hand_landmarks.landmark:
                    landmarks.extend([lm.x, lm.y, lm.z])  # Flatten x, y, z coordinates

                # Convert to NumPy array and reshape for model prediction
                landmarks = np.array(landmarks, dtype=np.float32).reshape(1, -1)

                # 🔹 Apply the same scaling as during training
                if landmarks.shape[1] == self.model.input_shape[1]:  # Input dimension check
                    landmarks_scaled = self.scaler.transform(landmarks)  # Normalize input

                    prediction = self.model.predict(landmarks_scaled, verbose=0)  # Suppress printing
                    predicted_class = np.argmax(prediction)  # Get highest probability class
                    gesture_name = self.label_encoder.inverse_transform([predicted_class])[0]

                    # Avoid redundant predictions
                    if gesture_name != self.last_prediction:
                        self.last_prediction = gesture_name  # Update last recognized gesture
                        return gesture_name  # Return the detected gesture
        return None

    def release(self):
        """Releases the camera resources."""
        self.cap.release()
        cv2.destroyAllWindows()
