# Import necessary libraries
from flask import Flask, request, jsonify
from openai import OpenAI
import os
from dotenv import load_dotenv 
load_dotenv()

app = Flask(__name__)

# Initialize OpenAI client with your API key
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

def generate_product_details(product_name):
    """
    Generates product details in markdown format for a given product name,
    including an example with diverse markdown formatting.
    """
    completion = client.chat.completions.create(
        model="gpt-4-1106-preview",
        messages=[
            {"role": "system", "content": "Given a product name, generate a detailed markdown document including the product's title, description, size variation, color variation, size chart, and other relevant details. Make sure there are at least 200 words in each point. Make table and listing as per requirement"},
            {"role": "user", "content": f'Product: {product_name}'},
        ],
        temperature=0.5,
        frequency_penalty=0.5,
    )

    return completion.choices[0].message.content

@app.route('/generateproductdetails', methods=['GET', 'POST'])
def generate_product_info():
    if request.method == 'POST':
        data = request.json
        product_names = data.get('Product_name', [])
        results = []
        for idx, product in enumerate(product_names, start=1):
            response = generate_product_details(product)
            results.append({
                "index": idx,
                "Product_name": product,
                "gpt4_markdown_response": response
            })
        return jsonify(results)
    elif request.method == 'GET':
        return "This endpoint only accepts POST requests."

if __name__ == '__main__':
    app.run(debug=True)
