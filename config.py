import os

# Notion API configuration
NOTION_API_KEY = os.getenv('NOTION_API_KEY')
NOTION_PARENT_PAGE_ID = os.getenv('NOTION_PARENT_PAGE_ID')

# API settings
NOTION_API_BASE_URL = "https://api.notion.com/v1/"
NOTION_API_VERSION = "2022-06-28"

# Date range for schedule (2025年下半期)
START_DATE = "2025-07-01"
END_DATE = "2025-07-08"
