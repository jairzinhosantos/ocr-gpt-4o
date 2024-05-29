import os
import json
import logging
from flask import request, jsonify
from dotenv import load_dotenv
from openai import OpenAI
import base64

# Load environment variables once at the beginning
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class OcrModel:
    """
    Represents a OCR Model with GPT-4o.
    """

    def __init__(self, parameters) -> None:
        # Set parameters
        self.llm_model = parameters["llm_model"]
        self.max_tokens = parameters["max_tokens"]
        self.instruction = parameters["instruction"]
        self.key_saveimage = parameters["key_saveimage"]
        self.key_saveresponse = parameters["key_saveresponse"]
        self.schema_path = parameters["schema_path"]
        self.input_path = parameters["input_path"]
        self.output_path = parameters["output_path"]


    def image_upload(self, saveimage):
        # Handles the image upload from a Flask request and saves it to a specified path.     
        try:
            logger.info("Capturing the image")
            image = request.files["image"]
            if saveimage.lower() == 'yes':
                logger.info("Saving the image")
                image_path = os.path.join(self.input_path, image.filename)
                image.save(image_path)
                logger.info(f"Image {image.filename} uploaded successfully.")
                return {
                        "status": "success",
                        "message": f"Image {image.filename} uploaded successfully.",
                        }, image
            return { 
                    "status": "not saved",
                    "message": f"Image {image.filename} not saved",
                    }, image
        except Exception as e:
            logger.error(f"Error during image upload: {e}")
            return jsonify({"error": str(e)}), 500

    def get_request(self, key):
        # Retrieves a specific key from a JSON request.
        return request.json.get(key)
    
    def process_data(self, file, mode):
        # Handles file reading and base64 encoding
        if mode == 'r':
            with open(file, mode) as data:
                return json.load(data)
        elif mode == 'rb':
            return base64.b64encode(file.read()).decode('utf-8')        

    def ocr_response(self):
        # Processes a image and generates a response from the OCR Model.
        try:
            logger.info("Setting OpenAI key secret...")
            openai_api_key = os.getenv("OPENAI_API_KEY")
            if not openai_api_key:
                raise ValueError("OPENAI_API_KEY not found in environment variables")
            
            logger.info("Setting OpenAI client...")
            client = OpenAI()

            logger.info("Setting schema for the text extraction...")
            schema = self.process_data(self.schema_path, 'r')

            #logger.info("Capturing keys and image from user...")
            #saveimage = self.get_request(self.key_saveimage)
            #saveresponse = self.get_request(self.key_saveresponse)

            logger.info("Setting variables to store input and output data...")
            saveimage = ''
            saveresponse = ''
            
            logger.info("Getting response from the image upload")
            response_image_upload = self.image_upload(saveimage)
            logger.info(response_image_upload["message"])

            logger.info("Transforming image to base64")
            image = response_image_upload[1]
            image_base64 = self.process_data(image, 'rb')

            logger.info("Setting the response configuration")
            response = client.chat.completions.create(
                            model=self.llm_model,
                            response_format={"type": "json_object"},
                            messages=[{
                                        "role": "user",
                                        "content": [{
                                            "type": "text", 
                                            "text": self.instruction + json.dumps(schema)},
                                                {
                                            "type": "image_url",
                                            "image_url": {
                                                    "url": f"data:image/jpeg;base64,{image_base64}"}}
                                                    ],}],
                                        max_tokens=self.max_tokens,
                                )

            logger.info("Getting the response")
            ocr_response = json.loads(response.choices[0].message.content)
            
            # Save the response if the user requests it
            if saveresponse.lower() == 'yes':
                logger.info("Saving the response")
                output_path = os.path.join(self.output_path, f"{image.filename}.json")
                with open(output_path, 'w') as file:
                    json.dump(ocr_response, file, indent=4)

            return jsonify(ocr_response), 200
        except Exception as e:
            logger.error(f"Error generating OCR Model response: {e}")
            return jsonify({"error": str(e)}), 500


