import numpy as np
from fastapi import FastAPI, File, UploadFile, BackgroundTasks
from tensorflow.keras.preprocessing import image
import tensorflow as tf
from io import BytesIO
from PIL import Image
import requests
import psutil
import os
import threading
import time
from collections import deque

REMOTE_SERVER_URL = os.getenv("REMOTE_SERVER_URL", "http://default-server:8080/data")

model = tf.keras.models.load_model('./cnn_model_converted.h5')

labels = [
    "airplane", "automobile", "bird", "cat", "deer",
    "dog", "frog", "horse", "ship", "truck"
]

app = FastAPI()

current_requests = 0
lock = threading.Lock()

# Zero snapshot template
zero_snapshot = {
    "current_requests": 0,
    "cpu_percent": 0.0,
    "memory_percent": 0.0,
    "net_bytes_sent": 0,
    "net_bytes_recv": 0,
    "num_threads": 0
}

# Initialize deque with 10 zero entries
metrics_window = deque([zero_snapshot.copy() for _ in range(10)], maxlen=10)

def send_image_to_remote_server(image_bytes: bytes, filename: str):
    try:
        files = {'file': (filename, image_bytes, 'image/jpeg')}
        response = requests.post(REMOTE_SERVER_URL, files=files)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Error sending image to remote server: {e}")

def capture_system_metrics():
    while True:
        cpu = psutil.cpu_percent(interval=0.1)
        mem = psutil.virtual_memory().percent
        net_io = psutil.net_io_counters()
        p = psutil.Process()
        num_threads = p.num_threads()

        snapshot = {
            "current_requests": current_requests,
            "cpu_percent": cpu,
            "memory_percent": mem,
            "net_bytes_sent": net_io.bytes_sent,
            "net_bytes_recv": net_io.bytes_recv,
            "num_threads": num_threads
        }

        with lock:
            metrics_window.append(snapshot)

        time.sleep(1)

@app.on_event("startup")
def startup_event():
    threading.Thread(target=capture_system_metrics, daemon=True).start()
    print("Background system metrics capturing started.")

@app.post("/predict")
async def predict(file: UploadFile = File(...), background_tasks: BackgroundTasks = None):
    global current_requests

    with lock:
        current_requests += 1

    try:
        image_bytes = await file.read()
        img = Image.open(BytesIO(image_bytes)).resize((32, 32))
        img_array = np.array(img) / 255.0
        img_array = np.expand_dims(img_array, axis=0)

        predictions = model.predict(img_array)
        predicted_index = np.argmax(predictions[0])
        predicted_label = labels[predicted_index]

        if background_tasks:
            background_tasks.add_task(send_image_to_remote_server, image_bytes, file.filename)

        return {
            "class": predicted_label,
            "current_requests": current_requests
        }
    finally:
        with lock:
            current_requests -= 1

@app.get("/metrics")
def get_metrics():
    with lock:
        metrics_list = list(metrics_window)
    return {"instances": metrics_list}
