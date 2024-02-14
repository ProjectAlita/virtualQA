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

import argparse
import logging

from .api_spec_agent.agent import RepoToSwagger
from analysta_llm_agents.tools.context import Context


logging.basicConfig(level=logging.ERROR)

# Task example:
# Use repository spring-petclinic/spring-framework-petclinic with 
# branch main It is Java Spring application, please create swagger spec. 
# Deployment URL is https://petclinic.example.com
git2swag = argparse.ArgumentParser(prog='Git to Swagger', description='Generates swagger files from a git repository')
git2swag.add_argument('-t', '--task', type=str, help='Task to be performed', required=True)

def git2swagger():
    ctx = Context()
    ctx.shared_memory = []
    ctx.input_tokens = 0
    ctx.output_tokens = 0
    agent = RepoToSwagger(ctx)
    args = git2swag.parse_args()

    print(f"\n\nTask: {args.task}\n\n")
    for message in agent.start(args.task):
        print(message)
        print("\n\n")

    print(f"Input tokens: {ctx.input_tokens}")
    print(f"Output tokens: {ctx.output_tokens}")
    