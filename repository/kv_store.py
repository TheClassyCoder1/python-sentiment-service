_VALUES: dict[str, str] = {}


def get_cursor_values(keys: set[str]) -> dict[str, str]:
    return {key: _VALUES[key] for key in keys if key in _VALUES}


def set_cursor_values(pairs: dict[str, str]) -> None:
    _VALUES.update(pairs)
