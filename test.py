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

from src.agents.api_spec_agent.agent import RepoToSwagger
from analysta_llm_agents.tools.context import Context

import logging

logging.basicConfig(level=logging.ERROR)

ctx = Context()
ctx.shared_memory = []
ctx.input_tokens = 0
ctx.output_tokens = 0
agent = RepoToSwagger(ctx)

task = """Use repository spring-petclinic/spring-framework-petclinic with 
branch main It is Java Spring application, please create swagger spec. 
Deployment URL is https://petclinic.example.com """

print(f"\n\nTask: {task}\n\n")
for message in agent.start(task):
    print(message)
    print("\n\n")

print(f"Input tokens: {ctx.input_tokens}")
print(f"Output tokens: {ctx.input_tokens}")
