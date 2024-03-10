
from langchain.pydantic_v1 import BaseModel, Field
from langchain_core.tools import tool, StructuredTool
from os import path, makedirs, walk

class getFileContentSchema(BaseModel):
    file_path: str = Field(description="The path of the file to read")

class storeFileSchema(BaseModel):
    filepath: str = Field(description="Relative path to store the file in")
    file_name: str = Field(description="The name of the file to store")
    file_content: str = Field(description="The content of the file to store")

class getFolderContentSchema(BaseModel):
    folder_path: str = Field(description="The path of the folder to list the files from")

def create_path_if_not_exists(file_path):
    if not path.exists(file_path):
        makedirs(file_path)

@tool(args_schema=getFileContentSchema)
def getFileContent(file_path: str):
    """Get the content of a file in of local file system."""
    try:
        with open(file_path, "r") as f:
            file_content = f.read()
        return file_content
    except Exception as e:
        return f"Error: {e}"

@tool(args_schema=storeFileSchema)
def storeFile(filepath:str, file_name:str, file_content:str):
    """Stores the content of a file in the shared memory of the context."""
    # Add the file name and content to the shared memory of the context
    create_path_if_not_exists(filepath)
    with open(path.join(filepath, file_name), "w") as f:
        f.write(file_content)
    return f"Stored file {path.join(filepath, file_name)}"

@tool(args_schema=getFolderContentSchema)
def getFolderContent(folder_path: str):
    """ Get listing of local file system files in a folder and its subfolder."""
    file_paths = []  # List to store file paths
    for root, _, files in walk(folder_path):
        for file in files:
            file_path = path.join(root, file)
            file_paths.append(file_path)
    return "\n".join(file_paths)
