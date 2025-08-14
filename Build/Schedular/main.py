from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
import numpy as np
import tensorflow as tf
import uvicorn
import os
import requests
from dotenv import load_dotenv
import threading
import time
from tensorflow.keras.losses import mse
from sklearn.preprocessing import MinMaxScaler
# Load .env file
load_dotenv()

BACKEND_URLS = os.getenv("BACKEND_URLS").split(",")
CLOUD_SERVER_URL = os.getenv("CLOUD_SERVER_URL")
MEM_THRESHOLD = float(os.getenv("MEM_THRESHOLD"))
CPU_THRESHOLD = float(os.getenv("CPU_THRESHOLD"))
CHECK_INTERVAL = float(os.getenv("CHECK_INTERVAL", "30"))
scaler=MinMaxScaler()
# Load LSTM model
model = tf.keras.models.load_model('lstm_model.h5',compile=False)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global variable + lock to track best backend safely
best_backend_url = None
best_backend_lock = threading.Lock()

def periodic_health_check():
    global best_backend_url
    while True:
        best_node = None
        best_score = float('inf')  # lower combined CPU+MEM is better

        for backend_url in BACKEND_URLS:
            try:
                metrics_response = requests.get(f"{backend_url}/metrics", timeout=5)
                if metrics_response.status_code == 200:
                    data = metrics_response.json()
                    instances_raw = data.get("instances")

                    last_10_instances = np.array([
                        [
                            inst["current_requests"],
                            inst["cpu_percent"],
                            inst["memory_percent"],
                            inst["net_bytes_sent"],
                            inst["net_bytes_recv"],
                            inst["num_threads"]
                        ]
                        for inst in instances_raw
                    ])
                    
                    last_10_instances = scaler.fit_transform(last_10_instances)
                    if last_10_instances.shape == (10, 6):
                        input_data = last_10_instances.reshape((1, 10, 6))
                        prediction = model.predict(input_data, verbose=0)
                        predicted_cpu = prediction[0][0]
                        predicted_mem = prediction[0][1]
                        combined_score = predicted_cpu + predicted_mem

                        print(f"[{backend_url}] CPU: {predicted_cpu:.4f}, MEM: {predicted_mem:.4f}, Score: {combined_score:.4f}")

                        if (predicted_cpu < CPU_THRESHOLD and
                            predicted_mem < MEM_THRESHOLD and
                            combined_score < best_score):
                            best_node = backend_url
                            best_score = combined_score
                    else:
                        print(f"[{backend_url}] Invalid shape after extraction: {last_10_instances.shape}")
                else:
                    print(f"[{backend_url}] Failed to get metrics (status {metrics_response.status_code})")
            except Exception as e:
                print(f"[{backend_url}] Error: {e}")

        with best_backend_lock:
            best_backend_url = best_node

        if best_node:
            print(f"[Health Check] Best backend selected: {best_node} (Score: {best_score:.4f})")
        else:
            print("[Health Check] No backend under threshold; will use cloud fallback")

        time.sleep(CHECK_INTERVAL)

@app.on_event("startup")
def startup_event():
    threading.Thread(target=periodic_health_check, daemon=True).start()

@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    image_bytes = await file.read()
    with best_backend_lock:
        target_url = best_backend_url if best_backend_url else CLOUD_SERVER_URL

    print(f"[Predict] Forwarding to: {target_url}")

    try:
        files = {'file': (file.filename, image_bytes, file.content_type)}
        response = requests.post(f"{target_url}/predict", files=files, timeout=10)
        if response.status_code != 200:
            return {"error": f"Failed to forward to {target_url}", "status_code": response.status_code}

        return {"handled_by": target_url, "response": response.json()}
    except Exception as e:
        return {"error": f"Exception forwarding to {target_url}: {e}"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=5001, reload=True)
