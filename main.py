import uvicorn
from fastapi import FastAPI, HTTPException, Header
from schema import UserCreate as UserSchema 
from schema import ResumeCreate as ResumeSchema
from models import User, Resume
from fastapi_sqlalchemy import DBSessionMiddleware, db
from fastapi.responses import JSONResponse
from flask_wtf.csrf import generate_csrf
from sqlalchemy.exc import IntegrityError
import os
from dotenv import load_dotenv
import json

load_dotenv(".env")

app = FastAPI()

app.add_middleware(DBSessionMiddleware, db_url=os.environ["DATABASE_URL"])

def get_db():
    db_session = db.session
    try:
        yield db_session
    finally:
        db_session.close()


@app.get("/")
async def read_root():
    csrf_token = generate_csrf()
    return JSONResponse(content={"csrf_token": csrf_token})

@app.post("/protected")
async def protected_route(csrf_token: str = Header(...)):
    # Validate the CSRF token (compare it with the one generated in the GET request)
    if not csrf_token == generate_csrf():
        raise HTTPException(status_code=403, detail="CSRF token mismatch")
    return {"message": "CSRF token is valid"}

@app.post("/signup/", response_model=UserSchema)
async def signup(user: UserSchema):
    try:
        db_user = User(
            name=user.name,
            username=user.username,
            email=user.email,
            password=user.password,
            resume_id=user.resume_id
        )
        db.session.add(db_user)
        db.session.commit()
        return db_user
    except Exception as e:
        print(f"Error during signup: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
    except IntegrityError as e:
        print(f"IntegrityError during signup: {e}")
        raise HTTPException(status_code=400, detail="User with this email or username already exists")
    except Exception as e:
        print(f"Error during signup: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

@app.post("/addResume/", response_model=ResumeSchema)
async def addResume(resume: ResumeSchema):
    try:
        db_resume = Resume(
            name = resume.name,
            title = resume.title,
            email = resume.email,
            phone = resume.phone,
            website = resume.website,
            linkedin = resume.linkedin,
            github = resume.github,
            address = resume.address,
            city = resume.city,
            state = resume.state,
            zipcode = resume.zipcode,
            summary = resume.summary,
            skills = resume.skills,
            experience = resume.experience,
            education = resume.education,
            projects = resume.projects,
            interests = resume.interests,
            references = resume.references
        )
        db.session.add(db_resume)
        db.session.commit()
        return db_resume
    except Exception as e:
        print(f"Error during signup: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
    except IntegrityError as e:
        print(f"IntegrityError during signup: {e}")
        raise HTTPException(status_code=400, detail="User with this email or username already exists")
    except Exception as e:
        print(f"Error during signup: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


if __name__ =='__main__':
    uvicorn.run(app, host='localhost', port=8000)