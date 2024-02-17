# import os
from openai import OpenAI
import pandas as pd
import os

from flask import Flask, request, jsonify

app = Flask(__name__)


client = OpenAI(
    api_key=os.getenv('OPENAI_API_KEY')
)


def generate_details(prompt):
    completion = client.chat.completions.create(
        model="gpt-4-1106-preview",
        messages=[
            {"role": "system", "content": "Given an input Topic name, you have to teach about the topic with proper details and examples. Here is an examples. Topic: How to talk to a customer? Response: Customers support your business and are the foundation for growth and development. Every client you work with is a potential spokesperson for your brand. Through proper customer communication, you'll be able to understand customers' concerns and establish personal relationships to improve the overall customer experience. You can learn how to talk to customers properly by practicing the following bullet points when you have a client conversation. 1. Be patient and respectful: When you talk to customers, listen actively and take the time to fully understand what they are saying to you. 2. Understand their goal or intention: You will have a more successful conversation with a customer when you identify the purpose of the conversation early on. 3. Maintain a positive tone while talking: Clients feel comfortable speaking to a customer support rep who maintains a consistent tone. 4. Validate your customers' concerns: You'll have a positive impact on how a customer feels when you make them feel validated. Don't dismiss their concerns or queries. 5. Admit any faults and offer a sincere apology:  When a customer reports a fault, take responsibility and apologize immediately. Also there are some other points like providing a useful solution, request for feedback, adding personal touch etc"},
            {"role": "user", "content":  f'Topic: {prompt} Response:'},
        ],
        temperature=0.5,
        frequency_penalty=0.5,
    )

    return completion.choices[0].message.content


# The training examples will come as api request. following is a dummy example
train_examples = ["How to Create a Marketing Plan?","How to Build a Brand Identity?","How to Use Social Media for Business?","How to Optimize Your Website for SEO?","How to Run Effective Email Marketing Campaigns?","How to Analyze Consumer Behavior?","How to Engage with Customers?","How to Conduct Market Research?","How to Measure Marketing ROI?"]



# to generate all inputs do "for i in range (0, len(confirmed_task)):"
@app.route('/generatedetails', methods=['GET', 'POST'])
def generate_questions():
    if request.method == 'POST':
        data = request.json
        topics = data.get('topics', [])  
        results = []
        for idx, topic in enumerate(topics, start=1):
            response = generate_details(topic)
            results.append({
                "index": idx,
                "Topic_name": topic,
                "gpt4_response": response
            })
        return jsonify(results)
    elif request.method == 'GET':
        return "This endpoint only accepts POST requests."

if __name__ == '__main__':
    app.run(debug=True)

# The json array will be the responce of the api request