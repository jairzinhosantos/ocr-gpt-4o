from flask import Flask, request, jsonify
from ocr_model import OcrModel
import json
import logging

# Initialize the Flask application
app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load configuration parameters from JSON file
def load_parameters():
    parameters_path = "config/parameters.json"
    try:
        with open(parameters_path) as file:
            parameters_list = json.load(file)
        return parameters_list
    except FileNotFoundError:
        logger.error(f"Configuration file not found at {parameters_path}")
        return {}
    except json.JSONDecodeError:
        logger.error(f"Error decoding JSON from the configuration file at {parameters_path}")
        return {}

# Initialize OCR Model with loaded parameters
parameters = load_parameters()
ocr_model = OcrModel(parameters)

@app.route("/ocr_model", methods=["POST"])
def ocr_endpoint():
    # API endpoint to extract text from a image using OCR Model with GPT-4o.
    try:
        logger.info("Running ocr_response instance...")
        ocr_response = ocr_model.ocr_response()
        return ocr_response
        #return jsonify(model_response), 200
    except Exception as e:
        logger.error(f"Error during OCR Model processing: {e}")
        return jsonify({"error": str(e)}), 500

def start_app():
    """
    Starts the Flask application.
    """
    # Set local parameters
    host=parameters["host"]
    port=parameters["port"]

    # Run app
    app.run(host=host, port=port, debug=True)