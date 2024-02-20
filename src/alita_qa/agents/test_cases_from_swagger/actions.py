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

from os import path, walk
from typing import Any
from analysta_llm_agents.tools.tool import tool
from langchain.schema import HumanMessage, AIMessage
import logging
from ...config import gherkin_path

logger = logging.getLogger(__name__)

@tool
def getFolderContent(ctx: Any, folder_path: str):
    """ Get listing of files in a folder and its subfolder.
    
    Args:
        folder_path (str): The path of the folder.
    """
    file_paths = []  # List to store file paths
    for root, _, files in walk(folder_path):
        for file in files:
            file_path = path.join(root, file)
            file_paths.append(file_path)
    return "\n".join(file_paths)

@tool
def getFileContent(ctx: Any, file_path: str):
    """ Get the content of a file.
    
    Args:
        file_path (str): The path of the file.
    """
    try:
        with open(file_path, "r") as f:
            file_content = f.read()
        return file_content
    except Exception as e:
        return f"Error: {e}"

@tool
def storeFeatureFile(ctx: Any, file_name:str, file_content:str):
    """Stores the content of a file in the file system.
    
    Args:
        file_name (str): The name of the file to be stored.
        file_content (str): The content of the file to be stored.
    """
    with open(path.join(gherkin_path, file_name), "w") as f:
        f.write(file_content)
    return f"Stored file '{file_name}"

@tool
def improveTestCoverate(ctx: Any, test_cases:str, api_spec:str):
    """Analyzes the test quality and provide suggestions on improvements
    
    Args:
        test_cases (str): The test cases.
        api_spec (str): The API specification.
    """
    message = """
You are bot tasked to analyze the test coverage and quality to provide suggestions on improvements for the test cases and the API specification.

Goal is to provide grounded suggestions on how to improve the test coverage or confirm that the test cases are good enough.

### API Specification: 
{api_spec}

### Test Cases: 
{test_cases}

### Expected Output:
List of suggestions on how to improve the test coverage or confirmation that the test cases are good enough."""
    suggestions = ctx.llm([HumanMessage(content=message)]).content
    prompt = f"""Implement following suggestions to improve test cases:
### Suggestions
{suggestions}

### API Specification: 
{api_spec}

### Test Cases: 
{test_cases}

### Expected Output:
Updated Gherkin feature files with improved test coverage."""
    return ctx.llm([HumanMessage(content=prompt)]).content

__all__ = [
    getFolderContent,
    getFileContent,
    storeFeatureFile,
    improveTestCoverate
]