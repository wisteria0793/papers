from arxiv.arxiv_client import fetch_papers
from notion.notion_client import add_paper_to_notion
# from slack.slack_client import notify_slack
from utils.duplicate_checker import initialize_database, is_duplicate, add_paper

def main():
    initialize_database()
    # papers = fetch_papers(keyword="machine learning", category="cs.LG")
    papers = fetch_papers(keyword="language model", category="cs.LG")
    for paper in papers:
        # print(paper)
        if not is_duplicate(paper['id']):
            # print(paper['id'])
            add_paper(paper['id'], paper['title'], paper['version'], paper['published_date'], paper['updated_date'])
            add_paper_to_notion(paper)
            # notify_slack(paper)

if __name__ == "__main__":
    main() 