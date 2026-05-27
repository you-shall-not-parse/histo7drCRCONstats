from __future__ import annotations

import os
from contextlib import contextmanager
from datetime import datetime, timezone
from typing import Any

from sqlalchemy import JSON, DateTime, ForeignKey, Integer, String, create_engine
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, foreign, mapped_column, relationship
from sqlalchemy.pool import NullPool

from .maps import TEAM_ALLIES, TEAM_AXIS
from .weapons import ALL_WEAPONS, WEAPON_SIDE_MAP

DB_ADDRESS = os.getenv("HLL_DB_HOST", "db")
DB_NAME = os.getenv("HLL_DB_NAME", "db")
DB_USER = os.getenv("HLL_DB_USER", "db_user")
DB_PASSWORD = os.getenv("HLL_DB_PASSWORD", "password")
DB_PORT = os.getenv("HLL_DB_HOST_PORT", "5432")
DISABLE_POOL = os.getenv("HLL_DB_DISABLE_CONNECTION_POOL", "")


class Base(DeclarativeBase):
    type_annotation_map = {
        dict[str, Any]: JSONB,
        dict: JSONB,
    }


_ENGINE = None


def get_engine(force_reinit: bool = False):
    global _ENGINE

    if _ENGINE is not None and not force_reinit:
        return _ENGINE

    kwargs: dict[str, Any] = {}
    if DISABLE_POOL:
        kwargs["poolclass"] = NullPool

    _ENGINE = create_engine(
        f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_ADDRESS}:{DB_PORT}/{DB_NAME}",
        **kwargs,
    )
    return _ENGINE


@contextmanager
def enter_session() -> Session:
    session = Session(get_engine(), expire_on_commit=False)
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


def _as_utc(value: datetime | None) -> str | None:
    if value is None:
        return None
    if value.tzinfo is None:
        value = value.replace(tzinfo=timezone.utc)
    return value.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")


def _categorize_weapon_usage(data: dict[str, int] | None) -> dict[str, int]:
    totals: dict[str, int] = {}
    for weapon_name, count in (data or {}).items():
        weapon_type = ALL_WEAPONS.get(weapon_name)
        if weapon_type is None:
            continue
        totals[weapon_type.value] = totals.get(weapon_type.value, 0) + count
    return totals


def _detect_team(kills_by_weapon: dict[str, int] | None, deaths_by_weapon: dict[str, int] | None) -> dict[str, str]:
    scores = {
        TEAM_ALLIES: 0,
        TEAM_AXIS: 0,
    }

    for data in (kills_by_weapon or {}, deaths_by_weapon or {}):
        for weapon_name, count in data.items():
            side = WEAPON_SIDE_MAP.get(weapon_name)
            if side is None:
                continue
            scores[side] += count

    if scores[TEAM_ALLIES] == 0 and scores[TEAM_AXIS] == 0:
        return {"side": "unknown", "confidence": "mixed"}
    if scores[TEAM_ALLIES] == scores[TEAM_AXIS]:
        return {"side": TEAM_ALLIES, "confidence": "mixed"}

    side = TEAM_ALLIES if scores[TEAM_ALLIES] > scores[TEAM_AXIS] else TEAM_AXIS
    confidence = "strong" if abs(scores[TEAM_ALLIES] - scores[TEAM_AXIS]) >= 2 else "mixed"
    return {"side": side, "confidence": confidence}


class PlayerID(Base):
    __tablename__ = "steam_id_64"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    player_id: Mapped[str] = mapped_column("steam_id_64", String, unique=True)
    steaminfo: Mapped["SteamInfo | None"] = relationship(
        back_populates="player",
        uselist=False,
        primaryjoin=lambda: PlayerID.id == foreign(SteamInfo.playersteamid_id),
    )


class SteamInfo(Base):
    __tablename__ = "steam_info"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    playersteamid_id: Mapped[int] = mapped_column(ForeignKey("steam_id_64.id"), unique=True)
    created: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    updated: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    profile: Mapped[dict[str, Any] | None] = mapped_column(JSONB, nullable=True)
    country: Mapped[str | None] = mapped_column(String, nullable=True)
    bans: Mapped[dict[str, Any] | None] = mapped_column(JSONB, nullable=True)

    player: Mapped[PlayerID] = relationship(
        back_populates="steaminfo",
        primaryjoin=lambda: foreign(SteamInfo.playersteamid_id) == PlayerID.id,
    )

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "created": _as_utc(self.created),
            "updated": _as_utc(self.updated),
            "profile": self.profile,
            "country": self.country,
            "bans": self.bans,
            "has_bans": bool(self.bans),
        }


class Maps(Base):
    __tablename__ = "map_history"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    creation_time: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    start: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    end: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    server_number: Mapped[int | None] = mapped_column(Integer, nullable=True)
    map_name: Mapped[str] = mapped_column(String)
    result: Mapped[dict[str, Any] | None] = mapped_column(JSONB, nullable=True)
    game_layout: Mapped[dict[str, Any] | None] = mapped_column(JSONB, nullable=True)

    player_stats: Mapped[list["PlayerStats"]] = relationship(back_populates="map", lazy="selectin")

    def to_dict(self, with_stats: bool = False) -> dict[str, Any]:
        payload = {
            "id": self.id,
            "creation_time": _as_utc(self.creation_time),
            "start": _as_utc(self.start),
            "end": _as_utc(self.end),
            "server_number": self.server_number,
            "map_name": self.map_name,
            "result": self.result or {},
            "game_layout": self.game_layout,
            "player_stats": None,
        }
        if with_stats:
            payload["player_stats"] = [player.to_dict() for player in self.player_stats]
        return payload


class PlayerStats(Base):
    __tablename__ = "player_stats"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    playersteamid_id: Mapped[int] = mapped_column(ForeignKey("steam_id_64.id"))
    player: Mapped[PlayerID] = relationship(lazy="joined")
    map_id: Mapped[int] = mapped_column(ForeignKey("map_history.id"))
    map: Mapped[Maps] = relationship(back_populates="player_stats")

    player_name: Mapped[str | None] = mapped_column("name", String, nullable=True)
    kills: Mapped[int] = mapped_column(Integer, default=0)
    kills_streak: Mapped[int] = mapped_column(Integer, default=0)
    deaths: Mapped[int] = mapped_column(Integer, default=0)
    deaths_without_kill_streak: Mapped[int] = mapped_column(Integer, default=0)
    teamkills: Mapped[int] = mapped_column(Integer, default=0)
    teamkills_streak: Mapped[int] = mapped_column(Integer, default=0)
    deaths_by_tk: Mapped[int] = mapped_column(Integer, default=0)
    deaths_by_tk_streak: Mapped[int] = mapped_column(Integer, default=0)
    nb_vote_started: Mapped[int] = mapped_column(Integer, default=0)
    nb_voted_yes: Mapped[int] = mapped_column(Integer, default=0)
    nb_voted_no: Mapped[int] = mapped_column(Integer, default=0)
    time_seconds: Mapped[int] = mapped_column(Integer, default=0)
    kills_per_minute: Mapped[int | float | None] = mapped_column(JSON, nullable=True)
    deaths_per_minute: Mapped[int | float | None] = mapped_column(JSON, nullable=True)
    kill_death_ratio: Mapped[int | float | None] = mapped_column(JSON, nullable=True)
    longest_life_secs: Mapped[int] = mapped_column(Integer, default=0)
    shortest_life_secs: Mapped[int] = mapped_column(Integer, default=0)
    combat: Mapped[int] = mapped_column(Integer, default=0)
    offense: Mapped[int] = mapped_column(Integer, default=0)
    defense: Mapped[int] = mapped_column(Integer, default=0)
    support: Mapped[int] = mapped_column(Integer, default=0)
    most_killed: Mapped[dict[str, int]] = mapped_column(JSONB, default=dict)
    death_by: Mapped[dict[str, int]] = mapped_column(JSONB, default=dict)
    weapons: Mapped[dict[str, int]] = mapped_column(JSONB, default=dict)
    death_by_weapons: Mapped[dict[str, int] | None] = mapped_column(JSONB, nullable=True)
    level: Mapped[int] = mapped_column(Integer, default=0)

    def to_dict(self) -> dict[str, Any]:
        player_id = self.player.player_id if self.player else None
        return {
            "id": self.id,
            "player_id": player_id,
            "steam_id_64": player_id,
            "player": self.player_name,
            "steaminfo": self.player.steaminfo.to_dict() if self.player and self.player.steaminfo else None,
            "map_id": self.map_id,
            "kills": self.kills,
            "kills_streak": self.kills_streak,
            "kills_by_type": _categorize_weapon_usage(self.weapons),
            "deaths": self.deaths,
            "deaths_by_type": _categorize_weapon_usage(self.death_by_weapons),
            "deaths_without_kill_streak": self.deaths_without_kill_streak,
            "teamkills": self.teamkills,
            "teamkills_streak": self.teamkills_streak,
            "deaths_by_tk": self.deaths_by_tk,
            "deaths_by_tk_streak": self.deaths_by_tk_streak,
            "nb_vote_started": self.nb_vote_started,
            "nb_voted_yes": self.nb_voted_yes,
            "nb_voted_no": self.nb_voted_no,
            "time_seconds": self.time_seconds,
            "kills_per_minute": self.kills_per_minute,
            "deaths_per_minute": self.deaths_per_minute,
            "kill_death_ratio": self.kill_death_ratio,
            "longest_life_secs": self.longest_life_secs,
            "shortest_life_secs": self.shortest_life_secs,
            "combat": self.combat,
            "offense": self.offense,
            "defense": self.defense,
            "support": self.support,
            "most_killed": self.most_killed or {},
            "death_by": self.death_by or {},
            "weapons": self.weapons or {},
            "death_by_weapons": self.death_by_weapons,
            "team": _detect_team(self.weapons, self.death_by_weapons),
            "level": self.level,
        }
