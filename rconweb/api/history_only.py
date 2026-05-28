import os
import re
from collections import Counter
from datetime import datetime
from functools import lru_cache

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from sqlalchemy import inspect

from archive_core.config import get_server_number, get_site_name
from archive_core.db import Maps, enter_session, get_engine
from archive_core.maps import parse_layer
from rconweb.settings import TAG_VERSION

from .decorators import require_http_methods


CLAN_TAG_MIN_PLAYERS = 10
CLAN_TAG_PATTERNS = (
    re.compile(r"^\[(?P<tag>[A-Za-z0-9]{2,8})\]\s*"),
    re.compile(r"^\((?P<tag>[A-Za-z0-9]{2,8})\)\s*"),
    re.compile(r"^(?P<tag>[A-Za-z0-9]{2,8})\s*[|/_-]\s*"),
    re.compile(r"^(?P<tag>[A-Z0-9]{2,8})\s+"),
)


def api_response(*, result=None, command: str, failed: bool, error=None, arguments=None, status_code=200):
    return JsonResponse(
        {
            "result": result,
            "command": command,
            "arguments": arguments,
            "failed": failed,
            "error": error,
            "forwards_results": None,
            "version": TAG_VERSION,
        },
        status=status_code,
    )


def _get_data(request):
    parsed_get = {}
    for key in request.GET.keys():
        values = request.GET.getlist(key)
        parsed_get[key] = values[0] if len(values) == 1 else values
    return parsed_get


def _normalize_result(result):
    if not result:
        return None

    allied = result.get("allied")
    axis = result.get("axis")

    if allied is None:
        allied = result.get("Allied")
    if axis is None:
        axis = result.get("Axis")

    if allied is None and axis is None:
        return None

    return {
        "allied": allied,
        "axis": axis,
    }


def _extract_clan_tag(player_name):
    if not player_name:
        return None

    stripped_name = player_name.strip()

    for pattern in CLAN_TAG_PATTERNS:
        match = pattern.match(stripped_name)
        if not match:
            continue

        tag = match.group("tag").upper()
        if not any(character.isalpha() for character in tag):
            return None
        return tag

    first_token = stripped_name.split()[0].strip("[](){}<>|/_-.:,")
    if 2 <= len(first_token) <= 8:
        normalized_token = first_token.upper()
        if any(character.isalpha() for character in normalized_token) and (
            any(character.isdigit() for character in normalized_token)
            or normalized_token == first_token
            or normalized_token == stripped_name[: len(first_token)].upper()
        ):
            return normalized_token

    return None


def _historical_name_sort_key(player_name_record):
    return player_name_record.last_seen or player_name_record.created or datetime.min


@lru_cache(maxsize=1)
def _has_player_soldier_table():
    try:
        return inspect(get_engine()).has_table("player_soldier")
    except Exception:
        return False


def _normalize_clan_tag_value(value):
    if not value:
        return None

    normalized = value.strip().upper()
    if not normalized or not any(character.isalpha() for character in normalized):
        return None
    return normalized


def _extract_player_clan_tag(player_stat, match_start=None):
    player = getattr(player_stat, "player", None)
    if _has_player_soldier_table() and player is not None:
        soldier = getattr(player, "soldier", None)
        direct_soldier_tag = _normalize_clan_tag_value(getattr(soldier, "clan_tag", None))
        if direct_soldier_tag:
            return direct_soldier_tag

    direct_tag = _extract_clan_tag(getattr(player_stat, "player_name", None))
    if direct_tag:
        return direct_tag

    player_names = getattr(player, "names", None) or []
    if not player_names:
        return None

    candidate_names = sorted(player_names, key=_historical_name_sort_key, reverse=True)
    if match_start is not None:
        dated_candidates = []
        undated_candidates = []
        for candidate in candidate_names:
            candidate_time = candidate.last_seen or candidate.created
            if candidate_time is None:
                undated_candidates.append(candidate)
            elif candidate_time <= match_start:
                dated_candidates.append(candidate)
        candidate_names = dated_candidates or undated_candidates or candidate_names

    for candidate in candidate_names:
        tag = _extract_clan_tag(candidate.name)
        if tag:
            return tag

    return None


def _build_clan_match(player_stats, match_start=None):
    tag_counts = Counter()
    for player_stat in player_stats:
        tag = _extract_player_clan_tag(player_stat, match_start)
        if tag:
            tag_counts[tag] += 1

    clans = [
        {"tag": tag, "count": count}
        for tag, count in tag_counts.most_common()
        if count >= CLAN_TAG_MIN_PLAYERS
    ]

    return {
        "detected": len(clans) >= 2,
        "clans": clans,
    }


def _get_latest_map(server_number: int | str | None):
    with enter_session() as sess:
        query = sess.query(Maps).order_by(Maps.start.desc())
        if server_number is not None:
            query = query.filter(Maps.server_number == server_number)

        latest_map = query.first()
        if latest_map is not None or server_number is None:
            return latest_map

        return sess.query(Maps).order_by(Maps.start.desc()).first()


@csrf_exempt
@require_http_methods(["GET"])
def get_public_info(request):
    server_number = get_server_number()
    short_name, display_name = get_site_name(server_number)
    latest_map = _get_latest_map(server_number)
    latest_layer = parse_layer(latest_map.map_name) if latest_map else None
    latest_start = latest_map.start.timestamp() if latest_map else None
    latest_result = _normalize_result(latest_map.result) or {}

    public_stats_port = os.getenv("PUBLIC_STATS_PORT", None)
    public_stats_port_https = os.getenv("PUBLIC_STATS_PORT_HTTPS", None)

    return api_response(
        result={
            "current_map": {"map": latest_layer, "start": latest_start},
            "next_map": {"map": latest_layer, "start": None},
            "player_count": 0,
            "max_player_count": 0,
            "player_count_by_team": {"allied": 0, "axis": 0},
            "score": {
                "allied": latest_result.get("allied", 0),
                "axis": latest_result.get("axis", 0),
            },
            "time_remaining": 0,
            "vote_status": [],
            "name": {
                "name": display_name,
                "short_name": short_name,
                "public_stats_port": int(public_stats_port) if public_stats_port else None,
                "public_stats_port_https": int(public_stats_port_https) if public_stats_port_https else None,
            },
        },
        command="get_public_info",
        failed=False,
    )


@csrf_exempt
@require_http_methods(["GET"])
def get_scoreboard_maps(request):
    data = _get_data(request)

    page_size = min(int(data.get("limit", 100)), 1000)
    page = max(1, int(data.get("page", 1)))
    server_number = data.get("server_number", os.getenv("SERVER_NUMBER"))

    with enter_session() as sess:
        query = (
            sess.query(Maps)
            .filter(Maps.server_number == server_number)
            .order_by(Maps.start.desc())
        )
        total = query.count()
        rows = query.limit(page_size).offset((page - 1) * page_size).all()

        maps = []
        for row in rows:
            payload = row.to_dict()
            maps.append(
                {
                    "map": parse_layer(payload["map_name"]),
                    "id": payload["id"],
                    "creation_time": payload["creation_time"],
                    "start": payload["start"],
                    "end": payload["end"],
                    "server_number": payload["server_number"],
                    "player_stats": payload["player_stats"],
                    "result": _normalize_result(payload["result"]),
                    "game_layout": payload["game_layout"],
                    "clan_match": _build_clan_match(row.player_stats, row.start),
                }
            )

    return api_response(
        result={
            "page": page,
            "page_size": page_size,
            "total": total,
            "maps": maps,
        },
        command="get_scoreboard_maps",
        failed=False,
    )


@csrf_exempt
@require_http_methods(["GET"])
def get_map_scoreboard(request):
    data = _get_data(request)

    try:
        map_id = int(data.get("map_id", None))
        with enter_session() as sess:
            game = sess.query(Maps).filter(Maps.id == map_id).one_or_none()

        if not game:
            return api_response(
                result=None,
                arguments=data,
                error="No map for this ID",
                failed=True,
                command="get_map_scoreboard",
            )

        payload = game.to_dict(with_stats=True)
        payload["map"] = parse_layer(payload["map_name"])
        payload["result"] = _normalize_result(payload.get("result"))
        payload["clan_match"] = _build_clan_match(game.player_stats, game.start)
        return api_response(
            result=payload,
            arguments=data,
            failed=False,
            command="get_map_scoreboard",
        )
    except Exception as exc:
        return api_response(
            result=None,
            arguments=data,
            error=repr(exc),
            failed=True,
            command="get_map_scoreboard",
        )
