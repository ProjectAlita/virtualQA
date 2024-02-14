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

import logging

from .test_cases_from_swagger.agent import SwaggerToGherkin
from analysta_llm_agents.tools.context import Context
from os import environ

logging.basicConfig(level=logging.ERROR)

def swag2gherkin():
    ctx = Context()
    ctx.shared_memory = []
    ctx.input_tokens = 0
    ctx.output_tokens = 0
    agent = SwaggerToGherkin(ctx)
    task = f"""Use repository '{environ.get("RESULT_PATH", "swaggers")}'"""
    print(f"\n\nTask: {task}\n\n")
    for message in agent.start(task):
        print(message)
        print("\n\n")

    print(f"Input tokens: {ctx.input_tokens}")
    print(f"Output tokens: {ctx.output_tokens}")
    