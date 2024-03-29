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
from langchain.schema import HumanMessage
from analysta_llm_agents.tools.tool import tool
import logging

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
def storeFile(ctx: Any, file_path:str, file_name:str, file_content:str):
    """Stores the content of a file in the file system.
    
    Args:
        file_path (str): The path of the folder where the file will be stored.
        file_name (str): The name of the file to be stored.
        file_content (str): The content of the file to be stored.
    """
    with open(path.join(file_path, file_name), "w") as f:
        f.write(file_content)
    return f"Stored file '{file_name}"

@tool
def improveImplementation(ctx: Any, gherkin_tests:str, python_tests:str):
    """analyze and improve the implementation of test cases on python pytest
    
    Args:
        gherkin_tests (str): The test cases.
        python_tests (str): The implementation of the test cases.
    """
    message = f"""
You are bot tasked to analyze the implementation of test cases on python pytest.

Goal is to provide grounded suggestions on how to improve the test or confirm that the test cases are good enough.

### Test cases: 
{gherkin_tests}

### Test implementation: 
{python_tests}

### Expected output:
List of suggestions to improve the test implementation of PyTest tests following the best practices"""
    suggestion = ctx.llm([HumanMessage(content=message)]).content
    prompt = f"""Implement following suggestions to improve test cases:
### Suggestions:
{suggestion}

### Test cases: 
{gherkin_tests}

### Test implementation: 
{python_tests}

### Expected output:
Imrpved test implementation"""
    return ctx.llm([HumanMessage(content=prompt)]).content


@tool
def runTests(ctx: Any, folder_with_tests: str):
    """Runs the tests from the specified folder.
    
    Args:
        folder_with_tests (str): The path of the folder with tests.
    """
    import pytest

    exit_code = pytest.main([
        folder_with_tests,
        "--verbose",
        "--html=pytest_report.html",
        "--junitxml=out_report.xml",
        "--reportportal"
    ])
    return f"Exit code of tests execution {exit_code} Results are stored in 'pytest_report.html' and 'out_report.xml'"
    

__all__ = [
    getFolderContent,
    getFileContent,
    storeFile,
    improveImplementation,
    runTests
]