import json
import urllib.request
from typing import Dict, Any, Optional
from mcp.server.fastmcp import FastMCP
import os
import subprocess
import dotenv

dotenv.load_dotenv()

mcp = FastMCP("Github")

@mcp.tool()
def get_github_issue(repo_owner: str, repo_name: str, issue_id: int) -> Dict[str, Any]:
    """
    Get a GitHub issue by ID.
    
    Args:
        repo_owner: The owner of the repository
        repo_name: The name of the repository
        issue_id: The ID of the issue
        
    Returns:
        Dictionary containing the issue data
        
    Raises:
        urllib.error.HTTPError: If the request fails
    """
    url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/issues/{issue_id}"
    
    req = urllib.request.Request(url)
    req.add_header("Accept", "application/vnd.github.v3+json")
    req.add_header("User-Agent", "GitHub-Issue-Fetcher")

    token = os.environ.get("GITHUB_TOKEN")  # Load token from environment variable
    if token:
        req.add_header("Authorization", f"token {token}")
    
    with urllib.request.urlopen(req) as response:
        return json.loads(response.read().decode())

@mcp.tool()
def create_github_pr(repo_owner: str, repo_name: str, title: str, body: str, head: str, base: str = "main") -> Dict[str, Any]:
    """
    Create a GitHub Pull Request.
    
    Args:
        repo_owner: The owner of the repository
        repo_name: The name of the repository
        title: The title of the pull request
        body: The body/description of the pull request
        head: The name of the branch with your changes
        base: The name of the branch you want the changes pulled into (default: "main")
        
    Returns:
        Dictionary containing the PR data
        
    Raises:
        ValueError: If token is not provided
        urllib.error.HTTPError: If the request fails
    """
    token = os.environ["GITHUB_TOKEN"]
    if not token:
        raise ValueError("GitHub token is required for creating pull requests")
    
    url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/pulls"
    
    pr_data = {
        "title": title,
        "body": body,
        "head": head,
        "base": base
    }
    
    req = urllib.request.Request(
        url, 
        data=json.dumps(pr_data).encode('utf-8'),
        method='POST'
    )

    
    req.add_header("Accept", "application/vnd.github.v3+json")
    req.add_header("Content-Type", "application/json")
    req.add_header("User-Agent", "GitHub-PR-Creator")
    req.add_header("Authorization", f"token {token}")
    
    with urllib.request.urlopen(req) as response:
        return json.loads(response.read().decode())

@mcp.tool()
def copy_and_create_branch(
    repo_url: str,
    branch_name: str,
    token: Optional[str] = None
) -> Dict[str, Any]:
    """
    Clone a repo, create a branch and create a branch
    """
    path = "/Users/camiloleonel/Desktop/repos"

    # Clone repo
    clone_url = repo_url
    if token:
        clone_url = repo_url.replace("https://", f"https://{token}@")
    
    subprocess.run(["git", "clone", clone_url, path], check=True)
    subprocess.run(["git", "checkout", "-b", branch_name], cwd=path, check=True)

    return {"branch_path": path}


@mcp.tool()
def list_all_files(directory: str) -> list[str]:
    """
    List all files in a directory and its subdirectories.
    """
    files = []
    for root, dirs, filenames in os.walk(directory):
        for filename in filenames:
            files.append(os.path.join(root, filename))
    return files

@mcp.tool()
def read_file(file_path: str) -> dict[str, str]:
    """
    Read the contents of a file.
    """
    with open(file_path, 'r') as file:
        return {"content": file.read()}
    

@mcp.tool()
def make_changes(file_path: str, changes: str) -> dict[str, str]:
    """
    Make changes to a file.

    args:
        file_path: the absolute path of the file to modify
    """
    with open(file_path, 'w') as file:
        file.write(changes)

    return {"status": "success"}


@mcp.tool()
def commit_and_push_changes(repo_path: str, branch_name: str) -> dict[str, str]:
    """
    Make changes to a file and push it to the repository.
    Do not creates the PR, do to that execute the tool create_github_pr

    args:
        repo_path: the absolute path of the repository
        branch_name: the name of the branch to push changes to
    """

    subprocess.run(["git", "add", "."], cwd=repo_path, check=True)
    subprocess.run(["git", "commit", "-m", '"Automated changes"'], cwd=repo_path, check=True)
    subprocess.run(["git", "push", "--set-upstream", "origin", branch_name], cwd=repo_path, check=True)

    return {"status": "success"}


mcp.run(transport="streamable-http")