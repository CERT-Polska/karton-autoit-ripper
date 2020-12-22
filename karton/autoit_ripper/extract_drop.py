import sys
from pathlib import Path
from typing import Optional

import regex  # type: ignore
from malduck import rc4  # type: ignore

BINARY_REGEX = (
    r'(\$.*)\s*=\s*"([A-Fa-f0-9x])+"\s+(\1\s*=\s'
    r'*\1\s*&\s*"([A-Fa-f0-9x]+)"\s*)+\1\s*=\s*.*\(\s*\1,\s*"(.*?)"'
)


def extract_binary(data: str) -> Optional[bytes]:
    match = regex.search(BINARY_REGEX, data)
    if not match:
        return None

    header = "".join(match.captures(2))
    rest = "".join(match.captures(4))
    key = match.group(5)

    payload = header + rest

    # reversed string
    if payload.endswith("x0"):
        payload = payload[::-1]

    if not payload.startswith("0x"):
        return None

    binary = rc4(key.encode(), bytes.fromhex(payload[2:]))
    if binary.startswith(b"\x4d\x5a"):
        return binary
    return None


def main() -> None:
    binary = Path(sys.argv[1])
    out = binary.with_suffix(".decrypted")
    binary_data = extract_binary(binary.read_text())
    if binary_data:
        out.write_bytes(binary_data)


if __name__ == "__main__":
    main()
