# Paper Search MCP

A Model Context Protocol (MCP) server for searching and downloading academic papers from multiple sources, including arXiv, PubMed, bioRxiv, and Sci-Hub (optional). Designed for seamless integration with large language models like Claude Desktop.

![PyPI](https://img.shields.io/pypi/v/paper-search-mcp.svg) ![License](https://img.shields.io/badge/license-MIT-blue.svg) ![Python](https://img.shields.io/badge/python-3.10+-blue.svg)

---

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Installation](#installation)
  - [Quick Start](#quick-start)
  - [For Development](#for-development)
- [Testing](#testing)
- [Usage](#usage)
  - [Running the Server](#running-the-server)
  - [Using with Claude Desktop](#using-with-claude-desktop)
  - [Example Commands](#example-commands)
- [Deployment](#deployment)
  - [Local Deployment](#local-deployment)
  - [Cloud Deployment](#cloud-deployment)
- [Contributing](#contributing)
- [License](#license)

---

## Overview

`paper-search-mcp` is a Python-based MCP server that enables users to search and download academic papers from various platforms. It provides tools for searching papers (e.g., `search_arxiv`) and downloading PDFs (e.g., `download_arxiv`), making it ideal for researchers and AI-driven workflows. Built with the MCP Python SDK, it integrates seamlessly with LLM clients like Claude Desktop.

---

## Features

- **Multi-Source Support**: Search and download papers from arXiv, PubMed, bioRxiv, and Sci-Hub (optional).
- **Standardized Output**: Papers are returned in a consistent dictionary format via the `Paper` class.
- **Asynchronous Tools**: Efficiently handles network requests using `httpx`.
- **MCP Integration**: Compatible with MCP clients for LLM context enhancement.
- **Extensible Design**: Easily add new academic platforms by extending the `academic_platforms` module.

---

## Installation

`paper-search-mcp` can be installed using `uv` or `pip`. Below are two approaches: a quick start for immediate use and a detailed setup for development.

### Quick Start

For users who want to quickly run the server:

1. **Install with uv** (recommended):
   ```bash
   uv add paper-search-mcp
   ```
   OR with pip:
   ```bash
   pip install paper-search-mcp
   ```

2. **Run the Server**:
   ```bash
   uv run -m paper_search_mcp.server  # With uv
   # OR
   python -m paper_search_mcp.server  # With pip
   ```

3. **Verify Installation**:
   ```bash
   python -c "import paper_search_mcp; print(paper_search_mcp.__version__)"
   ```

### For Development

For developers who want to modify the code or contribute:

1. **Setup Environment**:
   ```bash
   # Install uv if not installed
   curl -LsSf https://astral.sh/uv/install.sh | sh
   
   # Clone repository
   git clone https://github.com/yourusername/paper-search-mcp.git
   cd paper-search-mcp
   
   # Create and activate virtual environment
   uv venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

2. **Install Dependencies**:
   ```bash
   # Install project in editable mode
   uv add -e .
   
   # Add development dependencies (optional)
   uv add pytest flake8
   ```

3. **Verify Setup**:
   ```bash
   # Check installation
   python -c "import paper_search_mcp; print(paper_search_mcp.__version__)"
   
   # Run tests
   python -m unittest discover tests
   ```

---

## Testing

To ensure the server works correctly, run the included unit tests.

1. **Activate Environment**:
   ```bash
   source .venv/bin/activate
   ```

2. **Run Tests**:
   ```bash
   python -m unittest discover tests
   ```

   - `test_arxiv.py`: Tests the `ArxivSearcher` class.
   - `test_server.py`: Tests the MCP server tools (`search_arxiv` and `download_arxiv`).

   Expected Output:
   ```
   ....
   Ran 4 tests in X.XXXs
   OK
   ```

---

## Usage

### Running the Server

Start the MCP server locally:
```bash
python -m paper_search_mcp.server
```
The server runs with stdio transport, ready to accept MCP client connections.

### Using with Claude Desktop

1. **Install Claude Desktop**:
   Download from Anthropic's website and install the latest version.

2. **Configure MCP Server**:
   Open or create `~/Library/Application Support/Claude/claude_desktop_config.json` (Mac) or equivalent path (Windows/Linux). Add the server configuration:
   ```json
   {
       "mcpServers": {
           "paper_search_server": {
               "command": "python",
               "args": [
                   "-m",
                   "paper_search_mcp.server"
               ]
           }
       }
   }
   ```
   Save and restart Claude Desktop.

3. **Verify Integration**:
   In Claude Desktop, look for the hammer icon (🔨) in the UI. Click it to see available tools (`search_arxiv`, `download_arxiv`, etc.).

### Example Commands

- **Search Papers**:
  ```
  Search for "machine learning" papers on arXiv
  ```
  Returns a list of 10 papers (default `max_results`).

- **Download a Paper**:
  ```
  Download arXiv paper 2106.12345
  ```
  Saves the PDF to `./downloads` (default path).

- **Custom Search**:
  ```
  Search PubMed for "cancer treatment" with max_results=5
  ```
  Returns 5 papers from PubMed.

---

## Deployment

### Local Deployment

For personal use or development:
```bash
nohup python -m paper_search_mcp.server &
```
Keeps the server running in the background. Check `nohup.out` for server output.

### Cloud Deployment

To deploy on a cloud service (e.g., AWS EC2):

1. **Set Up EC2 Instance**:
   - Launch an Ubuntu instance.
   - Open port 22 (SSH) and ensure internet access.

2. **Install Dependencies**:
   ```bash
   sudo apt update
   sudo apt install python3 python3-pip git
   git clone https://github.com/yourusername/paper-search-mcp.git
   cd paper-search-mcp
   pip3 install -e .
   ```

3. **Run Server**:
   ```bash
   python3 -m paper_search_mcp.server
   ```

   Use `screen` or `tmux` to keep it running after logout:
   ```bash
   screen
   python3 -m paper_search_mcp.server
   # Press Ctrl+A, then D to detach
   ```

---

## Contributing

We welcome contributions! Here's how to get started:

1. **Fork the Repository**:
   Click "Fork" on GitHub.

2. **Clone and Set Up**:
   ```bash
   git clone https://github.com/yourusername/paper-search-mcp.git
   cd paper-search-mcp
   pip install -e ".[dev]"  # Install dev dependencies (if added to pyproject.toml)
   ```

3. **Make Changes**:
   - Add new platforms in `academic_platforms/`.
   - Update tests in `tests/`.

4. **Submit a Pull Request**:
   Push changes and create a PR on GitHub.

---


## Demo
<img src="docs\images\demo.png" alt="Demo" width="800">




## License

This project is licensed under the MIT License. See the LICENSE file for details.

---

Happy researching with `paper-search-mcp`! If you encounter issues, open a GitHub issue.