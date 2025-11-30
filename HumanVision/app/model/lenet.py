import tensorflow as tf
import numpy as np
import os


class HumanVisionModel:
    def __init__(self):
        self.model = tf.keras.models.Sequential([
            tf.keras.layers.Conv2D(filters=6, kernel_size=(5, 5), activation='relu', input_shape=(150, 150, 3)),
            tf.keras.layers.AvgPool2D(pool_size=(2, 2), strides=2),
            tf.keras.layers.Conv2D(filters=16, kernel_size=(5, 5), activation='relu'),
            tf.keras.layers.AvgPool2D(pool_size=(2, 2), strides=2),
            tf.keras.layers.Flatten(),
            tf.keras.layers.Dense(units=120, activation='relu'),
            tf.keras.layers.Dense(units=84, activation='relu'),
            tf.keras.layers.Dense(units=1, activation='sigmoid')
        ])
        print(self.model.summary())

        # Construct the absolute path to the weights file
        try:
            base_dir = os.path.dirname(os.path.abspath(__file__))
            weights_path = os.path.join(base_dir, 'weights', 'saved_models', 'human_prediction(2)_.weights.h5')

            if os.path.exists(weights_path):
                self.model.load_weights(weights_path)
                print(f"✅ Successfully loaded weights from: {weights_path}")
            else:
                print(f"❌ ERROR: Weights file not found at: {weights_path}")
        except Exception as e:
            print(f"❌ An error occurred while loading weights: {e}")

    def predict(self, img: np.ndarray):
        """
        Predicts the label for the input image.
        :param img: numpy array with shape (1, 150, 150, 3)
        :return: prediction result
        """
        preds = self.model.predict(img)
        return preds


human_vision_model = HumanVisionModel()
