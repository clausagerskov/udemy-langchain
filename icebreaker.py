"""Icebreaker module."""
from dotenv import load_dotenv
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_ollama import ChatOllama
from loguru import logger
from third_parties.linkedin import scrape_linkedin_profile
from agents.linkedin_lookup_agent import lookup as linkedin_lookup_agent

from output_parsers import summary_parser, Summary


def ice_break_with(name: str) -> Summary:
    linkedin_username = linkedin_lookup_agent(name=name)
    linkedin_data = scrape_linkedin_profile(linkedin_profile_url=linkedin_username, mock=True)

    summary_template = """
        given the LinkedIn information {information} about a person I want you to create:
        1. a short summary
        2. two interesting facts about them
    \n{format_instructions}

    """

    summary_prompt_template = PromptTemplate(
        input_variables=["information"],
        template=summary_template,
        partial_variables={"format_instructions": summary_parser.get_format_instructions()},
    )

    llm = ChatOllama(model="llama3")

    # chain = summary_prompt_template | llm | StrOutputParser()
    chain = summary_prompt_template | llm | summary_parser

    res:Summary = chain.invoke(input={"information": linkedin_data})

    
    return res

if __name__=="__main__":
    load_dotenv()
    logger.info("Ice Breaker Enter!")

    ice_break_with(name="Claus Agerskov")

