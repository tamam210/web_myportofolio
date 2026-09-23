#!/usr/bin/env python3
"""
Encode App Password jadi base64 biar nggak keliatan langsung di .env.

Cara pakai (jalanin di folder backend/):
    .venv/bin/python encode_password.py

Nanti diminta tempel App Password-nya (ketikan nggak bakal muncul di layar),
terus di print hasil encode-nya. Tempel hasil itu ke baris:

    SMTP_PASSWORD_B64=<hasilnya>

Script ini BUKAN enkripsi — base64 cuma nyamarin. ".env" jangan pernah
di-share atau masuk git (sudah di-gitignore).
"""
import base64
import getpass

value = getpass.getpass("Tempel App Password (ketikan disembunyiin): ")
if not value:
    print("Kosong, batal.")
    raise SystemExit(1)

encoded = base64.b64encode(value.encode("utf-8")).decode("ascii")
print()
print("Simpan ini di backend/.env :")
print(f"SMTP_PASSWORD_B64={encoded}")