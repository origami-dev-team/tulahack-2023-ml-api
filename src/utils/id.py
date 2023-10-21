from uuid import uuid4


def id() -> str:
    return str(uuid4())
