import requests
import json
from datetime import datetime, timedelta
import config

HEADERS = {
    "Authorization": f"Bearer {config.NOTION_API_KEY}",
    "Notion-Version": config.NOTION_API_VERSION,
    "Content-Type": "application/json",
}

def create_main_page(page_title, parent_page_id):
    url = f"{config.NOTION_API_BASE_URL}pages"
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
    url = f"{config.NOTION_API_BASE_URL}databases"
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
            "やるべきこと": {"rich_text": {}},
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
    # テンプレート用のデータ
    template_data = {
        "タスク名": "テンプレート - タスク名",
        "時間帯": "テンプレート - 時間帯",
        "最優先タスク？": False,
        "ステータス": "未着手",
        "達成度": "未評価",
        "やったこと！": "",
        "今日の達成感！": ""
    }

    # 週間スケジュールデータ
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

    start_date = datetime.strptime(config.START_DATE, "%Y-%m-%d")
    end_date = datetime.strptime(config.END_DATE, "%Y-%m-%d")
    
    current_date = start_date
    while current_date <= end_date:
        day_of_week_num = current_date.weekday()
        for task in weekly_schedule_data[day_of_week_num]:
            url = f"{config.NOTION_API_BASE_URL}pages"
            # テンプレートページの作成
            template_url = f"{config.NOTION_API_BASE_URL}pages"
            template_data = {
                "parent": {"database_id": database_id},
                "properties": {
                    "タスク名": {"title": [{"text": {"content": "テンプレート - タスク名"}}]},
                    "時間帯": {"select": {"name": "テンプレート - 時間帯"}},
                    "最優先タスク？": {"checkbox": False},
                    "ステータス": {"select": {"name": "未着手"}},
                    "達成度": {"select": {"name": "未評価"}},
                    "やったこと！": {"rich_text": []},
                    "今日の達成感！": {"rich_text": []}
                }
            }
            template_response = requests.post(template_url, headers=HEADERS, data=json.dumps(template_data))
            
            if template_response.status_code == 200:
                template_id = template_response.json()["id"]
                print("テンプレートページを作成しました。")
                
                # テンプレートをコピーして実際のタスクページを作成
                data = {
                    "parent": {"database_id": database_id},
                    "properties": {
                        "タスク名": {"title": [{"text": {"content": task["タスク名"]}}]},
                        "日付": {"date": {"start": current_date.isoformat()}},
                        "時間帯": {"select": {"name": task["時間帯"]}},
                        "最優先タスク？": {"checkbox": task["最優先タスク？"]},
                        "ステータス": {"select": {"name": "未着手"}},
                        "達成度": {"select": {"name": "未評価"}},
                        "やったこと！": {"rich_text": []},
                        "今日の達成感！": {"rich_text": []}
                    }
                }
            response = requests.post(url, headers=HEADERS, data=json.dumps(data))
            if response.status_code != 200:
                print(f"タスクの追加に失敗しました ({current_date.strftime('%Y-%m-%d')} {task['時間帯']} {task['タスク名']}): {response.status_code} - {response.text}")
            else:
                # テンプレートの日報テンプレートをコピー
                add_daily_report_template_to_page(template_id, "テンプレート - 日報")
                
                # 実際のタスクページを作成
                url = f"{config.NOTION_API_BASE_URL}pages"
                response = requests.post(url, headers=HEADERS, data=json.dumps(data))
                
                if response.status_code == 200:
                    page_id = response.json()["id"]
                    add_daily_report_template_to_page(page_id, current_date.strftime('%Y年%m月%d日（%a）'))
                print(f"タスクを追加しました: {current_date.strftime('%Y-%m-%d')} - {task['時間帯']} - {task['タスク名']}")
        current_date += timedelta(days=1)

def add_daily_report_template_to_page(page_id, date_str):
    url = f"{config.NOTION_API_BASE_URL}blocks/{page_id}/children"
    data = {
        "children": [
            {
                "object": "block",
                "type": "heading_2",
                "heading_2": {"rich_text": [{"type": "text", "text": {"content": "日報：今日の「やったこと！」と「達成感！」"}}]}
            },
            {
                "object": "block",
                "type": "paragraph",
                "paragraph": {"rich_text": [{"type": "text", "text": {"content": f"**日付：** {date_str}"}}]}
            },
            {
                "object": "block",
                "type": "divider",
                "divider": {}
            },
            {
                "object": "block",
                "type": "heading_3",
                "heading_3": {"rich_text": [{"type": "text", "text": {"content": "📝 今日の目標（事前に立てたもの）"}}]}
            },
            {
                "object": "block",
                "type": "bulleted_list_item",
                "bulleted_list_item": {"rich_text": [{"type": "text", "text": {"content": ""}}]}
            },
            {
                "object": "block",
                "type": "divider",
                "divider": {}
            },
            {
                "object": "block",
                "type": "heading_3",
                "heading_3": {"rich_text": [{"type": "text", "text": {"content": "✨ 今日、特に集中して取り組んだことは何ですか？"}}]}
            },
            {
                "object": "block",
                "type": "paragraph",
                "paragraph": {"rich_text": [{"type": "text", "text": {"content": ""}}]}
            },
            {
                "object": "block",
                "type": "divider",
                "divider": {}
            },
            {
                "object": "block",
                "type": "heading_3",
                "heading_3": {"rich_text": [{"type": "text", "text": {"content": "✅ 具体的に「できたこと！」は何ですか？"}}]}
            },
            {
                "object": "block",
                "type": "bulleted_list_item",
                "bulleted_list_item": {"rich_text": [{"type": "text", "text": {"content": ""}}]}
            },
            {
                "object": "block",
                "type": "divider",
                "divider": {}
            },
            {
                "object": "block",
                "type": "heading_3",
                "heading_3": {"rich_text": [{"type": "text", "text": {"content": "👍 今日の作業で、特に「よくできた！」と感じる点は何ですか？"}}]}
            },
            {
                "object": "block",
                "type": "paragraph",
                "paragraph": {"rich_text": [{"type": "text", "text": {"content": ""}}]}
            },
            {
                "object": "block",
                "type": "divider",
                "divider": {}
            },
            {
                "object": "block",
                "type": "heading_3",
                "heading_3": {"rich_text": [{"type": "text", "text": {"content": "💡 次に何をやるか？／今日の学び・気づき"}}]}
            },
            {
                "object": "block",
                "type": "paragraph",
                "paragraph": {"rich_text": [{"type": "text", "text": {"content": ""}}]}
            },
            {
                "object": "block",
                "type": "divider",
                "divider": {}
            },
            {
                "object": "block",
                "type": "heading_3",
                "heading_3": {"rich_text": [{"type": "text", "text": {"content": "😊 今日の気分・感想"}}]}
            },
            {
                "object": "block",
                "type": "paragraph",
                "paragraph": {"rich_text": [{"type": "text", "text": {"content": ""}}]}
            }
        ]
    }
    response = requests.patch(url, headers=HEADERS, data=json.dumps(data))
    if response.status_code != 200:
        print(f"日報テンプレートの追加に失敗しました ({page_id}): {response.status_code} - {response.text}")

def create_template_page(database_id):
    url = f"{config.NOTION_API_BASE_URL}pages"
    data = {
        "parent": {"database_id": database_id},
        "properties": {
            "タスク名": {
                "title": [{"text": {"content": "ウォームアップ＆計画(Mon)"}}]
            },
            "日付": {
                "date": {
                    "start": "2025-06-23T08:00:00+09:00"
                }
            },
            "時間帯": {
                "select": {"name": "8:00 - 9:00"}
            },
            "最優先タスク？": {"checkbox": False},
            "ステータス": {"select": {"name": "未着手"}},
            "達成度": {"select": {"name": "未評価"}},
            "やるべきこと": {
                "rich_text": [
                    {"text": {"content": "- 前日のBlenderファイル確認\n- 今日のモデリング目標設定\n- VibeCoding基礎復習（テキスト）\n- AIニュースチェック"}}
                ]
            },
            "メモ": {"rich_text": []}
        }
    }
    response = requests.post(url, headers=HEADERS, data=json.dumps(data))
    if response.status_code == 200:
        print("テンプレートページを作成しました。")
        return response.json()["id"]
    else:
        print(f"テンプレートページの作成に失敗しました: {response.status_code} - {response.text}")
        return None

if __name__ == "__main__":
    if not config.NOTION_API_KEY or not config.NOTION_PARENT_PAGE_ID:
        print("エラー: Notion APIキーまたは親ページIDが設定されていません。")
        print(".envファイルに以下の環境変数を設定してください：")
        print("NOTION_API_KEY=your_api_key_here")
        print("NOTION_PARENT_PAGE_ID=your_parent_page_id_here")
    else:
        print("Notionページとデータベースの自動生成を開始します。")
        main_page_id = create_main_page("2025年下半期 目標管理", config.NOTION_PARENT_PAGE_ID)
        if main_page_id:
            database_id = create_task_database(main_page_id)
            if database_id:
                print(f"\n作成されたデータベースID: {database_id}")
                template_id = create_template_page(database_id)
                if template_id:
                    print("\nテンプレートページが作成されました。Notionでご確認ください。")
                else:
                    print("テンプレートページの作成に失敗しました。")
            else:
                print("データベースの作成に失敗したため、テンプレートページの作成はスキップされました。")
        else:
            print("メインページの作成に失敗したため、データベースの作成はスキップされました。")
