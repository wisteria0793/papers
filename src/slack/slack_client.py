from slack_sdk import WebClient

def notify_slack(paper):
    client = WebClient(token="your_slack_api_token")
    message = f"New paper added: {paper['title']} - {paper['link']}"
    client.chat_postMessage(channel="#your-channel", text=message) 