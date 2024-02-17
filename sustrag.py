import os
from langchain_openai import ChatOpenAI
from langchain.tools import DuckDuckGoSearchRun
from langchain.agents import initialize_agent
from langchain.agents import Tool
from langchain.tools import WikipediaQueryRun
from langchain.utilities import WikipediaAPIWrapper
from langchain.tools import YouTubeSearchTool

from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
import os
# from langchain_community.llms import LlamaCpp

# TOOL FUNCTIONS
from dotenv import load_dotenv 
load_dotenv()
ddg_search = DuckDuckGoSearchRun()
wikipedia = WikipediaQueryRun(api_wrapper=WikipediaAPIWrapper())
youtube = YouTubeSearchTool()

# ans=ddg_search.run("What is a coplanar vector")
# print(ans)
os.environ["OPENAI_API_KEY"] = os.getenv('OPENAI_API_KEY')
llm = ChatOpenAI(model_name="gpt-4-1106-preview")

tools = [
   Tool(
       name="DuckDuckGo Search",
       func=ddg_search.run,
       description="Useful to browse information from the Internet.",
   ),
   Tool(
       name="Wikipedia Search",
       func=wikipedia.run,
       description="Useful when you need to get more explanations on something",
   ),
   Tool(
       name="Youtube Search",
       func=youtube.run,
       description="Useful for when the user asks you to find videos.",
   )
]
agent = initialize_agent(
   tools, llm=llm, agent="zero-shot-react-description", verbose=True,handle_parsing_errors=True
)
agent.run("How to find the resultant of two vectors. Explain to me with a few examples and maths in details. Also suggest me some videos on this as well")