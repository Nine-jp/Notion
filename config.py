import os

# Notion API設定
NOTION_API_KEY = os.getenv('NOTION_API_KEY')
NOTION_PARENT_PAGE_ID = os.getenv('NOTION_PARENT_PAGE_ID')

# APIキーが設定されていない場合のエラー
if NOTION_API_KEY is None:
    raise ValueError("環境変数 'NOTION_API_KEY' が設定されていません")
if NOTION_PARENT_PAGE_ID is None:
    raise ValueError("環境変数 'NOTION_PARENT_PAGE_ID' が設定されていません")
