from ultralytics import YOLO
import os

# Set API key
os.environ["ULTRALYTICS_API_KEY"] = "ul_5d36ad30ffb94858917e30780df6a6a3a52385dc"

# Load model
model = YOLO("yolo26n.pt")

# Train
model.train(
    data="ul://putr4hh/datasets/muka-baim-marcell",
    epochs=30,
    batch=16,
    imgsz=640,
    project="putr4hh/face-recognite-3"
)