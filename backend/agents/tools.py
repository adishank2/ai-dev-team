# pyre-ignore-all-errors
import os
import subprocess
import requests # type: ignore
from dotenv import load_dotenv # type: ignore
from crewai.tools import tool # type: ignore

load_dotenv()

def create_publish_tool(workspace_dir: str):
    @tool("Publish to GitHub")
    def publish_to_github(repo_name: str) -> str:
        """
        Publish the workspace files to a new GitHub repository automatically.
        This creates the repo on GitHub, initializes git, commits the files, and pushes them.
        Provide a repo_name string (lowercase letters and hyphens only).
        """
        github_user = os.getenv("GITHUB_USERNAME")
        github_token = os.getenv("GITHUB_TOKEN")
        
        if not github_user or not github_token:
            return "Error: GITHUB_USERNAME and GITHUB_TOKEN environment variables are missing. Ask the user to configure them."

        # Create Repo on GitHub
        headers = {"Authorization": f"token {github_token}", "Accept": "application/vnd.github.v3+json"}
        payload = {"name": repo_name, "private": False, "auto_init": False}
        resp = requests.post("https://api.github.com/user/repos", json=payload, headers=headers)
        
        if resp.status_code not in [201, 422]:  # 422 means might already exist
            return f"Failed to create GitHub repo. Response {resp.status_code}: {resp.text}"

        # Execute git commands in workspace
        try:
            remote_url = f"https://{github_user}:{github_token}@github.com/{github_user}/{repo_name}.git"
            
            subprocess.run(["git", "init"], cwd=workspace_dir, check=True)
            # Avoid error if already initialized
            subprocess.run(["git", "remote", "remove", "origin"], cwd=workspace_dir, stderr=subprocess.DEVNULL)
            subprocess.run(["git", "remote", "add", "origin", remote_url], cwd=workspace_dir, check=True)
            subprocess.run(["git", "add", "."], cwd=workspace_dir, check=True)
            
            # Check if there are changes to commit
            status = subprocess.run(["git", "status", "--porcelain"], cwd=workspace_dir, capture_output=True, text=True)
            if status.stdout.strip():
                subprocess.run(["git", "commit", "-m", "Initial AI Dev Team deployment"], cwd=workspace_dir, check=True)
            
            subprocess.run(["git", "branch", "-M", "main"], cwd=workspace_dir, check=True)
            subprocess.run(["git", "push", "-u", "origin", "main", "--force"], cwd=workspace_dir, check=True)
            
            return f"Successfully pushed code to https://github.com/{github_user}/{repo_name}"
        except subprocess.CalledProcessError as e:
            return f"Git execution failed: {e}"
        except Exception as e:
            return f"An error occurred: {str(e)}"
            
    return publish_to_github
