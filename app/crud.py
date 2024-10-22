from sqlalchemy.orm import Session
from . import models, schemas

def create_blog(db: Session, blog: schemas.BlogCreate):
    db_blog = models.Blog(**blog.dict())
    db.add(db_blog)
    db.commit()
    db.refresh(db_blog)
    return db_blog

def get_blogs(db: Session):
    return db.query(models.Blog).all()

def get_blog(db: Session, blog_id: int):
    return db.query(models.Blog).filter(models.Blog.id == blog_id).first()

def update_blog(db: Session, blog_id: int, blog: schemas.BlogCreate):
    db_blog = get_blog(db, blog_id)
    if db_blog:
        db_blog.title = blog.title
        db_blog.content = blog.content
        db.commit()
        db.refresh(db_blog)
    return db_blog

def delete_blog(db: Session, blog_id: int):
    db_blog = get_blog(db, blog_id)
    if db_blog:
        db.delete(db_blog)
        db.commit()

def add_comment(db: Session, blog_id: int, comment: schemas.CommentCreate):
    db_comment = models.Comment(**comment.dict(), blog_id=blog_id)
    db.add(db_comment)
    db.commit()
    db.refresh(db_comment)
    return db_comment

def like_blog(db: Session, blog_id: int):
    db_blog = get_blog(db, blog_id)
    if db_blog:
        db_blog.likes += 1
        db.commit()
        db.refresh(db_blog)
    return db_blog
