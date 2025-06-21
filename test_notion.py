import requests
import json
import config

def create_task_database(parent_page_id):
    """データベースを作成する関数"""
    url = f"{config.NOTION_API_BASE_URL}databases"
    HEADERS = {
        "Authorization": f"Bearer {config.NOTION_API_KEY}",
        "Notion-Version": config.NOTION_API_VERSION,
        "Content-Type": "application/json"
    }
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
    print("\nデータベース作成のリクエストデータ:")
    print("----------------------------------------")
    print(json.dumps(data, indent=2, ensure_ascii=False))
    print("----------------------------------------")
    
    response = requests.post(url, headers=HEADERS, data=json.dumps(data))
    
    print("\nデータベース作成のリクエストヘッダー:")
    print("----------------------------------------")
    print(f"Authorization: {HEADERS['Authorization'][:20]}... (truncated)")
    print(f"Notion-Version: {HEADERS['Notion-Version']}")
    print("----------------------------------------")
    
    try:
        response.raise_for_status()
        print(f"\nデータベース作成のAPI Response: {response.status_code} - 成功")
        print("Response JSON:")
        print("----------------------------------------")
        print(json.dumps(response.json(), indent=2, ensure_ascii=False))
        print("----------------------------------------")
        return response.json()["id"]
    except requests.exceptions.HTTPError as e:
        print(f"\nデータベース作成のAPI Error: {response.status_code} - {response.text}")
        print("Response JSON:")
        print("----------------------------------------")
        try:
            print(json.dumps(response.json(), indent=2, ensure_ascii=False))
        except:
            print("No response body")
        print("----------------------------------------")
        return None
    except Exception as e:
        print(f"\nデータベース作成のUnexpected error: {str(e)}")
        return None

def create_template_page(database_id, title, time_slot, todo, memo, start_time):
    try:
        # データベースIDの形式チェック
        if not database_id or not isinstance(database_id, str):
            raise ValueError("データベースIDが無効です。有効なUUIDが必要です。")
        
        url = f"{config.NOTION_API_BASE_URL}pages"
        HEADERS = {
            "Authorization": f"Bearer {config.NOTION_API_KEY}",
            "Notion-Version": config.NOTION_API_VERSION,
            "Content-Type": "application/json"
        }
        data = {
            "parent": {"database_id": database_id},
            "properties": {
                "タスク名": {
                    "title": [{"text": {"content": title}}]
                },
                "日付": {
                    "date": {
                        "start": f"2025-06-23T{start_time.zfill(5)}:00+09:00"
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
        print("\nテンプレートページ作成のリクエストデータ:")
        print("----------------------------------------")
        print(f"データベースID: {database_id}")
        print(f"タイトル: {title}")
        print(f"時間帯: {time_slot}")
        print(f"開始時刻: {start_time}")
        print("----------------------------------------")
        print("\nリクエストデータ:")
        print("----------------------------------------")
        print(json.dumps(data, indent=2, ensure_ascii=False))
        print("----------------------------------------")
        
        response = requests.post(url, headers=HEADERS, data=json.dumps(data))
        
        print("\nリクエストヘッダー:")
        print("----------------------------------------")
        print(f"Authorization: {HEADERS['Authorization'][:20]}... (truncated)")
        print(f"Notion-Version: {HEADERS['Notion-Version']}")
        print("----------------------------------------")
        
        try:
            response.raise_for_status()
            print(f"\nテンプレートページ作成のAPI Response: {response.status_code} - 成功")
            print("Response JSON:")
            print("----------------------------------------")
            print(json.dumps(response.json(), indent=2, ensure_ascii=False))
            print("----------------------------------------")
            return response.json()["id"]
        except requests.exceptions.HTTPError as e:
            print(f"\nテンプレートページ作成のAPI Error: {response.status_code} - {response.text}")
            print("Response JSON:")
            print("----------------------------------------")
            try:
                print(json.dumps(response.json(), indent=2, ensure_ascii=False))
            except:
                print("No response body")
            print("----------------------------------------")
            return None
        except Exception as e:
            print(f"\nテンプレートページ作成のUnexpected error: {str(e)}")
            return None
    except Exception as e:
        print(f"\nテンプレートページ作成のError: {str(e)}")
        return None

if __name__ == "__main__":
    if not config.NOTION_API_KEY or not config.NOTION_PARENT_PAGE_ID:
        print("エラー: Notion APIキーまたは親ページIDが設定されていません。")
        print(".envファイルに以下の環境変数を設定してください：")
        print("NOTION_API_KEY=your_api_key_here")
        print("NOTION_PARENT_PAGE_ID=your_parent_page_id_here")
    else:
        print("Notionページとデータベースの自動生成を開始します。")
        try:
            # データベースの作成
            database_id = create_task_database(config.NOTION_PARENT_PAGE_ID)
            if database_id:
                print(f"\nデータベースが正常に作成されました。データベースID: {database_id}")
                
                # 8:00 - 9:00 ウォームアップ＆計画
                page_id = create_template_page(
                    database_id,
                    "ウォームアップ＆計画",
                    "8:00 - 9:00",
                    "前日のBlenderファイル確認\n今日のモデリング目標設定\nVibeCoding基礎復習（テキスト）\nAIニュースチェック",
                    "",
                    "8:00"
                )
                
                # 9:00 - 11:00 Robloxアバター作成
                page_id = create_template_page(
                    database_id,
                    "Robloxアバター作成",
                    "9:00 - 11:00",
                    "ポテトくんの胴体・頭の基本形状をBlenderで作成（動画チュートリアル）\n次のステップ: 細部のモデリングへ進む準備",
                    "",
                    "9:00"
                )
                
                # 12:30 - 14:30 Blender取説
                page_id = create_template_page(
                    database_id,
                    "Blender取説",
                    "12:30 - 14:30",
                    "Roblox向けモデリングの注意点（ポリゴン数削減、エラーチェック）の基礎（動画チュートリアル）\n次のステップ: テクスチャリングの基礎知識",
                    "",
                    "12:30"
                )
                
                # 14:30 - 15:30 クールダウン＆記録
                page_id = create_template_page(
                    database_id,
                    "クールダウン＆記録",
                    "14:30 - 15:30",
                    "今日の作業を振り返る\n今日の達成感！記録（写真/メモ）\n明日やること整理\nやったこと例: Blenderでポテトくんの胴体と頭のベースモデルを完成させた",
                    "",
                    "14:30"
                )
                
                if page_id:
                    print(f"\nテンプレートページが正常に作成されました。ページID: {page_id}")
                else:
                    print("\nテンプレートページの作成に失敗しました。エラーメッセージを確認してください。")
            else:
                print("\nデータベースの作成に失敗しました。エラーメッセージを確認してください。")
        except Exception as e:
            print(f"\nエラー: {str(e)}")
