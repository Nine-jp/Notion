import requests
import json
from datetime import datetime, timedelta

# --- Notion API設定 ---
NOTION_API_KEY = "ntn_V5050303374bd0or47b7gcuiyix6d2xmglTyXP7KMQPcN6"
NOTION_PARENT_PAGE_ID = "21812d05838e81ee9392c24411ddfc0c"

NOTION_API_BASE_URL = "https://api.notion.com/v1/"
HEADERS = {
    "Authorization": f"Bearer {NOTION_API_KEY}",
    "Notion-Version": "2022-06-28",
    "Content-Type": "application/json",
}

# --- 次の火曜日の日付を計算する関数 ---
def get_next_tuesday_date():
    today = datetime.now()
    days_until_tuesday = (1 - today.weekday() + 7) % 7
    if days_until_tuesday == 0:
        days_until_tuesday = 7
    next_tuesday = today + timedelta(days=days_until_tuesday)
    return next_tuesday

# --- 1. 日次タスクページ（親ページ）の作成 ---
def create_daily_task_page(parent_id, target_date):
    page_title = target_date.strftime("%Y年%m月%d日") + " 火曜タスクと日報"

    url = NOTION_API_BASE_URL + "pages"
    data = {
        "parent": {"page_id": parent_id},
        "properties": {
            "title": {
                "title": [{"text": {"content": page_title}}]
            }
        }
    }

    response = requests.post(url, headers=HEADERS, data=json.dumps(data))
    if response.status_code == 200:
        print(f"✅ 火曜日のタスクページ '{page_title}' を作成しました。")
        return response.json()["id"]
    else:
        print(f"❌ 火曜日のタスクページの作成に失敗しました: {response.status_code} - {response.text}")
        print("エラー詳細:", response.text)
        return None

# --- 2. インラインデータベースと日報をページに追加 ---
def add_content_to_page(page_id, target_date):
    target_date_str = target_date.strftime("%Y年%m月%d日（%a）")
    
    url = NOTION_API_BASE_URL + f"blocks/{page_id}/children"
    data = {
        "children": [
            {
                "object": "block",
                "type": "heading_2",
                "heading_2": {
                    "rich_text": [{"type": "text", "text": {"content": "🗓️ 火曜日のタスクリスト"}}]
                }
            },
            {
                "object": "block",
                "type": "table",
                "table": {
                    "table_width": 6,
                    "has_column_header": True,
                    "has_row_header": False,
                    "children": [
                        { # ヘッダー行
                            "object": "block",
                            "type": "table_row",
                            "table_row": {
                                "cells": [
                                    [{"type": "text", "text": {"content": "時間帯"}}],
                                    [{"type": "text", "text": {"content": "タスク名"}}],
                                    [{"type": "text", "text": {"content": "タスク内容"}}],
                                    [{"type": "text", "text": {"content": "優先度"}}],
                                    [{"type": "text", "text": {"content": "進捗"}}],
                                    [{"type": "text", "text": {"content": "メモ"}}]
                                ]
                            }
                        },
                        { # デフォルトのタスク行 (ウォームアップ)
                            "object": "block",
                            "type": "table_row",
                            "table_row": {
                                "cells": [
                                    [{"type": "text", "text": {"content": "8:30 - 9:00"}}],
                                    [{"type": "text", "text": {"content": "ウォームアップ＆計画"}}],
                                    [{"type": "text", "text": {"content": ""}}],
                                    [{"type": "text", "text": {"content": "低"}}],
                                    [{"type": "text", "text": {"content": "未着手"}}],
                                    [{"type": "text", "text": {"content": ""}}]
                                ]
                            }
                        },
                        { # デフォルトのタスク行 (メイン作業例)
                            "object": "block",
                            "type": "table_row",
                            "table_row": {
                                "cells": [
                                    [{"type": "text", "text": {"content": "9:00 - 10:30"}}],
                                    [{"type": "text", "text": {"content": "Robloxアバター テクスチャリング集中"}}],
                                    [{"type": "text", "text": {"content": ""}}],
                                    [{"type": "text", "text": {"content": "高"}}],
                                    [{"type": "text", "text": {"content": "未着手"}}],
                                    [{"type": "text", "text": {"content": ""}}]
                                ]
                            }
                        },
                        { # デフォルトのタスク行 (クールダウン)
                            "object": "block",
                            "type": "table_row",
                            "table_row": {
                                "cells": [
                                    [{"type": "text", "text": {"content": "14:30 - 15:00"}}],
                                    [{"type": "text", "text": {"content": "クールダウン＆記録"}}],
                                    [{"type": "text", "text": {"content": ""}}],
                                    [{"type": "text", "text": {"content": "低"}}],
                                    [{"type": "text", "text": {"content": "未着手"}}],
                                    [{"type": "text", "text": {"content": ""}}]
                                ]
                            }
                        },
                    ]
                },
            },
            {
                "object": "block",
                "type": "divider",
                "divider": {}
            },
            # --- 日報の項目 ---
            {
                "object": "block",
                "type": "heading_2",
                "heading_2": {
                    "rich_text": [{"type": "text", "text": {"content": "📝 今日の日報"}}]
                }
            },
            {
                "object": "block",
                "type": "paragraph",
                "paragraph": {
                    "rich_text": [{"type": "text", "text": {"content": f"**日付：** {target_date_str}"}}]
                }
            },
            {
                "object": "block",
                "type": "heading_3",
                "heading_3": {
                    "rich_text": [{"type": "text", "text": {"content": "目標"}}]
                }
            },
            {
                "object": "block",
                "type": "bulleted_list_item",
                "bulleted_list_item": {
                    "rich_text": [{"type": "text", "text": {"content": ""}}]
                }
            },
            {
                "object": "block",
                "type": "heading_3",
                "heading_3": {
                    "rich_text": [{"type": "text", "text": {"content": "今日の「やったこと！」"}}]
                }
            },
            {
                "object": "block",
                "type": "bulleted_list_item",
                "bulleted_list_item": {
                    "rich_text": [{"type": "text", "text": {"content": ""}}]
                }
            },
            {
                "object": "block",
                "type": "heading_3",
                "heading_3": {
                    "rich_text": [{"type": "text", "text": {"content": "気づき・学び"}}]
                }
            },
            {
                "object": "block",
                "type": "paragraph",
                "paragraph": {
                    "rich_text": [{"type": "text", "text": {"content": ""}}]
                }
            },
            {
                "object": "block",
                "type": "heading_3",
                "heading_3": {
                    "rich_text": [{"type": "text", "text": {"content": "明日の予定"}}]
                }
            },
            {
                "object": "block",
                "type": "bulleted_list_item",
                "bulleted_list_item": {
                    "rich_text": [{"type": "text", "text": {"content": ""}}]
                }
            },
            {
                "object": "block",
                "type": "heading_3",
                "heading_3": {
                    "rich_text": [{"type": "text", "text": {"content": "気分・感想"}}]
                }
            },
            {
                "object": "block",
                "type": "paragraph",
                "paragraph": {
                    "rich_text": [{"type": "text", "text": {"content": ""}}]
                }
            }
        ]
    }
    response = requests.patch(url, headers=HEADERS, data=json.dumps(data))
    if response.status_code == 200:
        print("✅ ページ内にタスクリストと日報テンプレートを追加しました。")
    else:
        print(f"❌ ページコンテンツの追加に失敗しました: {response.status_code} - {response.text}")
        print("エラー詳細:", response.text)


# --- メイン処理 ---
if __name__ == "__main__":
    print("Notionページ作成を開始します。")
    
    # 次の火曜日の日付を計算
    target_tuesday = get_next_tuesday_date()
    print(f"ターゲット日: {target_tuesday.strftime('%Y年%m月%d日')}")

    daily_page_id = create_daily_task_page(NOTION_PARENT_PAGE_ID, target_tuesday)
    if daily_page_id:
        add_content_to_page(daily_page_id, target_tuesday)
        print("\n完了しました。Notionの親ページをご確認ください。")
        print("生成されたページの中に、タスクのテーブルと日報の項目があります。")
        print("--- 重要 ---")
        print("Notion APIの制限により、ページ内に自動生成されるテーブルは**シンプルなテーブルブロック**です。")
        print("データベースとしての機能（プロパティ、フィルター、ソートなど）を持たせるには、")
        print("このテーブルを**手動で「データベースに変換」**するか、")
        print("事前にフルページのデータベースを作成し、その日のタスクを**データベースの新しい項目として追加**する形式に変更する必要があります。")
