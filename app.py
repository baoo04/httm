from flask import Flask, render_template, jsonify, send_from_directory, request, session, redirect, url_for
from utils.exceptions import NotFoundException, UnAuthException
from services.model_service import ModelService
from services.sample_service import SampleService
from services.model_service import ModelService
from services.dataset_service import DatasetService
from services.admin_service import AdminService
from utils.middleware import login_required
import os

app = Flask(__name__)

sample_service = SampleService()
model_service = ModelService()
dataset_service = DatasetService()
admin_service = AdminService()

@app.route("/traffic_sign_model", methods=['GET'])
@login_required
def traffic_sign_model():
    return render_template("traffic_sign_model.html")

@app.route('/', methods=['GET'])
@login_required
def home():
    return render_template('Home.html')

@app.route('/models', methods=['GET'])
@login_required
def get_all_models():
    models = model_service.get_all_models()
    return jsonify({"models": models}), 200

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        return render_template('Login.html')
    data = request.json
    username = data.get("username")
    password = data.get("password")
    try:
        admin = admin_service.login(username, password)
        session["admin_id"] = admin.id
        return jsonify({ 
            "admin": {
                "id": admin.id,
                "username": admin.username,
                "full_name": admin.full_name
            },
        }), 200
    except UnAuthException as e:
        return jsonify({"error": str(e)}), 401
    except Exception as e:
        return jsonify({"error": "Internal server error"}), 500
    
@app.route('/logout', methods=['POST'])
@login_required
def logout():
    session.pop("admin_id", None)
    return redirect(url_for('login'))

@app.route('/datasets', methods=['GET'])
@login_required
def get_all_datasets():
    datasets = dataset_service.get_all_datasets()
    return jsonify({"datasets": datasets}), 200

@app.route('/samples/<int:id>', methods=['GET'])
@login_required
def get_sample_by_id(id):
    try:
        sample = sample_service.get_sample_by_id(id)
        image_path = sample.image_path
        directory = os.path.dirname(image_path)
        filename = os.path.basename(image_path)
        return send_from_directory(directory, filename)
    except NotFoundException as e:
        return jsonify({"error": str(e)}), 404
    except Exception as e:
        return jsonify({"error": "Internal server error"}), 500
    
@app.route("/models/<int:id>/retrain", methods=["PUT"])
@login_required
def retrain_selected():
    data = request.json
    selected_images = data.get("images")
    if not selected_images:
        return jsonify({"error": "No images selected"}), 400

    dataset_path, yaml_path = model_service.prepare_selected_dataset(selected_images)

    model = model_service.retrain(dataset_path=dataset_path, yaml_path=yaml_path)

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
