import sqlite3

# データベースの初期化
def initialize_database():
    conn = sqlite3.connect('papers.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS papers (
            arxiv_id TEXT PRIMARY KEY,
            title TEXT,
            version TEXT,
            published_date TEXT,
            updated_date TEXT
        )
    ''')
    conn.commit()
    conn.close()

# 重複チェック
def is_duplicate(paper_id):
    conn = sqlite3.connect('papers.db')
    cursor = conn.cursor()
    cursor.execute("SELECT 1 FROM papers WHERE arxiv_id=?", (paper_id,))
    result = cursor.fetchone()
    conn.close()
    return result is not None

# 論文情報の登録
def add_paper(paper_id, title, version, published_date, updated_date):
    conn = sqlite3.connect('papers.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO papers (arxiv_id, title, version, published_date, updated_date)
        VALUES (?, ?, ?, ?, ?)
    ''', (paper_id, title, version, published_date, updated_date))
    conn.commit()
    conn.close() 