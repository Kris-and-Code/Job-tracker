from sqlalchemy.orm import Session
from sqlalchemy import or_
from . import models, schemas, auth
from typing import Tuple, List, Optional
from datetime import datetime

# User operations
def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()

def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = auth.get_password_hash(user.password)
    db_user = models.User(email=user.email, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# Job operations
def get_jobs(
    db: Session,
    user_id: int,
    skip: int = 0,
    limit: int = 10,
    status: Optional[str] = None,
    company: Optional[str] = None,
    search: Optional[str] = None
) -> Tuple[List[models.Job], int]:
    query = db.query(models.Job).filter(models.Job.owner_id == user_id)
    
    if status:
        query = query.filter(models.Job.status == status)
    if company:
        query = query.filter(models.Job.company.ilike(f"%{company}%"))
    if search:
        search_filter = or_(
            models.Job.title.ilike(f"%{search}%"),
            models.Job.company.ilike(f"%{search}%"),
            models.Job.description.ilike(f"%{search}%")
        )
        query = query.filter(search_filter)
    
    total = query.count()
    jobs = query.order_by(models.Job.created_at.desc()).offset(skip).limit(limit).all()
    return jobs, total

def get_job(db: Session, job_id: int, user_id: int):
    return db.query(models.Job).filter(
        models.Job.id == job_id,
        models.Job.owner_id == user_id
    ).first()

def create_job(db: Session, job: schemas.JobCreate, user_id: int):
    db_job = models.Job(**job.model_dump(), owner_id=user_id)
    db.add(db_job)
    db.commit()
    db.refresh(db_job)
    return db_job

def update_job(db: Session, job_id: int, job: schemas.JobCreate, user_id: int):
    db_job = get_job(db, job_id, user_id)
    if db_job:
        for key, value in job.model_dump().items():
            setattr(db_job, key, value)
        db.commit()
        db.refresh(db_job)
    return db_job

def delete_job(db: Session, job_id: int, user_id: int) -> bool:
    db_job = get_job(db, job_id, user_id)
    if db_job:
        db.delete(db_job)
        db.commit()
        return True
    return False

# Job Note operations
def get_job_notes(
    db: Session,
    job_id: int,
    skip: int = 0,
    limit: int = 10
) -> Tuple[List[models.JobNote], int]:
    query = db.query(models.JobNote).filter(models.JobNote.job_id == job_id)
    total = query.count()
    notes = query.order_by(models.JobNote.created_at.desc()).offset(skip).limit(limit).all()
    return notes, total

def create_job_note(db: Session, note: schemas.JobNoteCreate, job_id: int):
    db_note = models.JobNote(**note.model_dump(), job_id=job_id)
    db.add(db_note)
    db.commit()
    db.refresh(db_note)
    return db_note

def update_job_note(db: Session, note_id: int, note: schemas.JobNoteCreate):
    db_note = db.query(models.JobNote).filter(models.JobNote.id == note_id).first()
    if db_note:
        for key, value in note.dict().items():
            setattr(db_note, key, value)
        db.commit()
        db.refresh(db_note)
    return db_note

def delete_job_note(db: Session, note_id: int):
    db_note = db.query(models.JobNote).filter(models.JobNote.id == note_id).first()
    if db_note:
        db.delete(db_note)
        db.commit()
        return True
    return False 