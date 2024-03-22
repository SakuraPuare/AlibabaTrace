

def md5(string: str) -> str:
    import hashlib
    return hashlib.md5(string.encode()).hexdigest()