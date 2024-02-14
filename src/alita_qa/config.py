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

from os import environ
# from dotenv import load_dotenv

# load_dotenv('.env')

langsmith_api_key = environ.get('LANGSMITH_API_KEY')
result_path = environ.get('RESULT_PATH', 'swaggers')
gherkin_path = environ.get('GHERKIN_PATH', 'gherkins')
ai_model='AzureChatOpenAI'
ai_model_params={
    "model_name": environ.get("MODEL_NAME", ""),
    "deployment_name": environ.get("DEPLOYMENT_NAME", ""),
    "openai_api_version": environ.get("OPENAI_API_VERSION", "2023-03-15-preview"),
    "azure_endpoint": environ.get("AZURE_LLM_ENDPOINT", ""),
    "openai_api_key": environ.get("OPENAI_API_KEY", ""),
    "max_tokens": int(environ.get("MAX_TOKEN", "512")), 
    "temperature": 0.5, 
    "top_p": 0.8, 
    "max_retries": 2
}

# ai_model='ChatOpenAI'

# ai_model_params={
#     "model_name": environ.get("MODEL_NAME", ""),
#     "openai_organization": environ.get("OPENAI_ORG_ID", ""),
#     "openai_api_key": environ.get("OPENAI_API_KEY", ""),
#     "temperature": 0.5,
#     "max_retries": 2,
#     "max_tokens": 1024,
# }    
