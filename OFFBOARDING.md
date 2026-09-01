# Offboarding a Client Library, same day

Open since the system was built, written 1 September 2026. The rule comes
from LGL: the freeze happens the day you hear, not the day it is convenient.

There is no password on a library. The wall is the Drive sharing and the fact
that nobody outside knows the slug. So offboarding is mostly about taking the
Drive access away and taking the page down, in that order.

## The five steps

**1. Unshare the Drive folders. Do this first.**
Every video link in their library points at Drive. Removing their email from
those folders is the only step that actually removes access to the work. The
library page is just a list of links: killing the page while the folders stay
shared removes the shelf, not the content.

**2. Mark them inactive in the backend.**
In Supabase, `bb_library_clients`, set `active` to false for their slug. The
caster only builds active clients, so their cast stops being rebuilt from the
next hourly run.

```sql
update bb_library_clients set active = false where slug = '<slug>';
```

**3. Delete their cast and their manifest from the repo.**

```bash
cd ~/bb-websites/bb-client-library
git rm cfg/<slug>.js cfg/<slug>.webmanifest
python3 scripts/check-casts.py
git commit -m "Offboard <name>" && git push
```

The guard must stay green after the removal. Once the files are gone the URL
returns 404. The service worker purges its cached copy on that 404, so
even a client who installed the app to their phone loses the library the next
time they open it online.

**4. Leave their rows in `bb_library_items` alone.**
Deleting the items destroys the record of what BB produced for them, which is
worth keeping for the case file and for any dispute about what was delivered.
Inactive plus no cast is enough: nothing renders.

**5. Note the date in their client memory file.**
`~/.claude/projects/-Users-thulaibhassen/memory/<client>.md`, with the date
you heard and the date you froze. LGL churned on 1 September and that date
being written down is what stops a future session treating them as live.

## What NOT to do

- Do not delete the client row. The events in `bb_library_events` reference
  the slug. Those visits are the only record of whether the library ever
  worked for them. That evidence outlives the account.
- Do not rotate a PIN. Libraries have carried no password since
  1 September 2026, so there is nothing to rotate. If you find a cast with a
  `pinHash` in it, that cast is out of date, not more secure.
- Do not tell a client the library is deleted while their Drive folders are
  still shared. That is the one statement in this runbook that would be untrue.

## Checking it worked

```bash
curl -o /dev/null -s -w "%{http_code}\n" \
  https://businessboosterlk.github.io/bb-client-library/?c=<slug>
```

A cast that is gone leaves the master loading its fallback, so also confirm
`cfg/<slug>.js` itself returns 404:

```bash
curl -o /dev/null -s -w "%{http_code}\n" \
  https://businessboosterlk.github.io/bb-client-library/cfg/<slug>.js
```

404 on the cast is the proof. Anything else means the file is still deployed.

## First real use

Nobody has been offboarded from the Client Library yet. When the first one
happens, run this, then correct whatever was wrong here while it is fresh.
A runbook that has never been run is a draft.
