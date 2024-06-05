import requests
from notion_client import Client
from os import getenv
import logging

# NotionのAPIトークンとデータベースIDを設定
#notion = "your_notion_api_token"
#database_id = "your_notion_database_id"
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

# DOIからBibTeXを取得
def get_bibtex_from_doi(doi):
    url = f"https://doi.org/{doi}"
    headers = {"Accept": "application/x-bibtex"}
    
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        return response.text
    else:
        print(f"Error: Unable to retrieve BibTeX for DOI {doi}")
        return None

# Notionデータベースからデータを取得
response = notion.databases.query(
        **{
            "database_id": database_id,
            "filter": {
                "property": "Generate",
                "checkbox": {
                    "equals": True
                }
            }
        }
)
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
                    '引用': {'rich_text': [{'text': {'content': citation}}]},
                    'Generate': {'checkbox': False},
                    'BibTeX': {'rich_text': [{'text': {'content': get_bibtex_from_doi(doi)}}]},
                }
            )
    except IndexError as e:
        logging.error(f"IndexError: {e} - DOI not found in item:")
        continue
    except KeyError as e:
        logging.error(f"KeyError: {e} - for item: {item}")
        continue
    except Exception as e:
        logging.error(f"Unexpected error: {e} - for item: {item}")
        continue