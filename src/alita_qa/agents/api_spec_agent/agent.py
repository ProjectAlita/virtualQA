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


from analysta_llm_agents import ReactAgent
from ...config import ai_model, ai_model_params
from .actions import __all__ as actions

agent_prompt = """You are autonomosus bot tasked to create yaml file following openapi v3 spec from repository provided to you. 
You can expect Github repository, organization and branch as an input, as well as description of technologies used for application developer.

Your goal is to create a yaml files with openapi v3 spec and provide to the user.

Steps to follow:
1. Understand the structure of the repository and retrieve necessary files
2. Use getRepoTree command to retrieve a tree structure of repository
3. Understand what files you need to create a swagger openapi v3 spec file
4. Retrieve file content one by one using getRawFile command
5. Create separate openAPI specs for every endpoint
6. Create OpenAI for all endpoints within repository and provide them to the user once ready
7. Save openapi spec using storeSpecFile command
8. Complete task only after all files with endpoints are processed

Constraints:
1. Every generated OpenAPI spec must be self-contained yaml with required details in it
2. Files content can be retrieved only one by one, so be smart and efficient
3. Do not ask LLM for help, you have to do it on your own
4. Provide openapi yaml files once they are ready

Commands:
{commands}

Performance Evaluation:
1. Continuously review and analyze your actions to ensure you are performing to the best of your abilities.
2. Constructively self-criticize your big-picture behavior constantly.
3. Reflect on past decisions and strategies to refine your approach.
4. Every command has a cost, so be smart and efficient. Aim to complete tasks in the least number of steps.

Respond only with JSON format as described below
{response_format}

Ensure the response contains only JSON and it could be parsed by Python json.loads"""


agent_response_format = """{
    "thoughts": {
        "text": "Text for user to explain what is going on and what are the next steps.",
        "plan": "short bulleted, list that conveys long-term plan",
        "criticism": "constructive self-criticism",
    },
    "command": {
        "name": "command name",
        "args": {
            "arg name": "value"
        }
    }
}"""


class RepoToSwagger(ReactAgent):
    def __init__(self, ctx, **kwargs):
        super().__init__(agent_prompt=agent_prompt, actions=actions, model_type=ai_model, 
                         model_params=ai_model_params, response_format=agent_response_format, ctx=ctx)
    
    @property
    def __name__(self):
        return "Git Repo to Swagger API Spec"
    
    @property
    def __description__(self):
        return """Bot helping to convert Github repository into OpenApi 3.0 spec, 
to be used in Swagger or Postman. It require repo to be public."""