#!/usr/bin/env python
import os
import sys


class ConfigurationError(Exception):
    pass


def _get_missing_env(keys, env):
    missing = []
    for k in keys:
        if not env.get(k):
            missing.append("'{}' was not specified in your configuration".format(k))
    return missing


def pre_flight_checks(env):
    required = [
        "HLL_DB_URL",
    ]
    optionnal = ["LOGGING_PATH", "LOGGING_LEVEL"]

    errors = _get_missing_env(required, env)
    warnings = _get_missing_env(optionnal, env)

    print(warnings)
    if errors:
        print(errors)
        raise ConfigurationError("\n".join(errors))


if __name__ == "__main__":
    env = os.environ
    try:
        pre_flight_checks(env)
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "rconweb.settings")
        rconweb_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "rconweb")
        if rconweb_path not in sys.path:
            sys.path.insert(0, rconweb_path)

        from django.core.management import execute_from_command_line

        execute_from_command_line(sys.argv)
    except ConfigurationError as e:
        print(repr(e))
        exit(1)
    except Exception as e:
        print(repr(e))
        exit(1)
