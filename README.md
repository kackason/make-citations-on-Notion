# Notionで論文管理
Notionデータベースでの論文を管理するためのツールです。**文献のDOIを入力するとAPA形式で文献引用を自動作成し出力します。**
pythonコードはChatGPTにより生成されたものです。


## 手順1: Notionデータベースの作成
　Notionで新しいデータベースを作成し、フィールド名（プロパティ名）を以下のように設定します：  
  ・タイトル (テキスト)*  
  ・DOI (テキスト)  
  ・著者 (テキスト)  
  ・年 (テキスト)  
  ・収録刊行物 (テキスト)  
  ・巻 (テキスト)  
  ・号 (テキスト)  
  ・ページ範囲 (テキスト)  
  ・引用 (テキスト)  

手順2: 必要なライブラリのインストール
　以下のコマンドを使って必要なPythonライブラリをインストールします：
  'pip install requests notion-client'

手順3: スクリプトの編集
  notion_make_citation.pyを開き、以下の変更を行います:  
  ・変数your_notion_api_tokenにNotionページに紐づいているインテグレーショントークンを入力  
  ・変数your_database_idに作成したデータベースのIDを入力  

手順4: DOIの入力
  保存したい論文のDOIをコピーし、Notionデータベースの"DOI"欄に貼り付けます

手順5: スクリプトの実行
  notion_make_citation.pyを実行します**
  完了後にNotion内の空欄が埋まっていれば成功です


注記:
*　"タイトル"プロパティが要素のページタイトルではなく追加したプロパティの場合エラーが出ます
**　データベース内に"DOI"プロパティが空欄の要素があるとエラーが出ます
