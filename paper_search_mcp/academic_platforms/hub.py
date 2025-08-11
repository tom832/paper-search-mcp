from typing import List
import requests
from bs4 import BeautifulSoup
import os
import random
import re
from urllib.parse import urlparse
from ..paper import Paper
from pypdf import PdfReader

class PaperSource:
    """Abstract base class for paper sources"""
    def search(self, query: str, **kwargs) -> List[Paper]:
        raise NotImplementedError

    def download_pdf(self, paper_id: str, save_path: str) -> str:
        raise NotImplementedError

    def read_paper(self, paper_id: str, save_path: str) -> str:
        raise NotImplementedError

class SciHubSearcher(PaperSource):

    BROWSERS = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36"
    ]

    def __init__(self):
        self.session = requests.Session()
        self.available_urls = self._get_available_scihub_urls()
        self.session.headers.update({'User-Agent': random.choice(self.BROWSERS)})
        self.url_index = 0

    def _get_available_scihub_urls(self) -> List[str]:
        '''
        Finds available scihub urls via https://www.sci-hub.pub/
        '''
        urls = []
        try:
            res = requests.get('https://www.sci-hub.pub/', timeout=10)
            res.raise_for_status()
            s = BeautifulSoup(res.content, 'html.parser')
            for a in s.find_all('a', href=True):
                if 'sci-hub.' in a['href'] and a['href'].startswith('http'):
                    urls.append(urlparse(a['href']).netloc)
        except requests.RequestException as e:
            return ['sci-hub.se', 'sci-hub.st', 'sci-hub.ru']
        return list(set(urls))

    def search(self, query: str, **kwargs) -> List[Paper]:
        """
        SciHub does not support keyword search directly.

        Returns:
            str: Message indicating the feature is not supported
        """
        raise NotImplementedError(
            "SciHub does not support keyword search directly."
            "Use paper IDs or DOIs to access papers."
        )

    def download_pdf(self, paper_id: str, save_path: str) -> str:
        if not self.available_urls:
            raise RuntimeError("No available Sci-Hub URLs found.")
        
        urls_to_try = self.available_urls[self.url_index:] + self.available_urls[:self.url_index]

        for i, base_url in enumerate(urls_to_try):
            pdf_url = None
            try:
                # Extract PDF url
                request_url = f"https://{base_url}/{paper_id}"
                res = self.session.get(request_url, timeout=20)
                res.raise_for_status()
                soup = BeautifulSoup(res.content, 'html.parser')

                # Plan A: Check embed
                embed = soup.find('embed', id=re.compile(r'pdf-?embed'))
                if embed and embed.get('original-url'):
                    pdf_url = embed['original-url']
                elif embed and embed.get('src'): # 作为备用
                    pdf_url = embed['src']

                # Plan B: Check iframe
                if not pdf_url:
                    iframe = soup.find('iframe')
                    if iframe and iframe.get('src'):
                        pdf_url = iframe['src']

                if not pdf_url:
                    # Did not find PDF URL in embed or iframe
                    continue

                if pdf_url.startswith('//'):
                    pdf_url = 'https:' + pdf_url
                
                # Download PDF
                pdf_response = self.session.get(pdf_url, timeout=20)
                pdf_response.raise_for_status()

                # Save PDF to file
                filename = f"{paper_id.replace('/', '_')}.pdf"
                pdf_path = os.path.join(save_path, filename)
                with open(pdf_path, 'wb') as f:
                    f.write(pdf_response.content)

                self.url_index = (self.url_index + i) % len(self.available_urls)

                return pdf_path

            except (requests.RequestException) as e:
                print(f"Error downloading from {base_url}: {e}")
                continue
            except Exception as e:
                print(f"Unexpected error with {base_url}: {e}")
                continue

        raise RuntimeError(f"Failed to download PDF for {paper_id} from all available Sci-Hub URLs.")

    def read_paper(self, paper_id: str, save_path: str) -> str:
        temporary_download = False
        pdf_path = f"{save_path}/{paper_id.replace('/', '_')}.pdf"
        if not os.path.exists(pdf_path):
            temporary_download = True
            pdf_path = self.download_pdf(paper_id, save_path)
        
        try:
            reader = PdfReader(pdf_path)
            text = ""
            for page in reader.pages:
                text += page.extract_text() + "\n"
            return text.strip()
        except Exception as e:
            print(f"Error reading PDF for paper {paper_id}: {e}")
            return ""
        finally:
            # Clean up the temporary file if we downloaded it
            if temporary_download and os.path.exists(pdf_path):
                os.remove(pdf_path)