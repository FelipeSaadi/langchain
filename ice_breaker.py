import os
import dotenv
import requests

from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_anthropic import ChatAnthropic
from langchain_openai import ChatOpenAI 

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

if __name__ == '__main__':
    print("Hello LangChain!")
    
    summary_template = """
        given the Linkedin information {information} about a person I want you to create:
        1. A short summary
        2. two interesting facts about the person
    """
    
    summary_prompt_template = PromptTemplate(input_variables=["information"], template=summary_template)
    
    # llm = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo")
    
    llm = ChatAnthropic(model_name="claude-3-5-haiku-20241022")
    
    chain = summary_prompt_template | llm | StrOutputParser()
    
    linkedin_data = scrape_linkedin_profile(linkedin_profile_url="", mock=True)
    
    res = chain.invoke(input={"information": linkedin_data})
    
    print(res)