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

from os import path
import requests
from typing import Any
from analysta_llm_agents.tools.tool import tool
import logging
from ...config import result_path

logger = logging.getLogger(__name__)

@tool
def getRepoTree(ctx: Any, organization: str, repository: str, branch: str, recursive:str = 'true'):
    """This API is used to retrieve the tree structure of a repository on GitHub.
    
    Agrs:
        organization (str): The name of the GitHub organization.
        repository (str): The name of the GitHub repository.
        branch (str): The branch of the GitHub repository.
        recursive (str): numeric boolean value to get repo content recursively, 1 or 0 allowed.
    """
    # Construct the API URL with the given parameters
    url = f"https://api.github.com/repos/{organization}/{repository}/git/trees/{branch}?recursive={recursive}"
    logger.info(f"URL: {url}")
    # Include the 'recursive' parameter in the query string if requested
    
    try:
        # Send the GET request to the GitHub API
        response = requests.get(url, headers={"Content-Type": "application/json"})
        
        # Raise an exception if the request was unsuccessful
        response.raise_for_status()
        
        # Return the JSON response if the request was successful
        resp = response.json()
        # Retain only the "path" key in each item of the "tree" list
        paths = "\n - ".join([item["path"] for item in resp["tree"]])

        # Replace the original "tree" list with the filtered one
        logger.debug(f"Response: {paths}")
        return paths
    except requests.exceptions.HTTPError as http_err:
        return f"ERROR: HTTP error occurred: {http_err}"
    except Exception as err:
        return f"ERROR: An error occurred: {err}"

@tool
def getRawFile(ctx: Any, org:str, repo:str, branch:str, file_path:str):
    """Fetches the content of a file in raw format from a specified GitHub repository, branch, and file path.
    
    Args:
        org (str): The name of the GitHub organization.
        repo (str): The name of the GitHub repository.
        branch (str): The branch of the GitHub repository.
        file_path (str): The path to the file in the repository.
    """
    # Construct the URL for accessing the raw file content
    url = f"https://raw.githubusercontent.com/{org}/{repo}/{branch}/{file_path}"
    
    try:
        # Send the GET request to the GitHub Raw Content Server
        response = requests.get(url)
        
        # Raise an exception if the request was unsuccessful
        response.raise_for_status()
        
        # Return the text content of the response
        return response.text
    except requests.exceptions.HTTPError as http_err:
        return f"ERROR: HTTP error occurred: {http_err}"
    except Exception as err:
        return f"ERROR: An error occurred: {err}"

@tool
def storeSpecFile(ctx: Any, file_name:str, file_content:str):
    """Stores the content of a file in the shared memory of the context.
    
    Args:
        file_name (str): The name of the file to be stored.
        file_content (str): The content of the file to be stored.
    """
    # Add the file name and content to the shared memory of the context
    with open(path.join(result_path, file_name), "w") as f:
        f.write(file_content)
    return f"Stored file '{file_name}"


__all__ = [
    getRepoTree,
    getRawFile,
    storeSpecFile
]