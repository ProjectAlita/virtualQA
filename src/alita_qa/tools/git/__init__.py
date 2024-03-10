import requests
import logging
from typing import Type, Optional, Any
from langchain.tools import BaseTool
from langchain.pydantic_v1 import BaseModel, Field
from langchain_core.tools import tool, StructuredTool

logger = logging.getLogger(__name__)

class getRepoTreeSchema(BaseModel):
    org: str = Field(description="The name of the organization that owns the repository.")
    repo: str = Field(description="The name of the repository.")
    branch: str = Field(default='main', description="The name of the branch to retrieve the tree structure from")
    recursive: str = Field(default='true', description="Whether to retrieve the tree structure recursively or not")


class getRawFileSchema(BaseModel):
    org: str = Field(description="The name of the organization that owns the repository.")
    repo: str = Field(description="The name of the repository.")
    branch: str = Field(default='main', description="The name of the branch to retrieve the file from.")
    file_path: str = Field(description="The path of the file to retrieve.")


class getGitPatchSchema(BaseModel):
    org: str = Field(description="The name of the organization that owns the repository.")
    repo: str = Field(description="The name of the repository.")
    commit_id: str = Field(description="The commit ID to retrieve the patch file from.")

class getPullRequestChangesSchema(BaseModel):
    org: str = Field(description="The name of the organization that owns the repository.")
    repo: str = Field(description="The name of the repository.")
    pr_number: str = Field(description="The pull request number to retrieve the changes from.")

def _get_request(url: str, headers: Optional[dict] = None):
    try:
        # Send the GET request to the GitHub API
        response = requests.get(url, headers={"Content-Type": "application/json"})
        response.raise_for_status()
        return response
    except requests.exceptions.HTTPError as http_err:
        return f"ERROR: HTTP error occurred: {http_err}"
    except Exception as err:
        return f"ERROR: An error occurred: {err}"

@tool(args_schema=getRepoTreeSchema)
def getRepoTree(org: str, repo: str, branch: Optional[str] = 'main', recursive: Optional[str] = 'true'):
    """This API is used to retrieve the tree structure of a repository on GitHub."""
    # Construct the API URL with the given parameters
    url = f"https://api.github.com/repos/{org}/{repo}/git/trees/{branch}?recursive={recursive}"
    logger.info(f"URL: {url}")
    # Include the 'recursive' parameter in the query string if requested
    resp = _get_request(url).json()
    paths = "\n - ".join([item["path"] for item in resp["tree"]])
    # Replace the original "tree" list with the filtered one
    logger.debug(f"Response: {paths}")
    return paths


@tool(args_schema=getRawFileSchema)
def getRawFile(org:str, repo:str, branch:str, file_path:str):
    """Fetches the content of a file in raw format from a specified GitHub repository, branch, and file path."""
    # Construct the URL for accessing the raw file content
    url = f"https://raw.githubusercontent.com/{org}/{repo}/{branch}/{file_path}"
    return _get_request(url).text


@tool(args_schema=getGitPatchSchema)
def getGitCommitPatch(org:str, repo:str, commit_id:str):
    """Get the changes made in a commit as a patch file."""
    url = 'https://github.com/{org}/{repo}/commit/{commit_id}.patch'
    return _get_request(url).text


@tool(args_schema=getPullRequestChangesSchema)
def getPullRequestChanges(org:str, repo:str, pr_number:str):
    """Get the changes made in a pull request."""
    url = f'https://patch-diff.githubusercontent.com/raw/{org}/{repo}/pull/{pr_number}.diff'
    return _get_request(url).text
