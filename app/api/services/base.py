from sqlalchemy import inspect


def to_dict(obj, replace: dict[str, str] = None) -> dict:
    if not hasattr(obj, "__table__"):
        raise TypeError(f"Object {obj} is not a SQLAlchemy model")

    data = {}
    for c in inspect(obj).mapper.column_attrs:
        key = c.key
        val = getattr(obj, key)

        if replace and key in replace:
            key = replace[key]

        data[key] = val
    return data
