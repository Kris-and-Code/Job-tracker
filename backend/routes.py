from fastapi import APIRouter, Depends, HTTPException, status, Query
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import timedelta
from . import crud, models, schemas, auth
from .database import get_db
from .config import settings
import logging

logger = logging.getLogger(__name__)
router = APIRouter()

# Authentication routes
@router.post("/token", response_model=schemas.Token)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    try:
        user = auth.authenticate_user(db, form_data.username, form_data.password)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = auth.create_access_token(
            data={"sub": user.email}, expires_delta=access_token_expires
        )
        return {"access_token": access_token, "token_type": "bearer"}
    except Exception as e:
        logger.error(f"Login error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred during login"
        )

@router.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    try:
        db_user = crud.get_user_by_email(db, email=user.email)
        if db_user:
            raise HTTPException(status_code=400, detail="Email already registered")
        return crud.create_user(db=db, user=user)
    except Exception as e:
        logger.error(f"User creation error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while creating the user"
        )

# Job routes
@router.post("/jobs/", response_model=schemas.Job)
def create_job(
    job: schemas.JobCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_active_user)
):
    try:
        return crud.create_job(db=db, job=job, user_id=current_user.id)
    except Exception as e:
        logger.error(f"Job creation error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while creating the job"
        )

@router.get("/jobs/", response_model=schemas.JobList)
def read_jobs(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    status: Optional[str] = None,
    company: Optional[str] = None,
    search: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_active_user)
):
    try:
        jobs, total = crud.get_jobs(
            db,
            user_id=current_user.id,
            skip=skip,
            limit=limit,
            status=status,
            company=company,
            search=search
        )
        return {
            "items": jobs,
            "total": total,
            "page": skip // limit + 1,
            "size": limit,
            "pages": (total + limit - 1) // limit
        }
    except Exception as e:
        logger.error(f"Job listing error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while fetching jobs"
        )

@router.get("/jobs/{job_id}", response_model=schemas.Job)
def read_job(
    job_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_active_user)
):
    try:
        db_job = crud.get_job(db, job_id=job_id, user_id=current_user.id)
        if db_job is None:
            raise HTTPException(status_code=404, detail="Job not found")
        return db_job
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Job retrieval error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while fetching the job"
        )

@router.put("/jobs/{job_id}", response_model=schemas.Job)
def update_job(
    job_id: int,
    job: schemas.JobCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_active_user)
):
    try:
        db_job = crud.update_job(db, job_id=job_id, job=job, user_id=current_user.id)
        if db_job is None:
            raise HTTPException(status_code=404, detail="Job not found")
        return db_job
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Job update error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while updating the job"
        )

@router.delete("/jobs/{job_id}")
def delete_job(
    job_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_active_user)
):
    try:
        success = crud.delete_job(db, job_id=job_id, user_id=current_user.id)
        if not success:
            raise HTTPException(status_code=404, detail="Job not found")
        return {"message": "Job deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Job deletion error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while deleting the job"
        )

# Job Note routes
@router.post("/jobs/{job_id}/notes/", response_model=schemas.JobNote)
def create_job_note(
    job_id: int,
    note: schemas.JobNoteCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_active_user)
):
    try:
        job = crud.get_job(db, job_id=job_id, user_id=current_user.id)
        if not job:
            raise HTTPException(status_code=404, detail="Job not found")
        return crud.create_job_note(db=db, note=note, job_id=job_id)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Note creation error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while creating the note"
        )

@router.get("/jobs/{job_id}/notes/", response_model=schemas.JobNoteList)
def read_job_notes(
    job_id: int,
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_active_user)
):
    try:
        job = crud.get_job(db, job_id=job_id, user_id=current_user.id)
        if not job:
            raise HTTPException(status_code=404, detail="Job not found")
        notes, total = crud.get_job_notes(db, job_id=job_id, skip=skip, limit=limit)
        return {
            "items": notes,
            "total": total,
            "page": skip // limit + 1,
            "size": limit,
            "pages": (total + limit - 1) // limit
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Note listing error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while fetching notes"
        ) 