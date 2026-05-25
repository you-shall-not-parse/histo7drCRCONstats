# Hell Let Loose Community RCON (CRCON)

An extended RCON tool for [Hell Let Loose](https://www.hellletloose.com/), meant to replace the official tool and go WAY beyond.

## Historical Matches Only

This workspace has been slimmed for an archive-only deployment where CRCON serves completed match history without controlling a live HLL server.

- Use [docker-templates/history-only.yaml](docker-templates/history-only.yaml) as the deployment entrypoint.
- The backend runs with `HISTORY_ONLY=true` and serves public match data from PostgreSQL instead of live RCON.
- The public frontend is built from [Dockerfile-frontend-history](Dockerfile-frontend-history) and lands on `/games` by default.a
- The history-only deployment no longer starts websocket/channels services, does not seed a Django admin user, and only serves the public historical API over gunicorn.
- The active archive runtime now uses the archive-only `archive_core` package instead of importing the old `rcon` package.
- The legacy live-server `rcon` package, supervisor jobs, and related test suite are no longer part of the archive deployment path.
- The default reverse-proxy target is `7drhistostats.hllfrontline.com`
- The remaining frontend surface is the historical match site only; the old live current-game and streamer views are no longer part of this repo.