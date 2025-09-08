from fastapi import FastAPI, UploadFile, File, Form
from transformers import pipeline
from fastapi.middleware.cors import CORSMiddleware
from PIL import Image
import torch
import torchvision.transforms as transforms
import torchvision.models as models
import io

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, use your frontend URL instead of "*"
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Text model (sentiment analysis)
sentiment_model = pipeline("sentiment-analysis")

# ✅ Image model (pretrained ResNet)
image_model = models.resnet18(pretrained=True)
image_model.eval()
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
])

# Labels for ImageNet classes
with open("imagenet_classes.txt") as f:
    labels = [line.strip() for line in f.readlines()]

@app.post("/predict-text")
async def predict_text(text: str = Form(...)):
    result = sentiment_model(text)[0]
    return {"label": result["label"], "score": result["score"]}

@app.post("/predict-image")
async def predict_image(file: UploadFile = File(...)):
    contents = await file.read()
    image = Image.open(io.BytesIO(contents)).convert("RGB")
    img_t = transform(image).unsqueeze(0)
    with torch.no_grad():
        outputs = image_model(img_t)
        _, predicted = outputs.max(1)
        label = labels[predicted.item()]
    return {"label": label}




