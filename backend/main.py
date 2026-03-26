# pyre-ignore-all-errors
from fastapi import FastAPI, BackgroundTasks, WebSocket, WebSocketDisconnect # type: ignore
from pydantic import BaseModel # type: ignore
from typing import Optional, List
from agents.team import AIDevTeam # type: ignore
import os
import json
import shutil
import datetime
from fastapi.responses import FileResponse # type: ignore

app = FastAPI(
    title="AI Dev Team API",
    description="Backend API with WebSockets for orchestrating the 5-Agent Development Team.",
    version="1.0.0"
)

# Workspace Directory
WORKSPACE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "workspace")
os.makedirs(WORKSPACE_DIR, exist_ok=True)

class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            try:
                await connection.send_text(message)
            except:
                pass

manager = ConnectionManager()

class ProjectRequest(BaseModel):
    project_prompt: str
    project_name: str

class ProjectResponse(BaseModel):
    message: str
    task_id: str

class LogMessage(BaseModel):
    message: str

@app.get("/")
def read_root():
    return {"message": "Welcome to the AI Dev Team API. The team is ready to build!"}

import asyncio

def run_project_task(project_prompt: str, project_name: str, loop: asyncio.AbstractEventLoop):
    def live_log(msg: str):
        asyncio.run_coroutine_threadsafe(manager.broadcast(msg), loop)

    try:
        safe_name = project_name.replace(' ', '_').replace('/', '_').replace('\\', '').lower()
        project_folder = os.path.join(WORKSPACE_DIR, safe_name)
        os.makedirs(project_folder, exist_ok=True)

        team = AIDevTeam(project_prompt=project_prompt, project_name=project_name, workspace_dir=project_folder, log_callback=live_log)
        team.build()
        
        # Save to History Database
        history_file = os.path.join(WORKSPACE_DIR, "history.json")
        history = []
        if os.path.exists(history_file):
            try:
                with open(history_file, "r", encoding="utf-8") as f:
                    content = f.read().strip()
                    if content:
                        history = json.loads(content)
            except Exception as e:
                pass
        
        history.append({
            "id": safe_name,
            "name": project_name,
            "prompt": project_prompt,
            "date": datetime.datetime.now().strftime("%B %d, %Y at %I:%M %p"),
            "path": project_folder
        })
        
        with open(history_file, "w", encoding="utf-8") as f:
            json.dump(history, f, indent=4)
            
    except Exception as e:
        live_log(f"❌ [System Error] The AI Team encountered a fatal crash: {str(e)}")

@app.post("/api/v1/start-project", response_model=ProjectResponse)
async def start_project(request: ProjectRequest, background_tasks: BackgroundTasks):
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        loop = asyncio.get_event_loop()
        
    task_id = f"task_{request.project_name.replace(' ', '_').lower()}"
    background_tasks.add_task(run_project_task, request.project_prompt, request.project_name, loop)
    return {
        "message": f"Project '{request.project_name}' has been initiated. The AI Dev Team is on it!",
        "task_id": task_id
    }

@app.websocket("/api/v1/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            await websocket.receive_text() # keep alive
    except WebSocketDisconnect:
        manager.disconnect(websocket)

@app.get("/api/v1/history")
def get_history():
    history_file = os.path.join(WORKSPACE_DIR, "history.json")
    if os.path.exists(history_file):
        try:
            with open(history_file, "r", encoding="utf-8") as f:
                content = f.read().strip()
                if content:
                    return json.loads(content)
        except Exception:
            pass
    return []

@app.get("/api/v1/projects/{project_id}/download")
def download_project_zip(project_id: str):
    project_folder = os.path.join(WORKSPACE_DIR, project_id)
    if not os.path.exists(project_folder):
        return {"error": "Project not found"}
    
    zip_path = os.path.join(WORKSPACE_DIR, f"{project_id}.zip")
    shutil.make_archive(zip_path.replace('.zip', ''), 'zip', project_folder)
    return FileResponse(zip_path, filename=f"{project_id}.zip", media_type="application/zip")
