from sqlalchemy.orm import Session
from . import models, schemas, auth
from typing import List, Optional
from datetime import datetime

# User operations
def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = auth.get_password_hash(user.password)
    db_user = models.User(email=user.email, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

# Job operations
def create_job(db: Session, job: schemas.JobCreate, user_id: int):
    db_job = models.Job(**job.dict(), owner_id=user_id)
    db.add(db_job)
    db.commit()
    db.refresh(db_job)
    return db_job

def get_jobs(db: Session, user_id: int, skip: int = 0, limit: int = 100):
    return db.query(models.Job).filter(models.Job.owner_id == user_id).offset(skip).limit(limit).all()

def get_job(db: Session, job_id: int, user_id: int):
    return db.query(models.Job).filter(models.Job.id == job_id, models.Job.owner_id == user_id).first()

def update_job(db: Session, job_id: int, job: schemas.JobCreate, user_id: int):
    db_job = get_job(db, job_id, user_id)
    if db_job:
        for key, value in job.dict().items():
            setattr(db_job, key, value)
        db.commit()
        db.refresh(db_job)
    return db_job

def delete_job(db: Session, job_id: int, user_id: int):
    db_job = get_job(db, job_id, user_id)
    if db_job:
        db.delete(db_job)
        db.commit()
        return True
    return False

# Job Note operations
def create_job_note(db: Session, note: schemas.JobNoteCreate, job_id: int):
    db_note = models.JobNote(**note.dict(), job_id=job_id)
    db.add(db_note)
    db.commit()
    db.refresh(db_note)
    return db_note

def get_job_notes(db: Session, job_id: int, skip: int = 0, limit: int = 100):
    return db.query(models.JobNote).filter(models.JobNote.job_id == job_id).offset(skip).limit(limit).all()

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