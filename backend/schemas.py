from pydantic import BaseModel, EmailStr, Field
from typing import List, Optional
from datetime import datetime

# Base schemas
class JobBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=100)
    company: str = Field(..., min_length=1, max_length=100)
    location: Optional[str] = Field(None, max_length=100)
    description: Optional[str] = None
    status: str = Field(..., min_length=1, max_length=50)
    application_date: Optional[datetime] = None

class JobNoteBase(BaseModel):
    content: str = Field(..., min_length=1)

class UserBase(BaseModel):
    email: EmailStr

# Create schemas
class JobCreate(JobBase):
    pass

class JobNoteCreate(JobNoteBase):
    pass

class UserCreate(UserBase):
    password: str = Field(..., min_length=8)

# Response schemas
class JobNote(JobNoteBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    job_id: int

    class Config:
        from_attributes = True

class Job(JobBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    owner_id: int
    notes: List[JobNote] = []

    class Config:
        from_attributes = True

class User(UserBase):
    id: int
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime] = None
    jobs: List[Job] = []

    class Config:
        from_attributes = True

# Pagination schemas
class PaginatedResponse(BaseModel):
    items: List
    total: int
    page: int
    size: int
    pages: int

class JobList(PaginatedResponse):
    items: List[Job]

class JobNoteList(PaginatedResponse):
    items: List[JobNote]

# Token schemas
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None 