from fastapi import FastAPI
from app import models, schemas, crud, database
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException

app = FastAPI()

from app.database import engine
from app.models import Base

# Initialize the database
Base.metadata.create_all(bind=engine)

@app.post("/blogs", response_model=schemas.Blog)
def create_blog(blog: schemas.BlogCreate, db: Session = Depends(database.get_db)):
    return crud.create_blog(db=db, blog=blog)

@app.get("/blogs", response_model=list[schemas.Blog])
def get_blogs(db: Session = Depends(database.get_db)):
    return crud.get_blogs(db)

@app.get("/blogs/{blog_id}", response_model=schemas.Blog)
def get_blog(blog_id: int, db: Session = Depends(database.get_db)):
    blog = crud.get_blog(db, blog_id)
    if not blog:
        raise HTTPException(status_code=404, detail="Blog not found")
    return blog

@app.put("/blogs/{blog_id}", response_model=schemas.Blog)
def update_blog(blog_id: int, blog: schemas.BlogUpdate, db: Session = Depends(database.get_db)):
    return crud.update_blog(db=db, blog_id=blog_id, blog=blog)

@app.delete("/blogs/{blog_id}")
def delete_blog(blog_id: int, db: Session = Depends(database.get_db)):
    return crud.delete_blog(db, blog_id)

@app.post("/blogs/{blog_id}/comments", response_model=schemas.Comment)
def add_comment(blog_id: int, comment: schemas.CommentCreate, db: Session = Depends(database.get_db)):
    return crud.add_comment(db, blog_id, comment)

@app.put("/blogs/{blog_id}/like")
def like_blog(blog_id: int, db: Session = Depends(database.get_db)):
    return crud.like_blog(db, blog_id)

