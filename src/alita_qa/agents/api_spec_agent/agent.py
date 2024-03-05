#    Copyright 2023 EPAM Systems

#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at

#        http://www.apache.org/licenses/LICENSE-2.0

#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.


from analysta_llm_agents.agent.agent import Agent
from ...config import ai_model, llm_model_config, embedding_model_params, vectorstore, vectorstore_params
from .actions import __all__ as actions

agent_prompt = """You are autonomosus bot tasked to create yaml file following openapi v3 spec from repository provided to you. 
You can expect Github repository, organization and branch as an input, as well as description of technologies used for application developer.

Your goal is to create a yaml files with openapi v3 spec and provide to the user.

Steps to follow:
1. Understand the structure of the repository and retrieve necessary files
2. Use getRepoTree command to retrieve a tree structure of repository
3. Retrieve file content one by one using getRawFile command
4. Create separate openAPI specs for every endpoint based on the code retrieved from the repository
5. Validate that requests and schemas in openapi spec is correct according to corresponsing code
6. Create OpenAI for all endpoints within repository and provide them to the user once ready
7. Save openapi spec using storeSpecFile command
8. Complete task only after all files with endpoints are processed
"""


agent_constraints = """ - Every generated OpenAPI spec must be self-contained yaml with required details in it
 - Files content can be retrieved only one by one, so be smart and efficient
 - Do not ask LLM for help, you have to do it on your own
 - Do not ask User for help, you have to do it on your own
 - Provide openapi yaml files once they are ready
 - Do not repeat commands, unless absolutely necessary
 """

class RepoToSwagger(Agent):
    def __init__(self, ctx, **kwargs):
        super().__init__(
            agent_prompt=agent_prompt,
            llm_model_type='AzureChatOpenAI',
            llm_model_params=llm_model_config,
            embedding_model='AzureOpenAIEmbeddings',
            embedding_model_params=embedding_model_params,
            short_term_memory_limit=16000,
            vectorstore=vectorstore,
            vectorstore_params=vectorstore_params,
            agent_constraints=agent_constraints,
            tools=actions,
            ctx=ctx
        )

    @property
    def __name__(self):
        return "Git Repo to Swagger API Spec"
    
    @property
    def __description__(self):
        return """Bot helping to convert Github repository into OpenApi 3.0 spec, 
to be used in Swagger or Postman. It require repo to be public."""