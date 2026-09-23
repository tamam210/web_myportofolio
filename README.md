# Web MyPortfolio

Portfolio pribadi dengan **chatbot sederhana** bawaan — dibangun dengan React (frontend) + FastAPI (backend) + MariaDB (database).

## Fitur

- Tampilan dark purple neon, animasi scroll-reveal & parallax
- **Chatbot di section "Chat With Me"** — bot jawab seputar skill, project, dan kontak
- **Bot bisa "belajar"** — pertanyaan yang belum kejawab masuk ke halaman admin, lalu pemilik isi jawabannya biar bot bisa jawab pertanyaan serupa nanti
- **Halaman admin `/admin`** — khusus pemilik, login pakai password bcrypt-hash, sesi pakai HttpOnly cookie
- Riwayat chat & pertanyaan pending tersimpan di MariaDB

## Struktur

```
web_myportfolio/
├── frontend/          # React + Vite (portfolio & UI chatbot)
├── backend/           # FastAPI (API, chatbot logic, admin)
└── jalankan.sh        # Jalanin frontend + backend sekaligus
```

## Tech Stack

- **Frontend:** React 18, Vite, Axios
- **Backend:** FastAPI, SQLAlchemy, PyMySQL
- **Database:** MariaDB/MySQL (database `mycv`)
- **Auth admin:** bcrypt, session token tersimpan hashed

## Cara Menjalankan

### 1. Siapkan database

```bash
cd backend
sudo systemctl start mariadb
sudo mariadb < setup_db.sql
```

> `setup_db.sql` berisi placeholder — ganti `GANTI_PASSWORD` dengan password asli kalian, atau buat manual user/database bernama `mycv`.

### 2. Konfigurasi backend

```bash
cd backend
cp .env.example .env
# isi DATABASE_URL dengan kredensial kalian

python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
```

Opsional (untuk halaman admin):

```bash
# bikin password admin (hasil hash otomatis masuk ke .env)
.venv/bin/python setup_admin.py
# atau manual: .venv/bin/python create_admin_password.py
```

### 3. Jalanin

```bash
./jalankan.sh
```

- Frontend: http://localhost:5173
- Halaman admin: http://localhost:8000/admin

## API Utama

| Method | Endpoint | Keterangan |
|---|---|---|
| POST | `/api/chat` | Kirim pesan ke chatbot |
| POST | `/api/admin/login` | Login admin |
| GET | `/api/admin/pending` | Daftar pertanyaan pending (butuh login) |
| POST | `/api/admin/pending/{id}/answer` | Isi jawaban supaya bot belajar |
| GET | `/health` | Cek status server |

Dokumentasi API lengkap: http://localhost:8000/docs

## Keamanan

- `.env` (password database, hash admin, token) **tidak pernah di-commit** — lihat `.gitignore`
- Password admin cuma disimpan sebagai **bcrypt hash**
- Session admin memakai **HttpOnly cookie** (tidak bisa dibaca JavaScript)

## Kontak

Email: [tamam.niamillah.rpw@gmail.com](mailto:tamam.niamillah.rpw@gmail.com)