import requests
import json
from datetime import datetime, timedelta
import sys
import os
from dotenv import load_dotenv

# 環境変数の読み込み
load_dotenv()

# Notion APIの設定
NOTION_API_KEY = os.getenv("NOTION_API_KEY")
NOTION_PARENT_PAGE_ID = os.getenv("NOTION_PARENT_PAGE_ID")
NOTION_API_VERSION = "2022-06-28"
NOTION_API_BASE_URL = "https://api.notion.com/v1/"

# 週間スケジュールデータ
WEEKLY_SCHEDULE_DATA = {
    0: [  # 月曜日
        {
            "time_slot": "8:00 - 9:00",
            "title": "ウォームアップ＆計画",
            "priority": "中",
            "todo_notes": "- 前日のBlenderファイル確認\n- 今日のモデリング目標設定\n- VibeCoding基礎復習（テキスト）\n- AIニュースチェック",
            "memo": ""
        },
        {
            "time_slot": "9:00 - 10:00",
            "title": "Robloxアバター作成1",
            "priority": "高",
            "todo_notes": "- ポテトくんの胴体・頭の基本形状をBlenderで作成（動画チュートリアル）",
            "memo": ""
        },
        {
            "time_slot": "10:00 - 11:00",
            "title": "Robloxアバター作成2",
            "priority": "中",
            "todo_notes": "- 次のステップ: 細部のモデリングへ進む準備",
            "memo": ""
        },
        {
            "time_slot": "11:00 - 12:30 (昼休憩)",
            "title": "昼休憩",
            "priority": "中",
            "todo_notes": "",
            "memo": ""
        },
        {
            "time_slot": "12:30 - 14:30",
            "title": "Blender取説",
            "priority": "中",
            "todo_notes": "- Roblox向けモデリングの注意点（ポリゴン数削減、エラーチェック）の基礎（動画チュートリアル）\n- 次のステップ: テクスチャリングの基礎知識",
            "memo": ""
        },
        {
            "time_slot": "14:30 - 15:30",
            "title": "クールダウン＆記録",
            "priority": "中",
            "todo_notes": "- 今日の作業を振り返る\n- 今日の達成感！記録（写真/メモ）\n- 明日やること整理",
            "memo": "やったこと 例: Blenderでポテトくんの胴体と頭のベースモデルを完成させた"
        }
    ],
    1: [  # 火曜日
        {
            "time_slot": "8:00 - 9:00",
            "title": "ウォームアップ＆計画",
            "priority": "中",
            "todo_notes": "- 前日のBlenderファイル確認\n- 今日のモデリング目標設定\n- VibeCoding基礎復習（テキスト）\n- AIニュースチェック",
            "memo": ""
        },
        {
            "time_slot": "9:00 - 10:00",
            "title": "Robloxアバター作成1",
            "priority": "高",
            "todo_notes": "- ポテトくんの胴体・頭の基本形状をBlenderで作成（動画チュートリアル）",
            "memo": ""
        },
        {
            "time_slot": "10:00 - 11:00",
            "title": "Robloxアバター作成2",
            "priority": "中",
            "todo_notes": "- 次のステップ: 細部のモデリングへ進む準備",
            "memo": ""
        },
        {
            "time_slot": "11:00 - 12:30 (昼休憩)",
            "title": "昼休憩",
            "priority": "中",
            "todo_notes": "",
            "memo": ""
        },
        {
            "time_slot": "12:30 - 14:30",
            "title": "Blender取説＆投資の勉強",
            "priority": "中",
            "todo_notes": "- Roblox向けモデリングの注意点（ポリゴン数削減、エラーチェック）の基礎（動画チュートリアル）\n- 次のステップ: テクスチャリングの基礎知識\n- 投資の基本概念の学習",
            "memo": ""
        },
        {
            "time_slot": "14:30 - 15:30",
            "title": "クールダウン＆記録",
            "priority": "中",
            "todo_notes": "- 今日の作業を振り返る\n- 今日の達成感！記録（写真/メモ）\n- 明日やること整理",
            "memo": "やったこと 例: Blenderでポテトくんの胴体と頭のベースモデルを完成させた"
        }
    ],
    2: [  # 水曜日
        {
            "time_slot": "8:00 - 9:00",
            "title": "オフ",
            "priority": "中",
            "todo_notes": "- 休息とリフレッシュ",
            "memo": ""
        },
        {
            "time_slot": "9:00 - 11:00",
            "title": "オフ",
            "priority": "中",
            "todo_notes": "- 休息とリフレッシュ",
            "memo": ""
        },
        {
            "time_slot": "11:00 - 12:30 (昼休憩)",
            "title": "オフ",
            "priority": "中",
            "todo_notes": "- 休息とリフレッシュ",
            "memo": ""
        },
        {
            "time_slot": "12:30 - 14:30",
            "title": "オフ",
            "priority": "中",
            "todo_notes": "- 休息とリフレッシュ",
            "memo": ""
        },
        {
            "time_slot": "14:30 - 15:30",
            "title": "オフ",
            "priority": "中",
            "todo_notes": "- 休息とリフレッシュ",
            "memo": ""
        }
    ],
    3: [  # 木曜日
        {
            "time_slot": "8:00 - 9:00",
            "title": "ウォームアップ＆計画",
            "priority": "中",
            "todo_notes": "- 前日のBlenderファイル確認\n- 今日のモデリング目標設定\n- VibeCoding基礎復習（テキスト）\n- AIニュースチェック",
            "memo": ""
        },
        {
            "time_slot": "9:00 - 10:00",
            "title": "Robloxアバター作成1",
            "priority": "高",
            "todo_notes": "- ポテトくんの胴体・頭の基本形状をBlenderで作成（動画チュートリアル）",
            "memo": ""
        },
        {
            "time_slot": "10:00 - 11:00",
            "title": "Robloxアバター作成2",
            "priority": "中",
            "todo_notes": "- 次のステップ: 細部のモデリングへ進む準備",
            "memo": ""
        },
        {
            "time_slot": "11:00 - 12:30 (昼休憩)",
            "title": "昼休憩",
            "priority": "中",
            "todo_notes": "",
            "memo": ""
        },
        {
            "time_slot": "12:30 - 14:30",
            "title": "Roblox Studioインポート＆投資の勉強",
            "priority": "中",
            "todo_notes": "- Roblox Studioでのインポート手順の学習\n- 投資の基本概念の学習",
            "memo": ""
        },
        {
            "time_slot": "14:30 - 15:30",
            "title": "クールダウン＆記録",
            "priority": "中",
            "todo_notes": "- 今日の作業を振り返る\n- 今日の達成感！記録（写真/メモ）\n- 明日やること整理",
            "memo": "やったこと 例: Blenderでポテトくんの胴体と頭のベースモデルを完成させた"
        }
    ],
    4: [  # 金曜日
        {
            "time_slot": "8:00 - 9:00",
            "title": "ウォームアップ＆計画",
            "priority": "中",
            "todo_notes": "- 前日のBlenderファイル確認\n- 今日のモデリング目標設定\n- VibeCoding基礎復習（テキスト）\n- AIニュースチェック",
            "memo": ""
        },
        {
            "time_slot": "9:00 - 10:00",
            "title": "Robloxアバター作成1",
            "priority": "高",
            "todo_notes": "- ポテトくんの胴体・頭の基本形状をBlenderで作成（動画チュートリアル）",
            "memo": ""
        },
        {
            "time_slot": "10:00 - 11:00",
            "title": "Robloxアバター作成2",
            "priority": "中",
            "todo_notes": "- 次のステップ: 細部のモデリングへ進む準備",
            "memo": ""
        },
        {
            "time_slot": "11:00 - 12:30 (昼休憩)",
            "title": "昼休憩",
            "priority": "中",
            "todo_notes": "",
            "memo": ""
        },
        {
            "time_slot": "12:30 - 14:30",
            "title": "AIの勉強",
            "priority": "中",
            "todo_notes": "- AIの基本概念の学習\n- 投資の基本概念の学習",
            "memo": ""
        },
        {
            "time_slot": "14:30 - 15:30",
            "title": "クールダウン＆記録",
            "priority": "中",
            "todo_notes": "- 今日の作業を振り返る\n- 今日の達成感！記録（写真/メモ）\n- 明日やること整理",
            "memo": "やったこと 例: Blenderでポテトくんの胴体と頭のベースモデルを完成させた"
        }
    ],
    5: [  # 土曜日
        {
            "time_slot": "8:00 - 9:00",
            "title": "ウォームアップ＆計画",
            "priority": "中",
            "todo_notes": "- 前日のBlenderファイル確認\n- 今日のモデリング目標設定\n- VibeCoding基礎復習（テキスト）\n- AIニュースチェック",
            "memo": ""
        },
        {
            "time_slot": "9:00 - 10:00",
            "title": "ポテトくんゲームアイデア出し",
            "priority": "高",
            "todo_notes": "- ポテトくんゲームのコンセプト作成\n- ゲームの基本ルールの設計",
            "memo": ""
        },
        {
            "time_slot": "10:00 - 11:00",
            "title": "Robloxアクセサリー作成練習",
            "priority": "中",
            "todo_notes": "- Robloxアクセサリーの基本作成方法の学習\n- アクセサリーのインポート手順の確認",
            "memo": ""
        },
        {
            "time_slot": "11:00 - 12:30 (昼休憩)",
            "title": "昼休憩",
            "priority": "中",
            "todo_notes": "",
            "memo": ""
        },
        {
            "time_slot": "12:30 - 14:30",
            "title": "Robloxアクセサリー作成練習",
            "priority": "中",
            "todo_notes": "- Robloxアクセサリーの基本作成方法の学習\n- アクセサリーのインポート手順の確認",
            "memo": ""
        },
        {
            "time_slot": "14:30 - 15:30",
            "title": "クールダウン＆週次レビュー",
            "priority": "中",
            "todo_notes": "- 1週間の作業を振り返る\n- 今週の達成感！記録（写真/メモ）\n- 来週やること整理",
            "memo": "やったこと 例: Blenderでポテトくんの胴体と頭のベースモデルを完成させた"
        }
    ],
    6: [  # 日曜日
        {
            "time_slot": "8:00 - 9:00",
            "title": "オフ",
            "priority": "中",
            "todo_notes": "- 休息とリフレッシュ",
            "memo": ""
        },
        {
            "time_slot": "9:00 - 11:00",
            "title": "オフ",
            "priority": "中",
            "todo_notes": "- 休息とリフレッシュ",
            "memo": ""
        },
        {
            "time_slot": "11:00 - 12:30 (昼休憩)",
            "title": "オフ",
            "priority": "中",
            "todo_notes": "- 休息とリフレッシュ",
            "memo": ""
        },
        {
            "time_slot": "12:30 - 14:30",
            "title": "オフ",
            "priority": "中",
            "todo_notes": "- 休息とリフレッシュ",
            "memo": ""
        },
        {
            "time_slot": "14:30 - 15:30",
            "title": "オフ",
            "priority": "中",
            "todo_notes": "- 休息とリフレッシュ",
            "memo": ""
        }
    ]
}

HEADERS = {
    "Authorization": f"Bearer {NOTION_API_KEY}",
    "Notion-Version": NOTION_API_VERSION,
    "Content-Type": "application/json",
}

def create_main_page(parent_page_id):
    url = f"{NOTION_API_BASE_URL}pages"
    data = {
        "parent": {"page_id": parent_page_id},
        "properties": {
            "title": [{"text": {"content": "タスク管理ページ"}}]
        }
    }
    response = requests.post(url, headers=HEADERS, json=data)
    if response.status_code == 200:
        print("メインページが作成されました")
        return response.json()["id"]
    else:
        print(f"メインページの作成に失敗しました: {response.status_code} - {response.text}")
        print("エラー詳細:", response.text)
        return None

def create_task_database(parent_page_id):
    url = f"{NOTION_API_BASE_URL}databases"
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
                        {"name": "9:00 - 10:00", "color": "green"},
                        {"name": "10:00 - 11:00", "color": "green"},
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
    print("データベースのプロパティ定義:")
    print("----------------------------------------")
    print(f"タスク名: {data['properties']['タスク名']}")
    print(f"日付: {data['properties']['日付']}")
    print(f"時間帯: {data['properties']['時間帯']}")
    print(f"最優先タスク？: {data['properties']['最優先タスク？']}")
    print(f"ステータス: {data['properties']['ステータス']}")
    print(f"達成度: {data['properties']['達成度']}")
    print(f"やるべきこと: {data['properties']['やるべきこと']}")
    print(f"メモ: {data['properties']['メモ']}")
    print("----------------------------------------")
    response = requests.post(url, headers=HEADERS, json=data)
    if response.status_code == 200:
        print("データベース '週間タスク管理' を作成しました。")
        return response.json()["id"]
    else:
        print(f"データベースの作成に失敗しました: {response.status_code} - {response.text}")
        print("エラー詳細:", response.text)
        return None



def create_monday_pages(database_id):
    try:
        # 8:00 - 9:00 ウォームアップ＆計画
        create_template_page(database_id, "ウォームアップ＆計画(Mon)", "8:00 - 9:00", "- 前日のBlenderファイル確認\n- 今日のモデリング目標設定\n- VibeCoding基礎復習（テキスト）\n- AIニュースチェック", "", "8:00")
        
        # 9:00 - 10:00 Robloxアバター作成
        create_template_page(database_id, "Robloxアバター作成1(Mon)", "9:00 - 10:00", "- ポテトくんの胴体・頭の基本形状をBlenderで作成（動画チュートリアル）", "", "9:00")
        
        # 10:00 - 11:00 Robloxアバター作成
        create_template_page(database_id, "Robloxアバター作成2(Mon)", "10:00 - 11:00", "- 次のステップ: 細部のモデリングへ進む準備", "", "10:00")
        
        # 11:00 - 12:30 昼休憩
        create_template_page(database_id, "昼休憩(Mon)", "11:00 - 12:30 (昼休憩)", "", "", "11:00")
        
        # 12:30 - 14:30 Blender取説
        create_template_page(database_id, "Blender取説(Mon)", "12:30 - 14:30", "- Roblox向けモデリングの注意点（ポリゴン数削減、エラーチェック）の基礎（動画チュートリアル）\n- 次のステップ: テクスチャリングの基礎知識", "", "12:30")
        
        # 14:30 - 15:30 クールダウン＆記録
        create_template_page(database_id, "クールダウン＆記録(Mon)", "14:30 - 15:30", "- 今日の作業を振り返る\n- 今日の達成感！記録（写真/メモ）\n- 明日やること整理", "やったこと 例: Blenderでポテトくんの胴体と頭のベースモデルを完成させた", "14:30")
    except Exception as e:
        print(f"\nエラーが発生しました: {str(e)}")
        return None

def create_task_page_with_report(database_id, task, current_date):
    try:
        # タスクの詳細を取得
        title = task.get("title", "")
        time_slot = task.get("time_slot", "")
        todo_notes = task.get("todo_notes", "")
        memo = task.get("memo", "")
        priority = task.get("priority", "")
        
        # タスクページの作成
        url = f"{NOTION_API_BASE_URL}pages"
        data = {
            "parent": {"database_id": database_id},
            "properties": {
                "タスク名": {
                    "title": [{"text": {"content": title}}]
                },
                "日付": {
                    "date": {
                        "start": current_date.strftime("%Y-%m-%dT%H:%M:%S+09:00")
                    }
                },
                "時間帯": {
                    "select": {"name": time_slot}
                },
                "最優先タスク？": {"checkbox": priority == "高"},
                "ステータス": {"select": {"name": "未着手"}},
                "達成度": {"select": {"name": "未評価"}},
                "やるべきこと": {
                    "rich_text": [{"text": {"content": todo_notes}}]
                },
                "メモ": {
                    "rich_text": [{"text": {"content": memo}}]
                }
            }
        }
        
        # APIリクエストの実行
        response = requests.post(url, headers=HEADERS, json=data)
        
        # レスポンスの確認
        if response.status_code == 200:
            print(f"タスクページ '{title}' を作成しました。")
            return response.json()["id"]
        else:
            print(f"タスクページの作成に失敗しました: {response.status_code} - {response.text}")
            print("エラー詳細:", response.text)
            return None
    except Exception as e:
        print(f"エラーが発生しました: {str(e)}")
        return None

def create_template_page(database_id, title, time_slot, todo, memo, start_time):
    try:
        print(f"\nページ作成開始: {title} ({time_slot})")
        url = f"{NOTION_API_BASE_URL}pages"
        data = {
            "parent": {"database_id": database_id},
            "properties": {
                "タスク名": {
                    "title": [{"text": {"content": title}}]
                },
                "日付": {
                    "date": {
                        "start": f"{datetime.now().strftime('%Y-%m-%dT%H:%M:%S+09:00')}"
                    }
                },
                "時間帯": {
                    "select": {"name": time_slot}
                },
                "最優先タスク？": {"checkbox": False},
                "ステータス": {"select": {"name": "未着手"}},
                "達成度": {"select": {"name": "未評価"}},
                "やるべきこと": {
                    "rich_text": [{"text": {"content": todo}}]
                },
                "メモ": {
                    "rich_text": [{"text": {"content": memo}}]
                }
            }
        }
        
        response = requests.post(url, headers=HEADERS, json=data)
        
        if response.status_code == 200:
            print(f"\nAPI Response: {response.status_code} - 成功")
            print("Response JSON:")
            print("----------------------------------------")
            print(json.dumps(response.json(), indent=2, ensure_ascii=False))
            print("----------------------------------------")
            return response.json()["id"]
        else:
            print(f"\nAPI Error: {response.status_code} - {response.text}")
            print("Response JSON:")
            print("----------------------------------------")
            try:
                print(json.dumps(response.json(), indent=2, ensure_ascii=False))
            except:
                print("No response body")
            print("----------------------------------------")
            return None
    except Exception as e:
        print(f"\nError in create_template_page: {str(e)}")
        return None

if __name__ == "__main__":
    try:
        # 環境変数の確認
        if not NOTION_API_KEY or not NOTION_PARENT_PAGE_ID:
            print("エラー: Notion APIキーまたは親ページIDが設定されていません。")
            sys.exit(1)

        # メインページの作成
        main_page_id = create_main_page(NOTION_PARENT_PAGE_ID)
        if not main_page_id:
            print("メインページの作成に失敗しました。処理を終了します。")
            sys.exit(1)

        # タスクデータベースの作成
        database_id = create_task_database(main_page_id)
        if not database_id:
            print("タスクデータベースの作成に失敗しました。処理を終了します。")
            sys.exit(1)

        # 現在の日付から1週間分のタスクを追加
        current_date = datetime.now()
        for i in range(7):
            # 週間スケジュールデータから該当の曜日のタスクを取得
            day_of_week_num = current_date.weekday()
            tasks_for_day = WEEKLY_SCHEDULE_DATA.get(day_of_week_num, [])
            
            for task in tasks_for_day:
                create_task_page_with_report(database_id, task, current_date)
            
            # 次の日へ
            current_date += timedelta(days=1)

    except Exception as e:
        print(f"\nエラーが発生しました: {str(e)}")
    finally:
        print("\nスクリプトの実行が完了しました。")
