from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime

class JobNoteBase(BaseModel):
    content: str

class JobNoteCreate(JobNoteBase):
    pass

class JobNote(JobNoteBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime]
    job_id: int

    class Config:
        from_attributes = True

class JobBase(BaseModel):
    title: str
    company: str
    location: str
    description: str
    status: str
    application_date: datetime

class JobCreate(JobBase):
    pass

class Job(JobBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime]
    owner_id: int
    notes: List[JobNote] = []

    class Config:
        from_attributes = True

class UserBase(BaseModel):
    email: EmailStr

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime]
    jobs: List[Job] = []

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None 