import os


def get_server_number() -> int | None:
    value = os.getenv("SERVER_NUMBER")
    if not value:
        return None

    try:
        return int(value)
    except ValueError:
        return None


def get_site_name(server_number: int | None = None) -> tuple[str, str]:
    short_name = (
        os.getenv("ARCHIVE_SITE_NAME")
        or os.getenv("SITE_NAME")
        or (f"CRCON Archive {server_number}" if server_number is not None else "CRCON Archive")
    )
    return short_name, short_name
