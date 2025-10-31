import os
import time
from config import MODEL_STORAGE

def get_dataset_from_cloud(cloud_path):
    """
    Giả lập tải dataset từ cloud.
    cloud_path có thể là một URL hoặc ID. Ở đây ta mô phỏng bằng sleep và trả sample list.
    """
    # In log
    print(f"[Cloud] Fetching dataset from {cloud_path} ...")
    time.sleep(1)  # simulate network
    # Return a minimal structure
    dataset = {
        "dataset_name": os.path.basename(cloud_path) if cloud_path else "demo_dataset",
        "samples": [
            {"id": 1, "imagePath": "images/img1.jpg"},
            {"id": 2, "imagePath": "images/img2.jpg"},
            {"id": 3, "imagePath": "images/img3.jpg"},
        ],
        "labels": [
            {"id": 1, "title": "stop"},
            {"id": 2, "title": "no_entry"},
        ]
    }
    return dataset

def simulate_training(save_path, selected_samples, label_file):
    """
    Giả lập một job training — tạo file model giả, trả về metrics.
    """
    print("[Train] Start simulated training...")
    time_taken = 2
    time.sleep(time_taken)
    # create dummy model file
    model_file_path = os.path.join(save_path, f"yolo_sim_{int(time.time())}.pt")
    with open(model_file_path, "wb") as f:
        f.write(b"FAKE MODEL DATA")
    # fake metrics
    metrics = {
        "name": os.path.basename(model_file_path),
        "version": 1,
        "precision": 0.90,
        "recall": 0.88,
        "f1_score": 0.89,
        "is_active": False,
        "sample_quantity": len(selected_samples),
        "path": model_file_path
    }
    print(f"[Train] Finished. model saved at {model_file_path}")
    return metrics
