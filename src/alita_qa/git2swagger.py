import logging
from os import environ
from dotenv import load_dotenv

from alita_sdk.llms.alita import AlitaChatModel
from alita_sdk.agents import create_mixed_agent
from langchain.agents import  AgentExecutor
from langchain_community.chat_models.azure_openai import AzureChatOpenAI

## Defining tools
from .tools.git import getRawFile, getRepoTree
from .tools.file import storeFile

logger = logging.getLogger(__name__)
try:
    load_dotenv('.env')
except:
    logger.warning("No .env file found, gonna rely on whatever set in the environment.")
    pass

## Minimal set of setting for AlitaChatModel
settings = {
    "deployment": "https://eye.projectalita.ai",
    "model": "gpt-4",
    "api_key": environ.get("AUTH_TOKEN"),
    "project_id": environ.get("PROJECT_ID"),
    "integration_uid": environ.get("INTEGRATION_UID"),
    "max_tokens": 2048,
    "stream": True
}


def main(task: str):
    ## Instantiating AlitaChatModel
    llm = AlitaChatModel(**settings)

    tools = [
        getRepoTree,
        getRawFile,
        storeFile
    ]

    prompt = llm.client.prompt(prompt_id=5, prompt_version_id=11)

    # llm = AzureChatOpenAI(
    #     azure_endpoint=environ.get("DIAL_ENDPOINT"),
    #     deployment_name="gpt-4-1106-preview",
    #     openai_api_version="2023-03-15-preview",
    #     openai_api_key=environ.get('DIAL_AUTH_TOKEN')
    # )
    
    agent = create_mixed_agent(llm, tools, prompt)

    agent_executor = AgentExecutor.from_agent_and_tools(agent=agent, tools=tools,
        verbose=True, handle_parsing_errors=True, max_execution_time=None,
        return_intermediate_steps=True)

    yield from agent_executor.stream({"input": task}, include_run_info=True)


