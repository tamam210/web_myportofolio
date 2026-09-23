import re

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


def _looks_like_email(value: str) -> bool:
    return "@" in value and "." in value and len(value) < 255


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


def _looks_like_email(value: str) -> bool:
    return "@" in value and "." in value and len(value) < 255


@router.post("/chat", response_model=ChatOut)
async def chat(payload: ChatIn, db: Session = Depends(get_db)):
    message = payload.message.strip()
    if not message:
        return ChatOut(reply="Kirim pesan dong dulu 😸")

    # If we were waiting for the asker's email, this message is the email.
    if payload.session_id in _waiting_email:
        email = message
        if not _looks_like_email(email):
            return ChatOut(
                reply="Hmm, itu kayaknya bukan email yang valid. Boleh kirim alamat email yang bener ya 🙏",
                ask_email=True,
            )

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

    answer = _ask(message, db) or _ask_taught(db, message)

    if answer:
        db.add(ChatHistory(user_message=message, bot_reply=answer))
        db.commit()
        return ChatOut(reply=answer)

    # Bot cannot answer -> langsung catat pertanyaannya ke pending_questions,
    # lalu minta email buat kabar balik. Jadi muncul di /admin walau email belum dikasih.
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