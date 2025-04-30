import csv
from pathlib import Path

CSV_PATH = Path(__file__).resolve().parent.parent / "videos.csv"
FIELDNAMES = [
    "source_post_id", "post_url", "post_description", "post_created",
    "likes_count", "shares_count", "views_count", "comments_count",
]

def read_all():
    items = []
    with open(CSV_PATH, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f, delimiter="\t", fieldnames=FIELDNAMES)
        next(reader)  # skip header
        for row in reader:
            # convert numeric fields
            for fld in ("likes_count", "shares_count", "views_count", "comments_count"):
                row[fld] = int(row[fld])
            items.append(row)
    return items

def write_all(items):
    with open(CSV_PATH, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, delimiter="\t", fieldnames=FIELDNAMES)
        writer.writeheader()
        for item in items:
            writer.writerow(item)
