from fastapi import FastAPI, UploadFile, HTTPException
from fastapi.responses import PlainTextResponse
import pandas as pd

# # Path to the CSV dataset containing image results
DATA_FILE_PATH = 'Resources/dataset/Classification Results on Face Dataset (1000 images).csv'

def load_csv_to_dict():  
    """
     Checks if the image name exists in the lookup dictionary and returns its result.
     Raises a 404 error if the image is not found.
    """  
    try:
        data = pd.read_csv(DATA_FILE_PATH)
        return dict(zip(data['Image'], data['Results']))
    except FileNotFoundError:
        raise HTTPException(status_code=500, detail="CSV file not found")

image_result_lookup = load_csv_to_dict()

app = FastAPI()

async def find_image_result(image_name):
    """
    Checks if the image name exists in the lookup dictionary and returns its result.
    Raises a 404 error if the image is not found.
    """
    if image_name not in image_result_lookup:
        raise HTTPException(status_code=404, detail=f"Image '{image_name}' not found in the lookup dictionary")
    return image_result_lookup[image_name]

@app.post("/", response_class=PlainTextResponse)
async def classify_image(inputFile: UploadFile):
    """
    Endpoint to classify an uploaded image file based on its filename.
    Returns the result of the classification from the preloaded dataset.
    """
    image_name = inputFile.filename.split('.')[0]
    classification_result = await find_image_result(image_name)
    return f"{image_name}:{classification_result}"
