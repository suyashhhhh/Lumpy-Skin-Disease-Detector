import logging
import numpy as np
import tensorflow as tf
from tensorflow.keras.preprocessing import image as keras_image
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input

try:
    model = tf.keras.models.load_model("11JuneModel.h5")
    logging.info("Model loaded successfully.")
except Exception as e:
    logging.error(f"Model loading failed: {e}")

class_names = ['Healthy Cow', 'Lumpy Cow']

def predict_image(img):
    try:
        img_resized = img.resize((224, 224))
        img_array = keras_image.img_to_array(img_resized)
        img_preprocessed = preprocess_input(np.expand_dims(img_array, axis=0))
        prediction = model.predict(img_preprocessed)
        confidence = float(np.max(prediction)) * 100
        return class_names[np.argmax(prediction)], confidence
    except Exception as e:
        logging.error(f"Prediction failed: {e}")
        return "Prediction Error", 0.0
