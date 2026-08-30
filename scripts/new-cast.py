#!/usr/bin/env python3
# Scaffold a new Client Library client. Registers the row, mints a fresh PIN,
# prints it ONCE (only the salted hash is stored anywhere), casts the empty
# library. After this, everything is the SM's admin surface.
#
#   python3 scripts/new-cast.py <slug> "<Client Name>" <wa-digits> [#brand]
import hashlib, json, secrets, subprocess, sys, urllib.request, pathlib

BASE = "https://yyviiwnqgphyklcoijyd.supabase.co/rest/v1"
KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Inl5dmlpd25xZ3BoeWtsY29panlkIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzU3MjE5OTEsImV4cCI6MjA5MTI5Nzk5MX0.I8YiBr-rfLVcc6DE8Z1PxEP2oxXCelv6mxqAY_wY7lc"

def main():
    if len(sys.argv) < 4:
        print('usage: new-cast.py <slug> "<Client Name>" <wa-digits> [#brand]'); sys.exit(2)
    slug, name, wa = sys.argv[1], sys.argv[2], sys.argv[3]
    brand = sys.argv[4] if len(sys.argv) > 4 else "#2563eb"
    if not slug.replace("-", "").isalnum() or slug != slug.lower():
        print("REFUSED: slug must be lowercase letters, digits and dashes."); sys.exit(1)
    if not wa.isdigit() or len(wa) < 11:
        print("REFUSED: WhatsApp number as digits with country code, like 9476XXXXXXX."); sys.exit(1)
    pin = "".join(secrets.choice("0123456789") for _ in range(4))
    pin_hash = hashlib.sha256((pin + ":" + slug).encode()).hexdigest()
    body = json.dumps({"slug": slug, "name": name, "wa": wa, "pin_hash": pin_hash,
                       "theme": {"brand": brand}}).encode()
    req = urllib.request.Request(BASE + "/bb_library_clients", data=body, method="POST",
        headers={"apikey": KEY, "Authorization": "Bearer " + KEY,
                 "Content-Type": "application/json", "Prefer": "resolution=merge-duplicates"})
    urllib.request.urlopen(req, timeout=30).read()
    here = pathlib.Path(__file__).resolve().parent
    subprocess.run([sys.executable, str(here / "pull-month.py"), slug], check=True)
    print(f"\n{name} is registered and cast.")
    print(f"THE CLIENT'S CODE IS {pin} . Send it to them on WhatsApp yourself.")
    print("It is stored nowhere. Losing it means running rotate (re-run new-cast).")

if __name__ == "__main__":
    main()
