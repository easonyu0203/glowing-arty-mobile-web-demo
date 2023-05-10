import base64
from io import BytesIO
import torch
from PIL import Image

from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from transformers import pipeline

model_checkpoint = "eason0203/swin-tiny-patch4-window7-224-finetuned-arty"

# Check if CUDA is available, and set the device accordingly
if torch.cuda.is_available():
    device = 0  # Use GPU device 0
else:
    device = -1  # Use CPU

pipe = pipeline("image-classification", "eason0203/swin-tiny-patch4-window7-224-finetuned-arty", device=device)

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Base64Image(BaseModel):
    data_url: str


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}

@app.post("/predict")
async def predict(base64_image: Base64Image):
    # Extract the base64-encoded image data
    image_data = base64.b64decode(base64_image.data_url.split(",")[1])

    # Load the image data into a PIL Image object
    image = Image.open(BytesIO(image_data))

    # Run the image through the pre-trained model
    predictions = pipe(image)

    return JSONResponse(content=predictions)
