import os
import dotenv
import requests

from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_anthropic import ChatAnthropic
from langchain_openai import ChatOpenAI 
from core.tools.linkedin import scrape_linkedin_profile
from core.agents.linkedin_lookup import lookup as linkedin_lookup_agent

dotenv.load_dotenv()

def ice_break_with(name: str) -> str:
    linkedin_profile_url = linkedin_lookup_agent(name)
    linkedin_data = scrape_linkedin_profile(linkedin_profile_url=linkedin_profile_url, mock=True)
    
    summary_template = """
        given the Linkedin information {information} about a person I want you to create:
        1. A short summary
        2. two interesting facts about the person
    """
    
    summary_prompt_template = PromptTemplate(input_variables=["information"], template=summary_template)
    
    llm = ChatOpenAI(temperature=0, model_name="gpt-4o-mini")
    
    # llm = ChatAnthropic(model_name="claude-3-5-haiku-20241022")
    
    chain = summary_prompt_template | llm | StrOutputParser()
    
    res = chain.invoke(input={"information": linkedin_data})
    
    print(res)

if __name__ == '__main__':
    print("Hello LangChain!")

    ice_break_with("Eden Marco Udemy Profile")