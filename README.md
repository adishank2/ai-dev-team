# 🚀 AI Dev Team 4.0 

An autonomous, entirely local Multi-Agent Artificial Intelligence swarm. Designed to act as a 5-person engineering team that takes a single project idea and handles everything from **Product Requirements Analysis**, to **Writing React/Python Code**, to physically **Deploying it directly to GitHub**.

By leveraging state-of-the-art WebSockets, a stunning Glassmorphism UI, and `CrewAI`, this dashboard allows you to literally watch the LLM logic pipeline happen instantaneously without expensive cloud API costs.

---

## 🌟 Key Features
- **The Swarm:** 5 heavily customized System Prompts (Product Manager, Architect, Senior Developer, QA Analyst, DevOps) working sequentially.
- **Zero-Latency Live Feed:** Integrated WebSocket architecture that captures instantaneous agent execution from the FastAPI thread pool straight to the frontend dashboard.
- **Local & Offline Execution:** Hard-wired cognitive engine running strictly through local **Ollama** models (Llama 3) for absolute data privacy and free task completion.
- **Automated CI/CD Integration:** The DevOps Agent is equipped with custom Python `BaseTools`, enabling physical OS-level access to dynamically provision remote GitHub repositories and securely push the generated code live.
- **Project Persistence:** An automatic history database cataloging every built task, allowing native 1-click `.zip` frontend downloads of all generated source files.

---

## 🛠️ The Agents
1. 👔 **Product Manager:** Takes your raw prompt, analyzes project scope, and writes an exhaustive PRD.
2. 🏗️ **System Architect:** Receives the PRD and mathematically structures exact backend/frontend tech stacks and API endpoints.
3. 💻 **Senior Developer:** Actually translates the Architect's blueprints into raw, production-ready code.
4. 🕵️ **QA & Security Analyst:** Sweeps the Developer's code hunting for security flaws, edge cases, and performance bottlenecks.
5. 🚀 **DevOps & Release Manager:** Takes the tested build, provisions folders, creates CI/CD deployment scripts, and natively configures/pushes straight to GitHub.

---

## 💻 Tech Stack
* **Backend:** Python, FastAPI, WebSockets (`uvicorn`), CrewAI, LangChain, Subprocess Shell Automations
* **Frontend:** React, Vite, Vanilla CSS (Glassmorphism design system)
* **AI Tooling:** Offline Ollama Instances (Llama3)

---

## 🚀 How to Run Locally

### 1. Prerequisites 
- Ensure you have [Ollama](https://ollama.com/) installed and running locally on your machine.
- Pull a local model: `ollama run llama3`
- Node.js (for React frontend) & Python 3.10+ (for FastAPI backend)

### 2. Backend Setup
Navigate into the backend and boot up your virtual environment:
```bash
cd backend
python -m venv venv

# Windows
venv\Scripts\activate
# Mac / Linux
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```
Create a `.env` file inside `/backend` with:
```env
GITHUB_USERNAME=your_username
GITHUB_TOKEN=your_classic_github_token
```
Start the FastAPI server:
```bash
uvicorn main:app --reload
```

### 3. Frontend Setup
Open a second terminal, navigate to the frontend:
```bash
cd frontend
npm install
npm run dev
```

### 4. Deploy!
Head over to `http://localhost:5173` in your browser. Type your next big software idea into the "New Project" screen, hit **Deploy AI Team**, and watch your terminal light up as your Swarm builds it live!

---
> *Built iteratively with Advanced Agentic coding workflows.*
