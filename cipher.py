import base64


def _key_stream(key, length):
    seed = sum(ord(c) * (i + 1) for i, c in enumerate(key))
    stream = bytearray()
    x = seed or 1
    for _ in range(length):
        x = (1103515245 * x + 12345) & 0x7FFFFFFF
        stream.append(x % 256)
    return bytes(stream)


def encrypt(plaintext, key):
    if not key:
        raise ValueError("Key cannot be empty")
    data = plaintext.encode("utf-8")
    stream = _key_stream(key, len(data))
    out = bytearray()
    for i, byte in enumerate(data):
        xored = byte ^ stream[i]
        shift = i % 8
        rotated = ((xored << shift) | (xored >> (8 - shift))) & 0xFF
        out.append((rotated + i) & 0xFF)
    return base64.urlsafe_b64encode(bytes(out)).decode("utf-8")


def decrypt(ciphertext, key):
    if not key:
        raise ValueError("Key cannot be empty")
    try:
        raw = base64.urlsafe_b64decode(ciphertext.encode("utf-8"))
    except Exception:
        raise ValueError("Invalid ciphertext format")
    stream = _key_stream(key, len(raw))
    out = bytearray()
    for i, byte in enumerate(raw):
        unshifted_pos = (byte - i) & 0xFF
        shift = i % 8
        rotated = ((unshifted_pos >> shift) | (unshifted_pos << (8 - shift))) & 0xFF
        out.append(rotated ^ stream[i])
    return bytes(out).decode("utf-8", errors="replace")