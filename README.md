# schedule.py の使い方

`schedule.py` は、予定データを読み込み、指定した日の予定を開始時刻順に表示します。

## 実行方法

初回のみ、Richをインストールします。

```powershell
py -m pip install -r requirements.txt
```

日付を指定する場合:

```powershell
py schedule.py 2026-10-02
```

日付を省略すると、日本時間の今日の予定をRichの表形式で表示します。出力の装飾は `schedule_display.py` の `display_schedule` 関数が担当します。

```powershell
py schedule.py
```

## 予定データ

予定はJSONファイルから読み込みます。`schedule.py` と同じフォルダの `schedule.json` が優先されます。ファイルがない場合は `data/schedule.json.json` も読み込みます。

JSONは予定オブジェクトのリストで、各予定に `title`、`start`、`end` を指定します。`location` は任意です。日時は `YYYY-MM-DDTHH:MM` 形式です。

```json
[
  {
    "title": "研修 第2回（開発環境とAIコーディング）",
    "start": "2026-10-02T09:00",
    "end": "2026-10-02T18:00",
    "location": "オンライン"
  }
]
```

予定データのJSONファイルは読み取り専用で、プログラムから書き換えません。ファイルが見つからない場合やデータを読み込めない場合は、日本語でエラーを表示します。