import hashlib
import os
import secrets
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Optional
from uuid import uuid4

from fastapi import Depends, FastAPI, HTTPException, Request
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field
from pwdlib import PasswordHash
from sqlalchemy import DateTime, ForeignKey, JSON, String, create_engine, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column, sessionmaker
from sqlalchemy.pool import StaticPool
from starlette.middleware.sessions import SessionMiddleware

BASE_DIR = Path(__file__).resolve().parent
STATIC_DIR = BASE_DIR / "static"
DATABASE_URL = os.environ.get("DATABASE_URL", f"sqlite:///{BASE_DIR / 'safeher.db'}")
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql+psycopg://", 1)
elif DATABASE_URL.startswith("postgresql://"):
    DATABASE_URL = DATABASE_URL.replace("postgresql://", "postgresql+psycopg://", 1)

USER_ID_FOREIGN_KEY = "users.id"

engine_options = {"connect_args": {"check_same_thread": False}} if DATABASE_URL.startswith("sqlite") else {}
if DATABASE_URL == "sqlite://":
    engine_options["poolclass"] = StaticPool
engine = create_engine(DATABASE_URL, **engine_options)
SessionLocal = sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)
password_hasher = PasswordHash.recommended()


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid4()))
    email: Mapped[str] = mapped_column(String(254), unique=True, index=True)
    name: Mapped[str] = mapped_column(String(80))
    password_hash: Mapped[str] = mapped_column(String(255))
    owner_id: Mapped[Optional[str]] = mapped_column(ForeignKey(USER_ID_FOREIGN_KEY), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))


class ContactInvite(Base):
    __tablename__ = "contact_invites"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid4()))
    owner_id: Mapped[str] = mapped_column(ForeignKey(USER_ID_FOREIGN_KEY), index=True)
    code_hash: Mapped[str] = mapped_column(String(64), unique=True, index=True)
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    used_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)


class Activity(Base):
    __tablename__ = "activity"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid4()))
    owner_id: Mapped[str] = mapped_column(ForeignKey(USER_ID_FOREIGN_KEY), index=True)
    type: Mapped[str] = mapped_column(String(40))
    message: Mapped[str] = mapped_column(String(255))
    details: Mapped[dict] = mapped_column(JSON, default=dict)
    timestamp: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), index=True)


Base.metadata.create_all(engine)

app = FastAPI(title="SafeHer - Women Safety Support System", version="1.0.0")
app.add_middleware(
    SessionMiddleware,
    secret_key=os.environ.get("APP_SECRET", "local-development-secret-change-me"),
    same_site="lax",
    https_only=bool(os.environ.get("RENDER")),
)
app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")


class RegisterRequest(BaseModel):
    name: str = Field(min_length=1, max_length=80)
    email: str = Field(min_length=3, max_length=254)
    password: str = Field(min_length=12, max_length=128)


class ContactJoinRequest(RegisterRequest):
    code: str = Field(min_length=8, max_length=40)


class LoginRequest(BaseModel):
    email: str = Field(min_length=3, max_length=254)
    password: str = Field(min_length=1, max_length=128)


class SOSRequest(BaseModel):
    latitude: Optional[float] = None
    longitude: Optional[float] = None


class CheckinRequest(BaseModel):
    name: str = Field(default="", max_length=80)


class IncidentRequest(BaseModel):
    category: str = Field(min_length=1, max_length=80)
    description: str = Field(min_length=1, max_length=2000)
    location: str = Field(default="", max_length=250)


def get_db():
    with SessionLocal() as session:
        yield session


def get_current_user(request: Request, db: Session = Depends(get_db)) -> User:
    user_id = request.session.get("user_id")
    user = db.get(User, user_id) if user_id else None
    if user is None:
        request.session.clear()
        raise HTTPException(status_code=401, detail="Please sign in to continue.")
    return user


def require_owner(user: User = Depends(get_current_user)) -> User:
    if user.owner_id is not None:
        raise HTTPException(status_code=403, detail="Only the account owner can use this action.")
    return user


def normalized_email(value: str) -> str:
    email = value.strip().lower()
    if "@" not in email or email.startswith("@") or email.endswith("@"):
        raise HTTPException(status_code=422, detail="Enter a valid email address.")
    return email


def user_payload(user: User) -> dict:
    return {"id": user.id, "name": user.name, "email": user.email, "role": "contact" if user.owner_id else "owner"}


def activity_payload(item: Activity) -> dict:
    return {
        "id": item.id,
        "type": item.type,
        "message": item.message,
        "details": item.details or {},
        "timestamp": item.timestamp.isoformat(),
    }


def add_activity(db: Session, owner_id: str, kind: str, message: str, details: Optional[dict] = None) -> Activity:
    record = Activity(owner_id=owner_id, type=kind, message=message, details=details or {})
    db.add(record)
    db.commit()
    db.refresh(record)
    return record


@app.get("/")
def home():
    return FileResponse(STATIC_DIR / "index.html")


@app.get("/api/health")
def health():
    return {"status": "ok", "app": "SafeHer"}


@app.post("/api/auth/register")
def register_owner(payload: RegisterRequest, request: Request, db: Session = Depends(get_db)):
    email = normalized_email(payload.email)
    user = User(email=email, name=payload.name.strip(), password_hash=password_hasher.hash(payload.password))
    db.add(user)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail="An account with this email already exists.")
    request.session["user_id"] = user.id
    return {"user": user_payload(user)}


@app.post("/api/auth/join")
def join_as_contact(payload: ContactJoinRequest, request: Request, db: Session = Depends(get_db)):
    email = normalized_email(payload.email)
    invite = db.scalar(select(ContactInvite).where(ContactInvite.code_hash == hashlib.sha256(payload.code.strip().encode()).hexdigest()).with_for_update())
    now = datetime.now(timezone.utc)
    if invite is None:
        expires_at = now
    elif invite.expires_at.tzinfo is None:
        expires_at = invite.expires_at.replace(tzinfo=timezone.utc)
    else:
        expires_at = invite.expires_at
    if invite is None or invite.used_at is not None or expires_at <= now:
        raise HTTPException(status_code=400, detail="That invite code is invalid, expired, or already used.")
    user = User(
        email=email,
        name=payload.name.strip(),
        password_hash=password_hasher.hash(payload.password),
        owner_id=invite.owner_id,
    )
    invite.used_at = now
    db.add(user)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail="An account with this email already exists.")
    request.session["user_id"] = user.id
    return {"user": user_payload(user)}


@app.post("/api/auth/login")
def login(payload: LoginRequest, request: Request, db: Session = Depends(get_db)):
    email = normalized_email(payload.email)
    user = db.scalar(select(User).where(User.email == email))
    if user is None or not password_hasher.verify(payload.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Email or password is incorrect.")
    request.session.clear()
    request.session["user_id"] = user.id
    return {"user": user_payload(user)}


@app.post("/api/auth/logout")
def logout(request: Request):
    request.session.clear()
    return {"ok": True}


@app.get("/api/auth/me")
def current_account(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    result = user_payload(user)
    result["ownerName"] = db.get(User, user.owner_id).name if user.owner_id else None
    return {"user": result}


@app.post("/api/contacts/invite")
def create_contact_invite(owner: User = Depends(require_owner), db: Session = Depends(get_db)):
    code = secrets.token_urlsafe(12)
    expires_at = datetime.now(timezone.utc) + timedelta(hours=24)
    invite = ContactInvite(
        owner_id=owner.id,
        code_hash=hashlib.sha256(code.encode()).hexdigest(),
        expires_at=expires_at,
    )
    db.add(invite)
    db.commit()
    return {"code": code, "expiresAt": expires_at.isoformat()}


@app.post("/api/sos")
def create_sos(payload: SOSRequest, owner: User = Depends(require_owner), db: Session = Depends(get_db)):
    details = {}
    if payload.latitude is not None and payload.longitude is not None:
        details = {"latitude": payload.latitude, "longitude": payload.longitude}
    record = add_activity(db, owner.id, "SOS", "Demo SOS alert recorded", details)
    return {"ok": True, "message": "Demo SOS alert recorded. No emergency services were contacted.", "record": activity_payload(record)}


@app.post("/api/checkin")
def checkin(payload: CheckinRequest, owner: User = Depends(require_owner), db: Session = Depends(get_db)):
    name = payload.name.strip()
    message = f"{name or owner.name} checked in as safe"
    record = add_activity(db, owner.id, "Check-in", message, {"name": name})
    return {"ok": True, "message": "Safety check-in recorded.", "record": activity_payload(record)}


@app.post("/api/incidents")
def report_incident(payload: IncidentRequest, owner: User = Depends(require_owner), db: Session = Depends(get_db)):
    category = payload.category.strip()
    description = payload.description.strip()
    if not category or not description:
        raise HTTPException(status_code=400, detail="Category and description are required.")
    record = add_activity(
        db,
        owner.id,
        "Incident",
        f"{category} incident reported",
        {"category": category, "description": description, "location": payload.location.strip()},
    )
    return {"ok": True, "message": "Incident report recorded in this demo.", "record": activity_payload(record)}


@app.get("/api/history")
def get_history(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    owner_id = user.owner_id or user.id
    items = db.scalars(select(Activity).where(Activity.owner_id == owner_id).order_by(Activity.timestamp.desc()).limit(100)).all()
    return {"items": [activity_payload(item) for item in items]}
