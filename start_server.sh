#!/bin/bash
export http_proxy="http://pkumdl:pkumdl@162.105.160.81:7890"
export https_proxy="http://pkumdl:pkumdl@162.105.160.81:7890"

source .venv/bin/activate
python -m paper_search_mcp.server