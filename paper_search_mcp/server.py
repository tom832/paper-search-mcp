# paper_search_mcp/server.py
from typing import List, Dict
import httpx
from mcp.server.fastmcp import FastMCP
from .academic_platforms.arxiv import ArxivSearcher
# from .academic_platforms.pubmed import PubMedSearcher
# from .academic_platforms.biorxiv import BioRxivSearcher
# from .academic_platforms.hub import SciHubSearcher
from .paper import Paper

# Initialize MCP server
mcp = FastMCP("paper_search_server")

# Instances of searchers
arxiv_searcher = ArxivSearcher()
# pubmed_searcher = PubMedSearcher()
# biorxiv_searcher = BioRxivSearcher()
# scihub_searcher = SciHubSearcher()

# Asynchronous helper to adapt synchronous searchers
async def async_search(searcher, query: str, max_results: int) -> List[Dict]:
    async with httpx.AsyncClient() as client:
        # Assuming searchers use requests internally; we'll call synchronously for now
        papers = searcher.search(query, max_results)
        return [paper.to_dict() for paper in papers]

# Tool definitions
@mcp.tool()
async def search_arxiv(query: str, max_results: int = 10) -> List[Dict]:
    """Search academic papers from arXiv.

    Args:
        query: Search query string (e.g., 'machine learning').
        max_results: Maximum number of papers to return (default: 10).
    Returns:
        List of paper metadata in dictionary format.
    """
    papers = await async_search(arxiv_searcher, query, max_results)
    return papers if papers else []


@mcp.tool()
async def download_arxiv(paper_id: str, save_path: str = "./downloads") -> str:
    """Download PDF of an arXiv paper.

    Args:
        paper_id: arXiv paper ID (e.g., '2106.12345').
        save_path: Directory to save the PDF (default: './downloads').
    Returns:
        Path to the downloaded PDF file.
    """
    async with httpx.AsyncClient() as client:
        return arxiv_searcher.download_pdf(paper_id, save_path)


@mcp.tool()
async def read_arxiv_paper(paper_id: str, save_path: str = "./downloads") -> str:
    """Read and extract text content from an arXiv paper PDF.

    Args:
        paper_id: arXiv paper ID (e.g., '2106.12345').
        save_path: Directory where the PDF is/will be saved (default: './downloads').
    Returns:
        str: The extracted text content of the paper.
    """
    try:
        return arxiv_searcher.read_paper(paper_id, save_path)
    except Exception as e:
        print(f"Error reading paper {paper_id}: {e}")
        return ""

if __name__ == "__main__":
    mcp.run(transport="stdio")




