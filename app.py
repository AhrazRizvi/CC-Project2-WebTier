from fastapi import FastAPI, UploadFile, HTTPException
from fastapi.responses import PlainTextResponse
import pandas as pd

# Path to the CSV dataset containing image results
DATA_FILE_PATH = 'Resources/dataset/Classification Results on Face Dataset (1000 images).csv'

def load_csv_to_dict(file_path: str):
    """
    Reads the CSV file and converts it into a dictionary for fast lookup.
    The dictionary maps image names to their classification results.
    """
    try:
        data_frame = pd.read_csv(file_path)
        # return {row['Image']: row['Results'] for _, row in data_frame.iterrows()}
        return dict(zip(data_frame['Image'], data_frame['Results']))
    except FileNotFoundError:
        raise HTTPException(status_code=500, detail="CSV file is missing or cannot be found.")

# Preload the lookup dictionary from the CSV
image_result_lookup = load_csv_to_dict(DATA_FILE_PATH)

# Initialize FastAPI app
app = FastAPI()

async def find_image_result(image_name: str):
    """
    Checks if the image name exists in the lookup dictionary and returns its result.
    Raises a 404 error if the image is not found.
    """
    if image_name not in image_result_lookup:
        raise HTTPException(status_code=404, detail=f"Image '{image_name}' is not available in the dataset.")
    return image_result_lookup[image_name]

@app.post("/", response_class=PlainTextResponse)
async def classify_image(file: UploadFile):
    """
    Endpoint to classify an uploaded image file based on its filename.
    Returns the result of the classification from the preloaded dataset.
    """
    image_name = file.filename.rsplit('.', 1)[0]  # Get the image name without the file extension
    classification_result = await find_image_result(image_name)
    return f"{image_name}: {classification_result}"
