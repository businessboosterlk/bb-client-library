#!/usr/bin/env python3
# BB CLIENT LIBRARY caster. Reads bb_library_clients + bb_library_items and
# bakes cfg/<slug>.js per active client. Deterministic output, so a rebuild
# with unchanged data produces a byte-identical cast and git shows real edits.
#
#   python3 scripts/pull-month.py            # all active clients
#   python3 scripts/pull-month.py <slug>     # one client
#
# The anon key below is the same publishable key every BB app already ships.
# This table family holds deliverable metadata only, never finance or candid
# notes; the wall for the actual videos is Drive sharing to the client's email.
import json, sys, urllib.request, pathlib, datetime

BASE = "https://yyviiwnqgphyklcoijyd.supabase.co/rest/v1"
KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Inl5dmlpd25xZ3BoeWtsY29panlkIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzU3MjE5OTEsImV4cCI6MjA5MTI5Nzk5MX0.I8YiBr-rfLVcc6DE8Z1PxEP2oxXCelv6mxqAY_wY7lc"
ROOT = pathlib.Path(__file__).resolve().parent.parent

def get(path):
    r = urllib.request.Request(BASE + path, headers={"apikey": KEY, "Authorization": "Bearer " + KEY})
    with urllib.request.urlopen(r, timeout=30) as f:
        return json.load(f)

def js(v):  # compact, stable-key JSON so casts diff cleanly
    return json.dumps(v, ensure_ascii=False, sort_keys=True, separators=(",", ":"))

MONTH_NAMES = ["January","February","March","April","May","June","July",
               "August","September","October","November","December"]

def cast(client, items):
    slug = client["slug"]
    vis = [i for i in items if not i["hidden"]]
    months = {}
    for i in vis:
        if i["kind"] in ("video", "post") and i.get("month"):
            months.setdefault(i["month"], {"videos": [], "posts": []})
            key = "videos" if i["kind"] == "video" else "posts"
            months[i["month"]][key].append(i)
    ordered = sorted(months.keys(), reverse=True)
    mlist = []
    for mid in ordered:
        y, m = mid.split("-")
        label = MONTH_NAMES[int(m) - 1]
        b = months[mid]
        mlist.append({
            "id": mid, "label": label,
            "videos": [{"title": v["title"], "note": v["sub"], "drive": v["url"]}
                       for v in sorted(b["videos"], key=lambda x: (x["sort"], x["id"]))],
            "posts": [{"title": p["title"], "date": p["sub"], "platform": "", "link": p["url"]}
                      for p in sorted(b["posts"], key=lambda x: (x["sort"], x["id"]))],
        })
    docs = [{"title": d["title"], "kind": d["sub"] or "Document", "date": "", "href": d["url"]}
            for d in sorted([i for i in vis if i["kind"] == "doc"], key=lambda x: (x["sort"], x["id"]))]
    facts = [{"k": f["title"], "v": f["sub"]}
             for f in sorted([i for i in vis if i["kind"] == "fact"], key=lambda x: (x["sort"], x["id"]))]
    cfg = {
        "meta": {"slug": slug, "name": client["name"], "wa": client["wa"],
                 "pinHash": client["pin_hash"],
                 "updated": datetime.date.today().strftime("%-d %B %Y")},
        "theme": client.get("theme") or {},
        "copy": {"hello": client.get("hello") or ("Hello, " + client["name"] + "."),
                 "sub": "Everything we have produced for you, in one place."},
        "months": mlist, "docs": docs, "facts": facts, "beacon": None,
    }
    out = ROOT / "cfg" / (slug + ".js")
    out.write_text("/* cast by pull-month.py, do not hand-edit: edits belong in admin.html */\n"
                   "window.CFG=" + js(cfg) + ";\n")
    return out, len(vis)

def main():
    only = sys.argv[1] if len(sys.argv) > 1 else None
    clients = get("/bb_library_clients?select=*&active=eq.true" + ("&slug=eq." + only if only else ""))
    if not clients:
        print("REFUSED: no active client" + (" " + only if only else "s") + " in bb_library_clients."); sys.exit(1)
    items = get("/bb_library_items?select=*")
    for c in clients:
        out, n = cast(c, [i for i in items if i["client_slug"] == c["slug"]])
        print(f"{c['slug']:14s} {n:3d} items -> {out.name}")

if __name__ == "__main__":
    main()
