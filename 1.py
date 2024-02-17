from openai import OpenAI
import os
from dotenv import load_dotenv 
load_dotenv()

client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
print(os.getenv('OPENAI_API_KEY'))

image_url="https://i.ibb.co/Y3Xpncm/b.jpg"

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

print(detected_objects)