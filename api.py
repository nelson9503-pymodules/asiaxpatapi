from .cover_extractor import CoverExtractor
from .content_extractor import ContentExtractor

def extract_cover(page: int) -> dict:
    extractor = CoverExtractor()
    results = extractor.extract(page)
    return results

def extract_content(url: str) -> dict:
    extractor = ContentExtractor()
    results = extractor.extract(url)
    return results