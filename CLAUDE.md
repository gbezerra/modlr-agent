# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Python project called "modlr-agent" that uses the uv package manager for dependency management. The project is in its early stages with a minimal structure and uses LangGraph as its main dependency.

## Development Environment

- **Python Version**: 3.12 (specified in `.python-version`)
- **Package Manager**: uv (ultra-fast Python package manager)
- **Virtual Environment**: Managed by uv in `.venv/`

## Common Commands

### Environment Setup
```bash
# Sync dependencies and update environment
uv sync

# Add a new dependency
uv add <package-name>

# Remove a dependency
uv remove <package-name>
```

### Running the Application
```bash
# Run the main application
uv run python main.py

# Or using uv run directly
uv run main.py
```

### Development Commands
```bash
# Update lockfile
uv lock

# View dependency tree
uv tree

# Export requirements for compatibility
uv export --format requirements-txt --output-file requirements.txt
```

## Project Structure

The project currently has a minimal structure:
- `main.py` - Entry point with a basic "Hello World" implementation
- `pyproject.toml` - Project configuration and dependencies
- `uv.lock` - Lockfile for reproducible builds
- `.python-version` - Python version specification for pyenv/uv

## Dependencies

- **LangGraph** (>=1.0.0a3) - Framework for building language model applications with graph-based workflows
- **LangChain** (>=0.3.27) - Core LangChain library for LLM applications
- **LangChain Core** (>=0.3.76) - Core abstractions and base interfaces
- **LangChain Google GenAI** (>=2.1.11) - Google AI integration for LangChain
- **IPython** (>=9.5.0) - Interactive Python environment for development

## Architecture Notes

This is a modular agent project that uses LangGraph to create AI-powered workflows. The project includes:

- `search_flow.py` - Implements a LangGraph agent with tool calling capabilities using Google's Gemini model
- The agent can process user requests and call tools to perform specific tasks
- Uses a state-based graph architecture with conditional routing between LLM calls and tool execution