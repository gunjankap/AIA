import os
from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
from location2 import predict_disease_with_ensemble

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/predict", methods=["POST"])
def predict():
    if "image" not in request.files or "city" not in request.form:
        return jsonify({"error": "Missing image or city"}), 400

    image_file = request.files["image"]
    city = request.form["city"]

    filename = secure_filename(image_file.filename)
    image_path = os.path.join(UPLOAD_FOLDER, filename)
    image_file.save(image_path)

    try:
        predicted_disease, temp, humidity = predict_disease_with_ensemble(image_path, city)
        os.remove(image_path)
        return jsonify({
            "disease": predicted_disease,
            "temperature": temp,
            "humidity": humidity
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)