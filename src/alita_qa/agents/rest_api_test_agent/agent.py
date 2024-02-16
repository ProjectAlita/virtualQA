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

agent_prompt = """You are autonomosus bot tasked to tranform Gherkin features into Python PyTest tests and execute them.

Your goal is to create set of new tests and update existing, as well as execute test suite and provide results to the user.

Steps to follow:
1. Understand available feature files, their content and structure
2. Plan what files in existing test framework will be affected and what new files will be created
3. Read content of the files that plan to be updated, and update them with new tests
4. Create new files with new tests
5. Execute test suite and provide results to the user


Constraints:
1. Use pytest.fixture for base_url where value obtained from environ.get('DEPLOYMENT_URL', "http://yourapiendpoint.com")
2. In case of many similar tests use @pytest.mark.parametrize to reduce code duplication
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


class TestGenAgent(ReactAgent):
    def __init__(self, ctx, **kwargs):
        super().__init__(agent_prompt=agent_prompt, actions=actions, model_type=ai_model, 
                         model_params=ai_model_params, ctx=ctx)
    
    @property
    def __name__(self):
        return "Agent for Test Generation"
    
    @property
    def __description__(self):
        return """Bot to create pytest tests from Gherkin feature files and execute them."""