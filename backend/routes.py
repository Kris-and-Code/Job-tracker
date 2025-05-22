from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from typing import List
from datetime import timedelta
from . import crud, models, schemas, auth
from .database import get_db

router = APIRouter()

# Authentication routes
@router.post("/token", response_model=schemas.Token)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    user = auth.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth.create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)

# Job routes
@router.post("/jobs/", response_model=schemas.Job)
def create_job(
    job: schemas.JobCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_active_user)
):
    return crud.create_job(db=db, job=job, user_id=current_user.id)

@router.get("/jobs/", response_model=List[schemas.Job])
def read_jobs(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_active_user)
):
    jobs = crud.get_jobs(db, user_id=current_user.id, skip=skip, limit=limit)
    return jobs

@router.get("/jobs/{job_id}", response_model=schemas.Job)
def read_job(
    job_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_active_user)
):
    db_job = crud.get_job(db, job_id=job_id, user_id=current_user.id)
    if db_job is None:
        raise HTTPException(status_code=404, detail="Job not found")
    return db_job

@router.put("/jobs/{job_id}", response_model=schemas.Job)
def update_job(
    job_id: int,
    job: schemas.JobCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_active_user)
):
    db_job = crud.update_job(db, job_id=job_id, job=job, user_id=current_user.id)
    if db_job is None:
        raise HTTPException(status_code=404, detail="Job not found")
    return db_job

@router.delete("/jobs/{job_id}")
def delete_job(
    job_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_active_user)
):
    success = crud.delete_job(db, job_id=job_id, user_id=current_user.id)
    if not success:
        raise HTTPException(status_code=404, detail="Job not found")
    return {"message": "Job deleted successfully"}

# Job Note routes
@router.post("/jobs/{job_id}/notes/", response_model=schemas.JobNote)
def create_job_note(
    job_id: int,
    note: schemas.JobNoteCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_active_user)
):
    # Verify job exists and belongs to user
    job = crud.get_job(db, job_id=job_id, user_id=current_user.id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    return crud.create_job_note(db=db, note=note, job_id=job_id)

@router.get("/jobs/{job_id}/notes/", response_model=List[schemas.JobNote])
def read_job_notes(
    job_id: int,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_active_user)
):
    # Verify job exists and belongs to user
    job = crud.get_job(db, job_id=job_id, user_id=current_user.id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    return crud.get_job_notes(db, job_id=job_id, skip=skip, limit=limit) 