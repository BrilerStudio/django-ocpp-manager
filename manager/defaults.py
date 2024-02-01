import secrets


def tagid_generator() -> str:
    return 't' + secrets.token_urlsafe(5)[:5]


def code_generator() -> str:
    return secrets.token_urlsafe(20)[:20]
