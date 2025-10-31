from flask import Flask, render_template
from controllers import model_controller

app = Flask(__name__)

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

if __name__ == '__main__':
    app.run(debug=True)
