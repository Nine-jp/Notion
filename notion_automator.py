import requests
import json
from datetime import datetime, timedelta
import os

# Notion APIの設定
NOTION_API_BASE_URL = "https://api.notion.com/v1/"

# Notion APIキーと親ページIDを直接設定
NOTION_API_KEY = "ntn_V5050303374bd0or47b7gcuiyix6d2xmglTyXP7KMQPcN6"
NOTION_PARENT_PAGE_ID = "21812d05838e808fbe3bd0340e7f6177"

HEADERS = {
    "Authorization": f"Bearer {NOTION_API_KEY}",
    "Notion-Version": "2022-06-28",
    "Content-Type": "application/json",
}

def create_main_page(page_title, parent_page_id):
    url = NOTION_API_BASE_URL + "pages"
    data = {
        "parent": {"page_id": parent_page_id},
        "properties": {
            "title": {
                "title": [{"text": {"content": page_title}}]
            }
        }
    }
    response = requests.post(url, headers=HEADERS, data=json.dumps(data))
    if response.status_code == 200:
        print(f"メインページ '{page_title}' を作成しました。")
        return response.json()["id"]
    else:
        print(f"メインページの作成に失敗しました: {response.status_code} - {response.text}")
        print("エラー詳細:", response.text)
        return None

def create_task_database(parent_page_id):
    url = NOTION_API_BASE_URL + "databases"
    data = {
        "parent": {"page_id": parent_page_id},
        "title": [{"text": {"content": "週間タスク管理"}}],
        "properties": {
            "タスク名": {"title": {}},
            "日付": {"date": {}},
            "時間帯": {
                "select": {
                    "options": [
                        {"name": "8:00 - 9:00", "color": "blue"},
                        {"name": "9:00 - 11:00", "color": "green"},
                        {"name": "11:00 - 12:30 (昼休憩)", "color": "gray"},
                        {"name": "12:30 - 14:30", "color": "purple"},
                        {"name": "14:30 - 15:30", "color": "yellow"}
                    ]
                }
            },
            "最優先タスク？": {"checkbox": {}},
            "ステータス": {
                "select": {
                    "options": [
                        {"name": "未着手", "color": "red"},
                        {"name": "進行中", "color": "orange"},
                        {"name": "完了", "color": "green"},
                        {"name": "保留", "color": "gray"}
                    ]
                }
            },
            "達成度": {
                "select": {
                    "options": [
                        {"name": "未評価", "color": "default"},
                        {"name": "☆ (0%)", "color": "red"},
                        {"name": "☆☆ (25%)", "color": "orange"},
                        {"name": "☆☆☆ (50%)", "color": "yellow"},
                        {"name": "☆☆☆☆ (75%)", "color": "blue"},
                        {"name": "☆☆☆☆☆ (100%)", "color": "green"}
                    ]
                }
            },
            "やったこと！": {"rich_text": {}},
            "今日の達成感！": {"rich_text": {}},
            "メモ": {"rich_text": {}}
        }
    }
    response = requests.post(url, headers=HEADERS, data=json.dumps(data))
    if response.status_code == 200:
        print("データベース '週間タスク管理' を作成しました。")
        return response.json()["id"]
    else:
        print(f"データベースの作成に失敗しました: {response.status_code} - {response.text}")
        print("エラー詳細:", response.text)
        return None

def add_weekly_schedule_and_daily_report(database_id):
    # 7月1日のみを生成
    current_date = datetime.strptime("2025-07-01", "%Y-%m-%d")
    day_of_week_num = current_date.weekday() # 0=月曜日, ..., 6=日曜日
    
    # 1日分のタスクを1ページにまとめる
    url = NOTION_API_BASE_URL + "pages"
    page_data = {
        "parent": {"database_id": database_id},
        "properties": {
            "タスク名": {
                "title": [{"text": {"content": f"{current_date.strftime('%Y年%m月%d日（%a）')}のスケジュール"}}]
            },
            "日付": {
                "date": {"start": current_date.isoformat()}
            },
            "時間帯": {"select": {"name": "--"}},
            "最優先タスク？": {"checkbox": False},
            "ステータス": {"select": {"name": "未着手"}},
            "達成度": {"select": {"name": "未評価"}},
            "やったこと！": {"rich_text": []},
            "今日の達成感！": {"rich_text": []}
        }
    }
    response = requests.post(url, headers=HEADERS, data=json.dumps(page_data))
    
    if response.status_code == 200:
        page_id = response.json()["id"]
        
        # ページに1日分のタスクをテーブル形式で追加
        url = NOTION_API_BASE_URL + f"blocks/{page_id}/children"
        tasks = weekly_schedule_data[day_of_week_num]
        
        # テーブルのヘッダーを追加
        blocks = [
            {
                "object": "block",
                "type": "heading_2",
                "heading_2": {
                    "rich_text": [{"text": {"content": f"{current_date.strftime('%Y年%m月%d日（%a）')}のスケジュール"}}]
                }
            },
            {
                "object": "block",
                "type": "table",
                "table": {
                    "table_width": 6,
                    "has_column_header": True,
                    "children": [
                        {
                            "object": "block",
                            "type": "table_row",
                            "table_row": {
                                "cells": [
                                    [{"text": {"content": "時間帯"}}],
                                    [{"text": {"content": "タスク名"}}],
                                    [{"text": {"content": "タスク内容"}}],
                                    [{"text": {"content": "優先度"}}],
                                    [{"text": {"content": "進捗"}}],
                                    [{"text": {"content": "メモ"}}]
                                ]
                            }
                        }
                    ]
                }
            }
        ]
        
        # テーブルの例を追加
        example_tasks = [
            {"時間帯": "8:30 - 9:00", "タスク名": "ウォームアップ", "タスク内容": "", "優先度": "低", "進捗": "未着手", "メモ": ""},
            {"時間帯": "9:00 - 10:30", "タスク名": "メイン作業A", "タスク内容": "", "優先度": "高", "進捗": "未着手", "メモ": ""},
            {"時間帯": "10:30 - 11:00", "タスク名": "休憩", "タスク内容": "", "優先度": "低", "進捗": "未着手", "メモ": ""},
            {"時間帯": "11:00 - 12:30", "タスク名": "メイン作業B", "タスク内容": "", "優先度": "中", "進捗": "未着手", "メモ": ""},
            {"時間帯": "12:30 - 13:00", "タスク名": "クールダウン", "タスク内容": "", "優先度": "低", "進捗": "未着手", "メモ": ""}
        ]
        
        # 各タスクをテーブルに追加
        for task in example_tasks:
            blocks.append({
                "object": "block",
                "type": "table_row",
                "table_row": {
                    "cells": [
                        [{"text": {"content": task["時間帯"]}}],
                        [{"text": {"content": task["タスク名"]}}],
                        [{"text": {"content": task["タスク内容"]}}],
                        [{"text": {"content": task["優先度"]}}],
                        [{"text": {"content": task["進捗"]}}],
                        [{"text": {"content": task["メモ"]}}]
                    ]
                }
            })
        
        # 日報テンプレートを追加
        blocks.extend([
            {
                "object": "block",
                "type": "divider",
                "divider": {}
            },
            {
                "object": "block",
                "type": "heading_2",
                "heading_2": {
                    "rich_text": [{"text": {"content": "日報：今日の「やったこと！」と「達成感！」"}}]
                }
            },
            {
                "object": "block",
                "type": "heading_3",
                "heading_3": {
                    "rich_text": [{"text": {"content": "📝 今日の目標（事前に立てたもの）"}}]
                }
            },
            {
                "object": "block",
                "type": "bulleted_list_item",
                "bulleted_list_item": {
                    "rich_text": [{"text": {"content": ""}}]
                }
            },
            {
                "object": "block",
                "type": "heading_3",
                "heading_3": {
                    "rich_text": [{"text": {"content": "✨ 今日、特に集中して取り組んだことは何ですか？"}}]
                }
            },
            {
                "object": "block",
                "type": "paragraph",
                "paragraph": {
                    "rich_text": [{"text": {"content": ""}}]
                }
            },
            {
                "object": "block",
                "type": "heading_3",
                "heading_3": {
                    "rich_text": [{"text": {"content": "✅ 具体的に「できたこと！」は何ですか？"}}]
                }
            },
            {
                "object": "block",
                "type": "bulleted_list_item",
                "bulleted_list_item": {
                    "rich_text": [{"text": {"content": ""}}]
                }
            },
            {
                "object": "block",
                "type": "heading_3",
                "heading_3": {
                    "rich_text": [{"text": {"content": "👍 今日の作業で、特に「よくできた！」と感じる点は何ですか？"}}]
                }
            },
            {
                "object": "block",
                "type": "paragraph",
                "paragraph": {
                    "rich_text": [{"text": {"content": ""}}]
                }
            },
            {
                "object": "block",
                "type": "heading_3",
                "heading_3": {
                    "rich_text": [{"text": {"content": "💡 次に何をやるか？／今日の学び・気づき"}}]
                }
            },
            {
                "object": "block",
                "type": "paragraph",
                "paragraph": {
                    "rich_text": [{"text": {"content": ""}}]
                }
            },
            {
                "object": "block",
                "type": "heading_3",
                "heading_3": {
                    "rich_text": [{"text": {"content": "😊 今日の気分・感想"}}]
                }
            },
            {
                "object": "block",
                "type": "paragraph",
                "paragraph": {
                    "rich_text": [{"text": {"content": ""}}]
                }
            }
        ])
        
        response = requests.patch(url, headers=HEADERS, data=json.dumps({"children": blocks}))
        if response.status_code != 200:
            print(f"ページのコンテンツ追加に失敗しました ({current_date.strftime('%Y-%m-%d')}): {response.status_code} - {response.text}")
        else:
            print(f"{current_date.strftime('%Y-%m-%d')}のページを追加しました")
    else:
        print(f"ページの作成に失敗しました ({current_date.strftime('%Y-%m-%d')}): {response.status_code} - {response.text}")

# --- メイン処理 ---
if __name__ == "__main__":
    if NOTION_API_KEY is None or NOTION_PARENT_PAGE_ID is None:
        print("エラー: Notion APIキーまたは親ページIDが設定されていません。")
        print("環境変数に NOTION_API_KEY と NOTION_PARENT_PAGE_ID を設定してください。")
    else:
        print("Notionページとデータベースの自動生成を開始します。")
        main_page_id = create_main_page("2025年下半期 目標管理", NOTION_PARENT_PAGE_ID)
        if main_page_id:
            database_id = create_task_database(main_page_id)
            if database_id:
                print(f"\n作成されたデータベースID: {database_id}")
                print("7月1日のスケジュールと日報テンプレートをデータベースに追加中です...")
                add_weekly_schedule_and_daily_report(database_id)
                print("\n7月1日のスケジュールと日報テンプレートの追加を試行しました。Notionでご確認ください。")
                print("\n--- Notionでの推奨設定 ---")
                print("1. 「週間タスク管理」データベースを開き、新しいビューで「カレンダー」を選択してください。")
                print("2. カレンダービューの右上の「...」メニューから「グループ」を選択し、「時間帯」でグループ化すると時間割形式になります。")
                print("3. 「達成度」プロパティで、各タスクの達成度を視覚的に追うことができます。")
                print("4. 月別・週別の確認には、カレンダービューやデータベースのフィルター・ソート機能をご活用ください。")
            else:
                print("データベースの作成に失敗したため、スケジュールと日報の追加はスキップされました。")
        else:
            print("メインページの作成に失敗したため、データベースの作成はスキップされました。")
    
    weekly_schedule_data = {
        0: [ # 月曜日
            {"時間帯": "8:00 - 9:00", "タスク名": "ウォームアップ＆計画", "最優先タスク？": False},
            {"時間帯": "9:00 - 11:00", "タスク名": "Robloxアバター モデリング集中", "最優先タスク？": True},
            {"時間帯": "11:00 - 12:30 (昼休憩)", "タスク名": "昼休憩", "最優先タスク？": False},
            {"時間帯": "12:30 - 14:30", "タスク名": "Blender取説", "最優先タスク？": False},
            {"時間帯": "14:30 - 15:30", "タスク名": "クールダウン＆記録", "最優先タスク？": False}
        ],
        1: [ # 火曜日
            {"時間帯": "8:00 - 9:00", "タスク名": "ウォームアップ＆計画", "最優先タスク？": False},
            {"時間帯": "9:00 - 11:00", "タスク名": "Robloxアバター テクスチャリング集中", "最優先タスク？": True},
            {"時間帯": "11:00 - 12:30 (昼休憩)", "タスク名": "昼休憩", "最優先タスク？": False},
            {"時間帯": "12:30 - 14:30", "タスク名": "Blender取説＆投資の勉強", "最優先タスク？": False},
            {"時間帯": "14:30 - 15:30", "タスク名": "クールダウン＆記録", "最優先タスク？": False}
        ],
        2: [ # 水曜日
            {"時間帯": "8:00 - 9:00", "タスク名": "オフ", "最優先タスク？": False},
            {"時間帯": "9:00 - 11:00", "タスク名": "オフ", "最優先タスク？": False},
            {"時間帯": "11:00 - 12:30 (昼休憩)", "タスク名": "オフ", "最優先タスク？": False},
            {"時間帯": "12:30 - 14:30", "タスク名": "オフ", "最優先タスク？": False},
            {"時間帯": "14:30 - 15:30", "タスク名": "オフ", "最優先タスク？": False}
        ],
        3: [ # 木曜日
            {"時間帯": "8:00 - 9:00", "タスク名": "ウォームアップ＆計画", "最優先タスク？": False},
            {"時間帯": "9:00 - 11:00", "タスク名": "Robloxアバター リギング・インポート集中", "最優先タスク？": True},
            {"時間帯": "11:00 - 12:30 (昼休憩)", "タスク名": "昼休憩", "最優先タスク？": False},
            {"時間帯": "12:30 - 14:30", "タスク名": "Roblox Studioインポート＆投資の勉強", "最優先タスク？": False},
            {"時間帯": "14:30 - 15:30", "タスク名": "クールダウン＆記録", "最優先タスク？": False}
        ],
        4: [ # 金曜日
            {"時間帯": "8:00 - 9:00", "タスク名": "ウォームアップ＆計画", "最優先タスク？": False},
            {"時間帯": "9:00 - 11:00", "タスク名": "VibeCoding基礎集中", "最優先タスク？": True},
            {"時間帯": "11:00 - 12:30 (昼休憩)", "タスク名": "昼休憩", "最優先タスク？": False},
            {"時間帯": "12:30 - 14:30", "タスク名": "AIの勉強", "最優先タスク？": False},
            {"時間帯": "14:30 - 15:30", "タスク名": "クールダウン＆記録", "最優先タスク？": False}
        ],
        5: [ # 土曜日
            {"時間帯": "8:00 - 9:00", "タスク名": "ウォームアップ＆計画", "最優先タスク？": False},
            {"時間帯": "9:00 - 11:00", "タスク名": "ポテトくんゲームアイデア出し", "最優先タスク？": True},
            {"時間帯": "11:00 - 12:30 (昼休憩)", "タスク名": "昼休憩", "最優先タスク？": False},
            {"時間帯": "12:30 - 14:30", "タスク名": "Robloxアクセサリー作成練習", "最優先タスク？": False},
            {"時間帯": "14:30 - 15:30", "タスク名": "クールダウン＆週次レビュー", "最優先タスク？": False}
        ],
        6: [ # 日曜日
            {"時間帯": "8:00 - 9:00", "タスク名": "オフ", "最優先タスク？": False},
            {"時間帯": "9:00 - 11:00", "タスク名": "オフ", "最優先タスク？": False},
            {"時間帯": "11:00 - 12:30 (昼休憩)", "タスク名": "オフ", "最優先タスク？": False},
            {"時間帯": "12:30 - 14:30", "タスク名": "オフ", "最優先タスク？": False},
            {"時間帯": "14:30 - 15:30", "タスク名": "オフ", "最優先タスク？": False}
        ]
    }

    current_date = start_date
    while current_date <= end_date:
        day_of_week_num = current_date.weekday() # 0=月曜日, ..., 6=日曜日
        
        # 1日分のタスクを1ページにまとめる
        url = NOTION_API_BASE_URL + "pages"
        page_data = {
            "parent": {"database_id": database_id},
            "properties": {
                "タスク名": {
                    "title": [{"text": {"content": f"{current_date.strftime('%Y年%m月%d日（%a）')}のスケジュール"}}]
                },
                "日付": {
                    "date": {"start": current_date.isoformat()}
                },
                "時間帯": {"select": {"name": "--"}},
                "最優先タスク？": {"checkbox": False},
                "ステータス": {"select": {"name": "未着手"}},
                "達成度": {"select": {"name": "未評価"}},
                "やったこと！": {"rich_text": []},
                "今日の達成感！": {"rich_text": []}
            }
        }
        response = requests.post(url, headers=HEADERS, data=json.dumps(page_data))
        
        if response.status_code == 200:
            page_id = response.json()["id"]
            
            # ページに1日分のタスクをテーブル形式で追加
            url = NOTION_API_BASE_URL + f"blocks/{page_id}/children"
            tasks = weekly_schedule_data[day_of_week_num]
            
            blocks = [
                {
                    "object": "block",
                    "type": "heading_2",
                    "heading_2": {
                        "rich_text": [{"text": {"content": f"{current_date.strftime('%Y年%m月%d日（%a）')}のスケジュール"}}]
                    }
                },
                {
                    "object": "block",
                    "type": "table",
                    "table": {
                        "table_width": 4,
                        "has_column_header": True,
                        "children": [
                            {
                                "object": "block",
                                "type": "table_row",
                                "table_row": {
                                    "cells": [
                                        [{"text": {"content": "時間帯"}}],
                                        [{"text": {"content": "タスク名"}}],
                                        [{"text": {"content": "最優先タスク？"}}],
                                        [{"text": {"content": "ステータス"}}]
                                    ]
                                }
                            }
                        ]
                    }
                }
            ]
            
            # 各タスクをテーブルに追加
            for task in tasks:
                blocks.append({
                    "object": "block",
                    "type": "table_row",
                    "table_row": {
                        "cells": [
                            [{"text": {"content": task["時間帯"]}}],
                            [{"text": {"content": task["タスク名"]}}],
                            [{"text": {"content": "はい" if task["最優先タスク？"] else "いいえ"}}],
                            [{"text": {"content": "未着手"}}]
                        ]
                    }
                })
            
            # 日報テンプレートを追加
            blocks.extend([
                {
                    "object": "block",
                    "type": "divider",
                    "divider": {}
                },
                {
                    "object": "block",
                    "type": "heading_2",
                    "heading_2": {
                        "rich_text": [{"text": {"content": "日報：今日の「やったこと！」と「達成感！」"}}]
                    }
                },
                {
                    "object": "block",
                    "type": "heading_3",
                    "heading_3": {
                        "rich_text": [{"text": {"content": "📝 今日の目標（事前に立てたもの）"}}]
                    }
                },
                {
                    "object": "block",
                    "type": "bulleted_list_item",
                    "bulleted_list_item": {
                        "rich_text": [{"text": {"content": ""}}]
                    }
                },
                {
                    "object": "block",
                    "type": "heading_3",
                    "heading_3": {
                        "rich_text": [{"text": {"content": "✨ 今日、特に集中して取り組んだことは何ですか？"}}]
                    }
                },
                {
                    "object": "block",
                    "type": "paragraph",
                    "paragraph": {
                        "rich_text": [{"text": {"content": ""}}]
                    }
                },
                {
                    "object": "block",
                    "type": "heading_3",
                    "heading_3": {
                        "rich_text": [{"text": {"content": "✅ 具体的に「できたこと！」は何ですか？"}}]
                    }
                },
                {
                    "object": "block",
                    "type": "bulleted_list_item",
                    "bulleted_list_item": {
                        "rich_text": [{"text": {"content": ""}}]
                    }
                },
                {
                    "object": "block",
                    "type": "heading_3",
                    "heading_3": {
                        "rich_text": [{"text": {"content": "👍 今日の作業で、特に「よくできた！」と感じる点は何ですか？"}}]
                    }
                },
                {
                    "object": "block",
                    "type": "paragraph",
                    "paragraph": {
                        "rich_text": [{"text": {"content": ""}}]
                    }
                },
                {
                    "object": "block",
                    "type": "heading_3",
                    "heading_3": {
                        "rich_text": [{"text": {"content": "💡 次に何をやるか？／今日の学び・気づき"}}]
                    }
                },
                {
                    "object": "block",
                    "type": "paragraph",
                    "paragraph": {
                        "rich_text": [{"text": {"content": ""}}]
                    }
                },
                {
                    "object": "block",
                    "type": "heading_3",
                    "heading_3": {
                        "rich_text": [{"text": {"content": "😊 今日の気分・感想"}}]
                    }
                },
                {
                    "object": "block",
                    "type": "paragraph",
                    "paragraph": {
                        "rich_text": [{"text": {"content": ""}}]
                    }
                }
            ])
            
            response = requests.patch(url, headers=HEADERS, data=json.dumps({"children": blocks}))
            if response.status_code != 200:
                print(f"ページのコンテンツ追加に失敗しました ({current_date.strftime('%Y-%m-%d')}): {response.status_code} - {response.text}")
            else:
                print(f"{current_date.strftime('%Y-%m-%d')}のページを追加しました")
        else:
            print(f"ページの作成に失敗しました ({current_date.strftime('%Y-%m-%d')}): {response.status_code} - {response.text}")

        current_date += timedelta(days=1)

def add_daily_report_template_to_page(page_id, date_str):
    url = NOTION_API_BASE_URL + f"blocks/{page_id}/children"
    data = {
        "children": [
            {
                "object": "block",
                "type": "heading_2",
                "heading_2": {
                    "rich_text": [{"type": "text", "text": {"content": "日報：今日の「やったこと！」と「達成感！」"}}],
                    "color": "default"
                }
            },
            {
                "object": "block",
                "type": "paragraph",
                "paragraph": {
                    "rich_text": [{"type": "text", "text": {"content": f"**日付：** {date_str}"}}]
                }
            },
            {
                "object": "block",
                "type": "divider",
                "divider": {}
            },
            {
                "object": "block",
                "type": "heading_3",
                "heading_3": {
                    "rich_text": [{"type": "text", "text": {"content": "📝 今日の目標（事前に立てたもの）"}}]
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
                "type": "divider",
                "divider": {}
            },
            {
                "object": "block",
                "type": "heading_3",
                "heading_3": {
                    "rich_text": [{"type": "text", "text": {"content": "✨ 今日、特に集中して取り組んだことは何ですか？"}}]
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
                "type": "divider",
                "divider": {}
            },
            {
                "object": "block",
                "type": "heading_3",
                "heading_3": {
                    "rich_text": [{"type": "text", "text": {"content": "✅ 具体的に「できたこと！」は何ですか？"}}]
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
                "type": "divider",
                "divider": {}
            },
            {
                "object": "block",
                "type": "heading_3",
                "heading_3": {
                    "rich_text": [{"type": "text", "text": {"content": "👍 今日の作業で、特に「よくできた！」と感じる点は何ですか？"}}]
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
                "type": "divider",
                "divider": {}
            },
            {
                "object": "block",
                "type": "heading_3",
                "heading_3": {
                    "rich_text": [{"type": "text", "text": {"content": "💡 次に何をやるか？／今日の学び・気づき"}}]
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
                "type": "divider",
                "divider": {}
            },
            {
                "object": "block",
                "type": "heading_3",
                "heading_3": {
                    "rich_text": [{"type": "text", "text": {"content": "😊 今日の気分・感想"}}]
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
    if response.status_code != 200:
        print(f"日報テンプレートの追加に失敗しました ({page_id}): {response.status_code} - {response.text}")

if __name__ == "__main__":
    if NOTION_API_KEY is None or NOTION_PARENT_PAGE_ID is None:
        print("エラー: Notion APIキーまたは親ページIDが設定されていません。")
        print("環境変数に NOTION_API_KEY と NOTION_PARENT_PAGE_ID を設定してください。")
    else:
        print("Notionページとデータベースの自動生成を開始します。")
        main_page_id = create_main_page("2025年下半期 目標管理", NOTION_PARENT_PAGE_ID)
        if main_page_id:
            database_id = create_task_database(main_page_id)
            if database_id:
                print(f"\n作成されたデータベースID: {database_id}")
                print("2025年下半期のスケジュールと日報テンプレートをデータベースに追加中です。")
                print("項目数が多いため、完了まで数分かかる場合があります。しばらくお待ちください...")
                add_weekly_schedule_and_daily_report(database_id)
                print("\nすべてのスケジュールと日報テンプレートの追加を試行しました。Notionでご確認ください。")
                print("\n--- Notionでの推奨設定 ---")
                print("1. 「週間タスク管理」データベースを開き、新しいビューで「カレンダー」を選択してください。")
                print("2. カレンダービューの右上の「...」メニューから「グループ」を選択し、「時間帯」でグループ化すると時間割形式になります。")
                print("3. 「達成度」プロパティで、各タスクの達成度を視覚的に追うことができます。")
                print("4. 月別・週別の確認には、カレンダービューやデータベースのフィルター・ソート機能をご活用ください。")
            else:
                print("データベースの作成に失敗したため、スケジュールと日報の追加はスキップされました。")
        else:
            print("メインページの作成に失敗したため、データベースの作成はスキップされました。")
