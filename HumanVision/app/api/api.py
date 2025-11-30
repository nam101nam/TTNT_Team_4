from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from PIL import Image
import numpy as np
import io
import os

# Import a single instance of the model that automatically loads weights
# The 'human_vision_model' object is created in app/model/lenet.py
try:
    from app.model.lenet import human_vision_model
except ImportError:
    # This fallback is for cases where the app is run from a different directory
    from model.lenet import human_vision_model


# Create the API router
api_router = APIRouter()

@api_router.post("/predict", tags=["Prediction"])
async def predict_image(file: UploadFile = File(...)):
    """
    Receives an image file, preprocesses it, and returns a prediction.
    """
    # Ensure the uploaded file is an image
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File provided is not an image.")

    try:
        # Read image content
        image_data = await file.read()
        image = Image.open(io.BytesIO(image_data)).convert('RGB')

        # Preprocess the image for the model
        # 1. Resize to the model's expected input size
        image = image.resize((150, 150))
        # 2. Convert to numpy array and scale pixels to [0, 1]
        image_array = np.array(image, dtype=np.float32) / 255.0
        # 3. Add a batch dimension
        image_batch = np.expand_dims(image_array, axis=0)

        # Make a prediction
        prediction = human_vision_model.predict(image_batch)

        # Extract the confidence value from the prediction array
        confidence = float(prediction[0][0])

        # Determine the label based on the confidence
        label = "person" if confidence > 0.5 else "no_person"

        # Return the result
        return JSONResponse(content={
            "prediction": label,
            "confidence": confidence
        })

    except Exception as e:
        # For debugging purposes
        print(f"An error occurred: {e}")
        # Return a generic error response
        raise HTTPException(status_code=500, detail=f"An error occurred during prediction: {str(e)}")