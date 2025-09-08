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

'''# ✅ Image model (pretrained ResNet)
image_model = models.resnet18(pretrained=True)
image_model.eval()
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
])
'''


# for custom trained image model
# ✅ Image moderation model
nsfw_model = pipeline("image-classification", model="Falconsai/nsfw_image_detection")


'''
# pip install ultralytics
from ultralytics import YOLO
yolo = YOLO('yolov8n.pt')  # small, fast
'''

''' for custom trained model
# Labels for ImageNet classes
with open("imagenet_classes.txt") as f:
    labels = [line.strip() for line in f.readlines()]
'''
labels = ["safe", "toxic", "hate", "spam"]  # example custom labels. Adjust as needed.

'''sentimanet analysis 
@app.post("/predict-text")
async def predict_text(text: str = Form(...)): # just replace predict_text(...)
    result = sentiment_model(text)[0]
    return {"label": result["label"], "score": result["score"]}
'''


classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")
@app.post("/moderate-text")
async def moderate_text(text: str = Form(...)):
    result = classifier(text, candidate_labels=labels)
    return {"category": result["labels"][0], "confidence": result["scores"][0]}


""" for rule based text detector
@app.post("/predict-text")
async def predict_text(text: str = Form(...)):
    txt = text.lower()
    keywords = ["won", "lottery", "click here", "free", "earn", "guaranteed", "transfer"]
    score = sum(1 for k in keywords if k in txt) / len(keywords)
    label = "SCAM" if score >= 0.25 else "LEGIT"
    return {"label": label, "score": float(score)}
"""

'''
#✅ Image model endpoint for sentimatent analysis
@app.post("/Moderate-image") # replace ResNet inference with a different detector (YOLO) if needed.
async def predict_image(file: UploadFile = File(...)):
    contents = await file.read()
    image = Image.open(io.BytesIO(contents)).convert("RGB")
    img_t = transform(image).unsqueeze(0)
    with torch.no_grad():
        outputs = image_model(img_t)
        _, predicted = outputs.max(1)
        label = labels[predicted.item()]
    return {"label": label}
'''
#✅ Image moderation endpoint
@app.post("/moderate-image")
async def moderate_image(file: UploadFile = File(...)):
    contents = await file.read()
    image = Image.open(io.BytesIO(contents)).convert("RGB")

    # Run moderation
    results = nsfw_model(image)

    # The pipeline returns a list of labels with scores
    return {"moderation_results": results}


'''
@app.post("/predict-image")
async def predict_image(file: UploadFile = File(...)):
    contents = await file.read()
    img_path = "/tmp/upload.jpg"
    with open(img_path, "wb") as f: f.write(contents)
    results = yolo(img_path)  # returns detection results
    # parse detections:
    detections = results[0].boxes  # .cls for classes, .conf for confidence
    # create human readable summary:
    if len(detections) == 0:
        return {"label": "no_objects"}
    top = detections.data[0]  # adjust parsing by version
    return {"label": str(top)}
'''




