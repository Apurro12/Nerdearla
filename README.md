# NerdearLA 2025 - LangChain & LangGraph Workshop

A comprehensive workshop demonstrating the evolution from simple AI responses to complex agent workflows using LangChain, LangGraph, and MCP (Model Context Protocol) servers.

## 🚀 Workshop Overview

This repository contains a progressive series of examples showcasing:
- Basic AI agent responses
- Tool integration with agents
- MCP server architecture
- Manual graph construction with LangGraph
- Interactive workflows with user permissions
- Multi-server deployments

## 📋 Prerequisites

- Python 3.12+
- uv package manager
- OpenAI API key

## 🛠️ Setup

1. **Clone and navigate to the repository**
```bash
cd 08_nerdearla
```

2. **Set up environment variables**
```bash
cp .env.example .env
# Edit .env and add your OpenAI API key
```

3. **Install dependencies**
```bash
uv sync
```

4. **Initialize the database**
```bash
cd 00_tables_creation
# Run the SQL commands from init_db.sql to create data.db in the parent folder
cd ..
```

## 📚 Workshop Modules

### 00 - Database Setup
**Location**: `00_tables_creation/`

Sets up SQLite database with sample sales data for the workshop examples.

**Files**:
- `init_db.sql` - Database schema and sample data

### 01 - Simple Response
**Location**: `01_simple_response/`

Basic implementation of an AI agent that can query a database and provide simple responses.

**Run**:
```bash
cd 01_simple_response
uv run main.py
```

**Example queries**:
- "Give me the sales grouped by genre"
- "Give me the total sales grouped by item category"

### 02 - React Agent with Tools
**Location**: `02_react_agent_with_tools/`

Introduction to ReAct (Reasoning + Acting) agents with tool calling capabilities. Note: This implementation doesn't have memory between interactions.

**Run**:
```bash
cd 02_react_agent_with_tools
uv run gradio_interface.py
```

**Features**:
- Gradio web interface
- Synchronous and asynchronous response modes
- Database query tools

### 03 - MCP Tools
**Location**: `03_mcp_tools/`

Demonstrates Model Context Protocol (MCP) server architecture for tool isolation and modularity.

**Run**:
```bash
cd 03_mcp_tools
# Start MCP server
uv run tool_mcp.py

# In another terminal, start the interface
uv run gradio_interface.py
```

**Benefits**:
- Tool isolation
- Modular architecture
- Same frontend interface

### 04 - LangGraph Manual Graph
**Location**: `04_langgraph_manual_graph/`

Manual construction of ReAct agents using LangGraph instead of built-in functions, providing more control over the agent workflow.

**Implementations**:
1. `01_agent_simple_decoupled.py` - Decoupled MCP connection
2. `01_agent_simple.py` - Standard implementation
3. `decoupled_yield.py` - Yield-based approach

**Run with LangGraph Studio**:
```bash
cd 04_langgraph_manual_graph
uv run langgraph dev
```

**Features**:
- Visual graph execution monitoring
- Custom agent compilation
- Multiple MCP connection patterns

### 05 - Graph with Pause
**Location**: `05_graph_with_pause/`

Enhanced workflow with user permission system - the agent asks for permission before executing tools.

**Run**:
```bash
cd 05_graph_with_pause
uv run gradio_interface.py
```

**Features**:
- Interactive tool execution approval
- User feedback integration
- Custom checkpoint management

**LangGraph Studio**:
```bash
# Comment the checkpointer line in agent.py first
uv run langgraph dev
```

### 06 - Multiple MCP Servers
**Location**: `06_langgraph_with_multiple_servers/`

Demonstrates deployment of multiple specialized MCP servers for different capabilities.

**Available Servers**:
1. **Image Analysis** - JPG image processing
2. **GitHub Integration** - Repository interactions
3. **Database Tools** - SQL query capabilities

**Use Cases**:
- Analyze data from images
- Fix GitHub issues automatically
- Extract database insights

**Exercise**: Implement simultaneous connection to multiple MCP servers using `AsyncExitStack` from `contextlib`.

### 07 - Images
**Location**: `00_images/`

Contains workshop screenshots and visual documentation.

## 🎯 Learning Path

1. **Start with basics** (01) - Understand simple AI responses
2. **Add complexity** (02) - Learn ReAct patterns and tools
3. **Introduce MCP** (03) - Understand server architecture
4. **Manual control** (04) - Build custom LangGraph workflows
5. **Interactive flows** (05) - Add user decision points
6. **Scale up** (06) - Deploy multiple specialized servers

## 🔧 Key Technologies

- **LangChain**: Framework for building applications with LLMs
- **LangGraph**: Library for building stateful, multi-actor applications
- **MCP (Model Context Protocol)**: Standard for connecting AI models to external tools
- **Gradio**: Web interface for machine learning applications
- **SQLite**: Lightweight database for examples

## 📝 Workshop Session Details

**Date**: March 23, 2025
**Time**: 11:50 AM - 1:00 PM (1 hour 10 minutes)
**Format**: Online workshop with live coding demonstrations

**🎥 Watch the Workshop**: [YouTube Live Stream](https://www.youtube.com/live/nSN8akWjJvc?si=pW5qFKPGjWkfVDlS&t=49)

## 🤝 Contributing

This workshop is designed for educational purposes. Feel free to experiment with the examples and extend them for your own learning.

## 📄 License

Educational content for NerdearLA 2025 workshop.