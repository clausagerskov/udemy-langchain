import json
from langchain_community.tools.tavily_search import TavilySearchResults
from loguru import logger

def get_profile_url_tavily(name: str, mock=True):
    """Searches for Linkedin or Twitter Profile Page."""
    if mock:
        logger.info("Mocking Tavily Search")
        with open("./tools/tavily_res.json", "r") as f:
            res = json.loads(f.read())
    else:
        search = TavilySearchResults()
        res = search.run(f"{name}")
    
    return res
