from flask import render_template, request, jsonify
from services.model_service import ModelService
from dao.model_dao import ModelDAO

model_service = ModelService()
model_dao = ModelDAO()

def get_models():
    models = model_dao.get_models()
    return render_template('TrafficSignManage.html', models=models)

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
