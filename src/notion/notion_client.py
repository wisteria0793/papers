from notion_client import Client
import os
from dotenv import load_dotenv
import requests
from transformers import pipeline
import re
from datetime import datetime

# .envファイルから環境変数を読み込む
load_dotenv(dotenv_path='../config/.env')
DATABASE_ID = os.getenv("NOTION_DATABASE_ID")
NOTION_API_KEY = os.getenv("NOTION_API_KEY")

url = "https://api.notion.com/v1/pages"
headers = {
    "Notion-Version": "2022-06-28",
    "Authorization": "Bearer " + NOTION_API_KEY,
    "Content-Type": "application/json",
}

# Initialize the translation pipeline with a valid model
translator = pipeline("translation", model="Helsinki-NLP/opus-mt-en-jap")
# If the model is private, authenticate with a token
# translator = pipeline("translation", model="Helsinki-NLP/opus-mt-en-jap", use_auth_token='your_token_here')

def add_paper_to_notion(paper):
    
    
    # Notion APIクライアントの初期化
    notion = Client(auth=os.getenv("NOTION_API_KEY"))
    
    # データベースIDの取得
    database_id = os.getenv("NOTION_DATABASE_ID")
    
    cleaned_title = re.sub(r'\n(?!\n)', ' ', paper['title'])
    cleaned_summary = re.sub(r'\n(?!\n)', ' ', paper['summary'])
    # Replace multiple spaces with a single space
    # cleaned_text = re.sub(r'\s+', ' ', cleaned_title)
    
    # Translate the summary from English to Japanese
    translated_summary = translator(cleaned_summary)[0]['translation_text']
    # paper['keywords'] = ['test', 'test2']
    # Get the current date in the standard format
    date_added = datetime.now().strftime('%Y-%m-%d')
    # 論文情報をNotionのデータベースに追加
    print('title:', paper['title'])
    print('authors:', paper['authors'])
    print('keywords:', paper['keywords'])
    print('url:', paper['url'])
    print('date_added:', date_added)
    try:
        json_data = {
            "parent": {"database_id": DATABASE_ID},
            "properties": {
                "Title": {"title": [{"text": {"content": cleaned_title}}]},
                "Authors": {"rich_text": [{"text": {"content": ', '.join(paper['authors'])}}]},
                "Keywords": {
                    "multi_select": [{"name": keyword} for keyword in paper['keywords']]
                },
                "Summary_en": {"rich_text": [{"text": {"content": cleaned_summary}}]},
                "Summary_ja": {"rich_text": [{"text": {"content": translated_summary}}]},
                "URL": {"url": paper['url']},
                "Date Added": {"date": {"start": date_added}}
            },
        }

        response = requests.post(url, headers=headers, json=json_data)
        print(response.status_code)
        # print(response.text)

    except Exception as e:
        print(f"Failed to add paper to Notion: {e}") 