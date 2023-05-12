import base64
from io import BytesIO
import PIL
from PIL import Image

from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from transformers import pipeline

model_checkpoint = "eason0203/swin-tiny-patch4-window7-224-finetuned-arty"
model_checkpoint = "facebook/convnext-base-224"


pipe = pipeline("image-classification", model_checkpoint, device=-1)

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

@app.post("/test")
async def post_test():
    return JSONResponse(content={"message": "Hello World"})

@app.post("/predict")
async def predict(base64_image: Base64Image):
    # Extract the base64-encoded image data
    image_data = base64.b64decode(base64_image.data_url.split(",")[1])

    # Load the image data into a PIL Image object
    try:
        image = Image.open(BytesIO(image_data))
    except PIL.UnidentifiedImageError:
        return JSONResponse(content=[])

    # Run the image through the pre-trained model
    predictions = pipe(image)

    return JSONResponse(content=predictions)
