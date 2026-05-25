# Hell Let Loose Community RCON (CRCON)

An extended RCON tool for [Hell Let Loose](https://www.hellletloose.com/), meant to replace the official tool and go WAY beyond.

## Historical Matches Only

This workspace has been slimmed for an archive-only deployment where CRCON serves completed match history without controlling a live HLL server.

- Use [docker-templates/history-only.yaml](docker-templates/history-only.yaml) as the deployment entrypoint.
- The backend runs with `HISTORY_ONLY=true` and serves public match data from PostgreSQL instead of live RCON.
- The public frontend is built from [Dockerfile-frontend-history](Dockerfile-frontend-history) and lands on `/games` by default.
- The history-only deployment no longer starts websocket/channels services, does not seed a Django admin user, and only serves the public historical API over gunicorn.
- The active archive runtime now uses the archive-only `archive_core` package instead of importing the old `rcon` package.
- The legacy live-server `rcon` package, supervisor jobs, and related test suite are no longer part of the archive deployment path.
- The default reverse-proxy target is `7drstats.hllfrontline.com`, with the frontend bound to `127.0.0.1` so Caddy can front it safely.
- The remaining frontend surface is the historical match site only; the old live current-game and streamer views are no longer part of this repo.

## Caddy Subdomain

To serve the archive on `7drstats.hllfrontline.com`, point your reverse proxy at the frontend port from [default.env](default.env).

Example Caddy block:

```caddyfile
www.7drstats.hllfrontline.com {
	redir https://7drstats.hllfrontline.com{uri} permanent
}

7drstats.hllfrontline.com {
	encode zstd gzip

	log {
		output file /var/log/caddy/7drstats.access.log {
			roll_size 10MiB
			roll_keep 10
			roll_keep_for 720h
		}
		format console
	}

	reverse_proxy 127.0.0.1:7010
}
```

## Historical Data Import

This site does not read a standalone stats file from a watched folder. Historical matches are read directly from PostgreSQL using `HLL_DB_URL`.

- If you receive a PostgreSQL dump (`.sql`, `.dump`, or `pg_dump` output), restore it into the database configured by `HLL_DB_NAME`, `HLL_DB_USER`, `HLL_DB_HOST`, and `HLL_DB_HOST_PORT`.
- In the Docker template, that target is the `postgres` service defined in [docker-templates/history-only.yaml](docker-templates/history-only.yaml).
- The minimum tables needed for the match list and match detail pages are `map_history`, `player_stats`, and `steam_id_64`.
- If you also want Steam profile and ban metadata to appear on player rows, restore `steam_info` as well.
- If the source arrives as CSV or JSON instead of a PostgreSQL dump, it still has to be imported into those PostgreSQL tables. There is no runtime file drop location for raw match data.

Examples:

```bash
docker compose -f docker-templates/history-only.yaml exec -T postgres \
	psql -U "$HLL_DB_USER" -d "$HLL_DB_NAME" < historical-matches.sql
```

```bash
docker compose -f docker-templates/history-only.yaml exec -T postgres \
	pg_restore -U "$HLL_DB_USER" -d "$HLL_DB_NAME" /backups/historical-matches.dump
```