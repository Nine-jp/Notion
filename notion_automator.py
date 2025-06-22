import requests
import json
from datetime import datetime, timedelta
import sys
import os
from dotenv import load_dotenv

# Notion APIの設定
NOTION_API_KEY = "ntn_V5050303374bd0or47b7gcuiyix6d2xmglTyXP7KMQPcN6"
NOTION_PARENT_PAGE_ID = "21812d05838e808fbe3bd0340e7f6177"
NOTION_API_VERSION = "2022-06-28"
NOTION_API_BASE_URL = "https://api.notion.com/v1/"

# 週間スケジュールデータ（0: 月曜日, 1: 火曜日, 2: 水曜日, 3: 木曜日, 4: 金曜日, 5: 土曜日, 6: 日曜日）
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
            "todo_notes": "- 今日の作業を振り返る\n- 今日の達成感！記録（写真/メモ）\n- 明日やすること整理",
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
    try:
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
        response = requests.post(url, headers=HEADERS, json=data)
        if response.status_code == 200:
            print("データベース '週間タスク管理' を作成しました。")
            return response.json()["id"]
        else:
            print(f"データベースの作成に失敗しました: {response.status_code} - {response.text}")
            print("エラー詳細:", response.text)
            return None
    except Exception as e:
        print(f"データベース作成中にエラーが発生しました: {str(e)}")
        return None

def create_task_page_with_report(database_id, task, current_date):
    try:
        title = task.get("title", "")
        time_slot = task.get("time_slot", "")
        todo_notes = task.get("todo_notes", "")
        memo = task.get("memo", "")
        priority = task.get("priority", "")

        print(f"\n処理中のタスク: {title}")
        print(f"時間帯: {time_slot}")
        print(f"優先度: {priority}")
        print(f"TODO: {todo_notes}")
        print(f"メモ: {memo}")

        # 時間帯の開始時刻を抽出
        if time_slot and time_slot != "":
            start_time_str = time_slot.split(' ')[0].split('-')[0].strip()
            try:
                hour, minute = map(int, start_time_str.split(':'))
                task_datetime = current_date.replace(hour=hour, minute=minute, second=0, microsecond=0)
                print(f"設定された日時: {task_datetime.strftime('%Y-%m-%d %H:%M:%S')}")
            except (ValueError, IndexError):
                task_datetime = current_date
                print("時間のパースに失敗しました。現在時刻を使用します。")
        else:
            task_datetime = current_date
            print("時間帯が設定されていません。現在時刻を使用します。")

        # Notion APIのデータ構造を構築
        properties = {
            "タスク名": {
                "title": [{"text": {"content": title}}]
            },
            "日付": {
                "date": {
                    "start": task_datetime.strftime("%Y-%m-%dT%H:%M:%S+09:00")
                }
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

        # time_slot が空でない場合のみ "時間帯" プロパティを追加
        if time_slot and time_slot != "":
            properties["時間帯"] = {
                "select": {"name": time_slot}
            }
        
        print("\n送信するデータ:")
        print(json.dumps(properties, indent=2, ensure_ascii=False))

        url = f"{NOTION_API_BASE_URL}pages"
        data = {
            "parent": {"database_id": database_id},
            "properties": properties
        }
        
        print("\nAPIリクエストを送信中...")
        response = requests.post(url, headers=HEADERS, json=data)
        
        print(f"\nレスポンスステータス: {response.status_code}")
        if response.status_code != 200:
            print("レスポンスヘッダー:", response.headers)
            print("レスポンスボディ:", response.text)
        
        if response.status_code == 200:
            print(f"\nタスクページ '{title}' を作成しました。日時: {task_datetime.strftime('%Y-%m-%d %H:%M:%S')}")
            return response.json()["id"]
        else:
            print(f"\nタスクページの作成に失敗しました: {response.status_code} - {response.text}")
            print("エラー詳細:", response.text)
            return None
    except Exception as e:
        print(f"\nエラーが発生しました: {str(e)}")
        print("エラー詳細:", sys.exc_info())
        return None

if __name__ == "__main__":
    try:
        if not NOTION_API_KEY or not NOTION_PARENT_PAGE_ID:
            print("エラー: Notion APIキーまたは親ページIDが設定されていません。")
            sys.exit(1)

        print("\nメインページの作成を開始します...")
        main_page_id = create_main_page(NOTION_PARENT_PAGE_ID)
        if not main_page_id:
            print("メインページの作成に失敗しました。処理を終了します。")
            sys.exit(1)
        print(f"メインページが作成されました。ID: {main_page_id}")

        print("\nタスクデータベースの作成を開始します...")
        database_id = create_task_database(main_page_id)
        if not database_id:
            print("タスクデータベースの作成に失敗しました。処理を終了します。")
            sys.exit(1)
        print(f"タスクデータベースが作成されました。ID: {database_id}")

        print("\nタスクページの作成を開始します...")
        current_date = datetime.now()
        print(f"開始日時: {current_date.strftime('%Y-%m-%d %H:%M:%S')}")
        
        # 現在の曜日から1週間分のタスクを作成
        current_date = datetime.now()
        print(f"開始日時: {current_date.strftime('%Y-%m-%d %H:%M:%S')}")
        
        # 1週間分のタスクを作成
        for i in range(7):
            # 現在の曜日を基準に、その日のタスクを取得
            day_of_week_num = current_date.weekday()
            
            # 0: 月曜日, 1: 火曜日, 2: 水曜日, 3: 木曜日, 4: 金曜日, 5: 土曜日, 6: 日曜日
            tasks_for_day = WEEKLY_SCHEDULE_DATA.get(day_of_week_num, [])
            
            print(f"\n{current_date.strftime('%Y-%m-%d')}のタスクを処理中...")
            print(f"曜日番号: {day_of_week_num}")
            
            # タスクの作成
            for task in tasks_for_day:
                print(f"タスク: {task['title']}")
                result = create_task_page_with_report(database_id, task, current_date)
                if result:
                    print(f"  -> タスクページ作成成功")
                else:
                    print(f"  -> タスクページ作成失敗")
            
            # 次の日へ
            current_date += timedelta(days=1)

    except Exception as e:
        print(f"\nエラーが発生しました: {str(e)}")
        print("エラー詳細:", sys.exc_info())
    finally:
        print("\nスクリプトの実行が完了しました。")
