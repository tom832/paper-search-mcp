from typing import List
import requests
import os
from datetime import datetime
from ..paper import Paper
from PyPDF2 import PdfReader

class PaperSource:
    """Abstract base class for paper sources"""
    def search(self, query: str, **kwargs) -> List[Paper]:
        raise NotImplementedError

    def download_pdf(self, paper_id: str, save_path: str) -> str:
        raise NotImplementedError

    def read_paper(self, paper_id: str, save_path: str) -> str:
        raise NotImplementedError

class BioRxivSearcher(PaperSource):
    """Searcher for bioRxiv papers"""
    BASE_URL = "https://api.biorxiv.org/details/biorxiv"

    def __init__(self):
        # 设置代理为空，避免使用系统代理
        self.session = requests.Session()
        self.session.proxies = {
            'http': None,
            'https': None
        }
        # 设置超时和重试次数
        self.timeout = 30
        self.max_retries = 3

    def search(self, query: str, max_results: int = 10) -> List[Paper]:
        url = f"{self.BASE_URL}/0/{max_results}?search={query}"
        tries = 0
        while tries < self.max_retries:
            try:
                response = self.session.get(url, timeout=self.timeout)
                response.raise_for_status()  # 检查响应状态
                data = response.json()
                papers = []
                for item in data.get('collection', []):
                    try:
                        date = datetime.strptime(item['date'], '%Y-%m-%d')
                        papers.append(Paper(
                            paper_id=item['doi'],
                            title=item['title'],
                            authors=item['authors'].split('; '),
                            abstract=item['abstract'],
                            url=f"https://www.biorxiv.org/content/{item['doi']}v1",
                            pdf_url=f"https://www.biorxiv.org/content/{item['doi']}v1.full.pdf",
                            published_date=date,
                            updated_date=date,
                            source='biorxiv',
                            categories=[item['category']],
                            keywords=[],
                            doi=item['doi']
                        ))
                    except Exception as e:
                        print(f"Error parsing bioRxiv entry: {e}")
                return papers
            except requests.exceptions.RequestException as e:
                tries += 1
                if tries == self.max_retries:
                    print(f"Failed to connect to bioRxiv API after {self.max_retries} attempts: {e}")
                    return []
                print(f"Attempt {tries} failed, retrying...")
        return []

    def download_pdf(self, paper_id: str, save_path: str) -> str:
        pdf_url = f"https://www.biorxiv.org/content/{paper_id}v1.full.pdf"
        tries = 0
        while tries < self.max_retries:
            try:
                response = self.session.get(pdf_url, timeout=self.timeout)
                response.raise_for_status()
                output_file = f"{save_path}/{paper_id.replace('/', '_')}.pdf"
                with open(output_file, 'wb') as f:
                    f.write(response.content)
                return output_file
            except requests.exceptions.RequestException as e:
                tries += 1
                if tries == self.max_retries:
                    raise Exception(f"Failed to download PDF after {self.max_retries} attempts: {e}")
                print(f"Attempt {tries} failed, retrying...")
    
    def read_paper(self, paper_id: str, save_path: str = "./downloads") -> str:
        """Read a paper and convert it to text format.
        
        Args:
            paper_id: bioRxiv DOI
            save_path: Directory where the PDF is/will be saved
            
        Returns:
            str: The extracted text content of the paper
        """
        # First ensure we have the PDF
        pdf_path = f"{save_path}/{paper_id.replace('/', '_')}.pdf"
        if not os.path.exists(pdf_path):
            pdf_path = self.download_pdf(paper_id, save_path)
        
        # Read the PDF
        try:
            reader = PdfReader(pdf_path)
            text = ""
            for page in reader.pages:
                text += page.extract_text() + "\n"
            return text.strip()
        except Exception as e:
            print(f"Error reading PDF for paper {paper_id}: {e}")
            return ""