import os
import requests
from dotenv import load_dotenv
from loguru import logger

load_dotenv()

def scrape_linkedin_profile(linkedin_profile_url: str, mock: bool = False):
    """Scrape information from LinkedIn profiles.

    Manually scrape the information from the LinkedIn profile.
    """
    if mock:
        linkedin_profile_url = "https://gist.githubusercontent.com/clausagerskov/d2c94b7157bdf5363575732c855ddb97/raw/2332f24b29cc269ea42d1930418f0a174fdbbaf3/claus-agerskov.json"
        response = requests.get(
            linkedin_profile_url,
            timeout=10,
        )
    else:
        api_key = os.environ["PROXYCURL_API_KEY"]
        api_endpoint = os.environ["PROXYCURL_API_ENDPOINT"]
        header_dict = {"Authorization": "Bearer " + api_key}
        params = {
            "url": linkedin_profile_url,
        }
        response = requests.get(api_endpoint,
                                params=params,
                                headers=header_dict,
                                timeout=10,
                            )

    data = response.json()
    data = {
        k: v
        for k, v in data.items()
        if v not in ([], "", "", None)
        and k not in ["people_also_viewed", "certifications"]
    }
    if data.get("groups"):
        for group_dict in data.get("groups"):
            group_dict.pop("profile_pic_url")

    return data

if __name__=="__main__":

    logger.info(scrape_linkedin_profile(
        linkedin_profile_url="https://www.linkedin.com/in/claus-agerskov-5b899263/",
        mock=True,
    ))
