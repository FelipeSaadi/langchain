import os
import dotenv

from langchain_core.tools import Tool
from langchain.agents import (
    create_react_agent,
    AgentExecutor
)
from langchain import hub
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from langchain_core.prompts import PromptTemplate
from core.tools.linkedin import get_profile_url_tavily

dotenv.load_dotenv()

def lookup(name: str) -> str:
    # llm = ChatOpenAI(
    #     temperature=0,
    #     model_name="gpt-4o-mini"
    # )
    
    llm = ChatAnthropic(model_name="claude-3-5-haiku-20241022")
    
    template = """
    given the full name {name_of_person} I want you to get it me a link to ther Linkedin profile page. Your answer should contain only a URL
    """
    
    prompt_template = PromptTemplate(
        template=template, input_variables=["name_of_person"]
    )
    tools_for_agent = [
        Tool(
            name="Crawl Google 4 linkedin profile page",
            func=get_profile_url_tavily,
            description="useful for when you need get the Linkedin Page URL"
        )
    ]
    
    react_prompt = hub.pull('hwchase17/react')
    
    agent = create_react_agent(llm=llm, tools=tools_for_agent, prompt=react_prompt)
    
    agent_executor = AgentExecutor(agent=agent, tools=tools_for_agent, verbose=True)
    
    result = agent_executor.invoke(
        input={"input": prompt_template.format_prompt(name_of_person=name)}
    )
    
    linkedin_profile_url = result['output']
    return linkedin_profile_url
