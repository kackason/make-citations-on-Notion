import requests
from notion_client import Client
from os import getenv

# NotionのAPIトークンとデータベースIDを設定
#notion = Client(auth="secret_2LWq64NdF6URDHwbQxggNhGkFoVlcsPrKc1cWmQzm4k")
#database_id = "514c4f85887e421aa475bb1552078e4b"
notion = Client(auth=getenv("NOTION_API"))
database_id =getenv("PAPER_DATABASE")

# CrossRef APIを使ってDOIからメタデータを取得
def get_metadata(doi):
    url = f"https://api.crossref.org/works/{doi}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        item = data["message"]
        title = item["title"][0]
        authors = ", ".join([author["family"] + " " + author["given"] for author in item["author"]])
        year = item["published-print"]["date-parts"][0][0]
        journal = item["container-title"][0]
        volume = item.get("volume", "")
        issue = item.get("issue", "")
        pages = item.get("page", "")
        return title, authors, year, journal, volume, issue, pages
    else:
        return None

# Notionデータベースからデータを取得
response = notion.databases.query(database_id=database_id)
items = response['results']

# 取得したデータの表示と更新
for item in items:
    try:
        doi = item['properties']['DOI']['rich_text'][0]['text']['content']
        metadata = get_metadata(doi)
        if metadata:
            title, authors, year, journal, volume, issue, pages = metadata
            citation = f"{authors}. ({year}). {title}. *{journal}, {volume}*({issue}), {pages}. https://doi.org/{doi}"
            
            # Notionデータベースに引用を追加
            notion.pages.update(
                page_id=item['id'],
                properties={
                    'タイトル': {'title': [{'text': {'content': title}}]},
                    '著者': {'rich_text': [{'text': {'content': authors}}]},
                    '年': {'rich_text': [{'text': {'content': str(year)}}]},
                    '収録刊行物': {'rich_text': [{'text': {'content': journal}}]},
                    '巻': {'rich_text': [{'text': {'content': volume}}]},
                    '号': {'rich_text': [{'text': {'content': issue}}]},
                    'ページ範囲': {'rich_text': [{'text': {'content': pages}}]},
                    '引用': {'rich_text': [{'text': {'content': citation}}]}
                }
            )
    except:
        continue

