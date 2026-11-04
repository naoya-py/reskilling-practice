import json
import sys
from datetime import date, datetime, timedelta, timezone
from pathlib import Path
from typing import Any

from schedule_display import display_schedule


def read_schedule() -> list[dict[str, Any]]:
    schedule_path = Path(__file__).with_name("schedule.json")
    if not schedule_path.exists():
        alternate_paths = (
            Path(__file__).with_name("schedule.json.json"),
            Path(__file__).parent / "data" / "schedule.json.json",
        )
        for alternate_path in alternate_paths:
            if alternate_path.exists():
                schedule_path = alternate_path
                break

    with schedule_path.open(encoding="utf-8") as file:
        events = json.load(file)

    if not isinstance(events, list) or not all(
        isinstance(event, dict) for event in events
    ):
        raise ValueError("schedule.json の形式が正しくありません。")

    return events


def filter_by_date(
    events: list[dict[str, Any]], target_date: date
) -> list[dict[str, Any]]:
    matching_events = [
        event
        for event in events
        if datetime.fromisoformat(event["start"]).date() == target_date
    ]
    return sorted(matching_events, key=lambda event: event["start"])


def format_event(event: dict[str, Any]) -> str:
    start = datetime.fromisoformat(event["start"])
    end = datetime.fromisoformat(event["end"])
    result = f"{start:%H:%M}-{end:%H:%M}  {event['title']}"
    if location := event.get("location"):
        result += f"  @{location}"
    return result


def main() -> int:
    if len(sys.argv) > 2:
        print("日付は1つだけ指定してください。例: 2026-10-02", file=sys.stderr)
        return 1

    try:
        target_date = (
            date.fromisoformat(sys.argv[1])
            if len(sys.argv) == 2
            else datetime.now(timezone(timedelta(hours=9))).date()
        )
        events = filter_by_date(read_schedule(), target_date)
    except FileNotFoundError:
        print("schedule.json が見つかりません。同じフォルダに配置してください。")
        return 1
    except (OSError, json.JSONDecodeError, KeyError, TypeError, ValueError) as error:
        print(f"予定の読み込みまたは日付の処理に失敗しました: {error}")
        return 1

    display_schedule(target_date, events)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
