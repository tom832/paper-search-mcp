# paper_search_mcp/server.py
from typing import List, Dict, Optional
import httpx
from mcp.server.fastmcp import FastMCP
from .academic_platforms.arxiv import ArxivSearcher
from .academic_platforms.pubmed import PubMedSearcher
from .academic_platforms.biorxiv import BioRxivSearcher
from .academic_platforms.medrxiv import MedRxivSearcher
from .academic_platforms.google_scholar import GoogleScholarSearcher
from .academic_platforms.iacr import IACRSearcher
from .academic_platforms.semantic import SemanticSearcher
from .academic_platforms.hub import SciHubSearcher

# Initialize MCP server
mcp = FastMCP(
    name="science-search",
    host="localhost",
    port=18001,
    streamable_http_path="/",
)

# Instances of searchers
arxiv_searcher = ArxivSearcher()
pubmed_searcher = PubMedSearcher()
biorxiv_searcher = BioRxivSearcher()
medrxiv_searcher = MedRxivSearcher()
google_scholar_searcher = GoogleScholarSearcher()
iacr_searcher = IACRSearcher()
semantic_searcher = SemanticSearcher()
scihub_searcher = SciHubSearcher()


"""
Search
"""


# Asynchronous helper to adapt synchronous searchers
async def async_search(searcher, query: str, max_results: int, **kwargs) -> List[Dict]:
    async with httpx.AsyncClient() as client:
        papers = searcher.search(query, max_results=max_results, **kwargs)
        return [paper.to_dict() for paper in papers]


@mcp.tool(
    title="Search arXiv",
    description="Search academic papers from arXiv using keywords."
)
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


@mcp.tool(
    title="Search PubMed",
    description="Search academic papers from PubMed using keywords."
)
async def search_pubmed(query: str, max_results: int = 10) -> List[Dict]:
    """Search academic papers from PubMed.

    Args:
        query: Search query string (e.g., 'machine learning').
        max_results: Maximum number of papers to return (default: 10).
    Returns:
        List of paper metadata in dictionary format.
    """
    papers = await async_search(pubmed_searcher, query, max_results)
    return papers if papers else []


@mcp.tool(
    title="Search bioRxiv",
    description="Search academic papers from bioRxiv using keywords."
)
async def search_biorxiv(query: str, max_results: int = 10) -> List[Dict]:
    """Search academic papers from bioRxiv.

    Args:
        query: Search query string (e.g., 'machine learning').
        max_results: Maximum number of papers to return (default: 10).
    Returns:
        List of paper metadata in dictionary format.
    """
    papers = await async_search(biorxiv_searcher, query, max_results)
    return papers if papers else []


@mcp.tool(
   title="Search medRxiv",
   description="Search academic papers from medRxiv using keywords."
)
async def search_medrxiv(query: str, max_results: int = 10) -> List[Dict]:
    """Search academic papers from medRxiv.

    Args:
        query: Search query string (e.g., 'machine learning').
        max_results: Maximum number of papers to return (default: 10).
    Returns:
        List of paper metadata in dictionary format.
    """
    papers = await async_search(medrxiv_searcher, query, max_results)
    return papers if papers else []


@mcp.tool(
    title="Search Google Scholar",
    description="Search academic papers from Google Scholar using keywords."
)
async def search_google_scholar(query: str, max_results: int = 10) -> List[Dict]:
    """Search academic papers from Google Scholar.

    Args:
        query: Search query string (e.g., 'machine learning').
        max_results: Maximum number of papers to return (default: 10).
    Returns:
        List of paper metadata in dictionary format.
    """
    papers = await async_search(google_scholar_searcher, query, max_results)
    return papers if papers else []


@mcp.tool(
    title="Search IACR",
    description="Search academic papers from IACR ePrint Archive using keywords."
)
async def search_iacr(
    query: str, max_results: int = 10, fetch_details: bool = True
) -> List[Dict]:
    """Search academic papers from IACR ePrint Archive.

    Args:
        query: Search query string (e.g., 'cryptography', 'secret sharing').
        max_results: Maximum number of papers to return (default: 10).
        fetch_details: Whether to fetch detailed information for each paper (default: True).
    Returns:
        List of paper metadata in dictionary format.
    """
    async with httpx.AsyncClient() as client:
        papers = iacr_searcher.search(query, max_results, fetch_details)
        return [paper.to_dict() for paper in papers] if papers else []


@mcp.tool(
    title="Search Semantic Scholar",
    description="Search academic papers from Semantic Scholar using keywords."
)
async def search_semantic(query: str, year: Optional[str] = None, max_results: int = 10) -> List[Dict]:
    """Search academic papers from Semantic Scholar.

    Args:
        query: Search query string (e.g., 'machine learning').
        year: Optional year filter (e.g., '2019', '2016-2020', '2010-', '-2015').
        max_results: Maximum number of papers to return (default: 10).
    Returns:
        List of paper metadata in dictionary format.
    """
    kwargs = {}
    if year is not None:
        kwargs['year'] = year
    papers = await async_search(semantic_searcher, query, max_results, **kwargs)
    return papers if papers else []


"""
Download
"""


# @mcp.tool(
#     title="Download arXiv Paper",
#     description="Download the PDF of an arXiv paper given its ID."
# )
# async def download_arxiv(paper_id: str, save_path: str = "./downloads") -> str:
#     """Download PDF of an arXiv paper.

#     Args:
#         paper_id: arXiv paper ID (e.g., '2106.12345').
#         save_path: Directory to save the PDF (default: './downloads').
#     Returns:
#         Path to the downloaded PDF file.
#     """
#     async with httpx.AsyncClient() as client:
#         return arxiv_searcher.download_pdf(paper_id, save_path)


# @mcp.tool(
#     title="Download PubMed Paper from Sci-Hub",
#     description="Attempt to download the PDF of a PubMed paper given its DOI."
# )
# async def download_pubmed(doi: str, save_path: str = "./downloads") -> str:
#     """Attempt to download PDF of a PubMed paper from Sci-Hub.

#     Args:
#         doi: DOI.
#         save_path: Directory to save the PDF (default: './downloads').
#     Returns:
#         str: Message indicating that direct PDF download is not supported.
#     """
#     try:
#         return scihub_searcher.download_pdf(doi, save_path)
#     except NotImplementedError as e:
#         return str(e)


# @mcp.tool(
#     title="Download bioRxiv Paper",
#     description="Download the PDF of a bioRxiv paper given its DOI."
# )
# async def download_biorxiv(paper_id: str, save_path: str = "./downloads") -> str:
#     """Download PDF of a bioRxiv paper.

#     Args:
#         paper_id: bioRxiv DOI.
#         save_path: Directory to save the PDF (default: './downloads').
#     Returns:
#         Path to the downloaded PDF file.
#     """
#     return biorxiv_searcher.download_pdf(paper_id, save_path)


# @mcp.tool(
#     title="Download medRxiv Paper",
#     description="Download the PDF of a medRxiv paper given its DOI."
# )
# async def download_medrxiv(paper_id: str, save_path: str = "./downloads") -> str:
#     """Download PDF of a medRxiv paper.

#     Args:
#         paper_id: medRxiv DOI.
#         save_path: Directory to save the PDF (default: './downloads').
#     Returns:
#         Path to the downloaded PDF file.
#     """
#     return medrxiv_searcher.download_pdf(paper_id, save_path)


# @mcp.tool(
#     title="Download Google Scholar Paper from Sci-Hub",
#     description="Download the PDF of a Google Scholar paper given its DOI."
# )
# async def download_google_scholar(doi: str, save_path: str = "./downloads") -> str:
#     """Download PDF of a Google Scholar paper given its DOI from Sci-Hub.
    
#     Args:
#         doi: DOI.
#         save_path: Directory to save the PDF (default: './downloads').
#     Returns:
#         str: Message indicating that direct PDF download is not supported.
#     """
#     try:
#         return scihub_searcher.download_pdf(doi, save_path)
#     except NotImplementedError as e:
#         return str(e)


# @mcp.tool(
#     title="Download IACR Paper",
#     description="Download the PDF of an IACR ePrint paper given its ID."
# )
# async def download_iacr(paper_id: str, save_path: str = "./downloads") -> str:
#     """Download PDF of an IACR ePrint paper.

#     Args:
#         paper_id: IACR paper ID (e.g., '2009/101').
#         save_path: Directory to save the PDF (default: './downloads').
#     Returns:
#         Path to the downloaded PDF file.
#     """
#     return iacr_searcher.download_pdf(paper_id, save_path)


# @mcp.tool(
#     title="Download Semantic Scholar Paper",
#     description="Download the PDF of a Semantic Scholar paper given its ID."
# )
# async def download_semantic(paper_id: str, save_path: str = "./downloads") -> str:
#     """Download PDF of a Semantic Scholar paper.    

#     Args:
#         paper_id: Semantic Scholar paper ID, Paper identifier in one of the following formats:
#             - Semantic Scholar ID (e.g., "649def34f8be52c8b66281af98ae884c09aef38b")
#             - DOI:<doi> (e.g., "DOI:10.18653/v1/N18-3011")
#             - ARXIV:<id> (e.g., "ARXIV:2106.15928")
#             - MAG:<id> (e.g., "MAG:112218234")
#             - ACL:<id> (e.g., "ACL:W12-3903")
#             - PMID:<id> (e.g., "PMID:19872477")
#             - PMCID:<id> (e.g., "PMCID:2323736")
#             - URL:<url> (e.g., "URL:https://arxiv.org/abs/2106.15928v1")
#         save_path: Directory to save the PDF (default: './downloads').
#     Returns:
#         Path to the downloaded PDF file.
#     """ 
#     return semantic_searcher.download_pdf(paper_id, save_path)


# @mcp.tool(
#     title="Download paper from Sci-Hub",
#     description="Download the PDF of a paper from Sci-Hub given its DOI."
# )
# async def download_scihub(doi: str, save_path: str = "./downloads") -> str:
#     """Download PDF of a paper from Sci-Hub.

#     Args:
#         doi: DOI.
#         save_path: Directory to save the PDF (default: './downloads').
#     Returns:
#         Path to the downloaded PDF file.
#     """
#     return scihub_searcher.download_pdf(doi, save_path)


"""
Read
"""


@mcp.tool(
    title="Read arXiv Paper",
    description="Read and extract text content from an arXiv paper given its ID."
)
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


@mcp.tool(
    title="Read PubMed Paper through Sci-Hub",
    description="Read and extract text content from a PubMed paper given its DOI."
)
async def read_pubmed_paper(doi: str, save_path: str = "./downloads") -> str:
    """Read and extract text content of a PubMed paper from Sci-Hub.

    Note: Direct reading of PubMed papers is not supported, as they are not available in PDF format directly.
    Instead, this function attempts to read the paper through Sci-Hub.

    Args:
        doi: DOI.
        save_path: Directory where the PDF would be saved (unused).
    Returns:
        str: Message indicating that direct paper reading is not supported.
    """
    return scihub_searcher.read_paper(doi, save_path)


@mcp.tool(
    title="Read bioRxiv Paper",
    description="Read and extract text content from a bioRxiv paper given its ID."
)
async def read_biorxiv_paper(paper_id: str, save_path: str = "./downloads") -> str:
    """Read and extract text content from a bioRxiv paper PDF.

    Args:
        paper_id: bioRxiv DOI.
        save_path: Directory where the PDF is/will be saved (default: './downloads').
    Returns:
        str: The extracted text content of the paper.
    """
    try:
        return biorxiv_searcher.read_paper(paper_id, save_path)
    except Exception as e:
        print(f"Error reading paper {paper_id}: {e}")
        return ""


@mcp.tool(
    title="Read medRxiv Paper",
    description="Read and extract text content from a medRxiv paper given its ID."
)
async def read_medrxiv_paper(paper_id: str, save_path: str = "./downloads") -> str:
    """Read and extract text content from a medRxiv paper PDF.

    Args:
        paper_id: medRxiv DOI.
        save_path: Directory where the PDF is/will be saved (default: './downloads').
    Returns:
        str: The extracted text content of the paper.
    """
    try:
        return medrxiv_searcher.read_paper(paper_id, save_path)
    except Exception as e:
        print(f"Error reading paper {paper_id}: {e}")
        return ""


@mcp.tool(
    title="Read Google Scholar Paper from Sci-Hub",
    description="Read and extract text content from a Google Scholar paper given its DOI."
)
async def read_google_scholar_paper(doi: str, save_path: str = "./downloads") -> str:
    """Read and extract text content from a Google Scholar paper PDF.

    Args:
        doi: DOI.
        save_path: Directory where the PDF is/will be saved (default: './downloads').
    Returns:
        str: The extracted text content of the paper.
    """
    try:
        return scihub_searcher.read_paper(doi, save_path)
    except Exception as e:
        print(f"Error reading paper {doi}: {e}")
        return ""


@mcp.tool(
    title="Read IACR Paper",
    description="Read and extract text content from an IACR ePrint paper given its ID."
)
async def read_iacr_paper(paper_id: str, save_path: str = "./downloads") -> str:
    """Read and extract text content from an IACR ePrint paper PDF.

    Args:
        paper_id: IACR paper ID (e.g., '2009/101').
        save_path: Directory where the PDF is/will be saved (default: './downloads').
    Returns:
        str: The extracted text content of the paper.
    """
    try:
        return iacr_searcher.read_paper(paper_id, save_path)
    except Exception as e:
        print(f"Error reading paper {paper_id}: {e}")
        return ""


@mcp.tool(
    title="Read Semantic Scholar Paper",
    description="Read and extract text content from a Semantic Scholar paper given its ID."
)
async def read_semantic_paper(paper_id: str, save_path: str = "./downloads") -> str:
    """Read and extract text content from a Semantic Scholar paper. 

    Args:
        paper_id: Semantic Scholar paper ID, Paper identifier in one of the following formats:
            - Semantic Scholar ID (e.g., "649def34f8be52c8b66281af98ae884c09aef38b")
            - DOI:<doi> (e.g., "DOI:10.18653/v1/N18-3011")
            - ARXIV:<id> (e.g., "ARXIV:2106.15928")
            - MAG:<id> (e.g., "MAG:112218234")
            - ACL:<id> (e.g., "ACL:W12-3903")
            - PMID:<id> (e.g., "PMID:19872477")
            - PMCID:<id> (e.g., "PMCID:2323736")
            - URL:<url> (e.g., "URL:https://arxiv.org/abs/2106.15928v1")
        save_path: Directory where the PDF is/will be saved (default: './downloads').
    Returns:
        str: The extracted text content of the paper.
    """
    try:
        return semantic_searcher.read_paper(paper_id, save_path)
    except Exception as e:
        print(f"Error reading paper {paper_id}: {e}")
        return ""


@mcp.tool(
    title="Read DOI through Sci-Hub",
    description="Read and extract text content from a paper PDF downloaded from Sci-Hub."
)
async def read_scihub_paper(doi: str, save_path: str = "./downloads") -> str:
    """Read and extract text content from a Sci-Hub paper PDF.
    
    Args:
        doi: Paper ID (DOI).
        save_path: Directory where the PDF is/will be saved (default: './downloads').
    Returns:
        str: The extracted text content of the paper.
    """
    try:
        return scihub_searcher.read_paper(doi, save_path)
    except Exception as e:
        print(f"Error reading paper {doi}: {e}")
        return ""


if __name__ == "__main__":
    mcp.run(transport="streamable-http")
