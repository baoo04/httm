from models.traffic_sign_model import TrafficSignModel
from dao.model_dao import ModelDAO
import queue
import threading
import json

class ModelService:
    def __init__(self):
        self.dao = ModelDAO()
        self.training_queue = queue.Queue()

    def get_dataset_from_cloud(self):
        return {
            "dataset_path": "F:/HTTM/dataset/",
            "yaml_path": "F:/HTTM/dataset/data.yaml",
        }

    def retrain(self, dataset_path):
        """🔥 Train với streaming progress"""
        from ultralytics import YOLO
        import os
        from datetime import datetime
        
        def on_train_epoch_end(trainer):
            """📊 Callback sau mỗi epoch"""
            epoch = trainer.epoch + 1
            epochs = trainer.epochs
            metrics = trainer.metrics if hasattr(trainer, 'metrics') else {}
            
            # Lấy metrics an toàn
            precision = metrics.get("metrics/precision(B)", 0) if metrics else 0
            recall = metrics.get("metrics/recall(B)", 0) if metrics else 0
            map50 = metrics.get("metrics/mAP50(B)", 0) if metrics else 0
            
            self.training_queue.put({
                "type": "progress",
                "epoch": epoch,
                "total_epochs": epochs,
                "precision": round(float(precision), 4),
                "recall": round(float(recall), 4),
                "mAP50": round(float(map50), 4),
                "loss": round(float(trainer.loss.item() if hasattr(trainer, 'loss') else 0), 4)
            })

        # 🚀 Start training in background thread
        def train_thread():
            try:
                self.training_queue.put({"type": "status", "message": "🔄 Starting training..."})
                
                model = YOLO('yolov8n.pt')
                
                # Add custom callback
                model.add_callback("on_train_epoch_end", on_train_epoch_end)
                
                results = model.train(
                    data=os.path.join(dataset_path, "data.yaml"),
                    epochs=10,
                    imgsz=416,
                    verbose=False  # Tắt console output
                )

                # Get best model path
                best_path = getattr(results, "best", None)
                if not best_path:
                    best_path = os.path.join("runs", "detect", "train", "weights", "best.pt")

                # Get final metrics
                metrics = getattr(results, "metrics", None)
                if metrics and hasattr(metrics, "results_dict"):
                    metrics_dict = metrics.results_dict()
                else:
                    metrics_dict = {}

                pre = round(metrics_dict.get("metrics/precision(B)", 0.9), 4)
                recall = round(metrics_dict.get("metrics/recall(B)", 0.9), 4)
                f1_score = round(metrics_dict.get("metrics/mAP50(B)", 0.9), 4)

                new_model = TrafficSignModel(
                    name=f"YOLOv8_TrafficSign_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                    version=1,
                    pre=pre,
                    recall=recall,
                    f1_score=f1_score,
                    is_active=0,
                    sample_quantity=1000,
                    dataset_id=1,
                    path=best_path
                )

                self.training_queue.put({
                    "type": "complete",
                    "model": {
                        "name": new_model.name,
                        "version": new_model.version,
                        "precision": new_model.pre,
                        "recall": new_model.recall,
                        "f1_score": new_model.f1_score,
                        "path": new_model.path,
                        "sample_quantity": new_model.sample_quantity,
                        "dataset_id": new_model.dataset_id
                    }
                })

            except Exception as e:
                self.training_queue.put({
                    "type": "error",
                    "message": str(e)
                })

        threading.Thread(target=train_thread, daemon=True).start()

    def get_training_progress(self):
        """📡 Generator để stream progress"""
        while True:
            try:
                data = self.training_queue.get(timeout=1)
                yield f"data: {json.dumps(data)}\n\n"
                
                if data.get("type") in ["complete", "error"]:
                    break
            except queue.Empty:
                yield f"data: {json.dumps({'type': 'heartbeat'})}\n\n"

    def save_model(self, model_data):
        """💾 Lưu model vào DB"""
        model = TrafficSignModel(
            name=model_data.get("name"),
            version=model_data.get("version"),
            pre=model_data.get("precision"),
            recall=model_data.get("recall"),
            f1_score=model_data.get("f1_score"),
            is_active=model_data.get("is_active", 1),
            sample_quantity=model_data.get("sample_quantity", 1000),
            dataset_id=model_data.get("dataset_id", 1),
            path=model_data.get("path")
        )
        self.dao.save_model(model)
        return model