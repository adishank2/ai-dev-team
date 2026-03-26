import os
import requests # type: ignore
from crewai import Agent, Task, Crew, Process # type: ignore
from langchain_openai import ChatOpenAI # type: ignore
from agents.tools import create_publish_tool

def get_agent_callback(agent_name: str, log_callback):
    def callback(step_output):
        msg = ""
        # If it's an AgentAction, it has tool, tool_input, log
        if hasattr(step_output, 'log'):
            msg = f"[{agent_name}] 🤔 Thought: {step_output.log}"
        else:
            output_text = f"{step_output}"
            msg = f"[{agent_name}] 📝 Output: {output_text[:300]}..." # type: ignore
        
        try:
            log_callback(msg)
        except:
            pass
    return callback

class AIDevTeam:
    def __init__(self, project_prompt: str, project_name: str, workspace_dir: str, log_callback):
        self.project_prompt = project_prompt
        self.project_name = project_name
        self.workspace_dir = workspace_dir
        self.log_callback = log_callback
        self.llm = "ollama/llama3"

        self.pm = None
        self.architect = None
        self.developer = None
        self.qa = None
        self.devops = None
        self.tasks = []
        self.crew = None

        # ensure workspace exists
        os.makedirs(self.workspace_dir, exist_ok=True)

    def create_agents(self):
        self.pm = Agent(
            role='Product Manager',
            goal='Define project scope, manage timelines, and ensure the project meets its objectives.',
            backstory='An experienced Product Manager who translates customer requirements into actionable plans and oversees the entire lifecycle of software projects.',
            verbose=True,
            allow_delegation=False,
            llm=self.llm,
            step_callback=get_agent_callback("Product Manager", self.log_callback)
        )

        self.architect = Agent(
            role='System Architect',
            goal='Design scalable, robust, and maintainable software architecture and system design.',
            backstory='A senior System Architect capable of breaking down complex requirements into solid system structures, deciding on tech stacks, and creating architecture diagrams.',
            verbose=True,
            allow_delegation=False,
            llm=self.llm,
            step_callback=get_agent_callback("System Architect", self.log_callback)
        )

        self.developer = Agent(
            role='Senior Developer',
            goal='Write clean, efficient, and well-documented real code based on the architectural design.',
            backstory='An elite full-stack developer who loves writing production-ready code and is fluent in multiple programming languages and frameworks.',
            verbose=True,
            allow_delegation=False,
            llm=self.llm,
            step_callback=get_agent_callback("Senior Developer", self.log_callback)
        )

        self.qa = Agent(
            role='QA & Testing Analyst',
            goal='Analyze the codebase, run tests, finding bugs, and ensure the code quality is flawless.',
            backstory='A meticulous Quality Assurance engineer with a sharp eye for edge cases, security flaws, and performance bottlenecks.',
            verbose=True,
            allow_delegation=False,
            llm=self.llm,
            step_callback=get_agent_callback("QA Analyst", self.log_callback)
        )

        self.devops = Agent(
            role='DevOps & Release Manager',
            goal='Execute deployments and strictly push code live via the Publish to GitHub tool.',
            backstory='A DevOps master. You NEVER just write scripts, you actually run tools to push code directly to remote servers.',
            verbose=True,
            allow_delegation=False,
            tools=[create_publish_tool(self.workspace_dir)],
            llm=self.llm,
            step_callback=get_agent_callback("DevOps", self.log_callback)
        )

    def create_tasks(self):
        # Using workspace files to store real outputs
        prd_file = os.path.join(self.workspace_dir, "PRD.md")
        architecture_file = os.path.join(self.workspace_dir, "Architecture.md")
        source_code_file = os.path.join(self.workspace_dir, "app_source_code.py")
        qa_report_file = os.path.join(self.workspace_dir, "QA_Report.md")
        deployment_script = os.path.join(self.workspace_dir, "deploy.sh")

        task_planning = Task(
            description=f'Create a detailed PRD based on requirements: "{self.project_prompt}". Project Name: {self.project_name}.',
            expected_output='A comprehensive PRD document.',
            agent=self.pm,
            output_file=prd_file
        )

        task_architecture = Task(
            description='Read the PRD and design the software architecture. Define the tech stack, data models, API endpoints.',
            expected_output='A full system architecture specification.',
            agent=self.architect,
            output_file=architecture_file
        )

        task_development = Task(
            description='Write the core source code for the project. Implement the backend and APIs.',
            expected_output='Production-ready python source code files.',
            agent=self.developer,
            output_file=source_code_file
        )

        task_qa = Task(
            description="Review the developer's source code. Create testing strategies, identify bugs, suggest fixes.",
            expected_output='A detailed QA report with bugs and test cases.',
            agent=self.qa,
            output_file=qa_report_file
        )

        task_deployment = Task(
            description='Take the final QA code, write a deployment bash script, and crucially, EXECUTABLY use your "Publish to GitHub" tool passing the project name as the repo_name argument to push the workspace directly to GitHub.',
            expected_output='A bash script (deploy.sh) and a successful execution message from the Github tool.',
            agent=self.devops,
            output_file=deployment_script
        )

        self.tasks = [task_planning, task_architecture, task_development, task_qa, task_deployment]

    def build(self):
        try:
            self.log_callback("🚀 [System] Swarm Initiated! Kickstarting the process...")
        except:
            pass

        self.create_agents()
        self.create_tasks()
        
        self.crew = Crew(
            agents=[self.pm, self.architect, self.developer, self.qa, self.devops],
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True
        )

        result = self.crew.kickoff()
        
        try:
            self.log_callback("✅ [System] Development Complete! Code has been written to the workspace.")
        except:
            pass

        return result
