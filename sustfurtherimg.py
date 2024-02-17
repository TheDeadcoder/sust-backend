import requests
from flask import Flask, request, jsonify
from openai import OpenAI
from langchain_openai import ChatOpenAI
from langchain.tools import DuckDuckGoSearchRun
from langchain.agents import initialize_agent
from langchain.agents import Tool
from langchain.tools import WikipediaQueryRun
from langchain.utilities import WikipediaAPIWrapper
from langchain.tools import YouTubeSearchTool
# from langchain_community.utilities import GoogleSearchAPIWrapper
from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
import os
from dotenv import load_dotenv 

load_dotenv()


# search = GoogleSearchAPIWrapper()

app = Flask(__name__)

# # Initialize OpenAI client with your API key
ddg_search = DuckDuckGoSearchRun()
wikipedia = WikipediaQueryRun(api_wrapper=WikipediaAPIWrapper())
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
print(os.getenv('OPENAI_API_KEY'))
os.environ["OPENAI_API_KEY"] = os.getenv('OPENAI_API_KEY')
llm = ChatOpenAI(model_name="gpt-4-1106-preview")

# tools = [
#    Tool(
#        name="DuckDuckGo Search",
#        func=ddg_search.run,
#        description="Useful to browse information from the Internet.",
#    ),
#    Tool(
#        name="Wikipedia Search",
#        func=wikipedia.run,
#        description="Useful when you need to get more explanations on something",
#    ),
# #    Tool(
# #     name="google_search",
# #     description="Search Google for recent results.",
# #     func=search.run,
# #     )
# ]

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
                    "text": "What is the object in the following image? just Mention the object Avoid any detail",
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
        objects_list = detected_objects.split(', ')
        search_results = {}
        for obj in objects_list:
            # Here you can make API calls to other tools/services
            # For demonstration, using DuckDuckGo search
            search_query = f"Search the web for related products of {obj} and list some product URLs from marketplaces"
            # Assuming 'run' method exists and works for your search tools
            search_results[obj] = wikipedia.run(search_query)

        return jsonify(search_results)
    
    elif request.method == 'GET':
        return "This endpoint only accepts POST requests."

if __name__ == '__main__':
    app.run(debug=True)
