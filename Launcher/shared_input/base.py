# shared_input/base.py

import os
import joblib
import tensorflow as tf

def load_model_and_scaler(model_path="gesture_recognition_model.h5",
                          encoder_path="label_encoder.pkl",
                          scaler_path="scaler.pkl"):
    base_path = os.path.dirname(__file__)
    model = tf.keras.models.load_model(os.path.join(base_path, model_path))
    encoder = joblib.load(os.path.join(base_path, encoder_path))
    scaler = joblib.load(os.path.join(base_path, scaler_path))
    return model, encoder, scaler
