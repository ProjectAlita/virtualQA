import logging
from os import environ
from dotenv import load_dotenv

from alita_sdk.llms.alita import AlitaChatModel
from alita_sdk.agents import create_mixed_agent
from langchain.agents import  AgentExecutor
from langchain_openai import AzureChatOpenAI
from src.alita_qa.tools.git import getRawFile, getRepoTree
from src.alita_qa.tools.file import storeFile

from alita_sdk.tools.datasource import DatasourcePredict, DatasourceSearch


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

llm = AlitaChatModel(**settings)

pylonds = llm.client.datasource(1)
authds = llm.client.datasource(2)
coreds = llm.client.datasource(3)

tools = [
    DatasourcePredict(name="PylonAnalyse", description="Alita runtime and plugin framework codebase summarization", datasource=pylonds),
    DatasourcePredict(name="AuthAnalyse", description="Alita auth codebase summarization", datasource=authds),
    DatasourcePredict(name="CoreAnalyse", description="Alita core modules codebase summarization", datasource=coreds),
    DatasourceSearch(name="PylonSearch", description="Search Runtime Codebase", datasource=pylonds),
    DatasourceSearch(name="AuthSearch", description="Search Auth Codebase", datasource=authds),
    DatasourceSearch(name="CoreSearch", description="Search Core Modules Codebase", datasource=coreds)
]



# from langchain_core.utils.function_calling import convert_to_openai_function

# openai_tools = [convert_to_openai_function(tool) for tool in tools]

# print(openai_tools)

prompt = llm.client.prompt(prompt_id=1, prompt_version_id=1)

agent = create_mixed_agent(llm, tools, prompt)

agent_executor = AgentExecutor.from_agent_and_tools(agent=agent, tools=tools,
    verbose=True, handle_parsing_errors=True, max_execution_time=None,
    return_intermediate_steps=True)

# task = """Where is tools comming from, in case of `from tools import MinioClient` - what are the tools?"""

# for message in agent_executor.stream({"input": task}, include_run_info=True):
#     print(message)
    
    
from langchain_community.callbacks.streamlit import (
    StreamlitCallbackHandler,
)
import streamlit as st

st_callback = StreamlitCallbackHandler(st.container())

import streamlit as st
from langchain import hub
from langchain.agents import AgentExecutor, create_react_agent, load_tools

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state["messages"] = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

llm = AzureChatOpenAI(
        azure_endpoint=environ.get("DIAL_ENDPOINT"),
        deployment_name="gpt-4-1106-preview",
        openai_api_version="2023-03-15-preview",
        openai_api_key=environ.get('DIAL_AUTH_TOKEN')
    )

# from langchain_core.messages import HumanMessage, SystemMessage

# print(llm.invoke([
#     HumanMessage(content="What is the code for `from tools import MinioClient`?")
#     ], functions=tools))

if prompt := st.chat_input():
    st.chat_message("user").write(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("assistant"):
        st_callback = StreamlitCallbackHandler(st.container())
        response = agent_executor.invoke(
            {"input": prompt, "chat_history": st.session_state.messages}, {"callbacks": [st_callback]}
        )
        st.write(response["output"])
        
        st.session_state.messages.append({"role": "assistant", "content": response["output"]})