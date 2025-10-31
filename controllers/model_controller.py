from dao.dataset_dao import DatasetDAO
from flask import render_template, request, jsonify
from services.model_service import ModelService
from dao.model_dao import ModelDAO

model_service = ModelService()
model_dao = ModelDAO()

def get_models():
    models = model_dao.get_models()
    models_list = []
    for m in models:
        models_list.append({
            "name": m.name,
            "version": m.version,
            "pre": m.pre,
            "recall": m.recall,
            "f1_score": m.f1_score,
            "sample_quantity": m.sample_quantity,
            "dataset_id": m.dataset_id,
            "path": m.path
        })
    return jsonify(models_list)

def retrain_model():
    dataset = model_service.get_dataset_from_cloud()
    dataset_path = dataset["dataset_path"]
    model = model_service.retrain(dataset_path)
    return jsonify({
        "name": model.name,
        "version": model.version,
        "precision": model.pre,
        "recall": model.recall,
        "f1_score": model.f1_score,
        "sample_quantity": model.sample_quantity,
        "dataset_id": model.dataset_id,
        "path": model.path
    })

def save_model():
    model_data = request.json
    saved_model = model_service.save_model(model_data)
    return jsonify({
        "message": "Model saved successfully!",
        "model_name": saved_model.name,
        "path": saved_model.path
    })

def get_datasets_from_cloud():
    dao = DatasetDAO()
    datasets = dao.get_datasets()

    return datasets