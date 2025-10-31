import shutil
import os
import random
import json
from ultralytics import YOLO
from datetime import datetime
from models.traffic_sign_model import TrafficSignModel
from dao.model_dao import ModelDAO
from dao.sample_dao import SampleDAO
from dao.dataset_dao import DatasetDAO
from utils.exceptions import NotFoundException
from flask import session

class ModelService:
    def __init__(self):
        self.model_dao = ModelDAO()
        self.sample_dao = SampleDAO()
        self.dataset_dao = DatasetDAO()

    def get_all_models(self):
        models = self.model_dao.find_all()
        models_list = []
        for m in models:
            models_list.append(m.to_dict())
        return models_list

    def split_dataset(self):
        IMG_DIR = "temp_dataset/images"
        LABEL_DIR = "temp_dataset/labels"
        TRAIN_IMG = "temp_dataset/images/train"
        TEST_IMG = "temp_dataset/images/test"
        TRAIN_LBL = "temp_dataset/labels/train"
        TEST_LBL = "temp_dataset/labels/test"

        for d in [TRAIN_IMG, TEST_IMG, TRAIN_LBL, TEST_LBL]:
            os.makedirs(d, exist_ok=True)

        images = [f for f in os.listdir(IMG_DIR) if f.endswith('.jpg')]
        random.shuffle(images)

        split_idx = int(0.7 * len(images))
        train_files = images[:split_idx]
        test_files = images[split_idx:]

        for files, img_dest, lbl_dest in [(train_files, TRAIN_IMG, TRAIN_LBL), (test_files, TEST_IMG, TEST_LBL)]:
            for f in files:
                shutil.copy(os.path.join(IMG_DIR, f), os.path.join(img_dest, f))
                label_file = f.replace('.jpg', '.txt')
                shutil.copy(os.path.join(LABEL_DIR, label_file), os.path.join(lbl_dest, label_file))

        print(f"✅ Done! Train: {len(train_files)}, Test: {len(test_files)}")

    
    def retrain(self, id, dataset_id, image_ids):
        dataset = self.dataset_dao.find_by_id(dataset_id)
        if not dataset:
            raise NotFoundException("Dataset not found")

        samples = self.sample_dao.find_all_by_ids(image_ids)

        temp_dir = "F:/HTTM/temp_dataset"
        images_dir = os.path.join(temp_dir, "images")
        labels_dir = os.path.join(temp_dir, "labels")
        os.makedirs(images_dir, exist_ok=True)
        os.makedirs(labels_dir, exist_ok=True)

        for sample in samples:
            shutil.copy(sample.image_path, images_dir)
            shutil.copy(sample.label_path, labels_dir)

        yaml_path = dataset.yaml_path
        
        self.split_dataset()

        # Train YOLO
        yolo = YOLO("yolov8n.pt")
        results = yolo.train(data=yaml_path, epochs=10, imgsz=416)

        # Lấy đường dẫn thư mục train
        train_dir = results.save_dir  # ví dụ: runs/detect/train5

        # Đọc file metrics từ YOLO output
        metrics_file = os.path.join(train_dir, "results.json")
        if os.path.exists(metrics_file):
            with open(metrics_file, "r") as f:
                metrics = json.load(f)
            precision = metrics.get("metrics/precision(B)", 0)
            recall = metrics.get("metrics/recall(B)", 0)
            f1_score = metrics.get("metrics/f1(B)", 0)
        else:
            precision, recall, f1_score = 0, 0, 0

        # Cập nhật is_trained = True
        id_list = [sample.id for sample in samples]
        self.sample_dao.mark_as_trained(id_list)

        # Xóa folder tạm
        shutil.rmtree(temp_dir, ignore_errors=True)

        # Trả ra model info
        model = TrafficSignModel(
            id=id,
            name=f"YOLOv8_TrafficSign_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            version=int(datetime.now().strftime('%H%M%S')),
            pre=precision,
            recall=recall,
            f1_score=f1_score,
            sample_quantity=len(samples),
            dataset_id=dataset.id,
            path=os.path.join(train_dir, "weights", "best.pt"),
        )
        
        session["pending_model"] = model.to_dict()
        return model
    
    def save_trained_model(self, model_id):
        pending_model_data = session.get("pending_model")
        if not pending_model_data or pending_model_data.get("id") != model_id:
            raise NotFoundException("No pending model found")

        model = TrafficSignModel(
            id=model_id,
            name=pending_model_data["name"],
            version=pending_model_data["version"] + 1,
            pre=pending_model_data["pre"],
            recall=pending_model_data["recall"],
            f1_score=pending_model_data["f1_score"],
            is_active=True,
            sample_quantity=pending_model_data["sample_quantity"],
            dataset_id=pending_model_data["dataset_id"],
            path=pending_model_data["path"],
        )

        self.model_dao.update(model)
        return model
        
        