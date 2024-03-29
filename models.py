from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, func, Text
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Author(Base):
    __tablename__ = 'author'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    users = relationship("User", backref="author")

class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    username = Column(String)
    email = Column(String, nullable=True)
    password = Column(String, nullable=True)
    created_date = Column(DateTime(timezone=True), server_default=func.now())
    updated_date = Column(DateTime(timezone=True), onupdate=func.now())
    resume_id = Column(Integer, ForeignKey("user.id"))

    resume = relationship("Author")

class Resume(Base):
    __tablename__ = "resume"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    title = Column(String)
    email = Column(String)
    phone = Column(String)
    website = Column(String)
    linkedin = Column(String)
    github = Column(String)
    address = Column(String)
    city = Column(String)
    state = Column(String)
    zipcode = Column(String)
    summary = Column(String)
    skills = Column(String)
    experience = Column(Text)
    education = Column(Text)
    projects = Column(Text)
    interests = Column(String)
    references = Column(String)
    created_date = Column(DateTime(timezone=True), server_default=func.now())
    updated_date = Column(DateTime(timezone=True), onupdate=func.now())