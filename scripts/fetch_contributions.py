#!/usr/bin/env python3
"""
Fetch all-time and past-year contribution counts for RusdiEneri.
Calculates real-time streak across all years (1,000+ days!), consistency,
monthly breakdown, and caches results to data/contributions.json.
"""
import datetime
import json
import os
import sys
import requests

USERNAME = os.environ.get("GH_PROFILE_USER", "RusdiEneri")
OUT_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data", "contributions.json")


def fetch_all_contributions(user):
    url = f"https://github-contributions-api.jogruber.de/v4/{user}"
    try:
        resp = requests.get(url, headers={"User-Agent": "profile-readme-bot/1.0"}, timeout=25)
        resp.raise_for_status()
        data = resp.json()
        raw_contribs = data.get("contributions", [])
        if raw_contribs:
            today_str = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d")
            # Filter out future placeholder dates
            days = [
                {
                    "date": item["date"],
                    "count": item.get("count", 0),
                    "level": item.get("level", 0)
                }
                for item in raw_contribs
                if item["date"] <= today_str
            ]
            days.sort(key=lambda d: d["date"])
            return days, data.get("total", {})
    except Exception as e:
        print(f"All-time API fetch failed: {e}", file=sys.stderr)
    return None, {}


def compute_streaks(days):
    if not days:
        return (0, None, None), (0, None, None)

    # 1. Current streak (walk backwards from today / yesterday)
    idx = len(days) - 1
    if days[idx]["count"] == 0 and idx > 0:
        idx -= 1  # If today hasn't received commits yet, don't break streak

    cur_streak = 0
    cur_end = days[idx]["date"] if idx >= 0 else None
    cur_start = None

    while idx >= 0 and days[idx]["count"] > 0:
        cur_streak += 1
        cur_start = days[idx]["date"]
        idx -= 1

    # 2. Longest streak
    longest_streak = 0
    longest_start = None
    longest_end = None
    run = 0
    run_start = None

    for d in days:
        if d["count"] > 0:
            if run == 0:
                run_start = d["date"]
            run += 1
            if run > longest_streak:
                longest_streak = run
                longest_start = run_start
                longest_end = d["date"]
        else:
            run = 0

    return (cur_streak, cur_start, cur_end), (longest_streak, longest_start, longest_end)


def build_data(all_days, yearly_totals):
    if not all_days:
        return {}

    (cur_len, cur_start, cur_end), (long_len, long_start, long_end) = compute_streaks(all_days)

    all_time_total = sum(yearly_totals.values()) if yearly_totals else sum(d["count"] for d in all_days)

    # Last 365 days for the profile calendar & monthly charts
    past_year_days = all_days[-365:] if len(all_days) >= 365 else all_days
    past_year_total = sum(d["count"] for d in past_year_days)
    past_year_active = sum(1 for d in past_year_days if d["count"] > 0)
    best = max(all_days, key=lambda d: d["count"])

    # Monthly breakdown for the past 12 months
    monthly_dict = {}
    for d in past_year_days:
        m_key = d["date"][:7]
        monthly_dict[m_key] = monthly_dict.get(m_key, 0) + d["count"]
    monthly_list = [{"month": k, "total": v} for k, v in sorted(monthly_dict.items())]

    return {
        "username": USERNAME,
        "generated_at": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "all_time_total": all_time_total,
        "past_year_total": past_year_total,
        "total_contributions": past_year_total,
        "active_days": past_year_active,
        "total_days": len(past_year_days),
        "consistency_pct": round((past_year_active / len(past_year_days)) * 100, 1) if past_year_days else 0,
        "avg_per_active_day": round(past_year_total / past_year_active, 1) if past_year_active else 0,
        "current_streak": {
            "length": cur_len,
            "start": cur_start,
            "end": cur_end
        },
        "longest_streak": {
            "length": long_len,
            "start": long_start,
            "end": long_end
        },
        "best_day": {
            "date": best["date"],
            "count": best["count"]
        },
        "yearly_totals": yearly_totals,
        "monthly": monthly_list,
        "days": past_year_days,
    }


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    print(f"Fetching real-time contribution dataset for {USERNAME}...")
    days, totals = fetch_all_contributions(USERNAME)

    if not days:
        print("Error: Could not retrieve all-time data", file=sys.stderr)
        if os.path.exists(OUT_PATH):
            return
        sys.exit(1)

    data = build_data(days, totals)
    os.makedirs(os.path.dirname(OUT_PATH), exist_ok=True)
    with open(OUT_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

    print(f"Success! Cached to {OUT_PATH}:")
    print(f"  * Current Streak : {data['current_streak']['length']} days ({data['current_streak']['start']} to {data['current_streak']['end']})")
    print(f"  * Longest Streak : {data['longest_streak']['length']} days")
    print(f"  * All-Time Total : {data['all_time_total']:,} contributions")
    print(f"  * Past Year Total: {data['past_year_total']:,} contributions ({data['consistency_pct']}% consistency)")


if __name__ == "__main__":
    main()
