"""
Scrape ECI statewise .htm pages (treat .htm as the endpoint).

Features:
- Single URL mode (--url)
- Template mode (--template with {} placeholder and start/end)
- Outputs JSON or CSV
- Extracts nested party name and tooltip trends (Leading In, Won In, Trailing In)
"""
from typing import List, Dict, Optional
import argparse
import json
import csv
import time
import re
import sys

import requests
from bs4 import BeautifulSoup

DEFAULT_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/147.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
}


def fetch_page(url: str, timeout: int = 20) -> Optional[str]:
    try:
        r = requests.get(url, headers=DEFAULT_HEADERS, timeout=timeout)
        if r.status_code != 200:
            print(f"Warning: {url} returned HTTP {r.status_code}", file=sys.stderr)
            return None
        return r.text
    except requests.RequestException as e:
        print(f"Request error for {url}: {e}", file=sys.stderr)
        return None


def _clean_text(s: Optional[str]) -> str:
    if not s:
        return ""
    return re.sub(r"\s+", " ", s).strip()


def parse_party_cell(td) -> Dict:
    """
    Extract party name and tooltip trends from a cell that contains nested table & tooltip.
    Returns: { "party": str, "trends": {"leading_in": int|str, "won_in": int|str, "trailing_in": int|str} }
    """
    party_name = ""
    trends: Dict[str, object] = {}
    # party name often appears in a nested <td align='left'>
    left_td = td.find(lambda tag: tag.name == "td" and tag.get("align") == "left")
    if left_td:
        party_name = _clean_text(left_td.get_text())
    else:
        party_name = _clean_text(td.get_text())

    tooltip = td.find("div", class_="tooltip")
    if tooltip:
        for tr in tooltip.find_all("tr"):
            tds = tr.find_all("td")
            if len(tds) >= 3:
                key = _clean_text(tds[0].get_text()).lower().replace(" ", "_")
                val = _clean_text(tds[2].get_text())
                # try convert to int
                try:
                    val_i = int(val.replace(",", ""))
                    trends[key] = val_i
                except Exception:
                    trends[key] = val
    return {"party": party_name, "trends": trends}


def parse_table(html: str) -> List[Dict]:
    soup = BeautifulSoup(html, "lxml")
    table = soup.find("table", class_="table table-striped table-bordered")
    if not table:
        cont = soup.find("div", class_="custom-table")
        table = cont.find("table") if cont else None
    if not table:
        return []

    tbody = table.find("tbody")
    if not tbody:
        return []

    rows: List[Dict] = []
    for tr in tbody.find_all("tr"):
        # top-level tds only (avoid nested table tds)
        tds = [td for td in tr.find_all("td", recursive=False)]
        if len(tds) < 9:
            continue
        constituency = _clean_text(tds[0].get_text())
        const_no = _clean_text(tds[1].get_text())
        leading_candidate = _clean_text(tds[2].get_text())
        leading_party = parse_party_cell(tds[3])
        trailing_candidate = _clean_text(tds[4].get_text())
        trailing_party = parse_party_cell(tds[5])
        margin = _clean_text(tds[6].get_text())
        round_info = _clean_text(tds[7].get_text())
        status = _clean_text(tds[8].get_text())

        # try convert
        try:
            const_no_i = int(const_no.replace(",", ""))
        except Exception:
            const_no_i = const_no
        try:
            margin_i = int(margin.replace(",", ""))
        except Exception:
            margin_i = margin

        row = {
            "constituency": constituency,
            "const_no": const_no_i,
            "leading_candidate": leading_candidate,
            "leading_party": leading_party,
            "trailing_candidate": trailing_candidate,
            "trailing_party": trailing_party,
            "margin": margin_i,
            "round": round_info,
            "status": status,
        }
        rows.append(row)
    return rows


def scrape_single(url: str, wait: float = 0.2) -> List[Dict]:
    html = fetch_page(url)
    if not html:
        return []
    time.sleep(wait)
    return parse_table(html)


def scrape_range(template: str, start: int, end: int, wait: float = 0.2) -> List[Dict]:
    all_rows: List[Dict] = []
    for i in range(start, end + 1):
        url = template.format(i)
        print(f"Fetching {url}", file=sys.stderr)
        rows = scrape_single(url, wait=wait)
        if not rows:
            print(f"No rows found on page {i} ({url}), stopping.", file=sys.stderr)
            break
        all_rows.extend(rows)
    return all_rows


def save_json(rows: List[Dict], path: str):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(rows, f, ensure_ascii=False, indent=2)


def save_csv(rows: List[Dict], path: str):
    if not rows:
        open(path, "w", encoding="utf-8").close()
        return
    fieldnames = [
        "constituency",
        "const_no",
        "leading_candidate",
        "leading_party",
        "leading_leading_in",
        "leading_won_in",
        "leading_trailing_in",
        "trailing_candidate",
        "trailing_party",
        "trailing_leading_in",
        "trailing_won_in",
        "trailing_trailing_in",
        "margin",
        "round",
        "status",
    ]
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        for r in rows:
            out = {
                "constituency": r.get("constituency", ""),
                "const_no": r.get("const_no", ""),
                "leading_candidate": r.get("leading_candidate", ""),
                "leading_party": r.get("leading_party", {}).get("party", ""),
                "leading_leading_in": r.get("leading_party", {}).get("trends", {}).get("leading_in", ""),
                "leading_won_in": r.get("leading_party", {}).get("trends", {}).get("won_in", ""),
                "leading_trailing_in": r.get("leading_party", {}).get("trends", {}).get("trailing_in", ""),
                "trailing_candidate": r.get("trailing_candidate", ""),
                "trailing_party": r.get("trailing_party", {}).get("party", ""),
                "trailing_leading_in": r.get("trailing_party", {}).get("trends", {}).get("leading_in", ""),
                "trailing_won_in": r.get("trailing_party", {}).get("trends", {}).get("won_in", ""),
                "trailing_trailing_in": r.get("trailing_party", {}).get("trends", {}).get("trailing_in", ""),
                "margin": r.get("margin", ""),
                "round": r.get("round", ""),
                "status": r.get("status", ""),
            }
            w.writerow(out)


def main():
    p = argparse.ArgumentParser(description="Scrape ECI statewiseS22*.htm pages")
    group = p.add_mutually_exclusive_group(required=True)
    group.add_argument("--url", help="Full url to a single .htm page")
    group.add_argument("--template", help="URL template with {} placeholder for page number")
    p.add_argument("--start", type=int, default=1, help="Start page number for template mode")
    p.add_argument("--end", type=int, default=12, help="End page number for template mode")
    p.add_argument("--output", "-o", default="out.json", help="Output path")
    p.add_argument("--format", choices=["json", "csv"], default="json", help="Output format")
    p.add_argument("--wait", type=float, default=0.2, help="Seconds to wait between requests")
    args = p.parse_args()

    rows: List[Dict] = []
    if args.url:
        print(f"Scraping {args.url}", file=sys.stderr)
        rows = scrape_single(args.url, wait=args.wait)
    else:
        if "{}" not in args.template:
            print("Template must contain {} placeholder for page number", file=sys.stderr)
            sys.exit(2)
        rows = scrape_range(args.template, args.start, args.end, wait=args.wait)

    if args.format == "json":
        save_json(rows, args.output)
    else:
        save_csv(rows, args.output)

    print(f"Saved {len(rows)} rows to {args.output}", file=sys.stderr)


if __name__ == "__main__":
    main()
