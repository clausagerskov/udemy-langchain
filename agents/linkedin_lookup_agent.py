from dotenv import load_dotenv
from langchain import hub
from langchain.agents import (
    AgentExecutor,
    create_react_agent,
    Tool,
)
from langchain_core.prompts import PromptTemplate
from langchain_ollama import ChatOllama
from tools.tools import get_profile_url_tavily

load_dotenv()


def lookup(name: str) -> str:
    llm = ChatOllama(
        temperature=0,
        model="llama3",
    )
    template = """given the full name {name_of_person} I want you to get me a link to their Linkedin profile page.
                        Your answer should contain only a URL."""

    prompt_template = PromptTemplate(
        template=template,
        input_variables=["name_of_person"],
    )

    tools_for_agent = [
        Tool(
            name="Crawl Google for linkedin profile page",
            func=get_profile_url_tavily,
            description="useful for when you need to get the Linkedin Page URL",
        ),
    ]

    react_prompt = hub.pull("hwchase17/react")
    agent = create_react_agent(llm=llm, tools=tools_for_agent, prompt=react_prompt)

    agent_executor = AgentExecutor(agent=agent, tools = tools_for_agent, handle_parsing_errors=True, verbose=True)

    results = agent_executor.invoke(
        input={"input": prompt_template.format_prompt(name_of_person=name)},
    )

    linkedin_profile_url = results["output"]
    return linkedin_profile_url


if __name__=="__main__":
    linkedin_url = lookup(name="Claus Agerskov")
