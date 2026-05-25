from __future__ import annotations

import re
from typing import Any

TEAM_ALLIES = "allies"
TEAM_AXIS = "axis"
ENV_DAY = "day"

RE_LAYER_NAME_LARGE = re.compile(
    r"^(?P<tag>[A-Za-z]+)(?:_(?P<year>\d{4}))?(?:_(?P<environment>Day|Night|Dawn|Dusk|Rain|Overcast|Morning))?_P_(?P<game_mode>Warfare|Offensive|Skirmish|Phased|Majority)(?:_(?P<attackers>US|GER|RUS|GB|CW|CAN))?$",
    re.IGNORECASE,
)
RE_LAYER_NAME_SMALL = re.compile(
    r"^(?P<tag>[A-Za-z]{3})_(?P<game_mode>WARFARE|OFFENSIVE|SKIRMISH)(?P<attackers>US|GER|RUS|GB|CW|CAN)?(?:_(?P<environment>DAY|NIGHT|DAWN|DUSK|RAIN|OVERCAST))?$",
    re.IGNORECASE,
)
RE_LEGACY_LAYER_NAME = re.compile(
    r"^(?P<name>[A-Za-z0-9]+?)(?:_(?:(?P<offensive>offensive)(?P<attackers>us|ger|rus|gb|cw|can)?|(?P<game_mode>warfare|skirmish|phased|majority))(?P<environment>_night|_dusk|_dawn|_rain|_overcast)?)?$",
    re.IGNORECASE,
)

MAPS: dict[str, dict[str, Any]] = {
    "unknown": {
        "id": "unknown",
        "name": "Unknown",
        "tag": "UNKNOWN",
        "pretty_name": "Unknown",
        "shortname": "Unknown",
        "allies": {"name": "us", "team": TEAM_ALLIES},
        "axis": {"name": "ger", "team": TEAM_AXIS},
    },
    "stmereeglise": {
        "id": "stmereeglise",
        "name": "SAINTE-MERE-EGLISE",
        "tag": "SME",
        "pretty_name": "St. Mere Eglise",
        "shortname": "SME",
        "allies": {"name": "us", "team": TEAM_ALLIES},
        "axis": {"name": "ger", "team": TEAM_AXIS},
    },
    "stmariedumont": {
        "id": "stmariedumont",
        "name": "SAINTE-MARIE-DU-MONT",
        "tag": "SMDM",
        "pretty_name": "St. Marie Du Mont",
        "shortname": "SMDM",
        "allies": {"name": "us", "team": TEAM_ALLIES},
        "axis": {"name": "ger", "team": TEAM_AXIS},
    },
    "utahbeach": {
        "id": "utahbeach",
        "name": "UTAH BEACH",
        "tag": "UTA",
        "pretty_name": "Utah Beach",
        "shortname": "Utah",
        "allies": {"name": "us", "team": TEAM_ALLIES},
        "axis": {"name": "ger", "team": TEAM_AXIS},
    },
    "omahabeach": {
        "id": "omahabeach",
        "name": "OMAHA BEACH",
        "tag": "OMA",
        "pretty_name": "Omaha Beach",
        "shortname": "Omaha",
        "allies": {"name": "us", "team": TEAM_ALLIES},
        "axis": {"name": "ger", "team": TEAM_AXIS},
    },
    "purpleheartlane": {
        "id": "purpleheartlane",
        "name": "PURPLE HEART LANE",
        "tag": "PHL",
        "pretty_name": "Purple Heart Lane",
        "shortname": "PHL",
        "allies": {"name": "us", "team": TEAM_ALLIES},
        "axis": {"name": "ger", "team": TEAM_AXIS},
    },
    "carentan": {
        "id": "carentan",
        "name": "CARENTAN",
        "tag": "CAR",
        "pretty_name": "Carentan",
        "shortname": "Carentan",
        "allies": {"name": "us", "team": TEAM_ALLIES},
        "axis": {"name": "ger", "team": TEAM_AXIS},
    },
    "hurtgenforest": {
        "id": "hurtgenforest",
        "name": "HURTGEN FOREST",
        "tag": "HUR",
        "pretty_name": "Hurtgen Forest",
        "shortname": "Hurtgen",
        "allies": {"name": "us", "team": TEAM_ALLIES},
        "axis": {"name": "ger", "team": TEAM_AXIS},
    },
    "hill400": {
        "id": "hill400",
        "name": "HILL 400",
        "tag": "HIL",
        "pretty_name": "Hill 400",
        "shortname": "Hill 400",
        "allies": {"name": "us", "team": TEAM_ALLIES},
        "axis": {"name": "ger", "team": TEAM_AXIS},
    },
    "foy": {
        "id": "foy",
        "name": "FOY",
        "tag": "FOY",
        "pretty_name": "Foy",
        "shortname": "Foy",
        "allies": {"name": "us", "team": TEAM_ALLIES},
        "axis": {"name": "ger", "team": TEAM_AXIS},
    },
    "kursk": {
        "id": "kursk",
        "name": "KURSK",
        "tag": "KUR",
        "pretty_name": "Kursk",
        "shortname": "Kursk",
        "allies": {"name": "rus", "team": TEAM_ALLIES},
        "axis": {"name": "ger", "team": TEAM_AXIS},
    },
    "stalingrad": {
        "id": "stalingrad",
        "name": "STALINGRAD",
        "tag": "STA",
        "pretty_name": "Stalingrad",
        "shortname": "Stalingrad",
        "allies": {"name": "rus", "team": TEAM_ALLIES},
        "axis": {"name": "ger", "team": TEAM_AXIS},
    },
    "remagen": {
        "id": "remagen",
        "name": "REMAGEN",
        "tag": "REM",
        "pretty_name": "Remagen",
        "shortname": "Remagen",
        "allies": {"name": "us", "team": TEAM_ALLIES},
        "axis": {"name": "ger", "team": TEAM_AXIS},
    },
    "kharkov": {
        "id": "kharkov",
        "name": "KHARKOV",
        "tag": "KHA",
        "pretty_name": "Kharkov",
        "shortname": "Kharkov",
        "allies": {"name": "rus", "team": TEAM_ALLIES},
        "axis": {"name": "ger", "team": TEAM_AXIS},
    },
    "driel": {
        "id": "driel",
        "name": "DRIEL",
        "tag": "DRL",
        "pretty_name": "Driel",
        "shortname": "Driel",
        "allies": {"name": "gb", "team": TEAM_ALLIES},
        "axis": {"name": "ger", "team": TEAM_AXIS},
    },
    "elalamein": {
        "id": "elalamein",
        "name": "EL ALAMEIN",
        "tag": "ELA",
        "pretty_name": "El Alamein",
        "shortname": "Alamein",
        "allies": {"name": "gb", "team": TEAM_ALLIES},
        "axis": {"name": "ger", "team": TEAM_AXIS},
    },
    "mortain": {
        "id": "mortain",
        "name": "MORTAIN",
        "tag": "MOR",
        "pretty_name": "Mortain",
        "shortname": "Mortain",
        "allies": {"name": "us", "team": TEAM_ALLIES},
        "axis": {"name": "ger", "team": TEAM_AXIS},
    },
    "elsenbornridge": {
        "id": "elsenbornridge",
        "name": "ELSENBORN RIDGE",
        "tag": "EBR",
        "pretty_name": "Elsenborn Ridge",
        "shortname": "Elsenborn",
        "allies": {"name": "us", "team": TEAM_ALLIES},
        "axis": {"name": "ger", "team": TEAM_AXIS},
    },
    "tobruk": {
        "id": "tobruk",
        "name": "TOBRUK",
        "tag": "TBK",
        "pretty_name": "Tobruk",
        "shortname": "Tobruk",
        "allies": {"name": "gb", "team": TEAM_ALLIES},
        "axis": {"name": "ger", "team": TEAM_AXIS},
    },
    "smolensk": {
        "id": "smolensk",
        "name": "SMOLENSK",
        "tag": "SMO",
        "pretty_name": "Smolensk",
        "shortname": "Smolensk",
        "allies": {"name": "rus", "team": TEAM_ALLIES},
        "axis": {"name": "ger", "team": TEAM_AXIS},
    },
    "junobeach": {
        "id": "junobeach",
        "name": "JUNO BEACH",
        "tag": "JUN",
        "pretty_name": "Juno Beach",
        "shortname": "Juno",
        "allies": {"name": "gb", "team": TEAM_ALLIES},
        "axis": {"name": "ger", "team": TEAM_AXIS},
    },
}

TAG_TO_MAP_ID = {value["tag"].lower(): key for key, value in MAPS.items()}


def _normalize_environment(value: str | None) -> str:
    if not value:
        return ENV_DAY

    lowered = value.lower().lstrip("_")
    if lowered == "morning":
        return "dawn"
    return lowered


ATTACKER_TO_TEAM = {
    "us": TEAM_ALLIES,
    "rus": TEAM_ALLIES,
    "gb": TEAM_ALLIES,
    "cw": TEAM_ALLIES,
    "can": TEAM_ALLIES,
    "ger": TEAM_AXIS,
}


def _map_from_name(name: str) -> dict[str, Any]:
    lowered = name.lower()
    if lowered in MAPS:
        return MAPS[lowered]
    if lowered in TAG_TO_MAP_ID:
        return MAPS[TAG_TO_MAP_ID[lowered]]

    return {
        "id": lowered,
        "name": name.upper(),
        "tag": name[:3].upper(),
        "pretty_name": name.replace("_", " ").title(),
        "shortname": name.replace("_", " ").title(),
        "allies": {"name": "us", "team": TEAM_ALLIES},
        "axis": {"name": "ger", "team": TEAM_AXIS},
    }


def _build_layer(layer_id: str, map_data: dict[str, Any], game_mode: str, attackers: str | None, environment: str) -> dict[str, Any]:
    pretty_bits = [map_data["pretty_name"], game_mode.title()]
    if game_mode == "offensive" and attackers:
        pretty_bits.append("Off. " + attackers.title())
    if environment != ENV_DAY:
        pretty_bits.append(environment.title())

    return {
        "id": layer_id,
        "map": map_data,
        "game_mode": game_mode,
        "attackers": attackers,
        "environment": environment,
        "pretty_name": " ".join(pretty_bits),
        "image_name": f"{map_data['id']}-{environment}.webp",
    }


def parse_layer(layer_name: str | dict[str, Any]) -> dict[str, Any]:
    if isinstance(layer_name, dict):
        return layer_name

    if not layer_name or "loading" in layer_name.lower():
        return _build_layer("unknown", MAPS["unknown"], "warfare", None, ENV_DAY)

    layer_match = RE_LAYER_NAME_LARGE.match(layer_name) or RE_LAYER_NAME_SMALL.match(layer_name)
    if layer_match:
        layer_data = layer_match.groupdict()
        map_data = _map_from_name(layer_data["tag"])
        game_mode = (layer_data.get("game_mode") or "warfare").lower()
        attackers = ATTACKER_TO_TEAM.get((layer_data.get("attackers") or "").lower()) if game_mode == "offensive" else None
        environment = _normalize_environment(layer_data.get("environment"))
        return _build_layer(layer_name, map_data, game_mode, attackers, environment)

    legacy_match = RE_LEGACY_LAYER_NAME.match(layer_name)
    if legacy_match:
        layer_data = legacy_match.groupdict()
        map_data = _map_from_name(layer_data["name"])
        if layer_data.get("offensive"):
            game_mode = "offensive"
            attackers = ATTACKER_TO_TEAM.get((layer_data.get("attackers") or "").lower())
        else:
            game_mode = (layer_data.get("game_mode") or "warfare").lower()
            attackers = None

        environment = _normalize_environment(layer_data.get("environment"))
        return _build_layer(layer_name, map_data, game_mode, attackers, environment)

    map_data = _map_from_name(layer_name)
    return _build_layer(layer_name, map_data, "warfare", None, ENV_DAY)
