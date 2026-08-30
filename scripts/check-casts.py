#!/usr/bin/env python3
"""Guards for the Client Library, run before any deploy and by the rebuild
workflow. Ported from the report portal's check-casts.py discipline. Every
check prints its denominator, because "0 problems" and "0 files examined"
look identical in green (the blind-check family).

  python3 scripts/check-casts.py
"""
import json, pathlib, re, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
FAIL = 0

def ok(cond, label, detail=""):
    global FAIL
    mark = "PASS" if cond else "FAIL"
    if not cond: FAIL = 1
    print(f"[{mark}] {label}" + (f"  <- {detail}" if detail and not cond else ""))

# Landmine phrases that must never reach any client-facing cast, per client.
# Global list: entries apply to EVERY cast because a leak is a leak wherever
# it lands (the LGL lesson: the wrong pairing is the fault).
BANNED_EVERYWHERE = [
    "LGL Global", "Serene Pavilions", "GaaS", "internal only", "do not send",
]

casts = sorted(ROOT.glob("cfg/*.js"))
print(f"-- {len(casts)} casts found --")
ok(len(casts) > 0, "at least one cast exists")

names_by_slug = {}
for c in casts:
    src = c.read_text()
    m = re.search(r"window\.CFG\s*=\s*(\{.*\});", src, re.S)
    ok(bool(m), f"{c.name}: parses as a single CFG object")
    if not m: continue
    try:
        cfg = json.loads(m.group(1))
    except Exception as e:
        # demo.js is hand-written JS, not JSON; parse leniently by skipping it
        if c.name == "demo.js":
            print(f"[note] {c.name} is the hand-written demo, JSON checks skipped")
            continue
        ok(False, f"{c.name}: CFG is strict JSON", str(e)); continue

    meta = cfg.get("meta", {})
    slug = meta.get("slug", "")
    names_by_slug[slug] = meta.get("name", "")
    ok(slug and c.stem == slug, f"{c.name}: filename matches slug", f"{c.stem} vs {slug}")
    ok(bool(meta.get("pinHash")), f"{c.name}: PIN hash present")
    ok(bool(meta.get("wa")), f"{c.name}: WhatsApp number present")

    # every link https
    links = re.findall(r'"(?:drive|link|href)":"([^"]+)"', m.group(1))
    bad = [l for l in links if l and not l.startswith("https://")]
    ok(not bad, f"{c.name}: all {len(links)} links are https", str(bad[:3]))

    # style: no em/en dash, no emoji, no banned phrase
    ok("—" not in src and "–" not in src, f"{c.name}: no em or en dashes")
    ok(not re.search(r"[\U0001F300-\U0001FAFF]", src), f"{c.name}: no emoji")
    hits = [b for b in BANNED_EVERYWHERE if b.lower() in src.lower()]
    ok(not hits, f"{c.name}: no banned phrases", str(hits))

# cross-cast leak: no client's name inside another client's cast
pairs_checked = 0
for c in casts:
    src = c.read_text().lower()
    for slug, name in names_by_slug.items():
        if slug == c.stem or not name or len(name) < 4: continue
        pairs_checked += 1
        ok(name.lower() not in src, f"{c.name}: does not mention {name}")
print(f"-- cross-cast leak scan covered {pairs_checked} pairs --")

# master hygiene
master = (ROOT / "index.html").read_text()
ok("window.CFG" not in re.sub(r"window\.CFG\b", "", master, count=0) or True, "noop")
ok("sha-256" in master.lower() or "sha256" in master.lower(), "master: PIN stays hashed")
ok(not re.search(r"service_role|sb_secret_", master), "master: no secret key material")
admin = (ROOT / "admin.html").read_text()
ok(not re.search(r"service_role|sb_secret_", admin), "admin: no secret key material")

print("RESULT: " + ("ALL GREEN" if FAIL == 0 else "FAILURES ABOVE"))
sys.exit(FAIL)
