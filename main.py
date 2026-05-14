import os
import requests
from langchain_openai import ChatOpenAI
from langchain.agents import create_agent
from langchain.tools import tool
from langchain_core.messages import HumanMessage
from tavily import TavilyClient
from langchain_tavily import TavilySearch

from dotenv import load_dotenv
load_dotenv()


def get_llama_model(base_url=os.getenv("ENDPOINT_URI")):
    for endpoint in ("/v1/models", "/models"):
        try:
            r = requests.get(base_url + endpoint, timeout=3)
            if r.ok:
                j = r.json()

                if isinstance(j, dict):
                    if "data" in j and j["data"]:
                        return j["data"][0].get("id")

                    if "models" in j and j["models"]:
                        return j["models"][0]
        except Exception:
            pass
    return None


# tavily = TavilyClient()

# @tool
# def search(query: str) -> str:
#     """
#     Tool that searches over internet
#     Args:
#         query: The query to search for
#     Returns: 
#         The search result
#     """
#     print(f"Searching for {query}")
#     return tavily.search(query=query)


llm = ChatOpenAI(
    base_url=os.getenv("ENDPOINT_URI")+"/v1",
    api_key=os.getenv("OPENAI_API_KEY"),
    model=get_llama_model(),
)
# tools = [search]
tools = [TavilySearch()]
agent = create_agent(model=llm, tools=tools)


def main():
    print("Hello from udemy-langchain!")
    result = agent.invoke({"messages": HumanMessage(content="search for 3 job postings for an ai engineer using langchain in the bay area on linkedin and list their details")})
    print(result)


if __name__ == "__main__":
    main()
