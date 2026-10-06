#!/usr/bin/env python3
"""
Fetch daily contribution counts for RusdiEneri and save data/contributions.json
with derived statistics: current streak, longest streak, best day, monthly totals.
"""
import datetime
import json
import os
import re
import sys
import requests
from bs4 import BeautifulSoup

USERNAME = os.environ.get("GH_PROFILE_USER", "RusdiEneri")
OUT_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data", "contributions.json")


def fetch_from_api(user):
    url = f"https://github-contributions-api.jogruber.de/v4/{user}?y=last"
    try:
        resp = requests.get(url, headers={"User-Agent": "profile-readme-bot/1.0"}, timeout=20)
        resp.raise_for_status()
        data = resp.json()
        raw_contribs = data.get("contributions", [])
        if raw_contribs:
            days = []
            for item in raw_contribs:
                days.append({
                    "date": item["date"],
                    "count": item.get("count", 0),
                    "level": item.get("level", 0)
                })
            days.sort(key=lambda d: d["date"])
            return days
    except Exception as e:
        print(f"API fetch failed: {e}", file=sys.stderr)
    return None


def fetch_from_html(user):
    url = f"https://github.com/users/{user}/contributions"
    try:
        resp = requests.get(url, headers={"User-Agent": "profile-readme-bot/1.0"}, timeout=20)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, "html.parser")
        cells = soup.select("td.ContributionCalendar-day")
        if not cells:
            return None

        days = []
        for td in cells:
            date = td.get("data-date")
            if not date:
                continue
            td_id = td.get("id")
            tooltip_el = soup.find("tool-tip", attrs={"for": td_id}) if td_id else None
            text = tooltip_el.get_text(strip=True) if tooltip_el else ""
            if re.search(r"no contributions", text, re.I):
                count = 0
            else:
                m = re.match(r"(\d+)", text)
                count = int(m.group(1)) if m else 0
            level = int(td.get("data-level") or 0)
            days.append({"date": date, "count": count, "level": level})

        days.sort(key=lambda d: d["date"])
        return days
    except Exception as e:
        print(f"HTML scraping failed: {e}", file=sys.stderr)
    return None


def compute_current_streak(days):
    if not days:
        return 0, None, None
    idx = len(days) - 1
    # If today has 0 contributions yet, check if streak continued until yesterday
    if days[idx]["count"] == 0 and idx > 0:
        idx -= 1
    streak = 0
    end_idx = idx
    while idx >= 0 and days[idx]["count"] > 0:
        streak += 1
        idx -= 1
    start_idx = idx + 1
    if streak == 0:
        return 0, None, None
    return streak, days[start_idx]["date"], days[end_idx]["date"]


def compute_longest_streak(days):
    longest = run = 0
    longest_start = longest_end = None
    run_start_idx = None
    for i, d in enumerate(days):
        if d["count"] > 0:
            if run == 0:
                run_start_idx = i
            run += 1
            if run > longest:
                longest = run
                longest_start = days[run_start_idx]["date"]
                longest_end = days[i]["date"]
        else:
            run = 0
    return longest, longest_start, longest_end


def build_data(days):
    total = sum(d["count"] for d in days)
    active_days = sum(1 for d in days if d["count"] > 0)
    best = max(days, key=lambda d: d["count"]) if days else {"date": "", "count": 0}
    cur_len, cur_start, cur_end = compute_current_streak(days)
    long_len, long_start, long_end = compute_longest_streak(days)

    monthly = {}
    for d in days:
        key = d["date"][:7]
        monthly[key] = monthly.get(key, 0) + d["count"]
    monthly_list = [{"month": k, "total": v} for k, v in sorted(monthly.items())]

    return {
        "username": USERNAME,
        "generated_at": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "range": {"start": days[0]["date"], "end": days[-1]["date"]} if days else {},
        "total_contributions": total,
        "active_days": active_days,
        "total_days": len(days),
        "avg_per_active_day": round(total / active_days, 1) if active_days else 0,
        "current_streak": {"length": cur_len, "start": cur_start, "end": cur_end},
        "longest_streak": {"length": long_len, "start": long_start, "end": long_end},
        "best_day": {"date": best["date"], "count": best["count"]},
        "monthly": monthly_list,
        "days": days,
    }


def main():
    print(f"Fetching contribution data for {USERNAME}...")
    days = fetch_from_api(USERNAME)
    if not days:
        print("Falling back to HTML scraper...")
        days = fetch_from_html(USERNAME)

    if not days:
        print("Error: Could not retrieve contributions data from either source.", file=sys.stderr)
        if os.path.exists(OUT_PATH):
            print(f"Keeping existing cache in {OUT_PATH}")
            return
        sys.exit(1)

    data = build_data(days)
    os.makedirs(os.path.dirname(OUT_PATH), exist_ok=True)
    with open(OUT_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

    print(f"Wrote {OUT_PATH}: {data['total_contributions']:,} contributions, "
          f"active days {data['active_days']}/{data['total_days']}, "
          f"current streak {data['current_streak']['length']} days, "
          f"longest streak {data['longest_streak']['length']} days.")


if __name__ == "__main__":
    main()
