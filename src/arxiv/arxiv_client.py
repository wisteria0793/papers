import requests
import xml.etree.ElementTree as ET
from keybert import KeyBERT


def fetch_papers(keyword, category):
    url = f"http://export.arxiv.org/api/query?search_query=all:{keyword}+AND+cat:{category}&start=0&max_results=10"
    response = requests.get(url)
    
    if response.status_code != 200:
        raise Exception(f"Failed to fetch papers from arXiv: {response.status_code}")
    
    papers = parse_arxiv_response(response.content)
    return papers

def parse_arxiv_response(xml_content):
    root = ET.fromstring(xml_content)
    papers = []
    
    for entry in root.findall('{http://www.w3.org/2005/Atom}entry'):
        paper_id = entry.find('{http://www.w3.org/2005/Atom}id').text.split('/')[-1]
        title = entry.find('{http://www.w3.org/2005/Atom}title').text.strip()
        summary = entry.find('{http://www.w3.org/2005/Atom}summary').text.strip()
        published_date = entry.find('{http://www.w3.org/2005/Atom}published').text
        updated_date = entry.find('{http://www.w3.org/2005/Atom}updated').text
        version = paper_id.split('v')[-1]  # Extract version from ID
        authors = [author.find('{http://www.w3.org/2005/Atom}name').text for author in entry.findall('{http://www.w3.org/2005/Atom}author')]
        url = entry.find('{http://www.w3.org/2005/Atom}id').text

        # キーワードを抽出し、重複なしのリストに変換
        kw_model = KeyBERT()
        keywords_with_scores = kw_model.extract_keywords(summary, keyphrase_ngram_range=(1, 2), stop_words='english')
        keywords = list(set([kw[0] for kw in keywords_with_scores]))  # 重複を排除してキーワードをリストに追加
        print('keywords:', keywords)

        papers.append({
            'id': paper_id,
            'title': title,
            'summary': summary,
            'published_date': published_date,
            'updated_date': updated_date,
            'version': version,
            'authors': authors,
            'keywords': keywords,
            'url': url
        })
        
    return papers 
