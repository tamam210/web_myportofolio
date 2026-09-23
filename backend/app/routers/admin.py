from datetime import datetime
from typing import Union

from fastapi import APIRouter, Depends, HTTPException, Request, Response
from pydantic import BaseModel
from sqlalchemy.orm import Session

from ..auth import (
    SESSION_COOKIE_NAME,
    create_session,
    destroy_session,
    get_current_admin,
    verify_admin_password,
)
from ..config import settings
from ..database import get_db
from ..models import AdminSession, PendingQuestion

router = APIRouter()


class LoginIn(BaseModel):
    username: str
    password: str


class AnswerIn(BaseModel):
    answer: str


@router.post("/api/admin/login")
def admin_login(payload: LoginIn, response: Response, db: Session = Depends(get_db)):
    if payload.username != settings.admin_username or not verify_admin_password(payload.password):
        raise HTTPException(status_code=401, detail="Username atau password salah")

    token = create_session(db)
    response.set_cookie(
        key=SESSION_COOKIE_NAME,
        value=token,
        httponly=True,
        samesite="lax",
        max_age=8 * 60 * 60,
        path="/",
    )
    return {"ok": True}


@router.post("/api/admin/logout")
def admin_logout(request: Request, response: Response, db: Session = Depends(get_db)):
    token = request.cookies.get(SESSION_COOKIE_NAME)
    if token:
        destroy_session(token, db)
    response.delete_cookie(SESSION_COOKIE_NAME, path="/")
    return {"ok": True}


@router.get("/api/admin/me")
def admin_me(session: AdminSession = Depends(get_current_admin)):
    return {"ok": True, "username": settings.admin_username}


@router.get("/api/admin/pending")
def list_pending(
    session: AdminSession = Depends(get_current_admin), db: Session = Depends(get_db)
):
    rows = db.query(PendingQuestion).order_by(PendingQuestion.created_at.desc()).all()
    return [
        {
            "id": r.id,
            "question": r.question,
            "user_email": r.user_email,
            "status": r.status,
            "answer": r.answer,
            "answered_at": r.answered_at.isoformat() if r.answered_at else None,
            "created_at": r.created_at.isoformat() if r.created_at else None,
        }
        for r in rows
    ]


@router.post("/api/admin/pending/{question_id}/answer")
def answer_question(
    question_id: int,
    payload: AnswerIn,
    session: AdminSession = Depends(get_current_admin),
    db: Session = Depends(get_db),
):
    row = db.query(PendingQuestion).filter(PendingQuestion.id == question_id).first()
    if not row:
        raise HTTPException(status_code=404, detail="Pertanyaan tidak ditemukan")

    row.answer = payload.answer
    row.status = "answered"
    row.answered_at = datetime.utcnow()
    db.commit()
    return {"ok": True}


@router.post("/api/admin/pending/{question_id}/delete")
def delete_question(
    question_id: int,
    session: AdminSession = Depends(get_current_admin),
    db: Session = Depends(get_db),
):
    row = db.query(PendingQuestion).filter(PendingQuestion.id == question_id).first()
    if not row:
        raise HTTPException(status_code=404, detail="Pertanyaan tidak ditemukan")

    db.delete(row)
    db.commit()
    return {"ok": True}