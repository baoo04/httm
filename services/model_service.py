from models.traffic_sign_model import TrafficSignModel
from dao.model_dao import ModelDAO
from ultralytics import YOLO
from datetime import datetime
import controllers.model_controller
import os
import shutil
import random

class ModelService:
    def __init__(self):
        self.dao = ModelDAO()

    def get_dataset(self):
        dataset_info = controllers.model_controller.get_dataset_from_cloud()
        return dataset_info["dataset_path"], dataset_info["yaml_path"]

    def prepare_selected_dataset(self, selected_images):
        """
        Tạo dataset tạm thời gồm images/labels/ và data.yaml
        """
        temp_dir = "temp_dataset"
        images_dir = os.path.join(temp_dir, "images")
        labels_dir = os.path.join(temp_dir, "labels")
        os.makedirs(images_dir, exist_ok=True)
        os.makedirs(labels_dir, exist_ok=True)

        for img_name in selected_images:
            # copy ảnh từ folder gốc vào temp
            shutil.copy(f"dataset/images/{img_name}", os.path.join(images_dir, img_name))

            # copy label tương ứng (giả sử tên trùng .txt)
            label_name = img_name.rsplit(".", 1)[0] + ".txt"
            shutil.copy(f"dataset/labels/{label_name}", os.path.join(labels_dir, label_name))

        # Tạo data.yaml giống cũ
        yaml_path = os.path.join(temp_dir, "data.yaml")
        with open(yaml_path, "w") as f:
            f.write(f"""
        train: {images_dir}
        val: {images_dir}
        nc: 10  # số class
        names: ['class0','class1','class2','class3','class4','class5','class6','class7','class8','class9']
        """)
        return temp_dir, yaml_path

    def retrain(self, dataset_path, yaml_path, selected_images):
        model = YOLO("yolov8n.pt")
        results = model.train(data=yaml_path, epochs=10, imgsz=416)

        best_path = getattr(results, "best", None)
        if not best_path:
            best_path = os.path.join("runs", "detect", "train", "weights", "best.pt")

        metrics_dict = getattr(results, "metrics", {}).results_dict() if hasattr(results, "metrics") else {}
        pre = round(metrics_dict.get("metrics/precision(B)", 0.9), 4)
        recall = round(metrics_dict.get("metrics/recall(B)", 0.9), 4)
        f1_score = round(metrics_dict.get("metrics/mAP50(B)", 0.9), 4)

        new_model = TrafficSignModel(
            name=f"YOLOv8_TrafficSign_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            version=random.randint(1,999),
            pre=pre,
            recall=recall,
            f1_score=f1_score,
            is_active=0,
            sample_quantity=len(selected_images),
            dataset_id=1,
            path=best_path
        )
        return new_model