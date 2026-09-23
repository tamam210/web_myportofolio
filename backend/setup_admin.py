#!/usr/bin/env python3
"""
Setup password admin otomatis:
  - bikin password kuat acak
  - hash pakai bcrypt
  - tulis ADMIN_PASSWORD_HASH ke .env (backend)
  - print password-nya SEKALI doang buat lu catat

Password asli nggak disimpen — cuma hash-nya yang masuk .env.
Ketik  : LIHAT OUTPUT "Password admin kamu" di bawah.
Run ulang script ini kapan aja buat ganti password.
"""
import getpass
import re
import secrets

import bcrypt

from pathlib import Path

ENV_PATH = Path(__file__).parent / ".env"

ALPHABET = "abcdefghjkmnpqrstuvwxyzABCDEFGHJKMNPQRSTUVWXYZ23456789!@#$%"
PASSWORD_LENGTH = 16


def random_password() -> str:
    return "".join(secrets.choice(ALPHABET) for _ in range(PASSWORD_LENGTH))


def update_env(hash_value: str) -> None:
    text = ENV_PATH.read_text(encoding="utf-8")
    if re.search(r"^ADMIN_PASSWORD_HASH=", text, flags=re.MULTILINE):
        text = re.sub(
            r"^ADMIN_PASSWORD_HASH=.*$",
            f"ADMIN_PASSWORD_HASH={hash_value}",
            text,
            flags=re.MULTILINE,
        )
    else:
        text += f"\nADMIN_PASSWORD_HASH={hash_value}\n"
    ENV_PATH.write_text(text, encoding="utf-8")


password = random_password()
hashed = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("ascii")
update_env(hashed)

print("===================================================")
print("  Password admin kamu (catat baik-baik, jangan kamu")
print("  share sama siapa-siapa):")
print()
print(f"  {password}")
print()
print("  Username default .env: admin")
print("  Hash-nya udah masuk ke backend/.env.")
print("===================================================")