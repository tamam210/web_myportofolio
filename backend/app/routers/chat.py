import re
from datetime import datetime

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..config import settings
from ..database import get_db
from ..email_sender import send_email
from ..models import ChatHistory, PendingQuestion
from ..schemas import ChatIn, ChatOut

router = APIRouter(prefix="/api", tags=["chat"])

# Stores which sessions are waiting for the asker's email.
# session_id -> id dari PendingQuestion yang udah dibuat.
_waiting_email: dict[str, int] = {}


def _ask(question: str, db: Session) -> str | None:
    q = question.lower()

    if re.search(r"\b(halo|hai|hello|hi)\b", q):
        return "Halo! 👋 Aku bot dari portfolio Tamam. Tanya-tanya soal skill, project, atau kontak boleh banget!"

    if any(w in q for w in ["siapa", "nama kamu", "kenalan", "introduce", "tentang"]):
        return "Aku bantu jawab soal Tamam Ni'amillah R.P.W. — mahasiswa Teknik Informatika yang fokus di Web Development & Machine Learning."

    if any(w in q for w in ["skill", "keahlian", "bisa apa", "teknologi", "stack"]):
        return "Skill utama: Frontend (React), Backend (FastAPI + Python), Database (MySQL/MariaDB), plus Docker dan Git. Mau yang mana mau kutunjukin project-nya?"

    if any(w in q for w in ["project", "proyek", "karya", "github"]):
        return "Beberapa project-ku: App Blocker (Python + Flask + Next.js), Sensory Platform (Next.js), dan UTC Landing Page (HTML/CSS/JS). Semua ada di GitHub github.com/tamam210."

    if any(w in q for w in ["backend", "api", "fastapi"]):
        return "Backend-nya pakai FastAPI dengan Python, database MySQL/MariaDB, dan pendataan lewat SQLAlchemy. API docs-nya bisa dibuka di /docs."

    if any(w in q for w in ["frontend", "react", "ui", "web"]):
        return "Frontend-ku pakai React + Vite, styling CSS custom dengan tema dark purple neon. Responsive buat mobile juga."

    if any(w in q for w in ["kontak", "contact", "hubungi", "email", "wa", "whatsapp"]):
        return (
            f"Bisa hubungi Tamam langsung di {settings.contact_email}. "
            "Kalau mau tanya soal portofolio di sini juga boleh banget loh!"
        )

    if any(w in q for w in ["makan", "makanan", "minum"]):
        return "Kalau soal makanan, favoritku juga suka yang enak. 😄"

    if "terima kasih" in q or "makasih" in q:
        return "Sama-sama! Senang bisa bantu. Ada lagi yang mau ditanya?"

    return None


_CAPABILITY_PATTERNS = [
    r"\b(perbaiki|perbaikan|servis|service|benerin|betulin|tukang)\b",
    r"\b(elektronik|laptop|komputer|\bpc\b|printer|\bhp\b|hardware|teknisi|rusak)\b",
    r"\b(kerjasama|kerja sama|berkerjasama|mitra|partner|partnership)\b",
    r"\b(mengajak|ngajak|\bajak\b|rekrut|merekrut|lowongan|jabatan|posisi)\b",
    r"\b(perusahaan|\bpt\b|kantor)\b",
]

_BISA_RE = re.compile(r"\bbisa(n\s?ggak| ga| gak| kah)?\b|\bbisakah\b")

_EXPERTISE_KEYWORDS = [
    "web", "website", "server", "coding", "ngoding", "program", "programmer",
    "programming", "aplikasi", "software", "bot", "chatbot", "machine learning",
    "artificial intelligence", "ai", "data", "database", "mysql", "sql",
    "frontend", "front end", "backend", "back end", "fullstack", "react",
    "python", "php", "javascript", "js", "django", "flask", "laravel",
    "desain", "ui", "ux", "html", "css", "git", "github", "docker", "hosting",
    "domain", "instalasi", "jaringan", "network", "error",
]


def _is_within_expertise(q: str) -> bool:
    pattern = r"\b(" + "|".join(kw.replace(" ", r"\s+") for kw in _EXPERTISE_KEYWORDS) + r")\b"
    return bool(re.search(pattern, q))


_CAPABILITY_INTRO = (
    "Soal kebisaan Tamam: fokus di Web Development (React, FastAPI, Python), "
    "Machine Learning, database MySQL/MariaDB, Git, dan Docker, plus urusan software "
    "(bikin web/bot, instalasi, ngatasin error aplikasi di laptop/PC/HP)."
)


def _capability_answer(question: str) -> str | None:
    q = question.lower()
    trigger = bool(_BISA_RE.search(q)) or any(re.search(p, q) for p in _CAPABILITY_PATTERNS)
    if not trigger:
        return None

    if _is_within_expertise(q):
        close = (
            "Yang kamu tanyain ini masuk kebisaannya Tamam, jadi bisa dibantu. "
            "Kalau mau lanjut, info kerja sama bisa lewat email yang kamu isi di awal chat ini."
        )
    else:
        close = (
            "Kalau yang kamu tanyain ini di luar kebisaan Tamam, nanti akan kami sampaikan "
            "ke developer kami. Kalau mau ada info lanjut, bisa hubungi lewat email yang kamu isi di awal chat ini."
        )
    return _CAPABILITY_INTRO + " " + close + " 🙏"


def _looks_like_email(value: str) -> bool:
    return "@" in value and "." in value and len(value) < 255


_QUESTION_WORDS = {
    "apa", "apakah", "sapa", "siapa", "kenapa", "kapan", "dimana", "dima",
    "gimana", "bagaimana", "knp", "kok", "bisa", "boleh", "mau", "kak", "gmn",
}

_CANCEL_EMAIL = {
    "skip", "skip aja", "gak", "ga", "nggak", "enggak", "tidak", "gajadi",
    "ga jadi", "gak jadi", "nggak jadi", "enggak jadi", "gak mau", "ga mau",
    "gak usah", "ga usah", "gausah", "gak guna", "ga guna", "gakpapa",
    "gak apa", "ga apa", "udah", "sudah", "nggak usah",
}


def _cancel_email_request(text: str) -> bool:
    t = re.sub(r"[^a-z0-9\s]", " ", text.lower())
    t = " ".join(t.split())
    return t in _CANCEL_EMAIL or not t


def _is_question_like(text: str) -> bool:
    t = text.strip()
    if len(t) > 25:
        return True
    if t.endswith("?"):
        return True
    words = _keywords(text)
    return bool(words & _QUESTION_WORDS)


_STOPWORDS = {
    "apa", "yang", "di", "ke", "dari", "ini", "itu", "kan", "ya", "kah",
    "hal", "sama", "dengan", "dan", "atau", "untuk", "tentang", "halo",
    "tolong", "boleh", "bs", "dikit", "dong", "nanya", "nan", "mandi",
    "hari", "berapa", "kamu", "lu", "gw", "aku", "gua", "nyari", "mau",
}


def _keywords(text: str) -> set[str]:
    clean = re.sub(r"[^a-z0-9\s]", " ", text.lower())
    words = clean.split()
    return {w for w in words if len(w) > 2 and w not in _STOPWORDS}


def _ask_taught(db: Session, question: str) -> str | None:
    """Cari pelajaran dari /admin: cocokkan kata kunci pertanyaan yang diajarkan.

    Makin banyak kata penting yang sama, makin yakin bot pakai jawaban itu.
    Butuh minimal 2 kata yang cocok biar nggak asal jawab.
    """
    learned = (
        db.query(PendingQuestion)
        .filter(
            PendingQuestion.status == "answered",
            PendingQuestion.answer.isnot(None),
        )
        .all()
    )
    q_words = _keywords(question)
    if not q_words:
        return None

    best: tuple[float, str] = (0.0, "")
    for row in learned:
        t_words = _keywords(row.question)
        if not t_words:
            continue
        overlap = len(q_words & t_words)
        score = overlap / len(t_words)
        if score >= 0.6 and score > best[0]:
            best = (score, row.answer)

    return best[1] if best[1] else None


@router.post("/chat", response_model=ChatOut)
async def chat(payload: ChatIn, db: Session = Depends(get_db)):
    message = payload.message.strip()
    if not message:
        return ChatOut(reply="Kirim pesan dong dulu 😸")

    user_email = payload.user_email.strip()

    # (Buat client lama) Kalau bot lagi menunggu email, pesan ini dianggap email.
    if payload.session_id in _waiting_email:
        email = message

        # Kalau dia nanya lagi / mau batal kasih email, jangan ditahan.
        if not _looks_like_email(email) and (_cancel_email_request(email) or _is_question_like(email)):
            pending_id = _waiting_email.pop(payload.session_id)
            db.query(PendingQuestion).filter(PendingQuestion.id == pending_id).delete()
            db.commit()

            if _cancel_email_request(email) and not _is_question_like(email):
                return ChatOut(
                    reply="Oke, gakpapa! 😊 Pertanyaannya tetap kucatat buat dipelajari developer-ku.",
                    ask_email=False,
                )
        elif not _looks_like_email(email):
            return ChatOut(
                reply="Hmm, itu kayaknya bukan email yang valid. Boleh kirim alamat email yang bener ya 🙏 "
                "(atau ketik 'skip' kalau gak mau kasih email).",
                ask_email=True,
            )
        else:
            pending_id = _waiting_email.pop(payload.session_id)
            pending = db.query(PendingQuestion).filter(PendingQuestion.id == pending_id).first()
            if pending:
                pending.user_email = email
                db.commit()

                send_email(
                    settings.contact_email,
                    "Pertanyaan baru menunggu dijawab (chatbot)",
                    f"Penanya: {email}\n\nPertanyaan:\n{pending.question}\n\n"
                    "Kasih jawabannya ke bot, nanti dikirim balik ke email penanya.",
                )

            return ChatOut(
                reply=f"Makasih {email.split('@')[0]}! 🙏 Pertanyaanmu sudah kucatat. "
                "Aku belum dikasih ilmunya sama developer-ku soal ini, jadi jawabannya bakal kukirim "
                "ke email kamu begitu aku udah diajarin. Mohon ditunggu ya!"
            )

    # Pertanyaan tentang kebisaan/kerja sama/elektronik -> bot bisa jawab,
    # dan dicatat ke admin sebagai kategori "penting" (answered).
    capability = _capability_answer(message)
    if capability:
        now = datetime.utcnow()
        exists = (
            db.query(PendingQuestion)
            .filter(
                PendingQuestion.status == "answered",
                PendingQuestion.category == "penting",
                PendingQuestion.question == message,
            )
            .first()
        )
        if not exists:
            db.add(
                PendingQuestion(
                    question=message,
                    user_email=user_email,
                    status="answered",
                    category="penting",
                    answer=capability,
                    answered_at=now,
                )
            )
        db.add(ChatHistory(user_message=message, bot_reply=capability))
        db.commit()
        return ChatOut(reply=capability)

    answer = _ask(message, db) or _ask_taught(db, message)

    if answer:
        db.add(ChatHistory(user_message=message, bot_reply=answer))
        db.commit()
        return ChatOut(reply=answer)

    # Bot cannot answer -> catat ke pending_questions.
    # Kalau email udah dikasih dari popup di awal, langsung kepake (nggak ada loop nanya email).
    if _looks_like_email(user_email):
        pending = PendingQuestion(question=message, user_email=user_email, status="pending")
        db.add(pending)
        db.commit()

        send_email(
            settings.contact_email,
            "Pertanyaan baru menunggu dijawab (chatbot)",
            f"Penanya: {user_email}\n\nPertanyaan:\n{message}\n\n"
            "Kasih jawabannya ke bot, nanti dikirim balik ke email penanya.",
        )
        db.add(ChatHistory(user_message=message, bot_reply="[belum terjawab, email pengirim ada]"))
        db.commit()

        return ChatOut(
            reply=f"Oke, pertanyaan yang bagus! 🧠 Aku belum dikasih pelajaran soal itu, "
            f"jadi kucatat dulu. Nanti jawabannya bakal kukirim ke {user_email} begitu aku udah "
            "diajarin developer-ku. Makasih ya!"
        )

    # Tanpa email: minta email dulu (biasanya udah diisi lewat popup).
    pending = PendingQuestion(question=message, user_email="", status="pending")
    db.add(pending)
    db.flush()
    db.refresh(pending)
    _waiting_email[payload.session_id] = pending.id
    db.add(ChatHistory(user_message=message, bot_reply="[belum terjawab, menunggu email pengirim]"))
    db.commit()

    return ChatOut(
        reply="Wah, pertanyaan yang bagus! Tapi aku belum dikasih pelajaran soal itu sama developer-ku 😅. "
        "Mohon ditunggu ya, biar aku tanyain dulu. Oiya, kasih alamat email kamu, nanti jawabannya baku kirim ke email kamu.",
        ask_email=True,
    )