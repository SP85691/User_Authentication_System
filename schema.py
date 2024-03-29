from pydantic import BaseModel
from typing import Optional

class UserCreate(BaseModel):
    name: str
    username: str
    email: str
    password: str
    resume_id: Optional[int] = None

    class Config:
        orm_mode = True

class ResumeCreate(BaseModel):
    name:str
    title:str
    email:str
    phone:str
    website:str
    linkedin:str
    github:str
    address:str
    city:str
    state:str
    zipcode:str
    summary:str
    skills:str
    experience:str
    education:str
    projects:str
    interests:str
    references:str

    class Config:
        orm_mode = True