import logging
from os import environ
from dotenv import load_dotenv

from alita_sdk.llms.alita import AlitaChatModel
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
    "model": "gpt-4-0125-preview",
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
    DatasourceSearch(name="PylonSearch", description="Search Runtime Codebase", datasource=pylonds),
    DatasourcePredict(name="AuthAnalyse", description="Alita auth codebase summarization", datasource=authds),
    DatasourcePredict(name="CoreAnalyse", description="Alita core modules codebase summarization", datasource=coreds),
    DatasourceSearch(name="AuthSearch", description="Search Auth Codebase", datasource=authds),
    DatasourceSearch(name="CoreSearch", description="Search Core Modules Codebase", datasource=coreds)
]

openai_tools = [
    {
        'name': 'PylonAnalyse', 
        'description': 'Alita runtime and plugin framework codebase summarization', 
        'parameters': {
            'properties': {
                'query': {
                    'description': 'qurty to search and summarize results for Alita Pylon', 
                    'type': 'string'
                }
            }, 
            'required': ['query'], 
            'type': 'object'
        }
    }, 
    {
        'name': 'AuthAnalyse', 
        'description': 'Alita auth codebase summarization', 
        'parameters': {
            'properties': {
                'query': {
                    'description': 'qurty to search and summarize results for Alita Auth', 
                    'type': 'string'
                }
            }, 
            'required': ['query'], 
            'type': 'object'
        }
    },  
    {
        'name': 'CoreAnalyse', 
        'description': 'Alita core modules codebase summarization', 
        'parameters': {
            'properties': {
                'query': {
                    'description': 'qurty to search and summarize results for Alita Core', 
                    'type': 'string'
                }
            }, 
            'required': ['query'], 
            'type': 'object'
        }
    }, 
    {
        'name': 'PylonSearch', 
        'description': 'Search Runtime Codebase',
        'parameters': {
            'properties': {
                'query': {
                    'description': 'qurty to search within Alita Pylon', 
                    'type': 'string'
                }
            }, 
            'required': ['query'], 
            'type': 'object'
        }
    }, 
    {
        'name': 'AuthSearch', 
        'description': 'Search Auth Codebase', 
        'parameters': {
            'properties': {
                'query': {
                    'description': 'qurty to search within Alita Auth', 
                    'type': 'string'
                }
            }, 
            'required': ['query'], 
            'type': 'object'
        }
    }, 
    {
        'name': 'CoreSearch', 
        'description': 'Search Core Modules Codebase', 
        'parameters': {
            'properties': {
                'query': {
                    'description': 'qurty to search within Alita Core Modules', 
                    'type': 'string'
                }
            }, 
            'required': ['query'], 
            'type': 'object'
        }
    }
]
    
from langchain_community.callbacks.streamlit import (
    StreamlitCallbackHandler,
)
import streamlit as st

st_callback = StreamlitCallbackHandler(st.container())

import streamlit as st

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state["messages"] = []
    
    #
    # This example is for langchain based agents. Obvious limitation - only gpt-4, mixtrail and other advanced models.
    #
    # assistant = llm.client.assistant(prompt_id=1, prompt_version_id=2, tools=tools, model_settings={}, client=llm)
    # st.session_state.agent_executor = assistant.getAgentExecutor()
    
    
    # This one is for openai based agents
    client = AzureChatOpenAI(
        api_key=environ.get("DIAL_AUTH_TOKEN"),
        azure_endpoint=environ.get("DIAL_ENDPOINT"),
        azure_deployment="gpt-4-0125-preview",
        api_version="2023-12-01-preview"
    )
    assistant = llm.client.assistant(prompt_id=1, prompt_version_id=1, 
                                     tools=tools, openai_tools=openai_tools, 
                                     model_settings={}, client=client)
    st.session_state.agent_executor = assistant.getOpenAIAgentExecutor()
    


for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


if prompt := st.chat_input():
    st.chat_message("user").write(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("assistant"):
        st_callback = StreamlitCallbackHandler(st.container())
        response = st.session_state.agent_executor.invoke(
            {"content": prompt, "chat_history": st.session_state.messages}, {"callbacks": [st_callback]}
        )
        st.write(response["output"])
        
        st.session_state.messages.append({"role": "assistant", "content": response["output"]})
    