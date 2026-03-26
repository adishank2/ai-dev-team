import { useState, useEffect, useRef } from 'react'
import './App.css'

function App() {
  const [projectName, setProjectName] = useState('')
  const [projectPrompt, setProjectPrompt] = useState('')
  const [status, setStatus] = useState('idle') // 'idle', 'loading', 'success', 'error'
  const [taskId, setTaskId] = useState(null)
  const [logs, setLogs] = useState([])
  const terminalEndRef = useRef(null)

  // Setup WebSocket for Live Feed
  useEffect(() => {
    const ws = new WebSocket('ws://127.0.0.1:8000/api/v1/ws')
    ws.onmessage = (event) => {
      setLogs((prevLogs) => [...prevLogs, event.data])
    }
    return () => {
      ws.close()
    }
  }, [])

  // Auto-scroll terminal
  useEffect(() => {
    if (terminalEndRef.current) {
      terminalEndRef.current.scrollIntoView({ behavior: 'smooth' })
    }
  }, [logs])

  const handleSubmit = async (e) => {
    e.preventDefault()
    if (!projectName || !projectPrompt) return

    setStatus('loading')
    setTaskId(null)
    setLogs([]) // clear previous logs

    try {
      const response = await fetch('/api/v1/start-project', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          project_name: projectName,
          project_prompt: projectPrompt
        })
      })

      const data = await response.json()

      if (response.ok) {
        setStatus('success')
        setTaskId(data.task_id)
      } else {
        setStatus('error')
        console.error(data)
      }
    } catch (err) {
      console.error(err)
      setStatus('error')
    }
  }

  const [selectedAgent, setSelectedAgent] = useState(null)
  const [activeTab, setActiveTab] = useState('new') // 'new' or 'history'
  const [historyDocs, setHistoryDocs] = useState([])

  useEffect(() => {
    if (activeTab === 'history') {
      fetch('/api/v1/history')
        .then(res => res.json())
        .then(data => setHistoryDocs(data))
        .catch(err => console.error(err))
    }
  }, [activeTab])

  const agentsData = [
    {
      id: 'pm',
      icon: '👔',
      role: 'Product Manager',
      skills: 'Requirements Analysis, Agile Planning, Scope Management',
      about: 'A Product Manager (PM) is responsible for planning, building, and improving a product like an app, website, or software by acting as a bridge between developers, designers, and business teams to ensure the product solves real user problems and succeeds in the market; they research user needs, decide which features to build, create a roadmap, coordinate with teams, and continuously analyze feedback and data to improve the product, requiring a mix of technical understanding, business sense, communication, and problem-solving skills, and it’s a great career for someone who enjoys strategy, innovation, and working on real-world solutions without focusing only on coding.Product Requirements Document (PRD) to guide the rest of the team.'
    },
    {
      id: 'architect',
      icon: '🏗️',
      role: 'System Architect',
      skills: 'System Design, Tech Stack Selection, API Architecture',
      about: 'The brain behind the infrastructure. A System Designer and Architect is a professional who plans and structures how a complete software system or application will work at a high level, focusing on designing scalable, efficient, and reliable systems before developers start coding; they decide the overall architecture (like microservices or monolithic), choose technologies, define how different components communicate (APIs, databases, servers), and ensure the system can handle growth, performance, and security requirements, acting as the blueprint creator of the system, and this role requires strong knowledge of data structures, system design concepts, cloud platforms, and problem-solving skills, making it ideal for someone who enjoys thinking big-picture, designing complex systems, and working deeply with technology.'
    },
    {
      id: 'dev',
      icon: '💻',
      role: 'Senior Developer',
      skills: 'Full-Stack Engineering, Algorithms, Clean Code',
      about: "An elite programming machine fluent in multiple languages and modern frameworks. Receiving the Architect's rigid blueprints, A Senior Developer is an experienced software engineer who not only writes high-quality code but also takes responsibility for designing solutions, and ensuring best practices are followed in a project; they have deep knowledge of programming languages, and performance optimization, and often collaborate closely with product managers and architects to turn requirements into efficient, scalable software, while also mentoring team members and helping solve complex technical problems, making this role ideal for someone with strong coding skills, leadership ability, and real-world development experience."
    },
    {
      id: 'qa',
      icon: '🕵️',
      role: 'QA & Security Analyst',
      skills: 'Automated Testing, Vulnerability Scanning, Bug Hunting',
      about: "A relentless and meticulous code-reviewer, A QA (Quality Assurance) Analyst is responsible for ensuring that a software product works correctly and is free of bugs by testing features, writing test cases, identifying issues, and working with developers to fix them before release, and Security Analyst focuses on protecting systems and data from cyber threats by identifying vulnerabilities, monitoring for attacks, implementing security measures like encryption and firewalls, and ensuring compliance with security standards; both roles are critical in software development, where QA ensures the product is reliable and user-friendly, and Security Analysts ensure it is safe, secure, and protected from risks."
    },
    {
      id: 'devops',
      icon: '🚀',
      role: 'DevOps & Release Manager',
      skills: 'CI/CD Pipelines, GitHub Automation, Server Deployment',
      about: 'The final boss of deployment operations, QA-approved software and manages actual repository environments. A DevOps Engineer is a professional who works at the intersection of development (Dev) and operations (Ops) to automate, streamline, and improve the process of deploying software, ensuring faster and more reliable releases; they manage tools and workflows for continuous integration and continuous deployment (CI/CD), handle cloud infrastructure, and automate repetitive tasks making it ideal for someone who enjoys both development and system management. to securely push the finalized codebase live to remote GitHub servers.'
    },
  ]

  const TeamAgent = ({ agent }) => (
    <button
      type="button"
      className={`agent-avatar ${selectedAgent?.id === agent.id ? 'active' : ''}`}
      onClick={() => setSelectedAgent(selectedAgent?.id === agent.id ? null : agent)}
    >
      <span className="agent-icon">{agent.icon}</span>
      <div className="agent-role">{agent.role}</div>
    </button>
  )

  return (
    <div className="app-container">
      <div className="hero">
        <h1>AI Dev Team 4.0</h1>
        <p>The Autonomous Agents to Build Your Next Big Idea.</p>
      </div>

      <div className="layout-grid">
        <div className="card form-card">
          <div className="tab-menu">
            <button className={`tab-btn ${activeTab === 'new' ? 'active' : ''}`} onClick={() => setActiveTab('new')}>New Project</button>
            <button className={`tab-btn ${activeTab === 'history' ? 'active' : ''}`} onClick={() => setActiveTab('history')}>Project History</button>
          </div>

          {activeTab === 'new' ? (
            <>
              <form onSubmit={handleSubmit}>
                <div className="input-group">
                  <label htmlFor="projectName">Project Name</label>
                  <input
                    type="text"
                    id="projectName"
                    className="input-field"
                    placeholder="e.g. NextGen SaaS Dashboard"
                    value={projectName}
                    onChange={(e) => setProjectName(e.target.value)}
                    required
                    disabled={status === 'loading'}
                  />
                </div>

                <div className="input-group">
                  <label htmlFor="projectPrompt">Describe Your Project</label>
                  <textarea
                    id="projectPrompt"
                    className="input-field"
                    placeholder="Describe the application you want the AI Team to build..."
                    value={projectPrompt}
                    onChange={(e) => setProjectPrompt(e.target.value)}
                    required
                    disabled={status === 'loading'}
                  />
                </div>

                <button
                  type="submit"
                  className="submit-btn"
                  disabled={status === 'loading'}
                >
                  {status === 'loading' ? 'Initializing Team...' : 'Deploy AI Team'}
                </button>
              </form>

              {status === 'success' && (
                <div className="status-box" style={{ background: 'rgba(16, 185, 129, 0.1)', borderColor: 'rgba(16, 185, 129, 0.3)' }}>
                  <span style={{ fontSize: '1.5rem' }}>🚀</span>
                  <div>
                    <p style={{ fontWeight: 600, color: '#10b981' }}>Project Initiated!</p>
                    <p style={{ fontSize: '0.9rem', marginTop: '4px' }}>Task ID: {taskId}. See terminal for live progress!</p>
                  </div>
                </div>
              )}

              {status === 'error' && (
                <div className="status-box" style={{ background: 'rgba(239, 68, 68, 0.1)', borderColor: 'rgba(239, 68, 68, 0.3)' }}>
                  <span style={{ fontSize: '1.5rem', color: '#ef4444' }}>⚠️</span>
                  <p style={{ color: '#fca5a5' }}>Failed to start the project. Check backend logs.</p>
                </div>
              )}
            </>
          ) : (
            <div className="history-list">
              {historyDocs.length === 0 ? (
                <p className="history-empty">No projects generated yet.</p>
              ) : (
                historyDocs.slice().reverse().map(proj => (
                  <div key={proj.id} className="history-card">
                    <div className="history-header">
                      <h4>{proj.name}</h4>
                      <span className="history-date">{proj.date}</span>
                    </div>
                    <p className="history-prompt">"{proj.prompt}"</p>
                    <button className="download-btn" type="button" onClick={() => window.location.href = `/api/v1/projects/${proj.id}/download`}>
                      ⬇️ Download Source Code (.zip)
                    </button>
                  </div>
                ))
              )}
            </div>
          )}
        </div>

        {/* Live Terminal Panel */}
        <div className="card terminal-card">
          <div className="terminal-header">
            <div className="dot red"></div>
            <div className="dot yellow"></div>
            <div className="dot green"></div>
            <span className="terminal-title">Agent Swarm Live Feed</span>
          </div>
          <div className="terminal-body">
            {logs.length === 0 ? (
              <div className="terminal-empty">Awaiting instructions...</div>
            ) : (
              logs.map((log, index) => (
                <div key={index} className="log-entry">
                  <span className="log-timestamp">[{new Date().toLocaleTimeString()}]</span> {log}
                </div>
              ))
            )}
            <div ref={terminalEndRef} />
          </div>
        </div>
      </div>

      <div className="agents-section">
        <h3 className="section-title">Meet The Agents <span>(Click an agent to view their profile)</span></h3>
        <div className="agents-container">
          {agentsData.map(agent => (
            <TeamAgent key={agent.id} agent={agent} />
          ))}
        </div>

        {selectedAgent && (
          <div className="agent-about-panel">
            <span className="agent-about-icon">{selectedAgent.icon}</span>
            <div className="agent-about-content">
              <h4>{selectedAgent.role}</h4>
              <div className="agent-skills"><strong>Core Skills:</strong> {selectedAgent.skills}</div>
              <p>{selectedAgent.about}</p>
            </div>
          </div>
        )}
      </div>
    </div>
  )
}

export default App
