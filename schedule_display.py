from datetime import date, datetime
from typing import Any

from rich import box
from rich.console import Console
from rich.panel import Panel
from rich.table import Table


def display_schedule(target_date: date, events: list[dict[str, Any]]) -> None:
    table = Table(
        box=box.ROUNDED,
        border_style="bright_blue",
        header_style="bold cyan",
        show_lines=True,
    )
    table.add_column("時間", style="green", no_wrap=True)
    table.add_column("予定", style="bold")
    table.add_column("場所", style="magenta")

    for event in events:
        start = datetime.fromisoformat(event["start"])
        end = datetime.fromisoformat(event["end"])
        table.add_row(
            f"{start:%H:%M}-{end:%H:%M}",
            event["title"],
            event.get("location", "—"),
        )

    heading = f"{target_date.isoformat()} の予定 {len(events)} 件"
    Console().print(Panel(table, title=heading, border_style="bright_blue"))
