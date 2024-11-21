import requests
import dotenv
import os
from langchain_community.tools.tavily_search import TavilySearchResults

dotenv.load_dotenv()

def scrape_linkedin_profile(*, linkedin_profile_url: str, mock: bool = False):
    """
    scrape information from LinkedIn profiles,
    Manually scrape the information from the LinkedIn profile
    """
    
    if mock:
        linkedin_profile_url = "https://gist.githubusercontent.com/FelipeSaadi/64faf209be21f0ee80932b6cd80c328a/raw/5216620a62a423c06e3c417f1d10eeff45fa2313/felipe-saadi.json"
        
        response = requests.get(linkedin_profile_url, timeout=10)
    else:
        api_endpoint = "https://nubella.co/proxycurl/api/v2/linkedin"
        header={"Authorization": f"Bearer {os.getenv('PROXY_API_KEY')}"}
        
        response = requests.get(
            api_endpoint,
            params={"url": linkedin_profile_url},
            headers=header,
            timeout=10
        )
        
    data = response.json()
    
    data = {
        k: v
        for k, v in data.items()
        if v not in ([], "", "",None)
        and k not in ["people_also_viewed", "certifications"]
    }
    
    if data.get("groups"):
        for group_dict in data.get("groups"):
            group_dict.pop("profile_pic_url")
    
    return data

def get_profile_url_tavily(name: str):
    """Searchs for Linkedin or Twitter Profile Page."""
    
    search = TavilySearchResults()
    
    res = search.run(f"{name}")
    return res