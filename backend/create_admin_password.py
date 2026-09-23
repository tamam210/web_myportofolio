#!/usr/bin/env python3
"""
Bikin bcrypt-hash untuk password admin halaman /admin.

Cara pakai (dari folder backend/):
    .venv/bin/python create_admin_password.py

Lu bakal diminta password (ketikan disembunyiin). Hash-nya di-print,
tempel ke baris ADMIN_PASSWORD_HASH= di file backend/.env .

Kenapa hash?
Password asli nggak pernah disimpan. Yang disimpan cuma hash-nya.
Kalau file .env/database bocor ke tangan hacker, password asli lu
tetep nggak bisa diketahui (bcrypt anti brute-force).
"""
import bcrypt
import getpass

password = getpass.getpass("Bikin password admin (ketikan disembunyiin): ")
if not password:
    print("Kosong, batal.")
    raise SystemExit(1)

hashed = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("ascii")
print()
print("Simpan baris ini di backend/.env :")
print(f"ADMIN_PASSWORD_HASH={hashed}")