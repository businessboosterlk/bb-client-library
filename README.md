# BB Client Library

One private, persistent place per client for everything Business Booster has
produced for them. A library, not a portal.

- `index.html?c=<slug>` the client view. PIN curtain per client (salted hash only).
- `admin.html` the SM editor: add, hide and remove videos, posts, documents and
  business facts per client per month. No developer needed.
- `cfg/<slug>.js` static casts, rebuilt hourly by the workflow from
  `bb_library_items`. Never hand-edited.
- `scripts/new-cast.py` registers a client and mints their PIN, printed once.
- `scripts/check-casts.py` guards: leak scan, https links, style, no secrets.

Static casts only: no client browser ever reads the database. The library is
never the database of record; it bakes from the systems. Drive folders are
shared to the client's email, never anyone-with-link. A churned client is
deactivated in `bb_library_clients` and their PIN dies at the next rebuild.
