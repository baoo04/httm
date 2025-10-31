from flask import Flask, render_template, jsonify, send_from_directory, request
import os
from controllers import model_controller
from services.model_service import ModelService

app = Flask(__name__)

@app.route("/traffic_sign_model")
def traffic_sign_model():
    return render_template("traffic_sign_model.html")

@app.route('/')
def home():
    return render_template('Home.html')

@app.route('/manage_model')
def manage_model():
    return model_controller.get_models()

@app.route('/retrain', methods=['POST'])
def retrain():
    return model_controller.retrain_model()

@app.route('/save_model', methods=['POST'])
def save_model():
    return model_controller.save_model()

@app.route('/get_dataset', methods=['GET'])
def get_dataset():
    dataset_info = model_controller.get_datasets_from_cloud()
    return dataset_info

# 🆕 Route để lấy danh sách ảnh từ dataset/images
@app.route('/get_images', methods=['GET'])
def get_images():
    datasets = model_controller.get_datasets_from_cloud()
    return jsonify({"datasets": datasets})

@app.route('/dataset/<int:dataset_id>/images/<filename>')
def serve_image(dataset_id, filename):
    datasets = model_controller.get_datasets_from_cloud()
    
    # Tìm dataset theo id
    dataset = next((d for d in datasets if d["id"] == dataset_id), None)
    if not dataset:
        return "Dataset not found", 404

    dataset_path = dataset["cloudPath"]
    image_dir = os.path.join(dataset_path, "images")
    return send_from_directory(image_dir, filename)

@app.route("/retrain_selected", methods=["POST"])
def retrain_selected():
    data = request.json
    selected_images = data.get("images", [])
    if not selected_images:
        return jsonify({"error": "No images selected"}), 400

    # 1️⃣ Tạo temporary dataset
    dataset_path, yaml_path = ModelService.prepare_selected_dataset(selected_images)

    # 2️⃣ Train model
    model = ModelService.retrain(dataset_path=dataset_path, yaml_path=yaml_path)

    return jsonify({
        "name": model.name,
        "version": model.version,
        "precision": model.pre,
        "recall": model.recall,
        "f1_score": model.f1_score,
        "path": model.path
    })


if __name__ == '__main__':
    app.run(debug=True)
