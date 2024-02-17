import requests
from flask import Flask, request, jsonify
from openai import OpenAI
import os
from dotenv import load_dotenv 

load_dotenv()

app = Flask(__name__)

# # Initialize OpenAI client with your API key
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
print(os.getenv('OPENAI_API_KEY'))

@app.route('/detectobjects', methods=['GET','POST'])
def detect_objects_api():
    if request.method == 'POST':
        # Get the image from the request body
        data = request.json
        image_url = data.get('image_url')
        print(image_url)
        
        # Prepare the request data for OpenAI API
        request_data = {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": "What are the objects in the following image? List just the item name separated by comma. Avoid any detail",
                },
                {
                    "type": "image_url",
                    "image_url": {
                        "url": image_url,
                    },
                },
            ],
        }

        # Make a request to OpenAI API
        response = client.chat.completions.create(
            model="gpt-4-vision-preview",
            messages=[request_data],
        )

        # Extract the detected objects from the response
        detected_objects = response.choices[0].message.content

        # Return the detected objects as JSON response
        return jsonify(detected_objects)
    
    elif request.method == 'GET':
        return "This endpoint only accepts POST requests."

if __name__ == '__main__':
    app.run(debug=True)
