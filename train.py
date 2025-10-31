import os
import glob
from ultralytics import YOLO
from dao.model_dao import ModelDAO
from models.traffic_sign_model import TrafficSignModel
import torch

def train_yolo_model():
    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"Đang train bằng: {device}")

    model = YOLO("yolov8n.pt")

    results = model.train(
        data="dataset/data.yaml",
        epochs=5,
        imgsz=416,
        batch=4,
        device=device,
        project="runs/detect",
        name="traffic_sign_model",
        exist_ok=True
    )

    metrics = results.results_dict
    precision = metrics.get('metrics/precision(B)', 0)
    recall = metrics.get('metrics/recall(B)', 0)
    f1_score = 2 * (precision * recall) / (precision + recall + 1e-8)

    print(f"\n📊 Kết quả training:")
    print(f"Precision: {precision:.4f}")
    print(f"Recall:    {recall:.4f}")
    print(f"F1-score:  {f1_score:.4f}")

    # ✅ Đếm số ảnh train/test thực tế
    base_dir = os.path.join(os.path.dirname(__file__), "dataset", "images")
    train_image_dir = os.path.join(base_dir, "train")
    test_image_dir = os.path.join(base_dir, "test")

    sample_quantity = (
        len(glob.glob(os.path.join(train_image_dir, "*.jpg"))) +
        len(glob.glob(os.path.join(train_image_dir, "*.png"))) +
        len(glob.glob(os.path.join(test_image_dir, "*.jpg"))) +
        len(glob.glob(os.path.join(test_image_dir, "*.png")))
    )

    dataset_id = 1
    model_path = os.path.abspath("runs/detect/traffic_sign_model")

    traffic_model = TrafficSignModel(
        name="YOLOv8 Traffic Sign",
        version=1,
        precision=round(precision, 4),
        recall=round(recall, 4),
        f1_score=round(f1_score, 4),
        is_active=1,
        sample_quantity=sample_quantity,
        dataset_id=dataset_id,
        path=model_path
    )

    dao = ModelDAO()
    dao.save_model(traffic_model)

    print("\n✅ Model đã được train và lưu thông tin vào CSDL thành công!")

if __name__ == "__main__":
    train_yolo_model()
